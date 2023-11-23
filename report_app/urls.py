from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.userPage, name='user_page'),
    path('accounts/register/', views.registerPage, name = 'register_page'),
    path('student/<int:student_id>/upload/', views.upload_files, name='upload_files')
]

#Allows django to display the pdf even in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
