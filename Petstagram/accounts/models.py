from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from Petstagram.photos.validators import validate_file_size


# Create your models here.
class PetstagramUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, validators=[MinLengthValidator(2)], blank=True, null=True)
    last_name = models.CharField(max_length=30, validators=[MinLengthValidator(2)], blank=True, null=True)
    # profile_pic = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_picture', validators=(validate_file_size,), blank=True, null=True)
    gender = models.CharField(max_length=11,
                              choices=[('Мъж', 'Мъж'), ('Жена', 'Жена'), ('Не показвай', 'Не показвай')],
                              default='Не показвай')

    def get_user_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        else:
            return self.username