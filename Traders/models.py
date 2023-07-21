from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have email address')

        email = self.normalize_email(email=email)
        user: UserAccount = self.model(email=email, username=username)
        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    cash = models.IntegerField(default=10000)

    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_name(self):
        return self.username

    def __str__(self) -> str:
        return f'User(email: {self.email}, username: {self.username}'


class Stock(models.Model):
    company = models.CharField(max_length=100)
    quantity = models.IntegerField()
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f'Stock(company: {self.company}, quantity: {self.quantity}, user: {self.user.__str__()})'


class History(models.Model):
    CHOICES = [("B", "BUY"),
               ("S", "SELL")]
    company = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    type = models.CharField(max_length=1, choices=CHOICES)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
