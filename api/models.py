# api/models.py
from django.db import models

class AdminCredential(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'admin_credentials'  # table name
        managed = False  # Django won't create/migrate this table

    def __str__(self):
        return self.username
