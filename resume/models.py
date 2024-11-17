from django.db import models
from common.models import BaseModel, Skills
from users.models import User


class Education(BaseModel):
    class EducationLevels(models.TextChoices):
        AVERAGE = 'Average'
        SECONDARY_SPECIAL = 'Secondary special'
        HIGHER = 'Higher'
        BACHELOR = 'Bachelor'
        MASTER_DEGREE = 'Master\'s degree'
        CANDIDATE_OF_SCIENCES = 'Candidate of sciences'
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
    skills = models.ManyToManyField("common.Skills", blank=True)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    experience = models.ManyToManyField(Experience, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.resume_name

    class Meta:
        verbose_name_plural = 'Resumes'
        verbose_name = 'Resume'
