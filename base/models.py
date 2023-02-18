from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
# from django.contrib.auth import get_user_model 
# User = get_user_model()

class BaseModel(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', _('active')
        INACTIVE = 'inactive', _('inactive')
        ARCHIVED = 'archived', _('archived')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    # updated_by=models.ForeignKey(User, related_name='updated_by_user')      
    # created_by=models.ForeignKey(User, related_name='created_by_user')

    class Meta:
        abstract = True
        app_label = 'base'
        
class NameBaseModel(BaseModel):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    slug = AutoSlugField(
        populate_from='first_name',
        always_update=True,
        unique=True,
        allow_unicode=True
    )

    class Meta:
        abstract = True