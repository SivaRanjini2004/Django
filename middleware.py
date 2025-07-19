from django.shortcuts import redirect
from django.contrib import messages
from .models import InstructorAccessRequest

class InstructorApprovalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if request.user.is_authenticated and request.user.is_staff is False:
            restricted_paths = ['/upload/', '/assignment/']
            if any(path.startswith(p) for p in restricted_paths):
                try:
                    access = InstructorAccessRequest.objects.get(user=request.user)
                    if access.status == 'rejected':
                        messages.error(request, 'Your instructor request was rejected.')
                        from django.contrib.auth import logout
                        logout(request)
                        return redirect('Instructor_login')
                    elif access.status != 'approved':
                        messages.warning(request, 'Access denied until your request is approved.')
                        return redirect('instructor_main')
                except InstructorAccessRequest.DoesNotExist:
                    return redirect('instructor_main')
        return self.get_response(request)
