from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username,staff_number,phone_number, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            staff_number = staff_number,
            phone_number = phone_number,
            first_name = first_name,
            last_name = last_name,
           
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, first_name, last_name, email, username,staff_number,phone_number, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            staff_number = staff_number,
            phone_number = phone_number,
            password = password,
            first_name = first_name,  
            last_name = last_name,
            
        )
        user.is_active = True
        user.is_staff = True
        user.is_cook= True
        user.is_chef = True
        user.is_admin = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    staff_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, unique=True)


    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_cook = models.BooleanField(default=False)
    is_chef = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'staff_number'
    REQUIRED_FIELDS = ['username', 'email', 'first_name', 'last_name', 'phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    class Meta:
        ordering = ['-id']

    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    staff_number = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(blank=True, max_length=20)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile', default="userprofile/default.png")
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.user.first_name

#@receiver(post_save, sender=UserProfile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = UserProfile.objects.create(
            user = user,
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            username = user.username,
            staff_number = user.staff_number,
            phone_number = user.phone_number
    
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.username = profile.username
        user.staff_number = profile.staff_number
        user.phone_number = profile.phone_number
        user.email = profile.email
        user.save()   

def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
 


post_save.connect(createProfile, sender=Account)
post_save.connect(updateUser, sender=UserProfile)
post_delete.connect(deleteUser, sender=UserProfile)




