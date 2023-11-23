from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from .models import *
from django.views import generic
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decarator import allowed_users
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    subjects = Subject.objects.all()  # Retrieve all Subject objects from the database
    print("All subject:", subjects)
    return render(request, 'report_app/index.html', {'subjects': subjects})

class TeacherListView(generic.ListView):
    model = Teacher
class TeacherDetailView(LoginRequiredMixin, generic.DetailView):
    model = Teacher

class SubjectListView(generic.ListView):
    model = Subject
class SubjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Subject
    
    def get_context_data(self, **kwargs):
        context = super(SubjectDetailView, self).get_context_data(**kwargs)
        subject = self.get_object()  
        context['students'] = subject.students.all()  
        return context
    
class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student
    
    def get_object(self):
        # Retrieve the student object based on the primary key captured in the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(Student, pk=pk)



@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def createStudent(request, subject_id):
    form = StudentForm()
    subject = Subject.objects.get(pk=subject_id)
    
    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        student_data = request.POST.copy()
        student_data['subject_id'] = subject_id
        
        form = StudentForm(student_data)
        if form.is_valid():
            # Save the form without committing to the database
            student = form.save(commit=False)
            # Set the portfolio relationship
            student.subject = subject
            student.save()

            # Redirect back to the portfolio detail page
            return redirect('subject-detail', subject_id)

    context = {'form': form}
    return render(request, 'report_app/student_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def deleteStudent(request, student_id):
    # Retrieve the project object or return a 404 response if it doesn't exist
    student = get_object_or_404(Student, pk=student_id)

    if request.method == "POST":
        
        if request.POST.get('confirm') == 'yes':

        # If the request method is POST, it's a confirmation to delete
         student.delete()

        # Redirect to the portfolio page after deletion
         return redirect('subject-detail', pk=student.subject.pk)
        
        elif request.POST.get('cancel') == 'no':
         
         #If the user "cancel" the deletion then go back to the portfolio page
         return redirect('subject-detail', pk=student.subject.pk)

    # If the request method is not POST, render a confirmation page
    return render(request, 'report_app/student_delete.html', {'student': student})

#This is the method used to update the project details
@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def updateStudent(request, student_id):
      
      #Get the project that needs to be updated
      student = get_object_or_404(Student, pk=student_id)
      form = StudentForm()
      
      if request.method == 'POST':
         
         #If a POST request was made, fill out the form
         form = StudentForm(request.POST, instance=student)

         #check if the form is valid
         if form.is_valid():
            #if so save the form
            form.save()
            
            #return to the portfolio detail page
            return redirect('subject-detail', pk=student.subject.pk)
         
         else:
            #if the form is not vaild, fill it out again
            form = StudentForm(instance=student)

      
      #This is the render request for the form itself to be displayed and filled out
      return render(request, 'report_app/student_form.html', {"form": form, 'student': student})


def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            #group = Group.objects.get(name='teacher')
            #user.groups.add(group)
            teacher = Teacher.objects.create(user=user)
            #subject = Subject.objects.create()
           #teacher.subject = subject
            teacher.save()

            messages.success(request, 'Account has been created for ' + username)
            return redirect('login')
    
    context = {'form':form}
    return render(request, 'registration/register.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def userPage(request):
    teacher = request.user.teacher
    form = TeacherForm(instance = teacher)
    print('teacher', teacher)
    subject = teacher.subject
    print(subject)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance = teacher)
        if form.is_valid():
            form.save()
    context = {'subjects':subject, 'form':form}
    return render (request, 'report_app/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def upload_pdf(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_document = form.save(commit=False)
            pdf_document.student = student  # Link the document to the student
            pdf_document.save()
            student.pdf_document = pdf_document  # Associate the document with the student
            student.save()
            return redirect('student-detail', pk=student.id)  # Redirect to student detail page 
    else:
        form = PDFForm()
    
    context = {'form': form, 'student': student}
    return render(request, 'report_app/upload_pdf.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def upload_files(request, student_id):
    student = get_object_or_404(Student, pk=student_id) #get the current student that is being used
    pdf_documents = PDFDocument.objects.filter(student=student) #Grab all the pdf documents for that student

    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid(): #Check if the form is valid
            pdf_document = form.save(commit=False)
            pdf_document.student = student  # Link the PDF to the student
            pdf_document.save()
            return redirect('upload_files', student_id=student_id)  # Redirect to the same page after upload
    else:
        form = PDFForm() #If not valid, render the form again

    return render(request, 'report_app/upload_files.html', {'form': form, 'pdf_documents': pdf_documents, 'student': student})