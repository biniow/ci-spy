#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from contextlib import contextmanager


def get_repo_url(repository):
    """
    Functions return URL for repository passed as parameter
    :param repository: object representing Repository model
    :return: str - concatenated URL
    """
    url_data = {
        'protocol': repository.address_protocol.lower(),
        'user': ''.join((repository.address_user, '@')) if repository.address_user else '',
        'host': repository.address_host.lower(),
        'port': ''.join((':', str(repository.address_port))) if repository.address_port else '',
        'repo': ''.join(('/', repository.address_repo))
    }
    return '{protocol}://{user}{host}{port}{repo}'.format(**url_data)


@contextmanager
def ch_dir(new_path):
    """
    Context manager function for temporary dir change (during 'with' scope)
    :param new_path: path to new location
    """
    if not os.path.exists(new_path):
        raise OSError('{path} does not exists'.format(path=new_path))
    old_path = os.getcwd()
    os.chdir(new_path)
    yield
    os.chdir(old_path)
