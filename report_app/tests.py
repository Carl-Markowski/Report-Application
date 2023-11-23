from django.test import TestCase, Client
from .models import *
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from django.urls import reverse


#Unit test for the teacher model
class TeacherModelTest(TestCase):
    
    def setUp(self):

        #Create the user that will be tied to this teacher
        self.user = User.objects.create_user(username = 'testUser', email= 'test@uccs.edu', password = 'testPass')

        #Create the subject for this teacher object
        self.subject = Subject.objects.create(name = 'Math', grade=1)

        #Create the teacher 
        self.teacher = Teacher.objects.create(name = 'test', email = 'testteacher@uccs.edu', school = 'uccs', subject = self.subject, grade = 1, user = self.user)


    #Check if the teacher was properly created
    def test_post_str(self):
        self.assertEqual(self.teacher.name, 'test')
        self.assertEqual(self.teacher.email, 'testteacher@uccs.edu')
        self.assertEqual(self.teacher.school, 'uccs')
        self.assertEqual(self.teacher.subject, self.subject)
        self.assertEqual(self.teacher.grade, 1)
        self.assertEqual(self.teacher.user, self.user)

    def test_teacher_str(self):
        self.assertEqual(str(self.teacher), 'test')



#Unit test for the student model
class StudentModelTest(TestCase):
    def setUp(self):
        #create the subject for the student model
        self.subject=Subject.objects.create(name = 'math', grade = 4)

        #create the student model
        self.student = Student.objects.create(name = 'carl', grade = 4, subject = self.subject, behavior_grade = 'B', teacher_report = 'Doing ok')

    #check if the student has been created successfully
    def test_student_create(self):
        self.assertEqual(self.student.name, 'carl')
        self.assertEqual(self.student.grade, 4)
        self.assertEqual(self.student.subject, self.subject)
        self.assertEqual(self.student.behavior_grade, 'B')
        self.assertEqual(self.student.teacher_report, 'Doing ok')

    #check if the name of the student is returned properly
    def test_student_str(self):
        self.assertEqual(str(self.student), 'carl')


#Unit test for updating a student in the database
class UpdateStudentTest(TestCase):
    def setUp(self):
     # Create a subject
        self.subject = Subject.objects.create(name='Math', grade = 5)

        # Create a student
        self.student = Student.objects.create(
            name='Alice',
            grade=5,
            subject=self.subject,
            behavior_grade='A',
            teacher_report='Doing well in class.'
        )

    def test_student_update(self):

        #get student object
        updated_student = Student.objects.get(name='Alice')

        #Update student
        updated_student.name = 'Bob'
        updated_student.grade = 6
        updated_student.behavior_grade = 'B'
        updated_student.teacher_report = 'Needs improvement in certain areas.'
        updated_student.save()

        #get updated student
        updated_student = Student.objects.get(id=updated_student.id)

        #Verify changes
        self.assertEqual(updated_student.name, 'Bob')
        self.assertEqual(updated_student.grade, 6)
        self.assertEqual(updated_student.behavior_grade, 'B')
        self.assertEqual(updated_student.teacher_report, 'Needs improvement in certain areas.')



#Selenium test 1
class UserCreationTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_user_creation(self):
        # Get the URL using reverse resolution for register and login URLs
        register_url = reverse('register_page')
        login_url = reverse('login') 

        # Ensure the form is accessible
        response = self.client.get(register_url)
        self.assertEqual(response.status_code, 200)

        # Fill in the registration form fields
        response = self.client.post(register_url, {
            'username': 'test_user',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
        })

        # Check for a successful redirect
        self.assertEqual(response.status_code, 200)


#Selenium Test 2
class Hosttest(LiveServerTestCase):
    def testHomePage(self):
    
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/')

        assert "Report Application" in driver.title

        driver.quit()