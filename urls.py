from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_logout

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('home', views.home, name='home'),
    path('homee', views.homee, name='homee'),
    path('main', views.main, name='main'),
    path('about', views.about, name='about'),
    path('Instructor_login', views.Instructor_login, name='Instructor_login'),
    path('Student_login', views.Student_login, name='Student_login'),
    path('Student_main', views.Student_main, name='Student_main'),
    path('explore', views.explore, name='explore'),
    path('change_password', views.change_password, name='change_password'),
    path('signup', views.signup, name='signup'),
    path('enroll', views.enroll, name='enroll'),
    path('my_dashboard', views.my_dashboard, name='my_dashboard'),
    path('pupel/logout/', custom_logout, name='logout'),
    path('pupel/logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
    path('instructor_main/', views.instructor_main, name='instructor_main'),
    path('assignment/', views.assignment, name='assignment'),
    path('classroom/', views.classroom, name='classroom'),
    path('delete-assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('upload/', views.upload_material, name='upload_material'),
    path('materials/<str:course_name>/', views.view_materials, name='view_materials'),
    path('view_student/', views.view_student, name='view_student'),
    path('submit_instructor_info/', views.submit_instructor_info, name='submit_instructor_info'),
    

    path('Instructor_login/', views.Instructor_login, name='Instructor_login'),
    path('instructor_main/', views.instructor_main, name='instructor_main'),
    path('submit_instructor_info/', views.submit_instructor_info, name='submit_instructor_info'),
    path('instructor_view/', views.instructor_view, name='instructor_view'),
    path('delete_instructor/<int:instructor_id>/', views.delete_instructor, name='delete_instructor'),
    path('submit_access_request/', views.submit_access_request, name='submit_access_request'),

    # path('submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),
    # path('chat/<int:submission_id>/', views.chat_submission, name='chat_submission'),

    path('', views.classroom, name='classroom'),
    path('assignments/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),
    path('chat/<int:submission_id>/', views.chat_submission, name='chat_submission'),

]