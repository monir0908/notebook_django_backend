import uuid
from django.db import models
from base.models import BaseModel
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model 
User = get_user_model()
from collection.models import Collection
from base.enums import DocumentStatus

# document model
class Document(BaseModel):
    collection = models.ForeignKey(
        Collection, models.CASCADE, blank=True, null=True, related_name='documents'
    )       
    doc_creator = models.ForeignKey(
        User, models.DO_NOTHING, blank=True, null=True
    )
    doc_key= models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        unique=True
    )
    doc_title = models.CharField(max_length=50,  blank=True, null=True, default=None)
    doc_body = models.TextField(blank=True, null=True, default=None)
    doc_status = models.IntegerField(
        choices=[(tag.value, _(tag.name)) for tag in DocumentStatus],
        default=DocumentStatus.DRAFTED.value
    )

    published_at = models.DateTimeField( blank=True, null=True)

    class Meta:
        db_table = 'user_document'
        ordering = ['id']
        # indexes = [
        #     models.Index(fields=['my_field']),
        # ]
        verbose_name = _('user_document')
        verbose_name_plural = _('user_documents')
    
    def __str__(self):
        return self.doc_title
    
# document attachment model
class Attachment(BaseModel):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name='attachments'
    )
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attachment'
        ordering = ['id']
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')

    def __str__(self):
        return self.file.name