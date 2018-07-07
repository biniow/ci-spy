# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response

from repository.models import Repository
from repository.serializers import RepositorySerializer
from repository.vcs_interfaces import git


class OwnPublicRepositoriesMixin(object):
    def get_queryset(self):
        public = Repository.objects.filter(private=False)
        if self.request.user.is_anonymous:
            return public

        own = Repository.objects.filter(created_by=self.request.user)
        return own | public


class RepositoriesList(OwnPublicRepositoriesMixin, generics.ListAPIView):
    serializer_class = RepositorySerializer


class RepositoryDetails(OwnPublicRepositoriesMixin, generics.RetrieveAPIView):
    serializer_class = RepositorySerializer


class RepositoryBranches(OwnPublicRepositoriesMixin, generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        repo_id = int(kwargs['pk'])
        branches = git.get_branches(get_object_or_404(self.get_queryset(), pk=repo_id))
        response = {
            'repository_id': repo_id,
            'number_of_branches': len(branches),
            'branches': branches
        }
        return Response(response)


class RepositoryParticipants(OwnPublicRepositoriesMixin, generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        repo_id = int(kwargs['pk'])
        try:
            n = int(request.GET.get('top'))
        except TypeError:
            n = None

        participants = git.get_participants(get_object_or_404(self.get_queryset(), pk=repo_id), n)

        response = {
            'repository_id': repo_id,
            'number_of_participants': len(participants),
            'participants': participants
        }
        return Response(response)


class RepositoryLog(OwnPublicRepositoriesMixin, generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        repo_id = int(kwargs['pk'])
        log = git.get_log(get_object_or_404(self.get_queryset(), pk=repo_id))

        response = {
            'repository_id': repo_id,
            'commits_returned': len(log),
            'log': log
        }
        return Response(response)
