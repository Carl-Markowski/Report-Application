from django.db import models
from django.urls import reverse

class Teacher (models.Model):

    SUBJECTS = (
        ('M','Math'),
        ('R','Reading'),
        ('S','Science'),
        ('E','English'),
        ('P.E','Physical Educaiton'),
        ('B','Band'),
        ('S.E','Special Education')
    )
    
    name = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    school = models.CharField(max_length = 200)
    subject = models.CharField(max_length = 200, choices=SUBJECTS)
    grade = models.IntegerField(
        choices=[ (1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (6, 'Sixth'), (7, 'Seventh'), (8, 'Eighth'), (9, "Ninth")], 
        blank = True)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('teacher-detail', args=[str(self.id)])
    
    
'''
class Subject (models.Model):

    name = models.CharField(max_length = 200)
    grade = models.IntegerField(
        choices=[ (1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (6, 'Sixth'), (7, 'Seventh'), (8, 'Eighth'), (9, "Ninth")], 
        blank = True)
   ''' 

class Student (models.Model):

    name = models.CharField(max_length = 200)
    subject = models.CharField(max_length = 200)
    grade = models.IntegerField(choices=[ (1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (6, 'Sixth'), (7, 'Seventh'), (8, 'Eighth'), (9, "Ninth")])
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])