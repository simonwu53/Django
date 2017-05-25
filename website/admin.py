from django.contrib import admin
from website.models import UserProfile, Course, Discuss, Consult, Message, Bulletin, Uploaded_files, Assignment, \
    Assignment_file, Assignment_comment
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

# Extend User
class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)


# other models
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'coursename', 'user', 'classes')
    list_filter = ('code', 'user', 'classes')


class DiscussAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'time', 'content')
    list_filter = ('code', 'user', 'time')


class ConsultAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time', 'code')
    list_filter = ('user', 'time', 'code')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'receive', 'time')
    list_filter = ('user', 'receive', 'time')


class BulletinAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'code', 'classes', 'time')
    list_filter = ('user', 'code', 'classes', 'time')


class Uploaded_filesAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'classes', 'time', 'file')
    list_filter = ('user', 'code', 'classes', 'time')


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'classes', 'time', 'user', 'deadline')
    list_filter = ('code', 'classes', 'user', 'time', 'deadline')


class Assignment_fileAdmin(admin.ModelAdmin):
    list_display = ('assignments_id', 'user_id', 'time', 'file')
    list_filter = ('assignments_id', 'user_id', 'time')


class Assignment_commentAdmin(admin.ModelAdmin):
    list_display = ('assignment_file_id', 'user_id', 'comment')
    list_filter = ('assignment_file_id', 'user_id')

admin.site.register(Course, CourseAdmin)
admin.site.register(Discuss, DiscussAdmin)
admin.site.register(Consult, ConsultAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Uploaded_files, Uploaded_filesAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Assignment_file, Assignment_fileAdmin)
admin.site.register(Assignment_comment, Assignment_commentAdmin)
