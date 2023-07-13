from django.db import models
import uuid

class Class(models.Model):
    class_choice = (
        ('Class 6','Class 6'),
        ('Class 7','Class 7'),
        ('Class 8','Class 8'),
        ('Class 9','Class 9'),
        ('Class 10','Class 10'),
        ('Class 11','Class 11'),
        ('Class 12','Class 12'),
    )
    class_name = models.CharField(max_length=50,choices=class_choice)
    def __str__(self):
        return self.class_name


class Subject(models.Model):
    Class = models.ForeignKey(Class,on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=200)

    def __str__(self):
        return self.subject_name + ' ' + self.Class.class_name

class Book(models.Model):
    Class = models.ForeignKey(Class,on_delete=models.CASCADE)
    Subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    book_name = models.CharField(max_length=200)

    def __str__(self):
        return self.book_name 
        
class Chapter(models.Model):
    Subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    Book = models.ForeignKey(Book,on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=200)
    def __str__(self):
        return self.chapter_name + ' ' + self.Book.book_name


class TheoryQuestion(models.Model):
    question = models.TextField()
    question_img = models.ImageField(upload_to='MediaFiles/', null=True,blank=True)
    answer = models.TextField()
    answer_img = models.ImageField(upload_to='MediaFiles/', null=True,blank=True)
    difficulty_choice = (
        ('Easy','Easy'),
        ('Medium','Medium'),
        ('Hard','Hard'),
    )
    difficulty = models.CharField(max_length=50,choices=difficulty_choice)
    length_choice = (
        ('one Word','One Word'),
        ('Very short','Very Short'),
        ('Short','Short'),
        ('Long','Long'),
        ('Very long','Very Long'),
    )
    length = models.CharField(max_length=100,choices=length_choice)
    Book = models.ForeignKey(Book,on_delete=models.CASCADE)
    Chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)

class FillUp(models.Model):
    question = models.TextField()
    answer = models.CharField(max_length=200)
    Book = models.ForeignKey(Subject,on_delete=models.CASCADE)
    Chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)

class TrueFalse(models.Model):
    question = models.TextField()
    answer = models.CharField(max_length=20,choices=(
        ('true','True'),
        ('false','False'),
    ))
    Book = models.ForeignKey(Book,on_delete=models.CASCADE)
    Chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)

class MCQ(models.Model):
    question = models.TextField()
    option_1 = models.CharField(max_length=100)   
    option_2 = models.CharField(max_length=100)   
    option_3 = models.CharField(max_length=100)   
    option_4 = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=100)
    Book = models.ForeignKey(Book,on_delete=models.CASCADE)
    Chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
   
