from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    objects = models.Manager()

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

class Education(BaseModel):
    class EducationLevels(models.TextChoices):
        AVERAGE = 'Average'
        SECONDARY_SPECIAL = 'Secondary special'
        HIGHER = 'Higher'
        BACHELOR = 'Bachelor'
        MASTER_DEGREE = 'Master\'s degree'
        CANDIATE_OF_SCIENCES = 'Candiate of sciences'
        DOCTOR_OF_SCIENCES = 'Doctor of sciences'

    education_level = models.CharField(max_length=25, choices=EducationLevels.choices)
    education_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    graduation = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.education_name

    class Meta:
        verbose_name_plural = 'Educations'
        verbose_name = 'Education'


class Experience(BaseModel):
    company_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)
    job_years = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = 'Experiences'
        verbose_name = 'Experience'


class Resume(BaseModel):
    resume_name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skills, blank=True, null=True, related_name='resumes')
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.resume_name

    class Meta:
        verbose_name_plural = 'Resumes'
        verbose_name = 'Resume'


class Profile(BaseModel):
    class Genders(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'

    class Themes(models.TextChoices):
        DARK = 'Dark'
        LIGHT = 'Light'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=Genders.choices)
    image = models.ImageField(upload_to='profile', null=True, blank=True)
    phone = models.CharField(max_length=14)
    description = models.TextField(null=True, blank=True)
    resume = models.ForeignKey
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    custom_region = models.ForeignKey(CustomRegion, on_delete=models.CASCADE)
    theme = models.CharField(max_length=5, choices=Themes.choices)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name_plural = 'Profile'
        verbose_name = 'Profile'


class Company(BaseModel):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='company', null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'
        verbose_name = 'Company'


class Announcement(BaseModel):
    title = models.CharField(max_length=150)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    description = models.TextField()
    experience = models.IntegerField()
    salary = models.IntegerField()
    job_format = models.ForeignKey(JobFormat, on_delete=models.CASCADE)
    recruitment = models.BooleanField(default=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    custom_region = models.ForeignKey(CustomRegion, on_delete=models.CASCADE, null=True, blank=True)
    skill = models.ManyToManyField(Skills, blank=True, null=True, related_name='skills')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Announcements'
        verbose_name = 'Announcement'
        ordering = ['updated_at']


class AnnouncementViews(BaseModel):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.IPAddressField()

    def __str__(self):
        return f'{self.announcement} - {self.user}'

    class Meta:
        verbose_name_plural = 'Announcements'
        verbose_name = 'Announcement'


class Response(BaseModel):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.announcement} - {self.author}'

    class Meta:
        verbose_name_plural = 'Responses'
        verbose_name = 'Response'


class Favorites(BaseModel):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.announcement} - {self.user}'

    class Meta:
        verbose_name_plural = 'Favorites'
        verbose_name = 'Favorite'

