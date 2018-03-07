#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from repository.api import api_views

urlpatterns = [
    url(r'^$', api_views.RepositoriesList.as_view()),
]
