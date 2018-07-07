from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Repository(models.Model):
    REPO_TYPES = (
        ('GIT', 'GIT'),
    )

    PROTOCOLS = (
        ('SSH', 'SSH'),
        ('GIT', 'GIT'),
        ('HTTP', 'HTTP'),
        ('HTTPS', 'HTTPS')
    )

    name = models.CharField(max_length=255)
    protocol = models.CharField(max_length=10, choices=PROTOCOLS)
    user = models.CharField(max_length=255, null=True, blank=True)
    host = models.CharField(max_length=255)
    port = models.IntegerField(null=True, blank=True,
                               validators=[MinValueValidator(0), MaxValueValidator(65536)])
    repo_remote_path = models.CharField(max_length=255)
    description = models.TextField()
    private = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_by', null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    repo_type = models.CharField(max_length=10, choices=REPO_TYPES)
    last_revision = models.CharField(max_length=40, null=True, blank=True)
    last_scan = models.DateTimeField(null=True, blank=True)
    scan_periodically = models.BooleanField(default=True)

    def __str__(self):
        return '{name}@{host}'.format(name=self.repo_remote_path, host=self.host)

    class Meta:
        unique_together = ('host', 'repo_remote_path')
        verbose_name_plural = 'Repositories'


class RepositoryErrorLog(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    command = models.CharField(max_length=1000)
    return_code = models.IntegerField()
    out = models.TextField(max_length=10000)
    err = models.TextField(max_length=10000)

    def __str__(self):
        return '{date} +++ {repo} +++ code:{return_code}'.format(date=str(self.timestamp), repo=self.repository.name,
                                                                 return_code=self.return_code)
