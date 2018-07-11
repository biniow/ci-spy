# Create your views here.
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response

from repository.models import Repository
from repository.serializers import RepositorySerializer
from repository.vcs_interfaces import git_features


def main_view(request):
    return render(request, 'repository/index.html', {})


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
        branches = git_features.get_branches(get_object_or_404(self.get_queryset(), pk=repo_id))
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

        participants = git_features.get_participants(get_object_or_404(self.get_queryset(), pk=repo_id), n)

        response = {
            'repository_id': repo_id,
            'number_of_participants': len(participants),
            'participants': participants
        }
        return Response(response)


class RepositoryLog(OwnPublicRepositoriesMixin, generics.RetrieveAPIView):
    @staticmethod
    def parse_params(params):
        start_rev = params.get('start_rev')
        stop_rev = params.get('stop_rev')

        if not start_rev and stop_rev:
            raise ValueError('start_rev is needed')

        return {
            'start_rev': start_rev,
            'stop_rev': stop_rev,
            'branch': params.get('branch'),
            'author': params.get('author'),
            'since': params.get('since'),
            'until': params.get('until')
        }

    def retrieve(self, request, *args, **kwargs):
        repo_id = int(kwargs['pk'])

        try:
            params = self.parse_params(request.GET)
        except ValueError:
            return Response('You should provide \'start_rev\' parameter', status=status.HTTP_400_BAD_REQUEST)

        log = git_features.get_log(get_object_or_404(self.get_queryset(), pk=repo_id), **params)

        response = {
            'repository_id': repo_id,
            'commits_returned': len(log),
            'log': log
        }
        return Response(response)
