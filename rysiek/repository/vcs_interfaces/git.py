#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.conf import settings

from repository.vcs_interfaces.utils import get_repo_url, ch_dir


def init_or_update(repository):
    repo_local_path = os.path.join(settings.REPO_STORAGE_PATH, repository.address_host, repository.address_repo)
    if os.path.exists(repo_local_path):
        command = 'git remote update --prune'
        with ch_dir(repo_local_path):
            os.system(command)
    else:
        url = get_repo_url(repository)
        command = 'git clone {url} {repo_local_path} --mirror --bare'.format(url=url, repo_local_path=repo_local_path)
        os.system(command)
