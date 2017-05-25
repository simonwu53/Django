from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
import os


# Create your models here.
# User model extend
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('0', '女'),
        ('1', '男'),
    )
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=11)
    major = models.CharField(max_length=20, null=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

        # post_save.connect(create_user_profile, sender=UserProfile)


# end of extend User model


# Course model
class Course(models.Model):
    CLASS_CHOICE = (
        ('1', '一班'),
        ('2', '二班'),
        ('3', '三班'),
    )
    IS_TEACHER = (
        ('0', '学生'),
        ('1', '教师'),
    )
    code = models.CharField(max_length=8)
    coursename = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    classes = models.CharField(max_length=1, choices=CLASS_CHOICE)
    is_teacher = models.CharField(max_length=1, null=True, choices=IS_TEACHER)


# Discuss model
class Discuss(models.Model):
    code = models.CharField(max_length=8)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)
    content = models.TextField()


# Consult
class Consult(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now=True)
    content = models.TextField()
    code = models.CharField(max_length=8)


# Message
class Message(models.Model):
    user = models.ForeignKey(User, related_name='sender')
    receive = models.ForeignKey(User, related_name='receiver')
    time = models.DateTimeField(auto_now=True)
    content = models.TextField()
    first = models.CharField(max_length=1, null=True)


# Bulletin
class Bulletin(models.Model):
    CLASS_CHOICE = (
        ('0', '所有'),
        ('1', '一班'),
        ('2', '二班'),
        ('3', '三班'),
    )
    title = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    code = models.CharField(max_length=8)
    classes = models.CharField(max_length=1, choices=CLASS_CHOICE)
    time = models.DateTimeField(auto_now=True)
    content = models.TextField()


# files
class Uploaded_files(models.Model):
    CLASS_CHOICE = (
        ('0', '所有'),
        ('1', '一班'),
        ('2', '二班'),
        ('3', '三班'),
    )
    user = models.ForeignKey(User)
    classes = models.CharField(max_length=1, choices=CLASS_CHOICE)
    code = models.CharField(max_length=8)
    time = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='media')


def delete_file(sender, **kwargs):
    patch = kwargs['instance']
    os.remove(patch.file.path)


post_delete.connect(delete_file, sender=Uploaded_files)


# assignment
class Assignment(models.Model):
    CLASS_CHOICE = (
        ('0', '所有'),
        ('1', '一班'),
        ('2', '二班'),
        ('3', '三班'),
    )
    title = models.CharField(max_length=30)
    content = models.TextField()
    code = models.CharField(max_length=8)
    classes = models.CharField(max_length=1, choices=CLASS_CHOICE)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Assignment_file(models.Model):
    assignments = models.ForeignKey(Assignment)
    file = models.FileField(upload_to='media/assignments')
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)


def delete_assignment(sender, **kwargs):
    patch = kwargs['instance']
    os.remove(patch.file.path)


post_delete.connect(delete_assignment, sender=Assignment_file)


class Assignment_comment(models.Model):
    assignment_file = models.ForeignKey(Assignment_file)
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=10, null=True)
    last_name = models.CharField(max_length=10, null=True)
    comment = models.TextField()


# the end of models file
