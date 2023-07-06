from django.shortcuts import redirect, render
from discussion.models import FacultyDiscussion, StudentDiscussion
from main.models import Student, Faculty, Course, myUser
# from main.views import is_faculty_authorised, is_student_authorised
from itertools import chain
from .forms import StudentDiscussionForm, FacultyDiscussionForm
from django.contrib.auth.decorators import login_required


# Create your views here.


''' We have two different user models.
    That's why we are filtering the discussions based on the user type and then combining them.'''


def context_list(course):
    try:
        studentDis = StudentDiscussion.objects.filter(course=course)
        facultyDis = FacultyDiscussion.objects.filter(course=course)
        discussions = list(chain(studentDis, facultyDis))
        discussions.sort(key=lambda x: x.sent_at, reverse=True)

        for dis in discussions:
            if dis.__class__.__name__ == 'StudentDiscussion':
                dis.author = Student.objects.get(id=dis.sent_by_id)
            else:
                dis.author = Student.objects.get(id=dis.sent_by_id)
    except:

        discussions = []

    return discussions

@login_required
def discussion(request, code):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False:
        course = Course.objects.get(code=code)
        student = Student.objects.get(user_id=user.id)
        discussions = context_list(course)
        form = StudentDiscussionForm()
        context = {
            'course': course,
            'student': student,
            'discussions': discussions,
            'form': form,
            'myId': user.id,
        }
        return render(request, 'discussion/discussion.html', context)

    elif user.is_teacher == True:
        course = Course.objects.get(code=code)
        faculty = Student.objects.get(user_id=user.id)
        discussions = context_list(course)
        form = FacultyDiscussionForm()
        context = {
            'course': course,
            'faculty': faculty,
            'discussions': discussions,
            'form': form,
            'myId': user.id,

        }
        return render(request, 'discussion/discussion.html', context)
    else:
        return redirect('std_login')

@login_required
def send(request, code, std_id):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == False:
        if request.method == 'POST':
            form = StudentDiscussionForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                course = Course.objects.get(code=code)
                try:
                    student = Student.objects.get(user_id=user.id)
                except:
                    return redirect('discussion', code=code)
                StudentDiscussion.objects.create(
                    content=content, course=course, sent_by=student)
                return redirect('discussion', code=code)
            else:
                return redirect('discussion', code=code)
        else:
            return redirect('discussion', code=code)
    else:
        return render(request, 'std_login.html')



@login_required
def send_fac(request, code, fac_id):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        if request.method == 'POST':
            form = FacultyDiscussionForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                course = Course.objects.get(code=code)
                try:
                    faculty = Student.objects.get(user_id=user.id)
                except:
                    return redirect('discussion', code=code)
                FacultyDiscussion.objects.create(
                    content=content, course=course, sent_by=faculty)
                return redirect('discussion', code=code)
            else:
                return redirect('discussion', code=code)
        else:
            return redirect('discussion', code=code)
    else:
        return render(request, 'std_login.html')
