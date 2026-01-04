from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Employee(AbstractUser):
    ROLES = [
        (1, 'manager'),
        (2, 'employee'),
    ]
    employee_role = models.PositiveSmallIntegerField(choices=ROLES, default=2)
    team_code = models.ForeignKey('Team', on_delete=models.PROTECT, related_name='employees', blank=True, null=True)

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return self.username

class Task(models.Model):
    STATUS_CHOICES = [(1,"new"),(2,"in process"),(3,"completed")]
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100,blank=False, null=False)
    task_description = models.TextField(blank=False, null=False)
    task_last_date = models.DateField(blank=False, null=False)
    task_completed_date = models.DateField(blank=False, null=False)
    task_status = models.IntegerField(choices=STATUS_CHOICES,blank=False, null=False)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='myTasks',blank=False, null=False)
    task_team = models.ForeignKey('Team',on_delete=models.PROTECT,related_name='tasks',blank=False, null=False)

    def __str__(self):
        return self.task_name + self.task_description

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_manager_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False, null=False, related_name='managed_teams')

    def __str__(self):
        return str(self.team_id)