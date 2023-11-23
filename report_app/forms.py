from django.forms import ModelForm
from .models import Subject, Student, Teacher, PDFDocument
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#create class for project form
class StudentForm(ModelForm):

    class Meta:
        model = Student
        fields =('name', 'grade','behavior_grade', 'teacher_report')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user','subject']


class PDFForm(ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'file']