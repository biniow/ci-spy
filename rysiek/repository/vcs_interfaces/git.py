#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from repository.vcs_interfaces.utils import get_repo_url, logged_execution, get_repo_local_path


@logged_execution
def init_or_update(repository):
    """
    Function generates git command based on current repository status. If bare repository already exists on
    local disk, update will be executed. In other case, there is a need to clone it
    :param repository: repository object, defines base for further actions
    :return: git command which will be executed in @logged_execution wrapper
    """
    repo_local_path = get_repo_local_path(repository)

    if os.path.exists(repo_local_path):
        return 'git -C {repo_local_path} remote update --prune'.format(repo_local_path=repo_local_path)
    else:
        url = get_repo_url(repository)
        return 'git clone {url} {repo_local_path} --mirror --bare'.format(url=url, repo_local_path=repo_local_path)