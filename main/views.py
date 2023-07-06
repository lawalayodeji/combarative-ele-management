import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Student, Course, Announcement, Assignment, Submission, Material, Faculty, Department,myUser,get_department
from django.template.defaulttags import register
from django.db.models import Count, Q
from django.http import HttpResponseRedirect

from .forms import AnnouncementForm, AssignmentForm, MaterialForm, CustomUserCreationForm,StudentRegDep,send_email,TeacherCourseForm,DepartmentForm,get_departmentf
from django import forms
from django.core import validators
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random
from django import forms
# from django.core.mail import send_mail
from django.conf import settings

# subject = "Email Subject"
# body = "This is my second text"
# sender = "lawalayodeji133@gmail.com"
# recipients = ["lawalayodeji311@gmail.com"]

class LoginForm(forms.Form):
    username = forms.CharField(label='username', min_length=5, max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# def is_student_authorised(request, code):
#     course = Course.objects.get(code=code)
#     if user.is_teacher == False and course in Student.objects.get(user_id = user.id).course.all():
#         return True
#     else:
#         return False


# user = myUser.objects.filter(username=request.user.username)
#  def login(request): # this function handles the login form POST
#     user = auth.authenticate(username=username, password=password)  
#     if user is not None: # if the user object exist
#          from mfa.helpers import has_mfa
#          res =  has_mfa(username = username,request=request) # has_mfa returns false or HttpResponseRedirect
#          if res:
#              return res
#          return log_user_in(request,username=user.username) 



def register_p(request):
    error_messages = []
    
    if request.method == 'POST':  
        username = request.POST['username']        
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            form.save()             
            error_messages.append('registration successful.')
            return redirect('std_login')

        else:
        
            error_messages.append('please check your credentials.')
        
    else:  
        form = CustomUserCreationForm()  
    context = {  
        'form':form,
        'messages':error_messages
    }  
    return render(request, 'register_page.html', context)  

def register_teacher(request):
    error_messages = []
    
    if request.method == 'POST':  
        username = request.POST['username']
        form = CustomUserCreationForm(request.POST)  
        if form.is_valid():
            form.save()  
            error_messages.append('registration successful.')
            return redirect('std_login')

        else:
        
            error_messages.append('please check your credentials.')
        
    else:  
        form = CustomUserCreationForm()  
    context = {  
        'form':form,
        'messages':error_messages
    }  
    return render(request, 'register_page.html', context)  


@login_required
def teacher_course(request):
    
    error_messages = []
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        if request.method == "POST":
            form = TeacherCourseForm(request.POST)
            teacher = Student.objects.get(user=user)
            department_name = teacher.department.name
            department = Department.objects.get(name=department_name)
            
            if form.is_valid():
                code = request.POST['code']
                mycourse_nam = request.POST['name']
                course_obj = Course()
                course_obj.name = mycourse_nam
                course_obj.code = code
                course_obj.department= department
                course_obj.faculty = teacher
                course_obj.save()
                error_messages.append("Course added successfully!")
                return redirect("courses")
        form = TeacherCourseForm()
        context = {
            "form": form,
            "error_messages":error_messages,
        }
        return render(request, 'main/teacher_course.html', context)  

            
    else:
        return redirect('std_login')



@login_required
def student_register_dep(request):
    error_messages = []

    user = myUser.objects.filter(username=request.user.username)
    if request.method == "POST":
        form = StudentRegDep(request.POST)
        student = Student()
        if form.is_valid():
            department = request.POST['department']
            depart_obj  = Department.objects.filter(name=department)
            if depart_obj.exists() and user.exists():
                if Student.objects.filter(user__username=request.user.username).exists() == False:
                    userobj = myUser.objects.get(username=request.user.username)
                    depart_obj1  = Department.objects.get(name=department)
                    student.user = userobj
                    student.department = depart_obj1
                    student.save()
                    form.save()  
                    error_messages.append('Details added successfully.')
                    return redirect('courses')
                else:

                    error_messages.append('You are already a student you dont need to register')


        else:
            print("eror")
            error_messages.append('please try again!.')
    else:
        form = StudentRegDep()
    context = {  
        'form':form,
        'error_messages':error_messages
    }  
    return render(request, 'main/student_cho.html', context)  






def std_login(request):
    error_messages = []
    get_department()


    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # from mfa.helpers import has_mfa
            user = authenticate(request,username=username, password=password)

            if user is not None:
                user1 = myUser.objects.get(username=username)
                otp= random.randrange(100000,999999)
                user1.otp_token = otp
                user1.save()
                request.session["username"] = username
                subject = "Token verification"
                password_email = "fgnwwdqgaphnnngn"

                body = f'Dear {username}, your OTP for login is {otp}. Use this OTP to validate your login.'
                send_email(subject, body, "lawalayodeji133@gmail.com", [user1.email], password_email)

                messages.success(request, "Your OTP has been send to your email.")
                return redirect("otpverification")

                # login(request, user)
                # # res =  has_mfa(username = id,request=request) # has_mfa returns false or HttpResponseRedirect
                # if  user.is_teacher == False:
                #     return redirect('myCourses')
                # else:
                #     return redirect('/facultyCourses/')
                

                # request.session['student_id'] = id
                # res =  has_mfa(username = id,request=request) # has_mfa returns false or HttpResponseRedirect
                # if res:
                # return redirect('myCourses')
            # elif Faculty.objects.filter(faculty_id=id, password=password).exists():
            #     request.session['faculty_id'] = id
            #     return redirect('facultyCourses')
            else:
                error_messages.append('Invalid login credentials.')
        else:
            error_messages.append('Invalid form data.')
    else:
        form = LoginForm()

    context = {'form': form, 'error_messages': error_messages}
    return render(request, 'login_page.html', context)




def otp_verification(request):
    username = request.session['username']

    if request.method == "POST":
        
        otp = request.POST.get('username')
        print(otp)
        user = myUser.objects.filter(username = username).first()
        print(f"{user.otp_token} is the user token")
        print(int(otp) == int(user.otp_token) )
        if int(otp) == int(user.otp_token):
            user = myUser.objects.get(username = username)
            user.otp_token = None
            user.save()
            messages.success(request, "OTP Success. Please login with your credentials!")
            login(request, user)
            if user.is_teacher == False:
                return redirect('myCourses')
            else:
                return redirect('/facultyCourses/')

        else:
            messages.error(request, "Wrong OTP!!")
    return render(request, "main/otpVerification.html")


# Clears the session on logout



def std_logout(request):
    logout(request)
    return redirect('std_login')

@login_required
def addDepartment(request):
    error_messages = []
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        if request.method == "POST":
            form = DepartmentForm(request.POST)
            student = Student()
            if form.is_valid():
                form.save()
                get_departmentf()

                error_messages.append("Department added successfully!")
            else:   
                error_messages.append("error check input!")                
                         

        form = DepartmentForm()
        context = {
            "error_messages":error_messages,
            "form": form,
            "myId": user.id
        }

        return render(request,"main/department_add.html", context)

    else:
        return redirect('std_login')



# Display all courses (student view)
@login_required
def myCourses(request):
    try:
        student = Student.objects.get(
            user__username=request.user.username)
        courses = student.course.all()
        # faculty = student.course.all().values_list('id', flat=True)
        context = {
            'courses': courses,
            'student': student,
            'faculty': student,
        }

        return render(request, 'main/myCourses.html', context)
    except:
        return redirect("registerDepart")


# Display all courses (faculty view)
@login_required
def facultyCourses(request):
    # try:
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        faculty = Student.objects.get(
            user__id=user.id)
        courses = Course.objects.filter(
            faculty__user__id=user.id)
        # Student count of each course to show on the faculty page
        studentCount = Course.objects.all().annotate(student_count=Count('students'))

        studentCountDict = {}

        for course in studentCount:
            studentCountDict[course.code] = course.student_count

        @register.filter
        def get_item(dictionary, course_code):
            return dictionary.get(course_code)

        context = {
            'courses': courses,
            'faculty': faculty,
            'studentCount': studentCountDict,
            'myId': user.id
        }

        return render(request, 'main/facultyCourses.html', context)

    else:
        return redirect('std_login')

# Particular course page (student view)
@login_required
def course_page(request, code):
    
    try:
        user = myUser.objects.get(username=request.user.username)

        course = Course.objects.get(code=code)
        try:
            announcements = Announcement.objects.filter(course_code=course)
            assignments = Assignment.objects.filter(
                course_code=course.code)
            materials = Material.objects.filter(course_code=course.code)

        except:
            announcements = None
            assignments = None
            materials = None

        context = {
            'course': course,
            'announcements': announcements,
            'assignments': assignments[:3],
            'materials': materials,
            'student': Student.objects.get(user_id=user.id),
            "myId": user.id,
        }

        return render(request, 'main/course.html', context)

    except:
        return render(request, 'error.html')


# Particular course page (faculty view)
@login_required
def course_page_faculty(request, code):
    course = Course.objects.get(code=code)
    user = myUser.objects.get(username=request.user.username)
    
    try:
        announcements = Announcement.objects.filter(course_code=course)
        assignments = Assignment.objects.filter(
            course_code=course.code)
        materials = Material.objects.filter(course_code=course.code)
        studentCount = Student.objects.filter(course=course).count()

    except:
        announcements = None
        assignments = None
        materials = None

    context = {
        'course': course,
        'announcements': announcements,
        'assignments': assignments[:3],
        'materials': materials,
        'faculty': Student.objects.get(user_id=user.id),
        'studentCount': studentCount,
        'myId': user.id,
    }

    return render(request, 'main/faculty_course.html', context)
  

def error(request):
    return render(request, 'error.html')


# Display user profile(student & faculty)
@login_required
def profile(request, id):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False:
        student = Student.objects.get(user_id=user.id)
        return render(request, 'main/profile.html', {'student': student, 'myId': user.id})
    else:
        faculty = Student.objects.get(user_id=user.id)
        return render(request, 'main/faculty_profile.html', {'faculty': faculty, 'myId': user.id})

@login_required
def addAnnouncement(request, code):
        user = myUser.objects.get(username=request.user.username)
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Announcement added successfully.')
                return redirect('/faculty/' + str(code))
        else:
            form = AnnouncementForm()
        return render(request, 'main/announcement.html', {'course': Course.objects.get(code=code), 'faculty': Student.objects.get(user_id=user.id), 'form': form, 'myId': user.id})
    
@login_required
def deleteAnnouncement(request, code, id):
    try:
        announcement = Announcement.objects.get(course_code=code, id=id)
        announcement.delete()
        messages.warning(request, 'Announcement deleted successfully.')
        return redirect('/faculty/' + str(code))
    except:
        return redirect('/faculty/' + str(code))

@login_required
def editAnnouncement(request, code, id):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        announcement = Announcement.objects.get(course_code=code, id=id)
        form = AnnouncementForm(instance=announcement)
        context = {
            'announcement': announcement,
            'course': Course.objects.get(code=code),
            'faculty': Student.objects.get(user_id=user.id),
            'form': form,
            'myId': user.id,
        }
        return render(request, 'main/update-announcement.html', context)
    else:
        return redirect('std_login')


@login_required
def updateAnnouncement(request, code, id):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        announcement = Announcement.objects.get(course_code=code, id=id)
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.info(request, 'Announcement updated successfully.')
            return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')


@login_required
def addAssignment(request, code):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher== True:
        if request.method == 'POST':
            form = AssignmentForm(request.POST, request.FILES)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                form.save()
                messages.success(request, 'Assignment added successfully.')
                return redirect('/faculty/' + str(code))
        else:
            form = AssignmentForm()
        return render(request, 'main/assignment.html', {'course': Course.objects.get(code=code), 'faculty': Student.objects.get(user_id=user.id), 'form': form,
        'myId': user.id,    
        })
    else:
        return redirect('std_login')

@login_required
def assignmentPage(request, code, id):
    user = myUser.objects.get(username=request.user.username)
    course = Course.objects.get(code=code)
    if user.is_teacher== False:
        assignment = Assignment.objects.get(course_code=course.code, id=id)
        try:

            submission = Submission.objects.get(assignment=assignment, student=Student.objects.get(
                user_id=user.id))

            context = {
                'assignment': assignment,
                'course': course,
                'submission': submission,
                'time': datetime.datetime.now(),
                'student': Student.objects.get(user_id=user.id),
                'courses': Student.objects.get(user_id=user.id).course.all(),
                'myId': user.id,

            }

            return render(request, 'main/assignment-portal.html', context)

        except:
            submission = None

        context = {
            'assignment': assignment,
            'course': course,
            'submission': submission,
            'time': datetime.datetime.now(),
            'student': Student.objects.get(user_id=user.id),
            'courses': Student.objects.get(user_id=user.id).course.all(),
            'myId': user.id,

        }

        return render(request, 'main/assignment-portal.html', context)
    else:

        return redirect('std_login')

@login_required
def allAssignments(request, code):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher==True:
        course = Course.objects.get(code=code)
        assignments = Assignment.objects.filter(course_code=course)
        studentCount = Student.objects.filter(course=course).count()

        context = {
            'assignments': assignments,
            'course': course,
            'faculty': Student.objects.get(user_id=user.id),
            'studentCount': studentCount,
            'myId': user.id,


        }
        return render(request, 'main/all-assignments.html', context)
    else:
        return redirect('std_login')

@login_required
def allAssignmentsSTD(request, code):
    user = myUser.objects.get(username=request.user.username)

    if user.is_teacher == False:
        course = Course.objects.get(code=code)
        assignments = Assignment.objects.filter(course_code=course)
        context = {
            'assignments': assignments,
            'course': course,
            'student': Student.objects.get(user_id = user.id),
            'myId': user.id,


        }
        return render(request, 'main/all-assignments-std.html', context)
    else:
        return redirect('std_login')


@login_required
def addSubmission(request, code, id):
    try:
        user = myUser.objects.get(username=request.user.username)
        course = Course.objects.get(code=code)
        if user.is_teacher == False:
            # check if assignment is open
            print("is me")
            assignment = Assignment.objects.get(course_code=course.code, id=id)
            if assignment.deadline < datetime.datetime.now():

                return redirect('/assignment/' + str(code) + '/' + str(id))

            if request.method == 'POST' and request.FILES['file']:
                assignment = Assignment.objects.get(
                    course_code=course.code, id=id)
                submission = Submission(assignment=assignment, student=Student.objects.get(
                    user_id = user.id), file=request.FILES['file'],)
                submission.status = 'Submitted'
                submission.save()
                return HttpResponseRedirect(request.path_info)
            else:
                assignment = Assignment.objects.get(
                    course_code=course.code, id=id)
                submission = Submission.objects.get(assignment=assignment, student=Student.objects.get(
                    user_id = user.id))
                context = {
                    'assignment': assignment,
                    'course': course,
                    'submission': submission,
                    'time': datetime.datetime.now(),
                    'student': Student.objects.get(user_id = user.id),
                    'courses': Student.objects.get(user_id = user.id).course.all(),
                    'myId': user.id,

                }

                return render(request, 'main/assignment-portal.html', context)
        else:
            return redirect('std_login')
    except:
        return HttpResponseRedirect(request.path_info)


@login_required
def viewSubmission(request, code, id):
    course = Course.objects.get(code=code)
    user = myUser.objects.get(username=request.user.username)

    if user.is_teacher==True:
        try:
            assignment = Assignment.objects.get(course_code_id=code, id=id)
            submissions = Submission.objects.filter(
                assignment_id=assignment.id)

            context = {
                'course': course,
                'submissions': submissions,
                'assignment': assignment,
                'totalStudents': len(Student.objects.filter(course=course)),
                'faculty': Student.objects.get(user_id=user.id),
                'courses': Course.objects.filter(user_id=user.id),
                'myId': user.id,

            }

            return render(request, 'main/assignment-view.html', context)

        except:
            return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')

@login_required
def gradeSubmission(request, code, id, sub_id):
    try:
        user = myUser.objects.get(username=request.user.username)
        course = Course.objects.get(code=code)
        if user.is_teacher==True:
            if request.method == 'POST':
                assignment = Assignment.objects.get(course_code_id=code, id=id)
                submissions = Submission.objects.filter(
                    assignment_id=assignment.id)
                submission = Submission.objects.get(
                    assignment_id=id, id=sub_id)
                submission.marks = request.POST['marks']
                if request.POST['marks'] == 0:
                    submission.marks = 0
                submission.save()
                return HttpResponseRedirect(request.path_info)
            else:
                assignment = Assignment.objects.get(course_code_id=code, id=id)
                submissions = Submission.objects.filter(
                    assignment_id=assignment.id)
                submission = Submission.objects.get(
                    assignment_id=id, id=sub_id)

                context = {
                    'course': course,
                    'submissions': submissions,
                    'assignment': assignment,
                    'totalStudents': len(Student.objects.filter(course=course)),
                    'faculty': Student.objects.get(user_id=user.id),
                    'courses': Course.objects.filter(user_id=user.id),
                    'myId': user.id,

                }

                return render(request, 'main/assignment-view.html', context)

        else:
            return redirect('std_login')
    except:
        return redirect('/error/')


@login_required
def addCourseMaterial(request, code):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher==True:
        if request.method == 'POST':
            form = MaterialForm(request.POST, request.FILES)
            form.instance.course_code = Course.objects.get(code=code)
            if form.is_valid():
                form.save()
                messages.success(request, 'New course material added')
                return redirect('/faculty/' + str(code))
            else:
                return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Student.objects.get(user_id=user.id), 'form': form,
                'myId': user.id,
            
                })
        else:
            form = MaterialForm()
            return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Student.objects.get(user_id=user.id), 'form': form,
            'myId': user.id,
            })
    else:
        return redirect('std_login')


@login_required
def deleteCourseMaterial(request, code, id):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher==True:
        course = Course.objects.get(code=code)
        course_material = Material.objects.get(course_code=course, id=id)
        course_material.delete()
        messages.warning(request, 'Course material deleted')
        return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')

@login_required
def courses(request):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False or user.is_teacher == True:

        courses = Course.objects.all()
        if user.is_teacher == False:
            student = Student.objects.get(
                user_id = user.id)
        else:
            student = None
        if user.is_teacher == True:
            faculty = Student.objects.get(
                user_id=user.id)
        else:
            faculty = None

        enrolled = student.course.all() if student else None
        accessed = Course.objects.filter(
            user_id = user.id) if faculty else None

        context = {
            'faculty': faculty,
            'courses': courses,
            'student': student,
            'enrolled': enrolled,
            'accessed': accessed,
            'myId': user.id,

        }

        return render(request, 'main/all-courses.html', context)

    else:
        return redirect('std_login')


@login_required
def departments(request):
    user = myUser.objects.get(username=request.user.username)
    print(user.id)
    if user.is_teacher == False or user.is_teacher == True:
        departments = Department.objects.all()
        if user.is_teacher == False:
            student = Student.objects.get(
                user_id = user.id)
        else:
            student = None
        if user.is_teacher == True:
            faculty = Student.objects.get(
                user_id=user.id)
        else:
            faculty = None
        context = {
            'faculty': faculty,
            'student': student,
            'deps': departments,
            "myId": user.id,
        }

        return render(request, 'main/departments.html', context)

    else:
        return redirect('std_login')

@login_required
def access(request, code):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False:
        course = Course.objects.get(code=code)
        student = Student.objects.get(user_id = user.id)
        if request.method == 'POST':
            if (request.POST['key']) == str(user.username):
                student.course.add(course)
                student.save()
                return redirect('/my/')
            else:
                messages.error(request, 'Invalid key')
                return HttpResponseRedirect(request.path_info)
        else:
            return render(request, 'main/access.html', {'course': course, 'student': student,
            'myId': user.id            
            })

    else:
        return redirect('std_login')


@login_required
def search(request):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False or user.is_teacher == True:
        if request.method == 'GET' and request.GET['q']:
            q = request.GET['q']
            courses = Course.objects.filter(Q(code__icontains=q) | Q(
                name__icontains=q) | Q(faculty__user__username__icontains=q))

            if user.is_teacher == False:
                student = Student.objects.get(
                    user_id = user.id)
            else:
                student = None
            if user.is_teacher == True:
                faculty = Student.objects.get(
                user_id=user.id)
            else:
                faculty = None
            enrolled = student.course.all() if student else None
            accessed = Course.objects.filter(
                user_id=user.id) if faculty else None

            context = {
                'courses': courses,
                'faculty': faculty,
                'student': student,
                'enrolled': enrolled,
                'accessed': accessed,
                'q': q,
                'myId': user.id,
            }
            return render(request, 'main/search.html', context)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('std_login')

@login_required
def changePasswordPrompt(request):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False or user.is_teacher == True:
        student = Student.objects.get(user_id = user.id)
        return render(request, 'main/changePassword.html', {'student': student, 
            'myId': user.id,
        
        })
    else:
        return redirect('std_login')

@login_required
def changePhotoPrompt(request):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False or user.is_teacher == True:
        student = Student.objects.get(user_id = user.id)
        return render(request, 'main/changePhoto.html', {'student': student,
            'myId': user.id,
        
        })
    else:
        return redirect('std_login')

@login_required
def changePassword(request):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False or user.is_teacher == True:
        student = Student.objects.get(
            user_id = user.id)
        if request.method == 'POST':
            if user.check_password(request.POST['oldPassword']) :
                # New and confirm password check is done in the client side
                user.set_password(request.POST['newPassword'])
                user.save()
                messages.success(request, 'Password was changed successfully')
                return redirect('/profile/' + str(user.id))
            else:
                messages.error(
                    request, 'Password is incorrect. Please try again')
                return redirect('/changePassword/')
        else:
            return render(request, 'main/changePassword.html', {'student': student,
            'myId': user.id,
            
            })
    else:
        return redirect('std_login')

# @login_required
# def changePasswordFaculty(request):
#     user = myUser.objects.get(username=request.user.username)
#     if user.is_teacher == True:
#         faculty = Student.objects.get(
#             user_id=user.id)
#         if request.method == 'POST':
#             if faculty.password == request.POST['oldPassword']:
#                 # New and confirm password check is done in the client side
#                 faculty.password = request.POST['newPassword']
#                 faculty.save()
#                 messages.success(request, 'Password was changed successfully')
#                 return redirect('/facultyProfile/' + str(faculty.faculty_id))
#             else:
#                 print('error')
#                 messages.error(
#                     request, 'Password is incorrect. Please try again')
#                 return redirect('/changePasswordFaculty/')
#         else:
#             print(faculty)
#             return render(request, 'main/changePasswordFaculty.html', {'faculty': faculty})
#     else:
#         return redirect('std_login')

@login_required
def changePhoto(request):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False:
        student = Student.objects.get(
            user_id = user.id)
        if request.method == 'POST':
            if request.FILES['photo']:
                student.photo = request.FILES['photo']
                student.save()
                messages.success(request, 'Photo was changed successfully')
                return redirect('/profile/' + str(user.id))
            else:
                messages.error(
                    request, 'Please select a photo')
                return redirect('/changePhoto/')
        else:
            return render(request, 'main/changePhoto.html', {'student': student,
            'myId': user.id,
            
            })
    else:
        return redirect('std_login')

@login_required
def changePhotoFaculty(request):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        student = Student.objects.get(user_username=request.user.username)

        if request.method == 'POST':
            if request.FILES['photo']:
                student.photo = request.FILES['photo']
                student.save()
                messages.success(request, 'Photo was changed successfully')
                return redirect('/facultyProfile/' + str(student.id))
            else:
                messages.error(
                    request, 'Please select a photo')
                return redirect('/changePhotoFaculty/')
        else:
            return render(request, 'main/changePhotoFaculty.html', {'student': student,
            'myId': user.id,
            
            })
    else:
        return redirect('std_login')


# def guestStudent(request):
#     request.session.flush()
#     try:
#         student = Student.objects.get(name='Guest Student')
#         request.session['student_id'] = str(student.student_id)
#         return redirect('myCourses')
#     except:
#         return redirect('std_login')


# def guestFaculty(request):
#     request.session.flush()
#     try:
#         faculty = Student.objects.get(name='Guest Faculty')
#         request.session['faculty_id'] = str(faculty.faculty_id)
#         return redirect('facultyCourses')
#     except:
#         return redirect('std_login')
