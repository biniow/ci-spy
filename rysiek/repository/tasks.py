#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery.task import task
from repository.vcs_interfaces import git
from repository.models import Repository


@task(name='repository_update_references')
def repository_update_references():

    for repository in Repository.objects.filter(scan_periodically=True):
        if repository.repo_type == 'GIT':
            git.init_or_update(repository)
