from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()



class MainTask(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(null=True, blank=True, max_length=1000)
    deadline = models.DateTimeField()
    color = models.CharField(max_length=10)
    complete = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    archive_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'maintask'

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, null=True, blank=True)
    deadline = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    maintask = models.ForeignKey(MainTask, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subtask'

    def __str__(self):
        return self.title


class Log(models.Model):
    matter = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    maintask = models.ForeignKey(MainTask, on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log'

    def __str__(self):
        return self.matter