#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.conf import settings


def get_repo_url(repository):
    result = '{protocol}://'.format(protocol=repository.address_protocol.lower())
    if repository.address_user:
        result += '{user}@'.format(user=repository.address_user)

    result += repository.address_host

    if repository.address_port:
        result += ':{port}'.format(port=str(repository.address_port))

    result += '/' + repository.address_repo
    return result


def init_or_update(repository):
    repo_local_path = os.path.join(settings.REPO_STORAGE_PATH, repository.address_host, repository.address_repo)
    if os.path.exists(repo_local_path):
        command = 'git -C {repo_path} remote update --prune'.format(repo_path=repo_local_path)
        print(command)
    else:
        url = get_repo_url(repository)
        command = 'git clone {url} {repo_local_path} --mirror --bare'.format(url=url, repo_local_path=repo_local_path)
        print(command)
