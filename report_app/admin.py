from django.contrib import admin
from .models import Teacher, Student, Subject

admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
