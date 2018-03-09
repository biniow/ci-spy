from django.contrib import admin
from repository.models import Repository, RepositoryType, Commit

admin.site.register(Repository)
admin.site.register(RepositoryType)
admin.site.register(Commit)
