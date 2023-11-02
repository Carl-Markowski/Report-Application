from django.forms import ModelForm
from .models import Subject, Student

#create class for project form
class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields =('name', 'grade','behavior_grade', 'teacher_report')