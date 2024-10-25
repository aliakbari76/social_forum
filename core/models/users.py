from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    first_name = models.CharField(max_length=64 , blank= True)
    last_name = models.CharField(max_length=64 , blank = True)
    username = models.CharField(max_length=64 , blank=False , null=False , unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_set',  # Custom related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_set',  # Custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.username