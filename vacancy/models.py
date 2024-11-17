from django.db import models
from users.models import User
from common.models import BaseModel, Job, JobFormat, Region, CustomRegion, Skills
from resume.models import Resume


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


class Vacancy(BaseModel):
    title = models.CharField(max_length=150)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    description = models.TextField()
    experience = models.IntegerField()
    salary = models.IntegerField()
    job_format = models.ForeignKey(JobFormat, on_delete=models.CASCADE)
    recruitment = models.BooleanField(default=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    custom_region = models.ForeignKey(CustomRegion, on_delete=models.CASCADE, null=True, blank=True)
    skill = models.ManyToManyField(Skills, blank=True, related_name='skills')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Announcements'
        verbose_name = 'Announcement'
        ordering = ['updated_at']


class VacancyViews(BaseModel):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    user = models.GenericIPAddressField()

    def __str__(self):
        return f'{self.vacancy} - {self.user}'

    class Meta:
        verbose_name_plural = 'Announcements'
        verbose_name = 'Announcement'


class Response(BaseModel):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.vacancy} - {self.author}'

    class Meta:
        verbose_name_plural = 'Responses'
        verbose_name = 'Response'


class Favorites(BaseModel):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.vacancy} - {self.user}'

    class Meta:
        verbose_name_plural = 'Favorites'
        verbose_name = 'Favorite'
