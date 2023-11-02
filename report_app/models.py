from django.db import models
from django.urls import reverse
  

class Subject (models.Model):

    name = models.CharField(max_length = 200)
    grade = models.IntegerField(
        choices=[ (1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (6, 'Sixth'), (7, 'Seventh'), (8, 'Eighth'), (9, "Ninth")], 
        blank = True)
    
    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('subject-detail', args=[str(self.id)])
    

class Teacher (models.Model):
    
    name = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    school = models.CharField(max_length = 200)
    subject = models.CharField(max_length = 200)
    grade = models.IntegerField(
    choices=[ (1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (6, 'Sixth'), (7, 'Seventh'), (8, 'Eighth'), (9, "Ninth")], 
        blank = True)
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, unique=True)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('teacher-detail', args=[str(self.id)])


class Student (models.Model):

    name = models.CharField(max_length = 200)
    grade = models.IntegerField(choices=[ (1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (6, 'Sixth'), (7, 'Seventh'), (8, 'Eighth'), (9, "Ninth")])
    subject = models.ForeignKey(Subject, related_name = 'students', on_delete=models.CASCADE, default = None)
    behavior_grade = models.CharField(max_length = 2, choices = [('A', 'Great Job!'), ('B', 'Good'), ('C', 'Somethings to Work On'), ('D', 'We need to setup a meeting')], blank = True)
    teacher_report = models.TextField(blank = True)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('student-detail', args=[str(self.id)])