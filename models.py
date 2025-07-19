from django.db import models
    
# from pupel.models import Enrollment
from django.utils import timezone

# Create your models here.
class explorecourse(models.Model):
    course_name = models.CharField(max_length=100)
    course_description = models.TextField()
    course_image = models.ImageField(upload_to='course_images/')
    course_duration = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name



class Enrollment(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    course_name = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.course_name}"
    

def my_dashboard(request):
    enrollments = Enrollment.objects.all()
    return (request, 'my_dashboard.html', {'enrollments': enrollments})


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='assignments/')
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    student_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50)
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.assignment.title}"


class UploadedMaterial(models.Model):
    course = models.ForeignKey(explorecourse, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.course.course_name}"
    

class InstructorVisit(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
from django.db import models
from django.contrib.auth.models import User
from .models import explorecourse

class InstructorAccessRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(explorecourse, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.course_name} ({self.status})"
    



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender} to {self.recipient} at {self.timestamp}"
    

from django.db import models

class Submission(models.Model):  # Assuming this already exists
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    file = models.FileField(upload_to='submissions/')
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

class SubmissionMessage(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=[('student', 'Student'), ('instructor', 'Instructor')])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

