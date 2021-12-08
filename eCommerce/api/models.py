from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator


# Create your models here.
class Product(models.Model):
    owner = models.ForeignKey('MyUser', related_name='products', on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.owner.username}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class MyUserManager(BaseUserManager):
	def create_user(self, first_name, last_name, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
            first_name=first_name,
            last_name=last_name,
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password, username,first_name=None, last_name=None):
		user = self.create_user(
			first_name, last_name, self.normalize_email(email), username, password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(verbose_name="email", max_length=60, unique=True)
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    username=models.CharField(max_length=30, unique=True, validators=[alphanumeric])
    not_owned_products=models.ManyToManyField(Product, blank=True)
    balance=models.DecimalField(max_digits=7, decimal_places=2, default=0)
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return f'/{self.username}/'

    def get_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_not_owned_products(self):
        return self.not_owned_products

    def get_balance(self):
        return self.balance

# class MyUser(AbstractUser):
#     not_owned_products = models.ManyToManyField(Product, blank=True)
#     balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)

#     def __str__(self):
#         return self.first_name + ' ' + self.last_name

#     def get_absolute_url(self):
#         return f'/{self.username}/'

#     def get_name(self):
#         return f'{self.first_name} {self.last_name}'

#     def get_unowned_products(self):
#         return self.not_owned_products


class Order(models.Model):
    user = models.ForeignKey(MyUser, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)