#!/usr/bin/env python
# -*- coding: utf-8 -*-

from repository.vcs_interfaces.utils import logged_execution, is_repo_mirrored


@logged_execution
def _update(*args, **kwargs):
    return 'git -C {repo_local_path} remote update --prune'.format(repo_local_path=kwargs['repo_local_path'])


@logged_execution
def _clone(*args, **kwargs):
    return 'git clone {url} {repo_local_path} --mirror --bare'.format(url=kwargs['repo_remote_url'],
                                                                      repo_local_path=kwargs['repo_local_path'])


@logged_execution
def _branch(*args, **kwargs):
    return 'git -C {repo_local_path} branch -av'.format(repo_local_path=kwargs['repo_local_path'])


def init_or_update(repository):
    if is_repo_mirrored(repository):
        _update(repository)
    else:
        _clone(repository)


def get_branches(repository):
    out = _branch(repository)
    result = []
    for branch in out.split('\n'):
        name, current_hash, commit_msg = branch.lstrip('* ').split(maxsplit=2)
        result.append({
            'name': name,
            'hash': current_hash,
            'commit_message_header': commit_msg
        })
    return result
