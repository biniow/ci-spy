#!/usr/bin/env python
# -*- coding: utf-8 -*-
from repository.vcs_interfaces.utils import logged_execution


@logged_execution
def update(*args, **kwargs):
    return 'git -C {repo_local_path} remote update --prune'.format(repo_local_path=kwargs['repo_local_path'])


@logged_execution
def clone(*args, **kwargs):
    return 'git clone {url} {repo_local_path} --mirror --bare'.format(url=kwargs['repo_remote_url'],
                                                                      repo_local_path=kwargs['repo_local_path'])


@logged_execution
def branch(*args, **kwargs):
    return 'git -C {repo_local_path} branch -av'.format(repo_local_path=kwargs['repo_local_path'])


@logged_execution
def log(*args, **kwargs):
    default_branch = kwargs['branch'] if kwargs.get('branch') else 'master'
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
        default_branch = ''
        if not stop_rev:
            stop_rev = 'HEAD'
        params += '{start_rev}..{stop_rev}'.format(start_rev=start_rev, stop_rev=stop_rev)

    return 'git -C {repo_local_path} log {branch} {params}'.format(repo_local_path=kwargs['repo_local_path'],
                                                                   branch=default_branch, params=params)
