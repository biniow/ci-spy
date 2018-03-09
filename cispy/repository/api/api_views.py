#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from repository.models import Commit, Repository
from repository.serializers import RepositorySerializer, CommitSerializer


class RepositoryViewSet(viewsets.ModelViewSet):
    serializer_class = RepositorySerializer
    http_method_names = ['get', 'post', 'head']

    def get_queryset(self):
        public_repos = Repository.objects.filter(private=False)
        private_repos = Repository.objects.filter(private=True, created_by=self.request.user.id)
        return public_repos | private_repos


class CommitViewSet(viewsets.ModelViewSet):
    serializer_class = CommitSerializer
    queryset = Commit.objects.all()
    http_method_names = ['get', 'head']

    def retrieve(self, request, pk=None, repository_pk=None):
        item = get_object_or_404(self.queryset, revision=pk, repository__id=repository_pk)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def list(self, request, repository_pk=None, **kwargs):
        try:
            items = get_list_or_404(self.queryset, repository__id=repository_pk)
        except (TypeError, ValueError):
            raise Http404
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
