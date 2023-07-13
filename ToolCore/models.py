from django.db import models

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


