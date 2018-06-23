from django.contrib import admin
from repository.models import Repository, RepositoryErrorLog

admin.site.register(Repository)
admin.site.register(RepositoryErrorLog)
