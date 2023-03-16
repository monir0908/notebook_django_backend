from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .enums import GenderTypes
from base.models import NameBaseModel
from .managers import UserManager

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class User(AbstractBaseUser, PermissionsMixin, NameBaseModel):       
    
    # email will be considered as username, password will automatically be mandatory
    email = models.EmailField(db_index=True, unique=True, max_length=200)
    user_code = models.CharField(max_length=300, blank=True, null=True, default=None)
    # other fields
    mobile = models.CharField(max_length=30, blank=True, null=True, default=None)
    alternative_mobile = models.CharField(max_length=30,  blank=True, null=True, default=None)
    occupation = models.CharField(max_length=100,  blank=True, null=True, default=None)
    address_one = models.TextField(max_length=500,  blank=True, null=True, default=None)
    address_two = models.TextField(max_length=500,  blank=True, null=True, default=None)
    dob = models.DateField( blank=True, null=True)
    gender = models.IntegerField(
        choices=[(tag.value, _(tag.name)) for tag in GenderTypes],
        default=GenderTypes.NOT_SET.value
    )
    
    
    telephone = models.CharField(max_length=30, blank=True, null=True, default=None)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False,
        help_text=_('Whether this user should be treated as active. Unselect\
             this instead of deleting accounts.')) 
    is_superuser = models.BooleanField( blank=True, null=True, default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
       
    #... ... first_name, last_name, slug coming from NameBaseModel

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    profile_pic_thumbnail = ImageSpecField(
        source='profile_pic',
        processors=[ResizeToFill(64, 64)],
        format='JPEG',
        options={'quality': 85})   
    
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name','last_name','mobile',)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    class Meta:
        db_table = 'user'
        verbose_name_plural = 'Users'
        verbose_name = 'User'
        ordering = ['-date_joined']
        default_permissions = ('add', 'change', 'view', )

    def __unicode__(self):
        return u"username: {}".format(self.email)
    
    def get_full_name(self):
        """ Returns the full name """
        name = u"{}".format(self.first_name + " " + self.last_name)
        return name.strip()

    def get_short_name(self):
        return u"{}".format(self.first_name)

    def __str__(self):
        return self.get_full_name()

    def get_customer_code(self):
        return self.customer_code

    
    