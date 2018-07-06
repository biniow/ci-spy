#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from collections import namedtuple
from contextlib import contextmanager

from django.conf import settings
from repository.models import RepositoryErrorLog

VCSCmdOutput = namedtuple('VCSCmdOutput', 'command return_code out err')


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


def get_repo_local_path(repository):
    """
    Function returns path to bare repository on local hard disk
    :param repository: repository instance
    :return: generated path to repository on local disk
    """
    return os.path.join(settings.REPO_STORAGE_PATH, repository.address_host, repository.address_repo)


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


def shell_cmd(command, print_out=False, return_out=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    """
    Wrapper for subprocess.Popen, allows to execute shell commands and returns shell return code, stdout, stderr
    :param command: command which will be executed
    :param print_out: defines if result should be printed to console, false default
    :param return_out: defines if stdout and stderr will be returned as string, false default
    :param stdout: out stream, subprocess.PIPE default
    :param stderr: err stream, subprocess.PIPE default
    :return: return_code, stdout or None, stderr or None
    """
    process = subprocess.Popen(command, shell=True, stdout=stdout, stderr=stderr)
    out, err = process.communicate()

    if print_out:
        print(out.decode().strip())

    if return_out:
        return process.returncode, out.decode().strip(), err.decode().strip()

    return process.returncode, None, None


def logged_execution(func):
    """
    Decorator which will log every error occured to database table RepositoryErrorLog
    :param func: function which will be wrapper
    """

    def wrapper(repository, *args, **kwargs):
        command = func(repository, *args, **kwargs)
        return_code, out, err = shell_cmd(command, return_out=True, print_out=True)
        if return_code != 0:
            RepositoryErrorLog(repository=repository, command=command, return_code=return_code, out=out, err=err).save()

    return wrapper
