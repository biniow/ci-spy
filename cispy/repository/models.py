from django.contrib.auth.models import User
from django.db import models


class RepositoryType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return '{name}'.format(name=self.name)


class Repository(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    description = models.TextField()
    private = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_by', null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    repo_type = models.ForeignKey(RepositoryType, on_delete=models.PROTECT)
    last_revision = models.CharField(max_length=40, null=True, blank=True)
    last_scan = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{address}:{branch}'.format(address=self.address, branch=self.branch)

    class Meta:
        unique_together = (('address', 'branch'),)
        verbose_name_plural = 'Repositories'


class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    revision = models.CharField(max_length=40)
    author = models.CharField(max_length=255)
    author_email = models.CharField(max_length=255, null=True, blank=True)
    commiter = models.CharField(max_length=255, null=True, blank=True)
    commiter_email = models.CharField(max_length=255, null=True, blank=True)
    parent_revision = models.CharField(max_length=40, null=True, blank=True)
    lines_inserted = models.PositiveIntegerField()
    lines_deleted = models.PositiveIntegerField()
    files_changed = models.PositiveIntegerField()

    def __str__(self):
        return '{revision}@{repo}'.format(revision=self.revision, repo=self.repository.address)

    class Meta:
        unique_together = (('repository', 'revision'),)
        verbose_name_plural = 'Commits'


class UserRepository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)







