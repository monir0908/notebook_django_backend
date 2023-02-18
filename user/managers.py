# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from time import time

from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, password, first_name, last_name,mobile, **extra_fields):
        """
        Creates and saves a User with the given mobile and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Email must be provided as username')
        if not password:
            raise ValueError('Password is not provided')
        if not mobile:
            raise ValueError('Mobile number is required')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            mobile = mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name,mobile,**extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password,first_name, last_name,mobile,**extra_fields)

    def create_superuser(self, email, password, first_name, last_name,mobile,**extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, first_name, last_name,mobile,**extra_fields)
