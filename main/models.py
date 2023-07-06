from django.db import models
from froala_editor.fields import FroalaField

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

global CHOICES_DEP
CHOICES_DEP = (
    ('COMPUTER SCIENCE','COMPUTER SCIENCE'),
    ('BIOCHEMISTRY','BIOCHEMISTRY'),
    ('CHEMISTRY','CHEMISTRY'),
    ('MICROBOLOGY','MICROBOLOGY'),
)




arr = []
def get_department():
    depv= Department.objects.all()
    
    for dep in depv:
        arr.append((dep.name, dep.name))
    CHOICES_DEP = tuple(arr)
    return CHOICES_DEP
    # return depv


class MyUserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username=username,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class myUser(AbstractBaseUser):
    username = models.CharField(max_length=100, null=False,unique=True)

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_teacher = models.BooleanField(default=False, null=True)
    otp_token = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = MyUserManager()

    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class StudentChoice(models.Model):

    department = models.CharField(
         max_length=30, choices =CHOICES_DEP)


class Student(models.Model):
    # student_id = models.IntegerField(primary_key=True)
    # name = models.CharField(max_length=100, null=False)
    # email = models.EmailField(max_length=100, null=True, blank=True)
    # password = models.CharField(max_length=255, null=False)
    user = models.ForeignKey('myUser', on_delete=models.CASCADE, null=False, related_name="UserStudent")
    role = models.CharField(
        default="Student", max_length=100, null=False, blank=True)
    course = models.ManyToManyField(
        'Course', related_name='students', blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True,
                              null=False, default='profile_pics/default_student.png')
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=False, blank=False, related_name='students')

    def delete(self, *args, **kwargs):
        if self.photo != 'profile_pics/default_student.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.user.username


class Faculty(models.Model):
    # faculty_id = models.IntegerField(primary_key=True)
    # name = models.CharField(max_length=100, null=False)
    # email = models.EmailField(max_length=100, null=True, blank=True)
    # password = models.CharField(max_length=255, null=False)
    user = models.ForeignKey('myUser', on_delete=models.CASCADE, null=False, related_name="UserFaculty")
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, null=False, related_name='faculty')
    role = models.CharField(
        default="Faculty", max_length=100, null=False, blank=True)
    # photo = models.ImageField(upload_to='profile_pics', blank=True,
    #                           null=False, default='profile_pics/default_faculty.png')

    # def delete(self, *args, **kwargs):
    #     if self.photo != 'profile_pics/default_faculty.png':
    #         self.photo.delete()
    #     super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Faculty'

    def __str__(self):
        return self.user.username


class Department(models.Model):
    # department_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

    def student_count(self):
        return self.students.count()

    def faculty_count(self):
        return self.faculty.count()

    def course_count(self):
        return self.courses.count()


class Course(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=False, related_name='courses')
    faculty = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True, blank=True,related_name='myfaculty')
    user = models.ForeignKey('myUser', on_delete=models.CASCADE, blank=True,null=True, related_name="CourseKey")
    

    class Meta:
        unique_together = ('code', 'department', 'name')
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Announcement(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    description = FroalaField()

    class Meta:
        verbose_name_plural = "Announcements"
        ordering = ['-datetime']

    def __str__(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")


class Assignment(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    deadline = models.DateTimeField(null=False)
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    class Meta:
        verbose_name_plural = "Assignments"
        ordering = ['-datetime']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def due_date(self):
        return self.deadline.strftime("%d-%b-%y, %I:%M %p")


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    file = models.FileField(upload_to='submissions/', null=True,)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    marks = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

    def file_name(self):
        return self.file.name.split('/')[-1]

    def time_difference(self):
        difference = self.assignment.deadline - self.datetime
        days = difference.days
        hours = difference.seconds//3600
        minutes = (difference.seconds//60) % 60
        seconds = difference.seconds % 60

        if days == 0:
            if hours == 0:
                if minutes == 0:
                    return str(seconds) + " seconds"
                else:
                    return str(minutes) + " minutes " + str(seconds) + " seconds"
            else:
                return str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"
        else:
            return str(days) + " days " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"

    def submission_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.student.name + " - " + self.assignment.title

    class Meta:
        unique_together = ('assignment', 'student')
        verbose_name_plural = "Submissions"
        ordering = ['datetime']


class Material(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    description = models.TextField(max_length=2000, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    file = models.FileField(upload_to='materials/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Materials"
        ordering = ['-datetime']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def post_date(self):
        return self.datetime.strftime("%d-%b-%y, %I:%M %p")

depv= Department.objects.all()
if len(depv) > len(CHOICES_DEP):
    CHOICES_DEP = get_department()

