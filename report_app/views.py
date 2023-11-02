from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import StudentForm

def index(request):
    subjects = Subject.objects.all()  # Retrieve all Subject objects from the database
    print("All subject:", subjects)
    return render(request, 'report_app/index.html', {'subjects': subjects})

class TeacherListView(generic.ListView):
    model = Teacher
class TeacherDetailView(generic.DetailView):
    model = Teacher

class SubjectListView(generic.ListView):
    model = Subject
class SubjectDetailView(generic.DetailView):
    model = Subject
    
    def get_context_data(self, **kwargs):
        context = super(SubjectDetailView, self).get_context_data(**kwargs)
        subject = self.get_object()  # Get the current Portfolio object
        context['students'] = subject.students.all()  # Fetch related projects
        return context
    
class StudentListView(generic.ListView):
    model = Student
class StudentDetailView(generic.DetailView):
    model = Student

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
            return redirect('portfolio-detail', pk=student.subject.pk)
         
         else:
            #if the form is not vaild, fill it out again
            form = StudentForm(instance=student)

      
      #This is the render request for the form itself to be displayed and filled out
      return render(request, 'report_app/student_form.html', {"form": form, 'student': student})