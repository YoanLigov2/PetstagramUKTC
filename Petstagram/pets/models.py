from django.db import models
from django.template.defaultfilters import slugify
from Petstagram.accounts.models import PetstagramUser
from Petstagram.pets.validators import validate_past_date
from Petstagram.photos.validators import validate_file_size


class Pet(models.Model):
    name = models.CharField(max_length=30)
    personal_photo = models.ImageField(upload_to='pet_images', validators=(validate_file_size,))
    date_of_birth = models.DateField(validators=[validate_past_date])
    #optional
    animal_type = models.CharField(max_length=30)
    specie = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    distinguishing_marks = models.CharField(max_length=50)

    slug = models.SlugField(unique=True, editable=False)
    user = models.ForeignKey(PetstagramUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.id}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name