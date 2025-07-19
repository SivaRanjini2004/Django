from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Max
from django.apps import apps
from django.utils.text import slugify

from .models import explorecourse, Assignment, Submission, UploadedMaterial, InstructorVisit, InstructorAccessRequest, SubmissionMessage


# Utility
def get_unique_username(base_email):
    base = slugify(base_email.split("@")[0])
    username = base
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1
    return username


# Basic pages
def home(request):
    return HttpResponse("hello!!")

def homee(request):
    return render(request, "homee.html")

def main(request):
    return render(request, "main.html")

def about(request):
    return render(request, "about.html")


# Authentication
def Instructor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        if email == "admin@gmail.com" and pwd == "1234":
            user = User.objects.filter(email=email).first()
            if not user:
                username = get_unique_username(email)
                user = User.objects.create_user(username=username, email=email, password='defaultpass')
            login(request, user)
            return redirect('instructor_main')
        else:
            messages.error(request, "Invalid login credentials")
    return render(request, 'Instructor_login.html')

def Student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Student_main')
        else:
            return render(request, 'Student_login.html', {'error': 'Invalid credentials'})
    return render(request, 'Student_login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password, email=email)
            return redirect('Student_login')
        else:
            return render(request, 'signup.html', {'error': 'Username already exists'})
    return render(request, 'signup.html')

@login_required
def change_password(request):
    error = ""
    if request.method == "POST":
        old = request.POST.get("pwd3")
        new = request.POST.get("pwd1")
        confirm = request.POST.get("pwd2")
        user = request.user
        if user.check_password(old):
            if new == confirm:
                user.set_password(new)
                user.save()
                logout(request)
                error = "yes"
            else:
                error = "not"
        else:
            error = "wrong"
    return render(request, "change_password.html", {"error": error})


# Dashboard
@login_required
def Student_main(request):
    return render(request, "Student_main.html")

@login_required
def my_dashboard(request):
    Enrollment = apps.get_model('pupel', 'Enrollment')
    latest_ids = Enrollment.objects.values('email').annotate(latest=Max('id')).values_list('latest', flat=True)
    enrollments = Enrollment.objects.filter(id__in=latest_ids).order_by('-id')
    return render(request, 'my_dashboard.html', {'enrollments': enrollments})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('main')


# Instructor Area
@login_required
def instructor_main(request):
    email = request.user.email
    form_filled = InstructorVisit.objects.filter(email=email).exists()
    access = InstructorAccessRequest.objects.filter(user=request.user, status='approved').first()
    is_approved = bool(access)
    approved_course = access.course if access else None
    courses = explorecourse.objects.all()
    return render(request, 'instructor_main.html', {
        'form_filled': form_filled,
        'user_email': email,
        'courses': courses,
        'is_approved': is_approved,
        'approved_course': approved_course,
    })

@login_required
def submit_access_request(request):
    if request.method == 'POST':
        course_id = request.POST.get('subject')
        course = explorecourse.objects.get(course_name=course_id)
        InstructorAccessRequest.objects.update_or_create(
            user=request.user,
            defaults={'course': course, 'status': 'pending'}
        )
        messages.success(request, "Your request has been submitted for approval.")
        return redirect('instructor_main')

@login_required
def submit_instructor_info(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')

        if not InstructorVisit.objects.filter(email=email).exists():
            InstructorVisit.objects.create(name=name, email=email, subject=subject)

        user = User.objects.filter(email=email).first()
        if not user:
            username = get_unique_username(email)
            user = User.objects.create_user(username=username, email=email, password='defaultpass')

        course = explorecourse.objects.filter(course_name=subject).first()
        if course:
            InstructorAccessRequest.objects.update_or_create(
                user=user,
                defaults={'course': course, 'status': 'pending'}
            )
        messages.success(request, "Your request has been submitted for approval.")
        return redirect('instructor_main')


# Course Exploration and Materials
def explore(request):
    courses = explorecourse.objects.all()
    return render(request, "explore.html", {"courses": courses})

@login_required
def upload_material(request):
    try:
        access = InstructorAccessRequest.objects.get(user=request.user, status='approved')
    except InstructorAccessRequest.DoesNotExist:
        messages.warning(request, "Access denied. Awaiting approval.")
        return redirect('instructor_main')

    allowed_course = access.course

    if request.method == 'POST':
        course_id = request.POST.get('course')
        if str(allowed_course.id) != course_id:
            messages.error(request, "You're only allowed to upload materials to your approved course.")
            return redirect('upload_material')

        title = request.POST.get('title')
        file = request.FILES.get('file')
        UploadedMaterial.objects.create(
            course=allowed_course,
            title=title,
            file=file,
            uploaded_at=timezone.now()
        )
        messages.success(request, "File uploaded successfully.")
        return redirect('upload_material')

    return render(request, 'upload.html', {
        'courses': [allowed_course],
        'uploaded_materials': UploadedMaterial.objects.filter(course=allowed_course).order_by('-uploaded_at')
    })


# Assignment Management
def assignment(request):
    if request.method == 'POST' and 'upload' in request.POST:
        Assignment.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            file=request.FILES.get('file'),
            due_date=request.POST.get('due_date')
        )
        return redirect('assignment')

    assignments = Assignment.objects.all().order_by('-created_at')
    return render(request, 'assignment.html', {'assignments': assignments})

def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
    return redirect('assignment')

def classroom(request):
    assignments = Assignment.objects.all().order_by('-created_at')
    now = timezone.now()
    last_submission = None

    if request.method == 'POST' and 'submit' in request.POST:
        assignment_id = request.POST.get('assignment_id')
        file = request.FILES.get('file')
        student_name = request.POST.get('student_name')
        roll_number = request.POST.get('roll_number')
        comments = request.POST.get('comments')

        assignment = get_object_or_404(Assignment, id=assignment_id)

        if now <= assignment.due_date:
            last_submission = Submission.objects.create(
                assignment=assignment,
                file=file,
                student_name=student_name,
                roll_number=roll_number,
                comments=comments
            )
        else:
            return render(request, 'classroom.html', {
                'assignments': assignments,
                'now': now,
                'error': "Submission closed! Due date has passed."
            })

    return render(request, 'classroom.html', {
        'assignments': assignments,
        'now': now,
        'last_submission': last_submission
    })


# Enrollment & Materials View
def enroll(request):
    Enrollment = apps.get_model('pupel', 'Enrollment')
    if request.method == 'POST':
        Enrollment.objects.create(
            student_name=request.POST.get('student_name'),
            email=request.POST.get('email'),
            course_name=request.POST.get('course_name'),
            date_time=request.POST.get('datetime')
        )
        return redirect('view_materials', course_name=request.POST.get('course_name'))
    elif request.method == 'GET':
        course_name = request.GET.get('course_name', '')
        current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        return render(request, 'enroll.html', {
            'course_name': course_name,
            'current_time': current_time,
        })

def view_materials(request, course_name):
    materials = UploadedMaterial.objects.filter(course__course_name__iexact=course_name)
    return render(request, 'materials.html', {'materials': materials, 'course_name': course_name})


# View and Manage Students/Instructors
def view_student(request):
    users = User.objects.all()
    return render(request, 'view_student.html', {'pro': users})

def instructor_view(request):
    instructors = InstructorVisit.objects.all()
    return render(request, 'instructor_view.html', {'instructors': instructors})

def delete_instructor(request, instructor_id):
    instructor = get_object_or_404(InstructorVisit, id=instructor_id)
    instructor.delete()
    return redirect('instructor_view')


# Submissions and Chat
def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment).order_by('-submitted_at')
    return render(request, 'submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })

def chat_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    messages_qs = SubmissionMessage.objects.filter(submission=submission).order_by('timestamp')

    if request.method == 'POST':
        sender = request.POST.get('sender')  # "student" or "instructor"
        message = request.POST.get('message')
        if message:
            SubmissionMessage.objects.create(
                submission=submission,
                sender=sender,
                message=message
            )
        return redirect('chat_submission', submission_id=submission.id)

    return render(request, 'chat.html', {
        'submission': submission,
        'messages': messages_qs
    })
