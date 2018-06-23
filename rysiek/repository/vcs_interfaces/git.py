#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from django.conf import settings

from repository.vcs_interfaces.utils import get_repo_url, shell_cmd, log_errors


@log_errors
def init_or_update(repository):
    repo_local_path = os.path.join(settings.REPO_STORAGE_PATH, repository.address_host, repository.address_repo)

    if os.path.exists(repo_local_path):
        command = 'git -C {repo_local_path} remote update --prune'.format(repo_local_path=repo_local_path)
    else:
        url = get_repo_url(repository)
        command = 'git clone {url} {repo_local_path} --mirror --bare'.format(url=url, repo_local_path=repo_local_path)

    return (command,) + shell_cmd(command, return_out=True)
