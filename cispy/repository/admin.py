from django.contrib import admin
from repository.models import Repository, RepositoryType

admin.site.register(Repository)
admin.site.register(RepositoryType)
