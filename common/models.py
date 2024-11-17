import uuid
from django.db import models

IMAGE_FILE_FORMATS = (
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'avif'
)

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'


class Job(BaseModel):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Jobs'
        verbose_name = 'Job'


class JobFormat(BaseModel):
    format = models.CharField(max_length=100)

    def __str__(self):
        return self.format

    class Meta:
        verbose_name_plural = 'Job Formats'
        verbose_name = 'Job Format'


class Country(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'
        verbose_name = 'Country'


class Region(BaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Regions'
        verbose_name = 'Region'


class CustomRegion(BaseModel):
    address = models.CharField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = 'Custom Regions'
        verbose_name = 'Custom Region'


class Skills(BaseModel):
    skill_name = models.CharField(max_length=100)
    custom_skill = models.BooleanField(default=False)

    def __str__(self):
        return self.skill_name

    class Meta:
        verbose_name_plural = 'Skills'
        verbose_name = 'Skill'

