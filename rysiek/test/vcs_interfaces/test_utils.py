#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from collections import namedtuple

import os

from repository.vcs_interfaces.utils import get_repo_url, ch_dir, shell_cmd

Repository = namedtuple('Repository', ['address_protocol', 'address_user', 'address_host', 'address_port', 'address_repo'])


class TestGetRepoUrl(unittest.TestCase):
    def test_fullRepoDataAvailable_properUrlConcatenated(self):
        # Arrange
        repo = Repository(address_protocol='ssh',
                          address_user='user',
                          address_host='samplehost.com',
                          address_port=22,
                          address_repo='sample/repo')
        valid_result = 'ssh://user@samplehost.com:22/sample/repo'

        # Act
        result = get_repo_url(repo)

        # Assert
        self.assertEqual(result, valid_result)

    def test_minimalRepoDataAvailable_properUrlConcatenated(self):
        # Arrange
        repo = Repository(address_protocol='ssh',
                          address_user=None,
                          address_host='samplehost.com',
                          address_port=None,
                          address_repo='sample/repo')

        valid_result = 'ssh://samplehost.com/sample/repo'

        # Act
        result = get_repo_url(repo)

        # Assert
        self.assertEqual(result, valid_result)

    def test_minimalDataNotAvailable_exceptionRaised(self):
        # Arrange
        repo = Repository(address_protocol=None,
                          address_user=None,
                          address_host=None,
                          address_port=None,
                          address_repo=None)

        # Act / Assert
        self.assertRaises(Exception, get_repo_url, repo)

    def test_invalidRepositoryInstancePassed_exceptionRaised(self):
        # Arrange / Act / Assert
        self.assertRaises(Exception, get_repo_url, None)

    def test_invalidLetterCaseOfProtocolPassed_lowerCaseProtocolReturned(self):
        # Arrange
        repo = Repository(address_protocol='HttP',
                          address_user=None,
                          address_host='samplehost.com',
                          address_port=None,
                          address_repo='sample/repo')

        # Act
        returned_value = get_repo_url(repo)

        # Assert
        self.assertEqual(returned_value[:4], 'http')


class TestChDir(unittest.TestCase):
    def test_notExistingPathProvided_osErrorRaised(self):
        # Arrange
        invalid_path = '/bla/bla/make/sure/it/is/invalid/path'

        # Act / Assert
        try:
            with ch_dir(invalid_path):
                pass
        except OSError:
            pass
        else:
            raise AssertionError

    def test_existingPath_dirChangedAsExpected(self):
        # Arrange
        valid_path = os.path.expanduser('~')

        # Act
        with ch_dir(valid_path):
            result_path = os.getcwd()

        # Assert
        self.assertEqual(valid_path, result_path)

    def test_existingPath_contextReturnedToStartState(self):
        # Arrange
        before_path = os.getcwd()

        # Act
        with ch_dir(os.path.expanduser('~')):
            pass

        # Assert
        self.assertEqual(before_path, os.getcwd())


class TestShellCmd(unittest.TestCase):
    def test_returnOutParameter_returnedProperValue(self):
        # Arrange
        command = 'echo test'

        # Act
        _, ret_stdout, _ = shell_cmd(command, return_out=True)

        # Assert
        self.assertEqual(ret_stdout, 'test')
