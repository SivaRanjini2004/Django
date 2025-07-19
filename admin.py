from django.contrib import admin

# Register your models here.
from .models import explorecourse
admin.site.register(explorecourse)

from .models import InstructorVisit  
admin.site.register(InstructorVisit)


from .models import InstructorAccessRequest

@admin.register(InstructorAccessRequest)
class InstructorAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'updated_at')
    actions = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        queryset.update(status='approved')
    def reject_selected(self, request, queryset):
        queryset.update(status='rejected')

    approve_selected.short_description = "Approve selected instructors"
    reject_selected.short_description = "Reject selected instructors"
from .models import InstructorAccessRequest

from .models import InstructorAccessRequest

# @admin.register(InstructorAccessRequest)
# class InstructorAccessAdmin(admin.ModelAdmin):
#     list_display = ('user', 'course', 'status', 'updated_at')
#     actions = ['approve_selected', 'reject_selected']

#     def approve_selected(self, request, queryset):
#         queryset.update(status='approved')

#     def reject_selected(self, request, queryset):
#         queryset.update(status='rejected')

 