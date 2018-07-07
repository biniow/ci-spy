#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from repository.views import RepositoriesList, RepositoryDetails, RepositoryBranches, RepositoryParticipants

urlpatterns = [
    url(r'repositories/$', RepositoriesList.as_view()),
    url(r'repository/(?P<pk>\d+)$', RepositoryDetails.as_view()),
    url(r'repository/(?P<pk>\d+)/branches$', RepositoryBranches.as_view()),
    url(r'repository/(?P<pk>\d+)/participants$', RepositoryParticipants.as_view())
]