#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from rest_framework import serializers

from repository.models import Repository, Commit


class TimestampField(serializers.Field):
    def to_internal_value(self, data):
        return datetime.datetime.fromtimestamp(data)

    def to_representation(self, value):
        return int(value.timestamp())


class RepositorySerializer(serializers.ModelSerializer):
    created_at = TimestampField('created_at')
    updated_at = TimestampField('updated_at')
    last_scan = TimestampField('last_scan')

    class Meta:
        model = Repository
        fields = ('id', 'name', 'address', 'branch', 'description', 'private', 'created_by', 'created_at', 'updated_by',
                  'updated_at', 'repo_type', 'last_revision', 'last_scan')


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ('repository', 'revision', 'author', 'author_email', 'commiter', 'commiter_email',
                  'parent_revision', 'lines_inserted', 'lines_deleted', 'files_changed')
