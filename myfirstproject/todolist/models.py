from xmlrpc.client import boolean
from django.db import models

# Create your models here.
class UserTask(models.Model):
    task_title = models.CharField(max_length=30)
    task_description = models.CharField(max_length=100)
    task_assigned_at = models.DateTimeField(null=False, blank=False)
    task_accomplish_date = models.DateTimeField(null=False, blank=False)
    task_assigned_by = models.CharField(max_length=50)
    task_progress_status = models.CharField(max_length=50)
    task_assigned_to = models.CharField(max_length=50)
    task_status = models.BooleanField()

    class Meta:
        db_table = "user_task"

class AssignedTaskDescription(models.Model):
    task_user = models.CharField(max_length=100)
    task_update_description = models.CharField(max_length=200)
    task_progress_status = models.CharField(max_length=50)
    task_update_file = models.CharField(max_length=200)
    task_updated_at = models.DateTimeField(null=False, blank=False)

    class Meta:
        db_table = "assgned_task_description"

class PersonalTask(models.Model):
    task_title = models.CharField(max_length=30)
    task_description = models.CharField(max_length=100)
    task_assigned_at = models.DateTimeField(null=False, blank=False)
    task_accomplish_date = models.DateTimeField(null=False, blank=False)
    task_progress_status = models.CharField(max_length=50)
    task_status = models.BooleanField()

    class Meta:
        db_table = "personal_task"

class UserNote(models.Model):
    note_title = models.CharField(max_length=50)
    note_description = models.CharField(max_length=200)
    note_added_at = models.DateTimeField(null=False)

    class Meta:
        db_table = "user_note"

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "users"

"""class UserLogin(models.model):
    user_username = models.CharField(max_length=50, blank=False)
    user_password = models.CharField(max_length=100, blank=False)

    class Meta:
        db_table = "user_login"

class UserRegistration(models.model):
    user_username = models.CharField(max_length=50, blank=False)
    user_password = models.CharField(max_length=100, blank=False)
    user_email = models.CharField(max_length=100, blank=False)
    user_gender = models.BooleanField()
    user_phone = models.IntegerField(max_length=20, blank=False)"""
