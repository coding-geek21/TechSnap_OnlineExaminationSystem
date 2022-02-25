from django.db import models
from admin_dash.models import Subject
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class UserManager(BaseUserManager):
	def create_user(self,username,email,name,password=None):
		if not username:
			raise ValueError('You Dont have Permission to do exam')
		user = self.model(
			username=username,
            email=email,
            name=name
		)
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self,username,email,name, password):
		user = self.create_user(username,email,name,password=password)
		user.is_admin = True
		user.is_staff=True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email= models.CharField(verbose_name='email', max_length=150,unique=True)
	name=models.CharField(max_length=150,null=True)
	username=models.CharField(max_length=20,verbose_name='username',unique=True)
	subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
	date_joind=models.DateTimeField(verbose_name='date joind', auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff=models.BooleanField(default=False)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['name','email']
	objects = UserManager()

	def __str__(self):
		return self.name

	def has_perm(self, perm, obj=None):
		return self.is_admin
	
	def has_module_perms(self, app_label):
		return True
