import uuid
from django.db import models
from base.models import BaseModel
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model 
User = get_user_model()


# collection related

class Collection(BaseModel):       
    collection_creator = models.ForeignKey(
        User, models.DO_NOTHING, blank=True, null=True
    )
    collection_key= models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        unique=True
    )
    collection_title = models.CharField(max_length=50,  blank=True, null=True, default=None)

    class Meta:
        db_table = 'user_collection'
        ordering = ['id']
        # indexes = [
        #     models.Index(fields=['my_field']),
        # ]
        verbose_name = _('user_collection')
        verbose_name_plural = _('user_collection')
    
    def __str__(self):
        return self.collection_title