from django.urls import path
from . import views

urlpatterns = [
    path ('', views.index, name='index'),
    path('teacher/', views.TeacherListView.as_view(), name= 'teacher'),
    path('teacher/<int:pk>', views.TeacherDetailView.as_view(), name='teacher-detail'),
    path('subject/', views.SubjectListView.as_view(), name= 'subject'),
    path('subject/<int:pk>', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('student/', views.StudentListView.as_view(), name= 'student'),
    path('student/<int:pk>', views.StudentDetailView.as_view(), name='student-detail'),
    path('subject/<int:subject_id>/create_student', views.createStudent, name='create_student'),
    path('subject/student/<int:student_id>/delete', views.deleteStudent, name='delete_student'),
    path("students/<int:student_id>/update-student/", views.updateStudent, name="update_student"),
    #path("subject/<int:subject_id>/update-subject/",views.updateSubject,name="update_Subject"),
]