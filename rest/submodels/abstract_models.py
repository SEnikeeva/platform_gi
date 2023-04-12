from django.contrib.auth import get_user_model
from django.db import models

from users.models import Company


class AuthorCompanyModel(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL
    )
    company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
