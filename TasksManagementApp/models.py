from django.db import models


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=100,blank=False)
    employee_phone = models.CharField(max_length=20,unique=True, blank=False)
    employee_address = models.CharField(max_length=10)
    employee_email = models.EmailField(unique=True,blank=False)
    ROLES=[(1,'manger'),(2,'employee')]
    employee_role = models.IntegerField(choices=ROLES,blank=False)
    team_code = models.ForeignKey('Team', on_delete=models.PROTECT,related_name='employees',blank=False)

    def __str__(self):
        return self.employee_name

class Task(models.Model):
    STATUS_CHOICES = [(1,"new"),(2,"in process"),(3,"completed")]
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100,blank=False)
    task_description = models.TextField(blank=False)
    task_last_date = models.DateField(blank=False)
    task_completed_date = models.DateField(blank=False)
    task_status = models.IntegerField(choices=STATUS_CHOICES,blank=False)
    employee = models.ForeignKey('Employee',on_delete=models.PROTECT,related_name='myTasks',blank=False)
    task_team = models.ForeignKey('Team',on_delete=models.PROTECT,related_name='tasks',blank=False)

    def __str__(self):
        return self.task_name + self.task_description

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_manager_id = models.ForeignKey('Employee', on_delete=models.PROTECT,blank=False)

    def __str__(self):
        return self.team_id