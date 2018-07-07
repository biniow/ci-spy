#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter

import datetime

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


@logged_execution
def _log(*args, **kwargs):
    branch = kwargs['branch'] if kwargs.get('branch') else 'master'
    start_rev = kwargs.get('start_rev')
    stop_rev = kwargs.get('stop_rev')
    number_of_commits = kwargs.get('number_of_commits', 100) if not start_rev else 0

    params = ""
    if kwargs.get('format'):
        params += '--format=\'{log_format}\' '.format(log_format=kwargs['format'])

    if int(number_of_commits) > 0:
        params += '-n {n} '.format(n=str(number_of_commits))

    if kwargs.get('author'):
        params += '--author=\"{author}\" '.format(author=kwargs['author'])

    if kwargs.get('since'):
        params += '--since=\"{since_date}\" '.format(since_date=kwargs['since'])

    if kwargs.get('until'):
        params += '--until=\"{until_date}\" '.format(until_date=kwargs['until'])

    if start_rev:
        branch = ''
        if not stop_rev:
            stop_rev = 'HEAD'
        params += '{start_rev}..{stop_rev}'.format(start_rev=start_rev, stop_rev=stop_rev)

    return 'git -C {repo_local_path} log {branch} {params}'.format(repo_local_path=kwargs['repo_local_path'],
                                                                   branch=branch, params=params)


def init_or_update(repository):
    if is_repo_mirrored(repository):
        _update(repository)
    else:
        _clone(repository)

    repository.last_scan = datetime.datetime.now()
    repository.save()


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


def get_participants(repository, n=None):
    out = _log(repository, format='%aE')
    return dict(Counter((participant.strip() for participant in out.split('\n')))
                .most_common(n))


def get_log(repository, **kwargs):
    out = _log(repository, **kwargs)
    result = []
    if out:
        for commit in out.strip().split('\ncommit'):
            commit_hash, author, date, message = [x.strip() for x in commit.strip().split('\n', maxsplit=3)]
            result.append({
                'hash': commit_hash,
                'author': author.split(maxsplit=1)[1].strip(),
                'date': date.split(maxsplit=1)[1].strip(),
                'commit_msg': message
            })
    return result
