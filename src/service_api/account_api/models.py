from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserAccountManger(BaseUserManager):
    """Handels the user account"""

    def create_user(self,name,surname,email,password=None):
        if not email:
            raise ValueError('user email is required')
        if not surname:
            raise ValueError('surname is required')
        if not name:
            raise ValueError('name is required')

        email = self.normalize_email(email)
        user = self.model(email=email,name=name,surname=surname)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self,name,surname,email,password):
        user = self.create_user(name,surname,email,password)

        user.is_staff=True
        user.is_superuser = True

        user.save(using=self._db)


class UserAccount(AbstractBaseUser,PermissionsMixin):

    name = models.CharField(max_length=255,blank=False)
    surname  = models.CharField(max_length=255,blank=False)
    email = models.EmailField( max_length=254,unique=True,blank=False)
    password_confirm=''
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserAccountManger()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','surname']

    def get_full_name(self):
        return self.name+" "+self.surname

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class UserDetail(models.Model):

    phone_number = models.CharField(max_length=255, blank=False)
    phone_number2 = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=False)
    address2 = models.CharField(max_length=255,)
    registered_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(UserAccount ,blank=True, on_delete=models.CASCADE,null=True)
    country = models.ForeignKey('business.Country',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.phone_number
