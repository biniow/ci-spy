#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from collections import Counter

import repository.vcs_interfaces.git as git
from repository.vcs_interfaces.utils import is_repo_mirrored


def init_or_update(repository):
    if is_repo_mirrored(repository):
        git.update(repository)
    else:
        git.clone(repository)

    repository.last_scan = datetime.datetime.now()
    repository.save()


def get_branches(repository):
    out = git.branch(repository)
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
    out = git.log(repository, format='%aE')
    return dict(Counter((participant.strip() for participant in out.split('\n')))
                .most_common(n))


def get_log(repository, **kwargs):
    out = git.log(repository, **kwargs)
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
