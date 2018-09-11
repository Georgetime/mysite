from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'student_name', 'student_sex', 'class_name', 'student_birthday')

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'org', 'telephone', 'mod_date')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'teacher_name', 'teacher_telephone')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', )

class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', )

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule_name', 'subject', 'class_name', 'teacher', 'representative')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'assignment_title', 'assignment_detail', 'schedule',
                    'create_date', 'finish_date')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'level', 'description')

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Student, StudentAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Subject, SubjectAdmin)
# admin.site.register(User)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Score, ScoreAdmin)
