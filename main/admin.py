from django.contrib import admin

# Register your models here.
from .models import Student, Faculty, Course, Department, Assignment, Announcement,StudentChoice,myUser


admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Assignment)
admin.site.register(Announcement)
admin.site.register(StudentChoice)
admin.site.register(myUser)

