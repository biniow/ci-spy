from django.contrib.auth.models import User
from django.db import models


class Repository(models.Model):
    REPO_TYPES = (
        ('g', 'GIT'),
        ('s', 'SVN'),
    )

    PROTOCOLS = (
        ('h', 'HTTPS'),
        ('s', 'SSH')
    )

    name = models.CharField(max_length=255)
    origin_address = models.CharField(max_length=255)
    protocol = models.CharField(max_length=1, choices=PROTOCOLS)
    description = models.TextField()
    private = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='updated_by', null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    repo_type = models.CharField(max_length=1, choices=REPO_TYPES)
    last_revision = models.CharField(max_length=40, null=True, blank=True)
    last_scan = models.DateTimeField(null=True, blank=True)
    scan_periodically = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Repositories'







