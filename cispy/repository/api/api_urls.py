#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from repository.api import api_views

router = DefaultRouter()
router.register(r'repositories', api_views.RepositoryViewSet, 'repository')

commits_router = NestedSimpleRouter(router, r'repositories', lookup='repository')
commits_router.register(r'commits', api_views.CommitViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(commits_router.urls)),
]
