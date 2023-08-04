from django.db import models
from django.utils import timezone

class PaperDetail(models.Model):
    school_name = models.CharField(max_length=300)
    class_choice = (
    
    )
    class_name = models.CharField(max_length=100,choices=class_choice)
    subject_choice = (
      
    )
    subject_name = models.CharField(max_length=100,choices=subject_choice)
    exam_name = models.CharField(max_length=100)
    date = models.DateField()
    duration = models.IntegerField()
    marks = models.IntegerField()
    instructions = models.TextField(null=True,blank=True)


# login register models

class UserLogin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    email_token = models.CharField(max_length=200,default=None,null=True)
    is_verified = models.BooleanField(default=False)
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class ToolLogin(models.Model):
    user = models.OneToOneField(UserLogin, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField(null=True)
    tool_id = models.CharField(max_length=100,unique=True)
    tool_password = models.CharField(max_length=128)
    paper_credential = models.IntegerField()
    
    def __str__(self):
        return self.tool_id + ' | ' + self.name
    
class Paper(models.Model):
    tool_login = models.ForeignKey(ToolLogin, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100)
    exam_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100,default='class_not_defined')
    subject_name = models.CharField(max_length=100,default='subject_not_defined')
    created_date = models.DateTimeField(default=timezone.now)
    paper_html = models.TextField()
    solution_html = models.TextField()
    saved_paper = models.FileField(upload_to='saved_papers/')
    saved_solution = models.FileField(upload_to='saved_solutions/')

    def __str__(self):
        return f"{self.tool_login.name} - {self.tool_login.tool_id}"