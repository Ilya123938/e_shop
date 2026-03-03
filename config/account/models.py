from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
import pycountry
# Create your models here.

def get_country():
    countries = list(pycountry.countries)
    country_choice = [(country.alpha_2,country.name)for country in countries]
    return country_choice

class AcoountManager(BaseUserManager):
    def create_user(self,username,first_name,last_name,email,country,password=None):
        if not email:
            raise ValueError('user most have email')
        user=self.model(
            email =self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            country = country
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,first_name,last_name,email,country,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            country=country,
            password=password,
        )

        user.is_active=True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser= True
        user.save(using=self._db)
        return user
    


class Account(AbstractBaseUser):
    last_cart = models.JSONField(default=dict, blank=True)
    username = models.CharField(max_length=200,unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200,unique=True)
    phone_number = models.CharField(max_length=200)
    country = models.CharField(max_length=200,choices=get_country())

    date_joined = models.DateTimeField(auto_now_add=True)

    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = AcoountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','country']


    def __str__(self):
        return self.email
    

    def has_perm(self,perm,obj=None):
        return self.is_admin
    

    def has_module_perms(self,app_label):
        return True
    


