#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from contextlib import contextmanager

import datetime
from django.conf import settings
from repository.models import RepositoryErrorLog


class ShellExecutionError(Exception):
    pass


def get_repo_url(repository):
    """
    Functions return URL for repository passed as parameter
    :param repository: object representing Repository model
    :return: str - concatenated URL
    """
    url_data = {
        'protocol': repository.protocol.lower(),
        'user': ''.join((repository.user, '@')) if repository.user else '',
        'host': repository.host.lower(),
        'port': ''.join((':', str(repository.port))) if repository.port else '',
        'repo': ''.join(('/', repository.repo_remote_path))
    }
    return '{protocol}://{user}{host}{port}{repo}'.format(**url_data)


def get_repo_local_path(repository):
    """
    Function returns path to bare repository on local hard disk
    :param repository: repository instance
    :return: generated path to repository on local disk
    """
    return os.path.join(settings.REPO_STORAGE_PATH, repository.host, repository.repo_remote_path)


def is_repo_mirrored(repository):
    return os.path.exists(get_repo_local_path(repository))


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

    def wrapper(*args, **kwargs):
        repository = args[0]
        kwargs['repo_local_path'] = get_repo_local_path(repository)
        kwargs['repo_remote_url'] = get_repo_url(repository)

        cmd = func(*args, **kwargs)
        ret_code, out, err = shell_cmd(cmd, return_out=True)

        if ret_code != 0:
            error_log = RepositoryErrorLog(repository=repository, command=cmd, return_code=ret_code, out=out, err=err)
            error_log.save()
            raise ShellExecutionError(str(error_log))
        else:
            repository.last_scan = datetime.datetime.now()
            repository.save()
            return out

    return wrapper
