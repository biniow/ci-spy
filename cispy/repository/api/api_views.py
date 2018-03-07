#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import generics

from repository.models import Repository
from repository.serializers import RepositorySerializer


class RepositoriesList(generics.ListAPIView):
    serializer_class = RepositorySerializer

    def get_queryset(self):
        public_repos = Repository.objects.filter(public=True)
        private_repos = Repository.objects.filter(public=False, created_by=self.request.user.id)
        return public_repos | private_repos
