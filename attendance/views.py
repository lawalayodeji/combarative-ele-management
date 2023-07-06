from django.contrib import messages
from django.shortcuts import render, redirect
from . models import Attendance
from main.models import Student, Course, Faculty, myUser
from django.contrib.auth.decorators import login_required

# from main.views import is_faculty_authorised

@login_required
def attendance(request, code):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        course = Course.objects.get(code=code)
        students = Student.objects.filter(course__code=code)

        return render(request, 'attendance/attendance.html', {'students': students, 'course': course, 'faculty': Student.objects.get(course=course), 'myId': user.id})

@login_required
def createRecord(request, code):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        if request.method == 'POST':
            date = request.POST['dateCreate']
            course = Course.objects.get(code=code)
            students = Student.objects.filter(course__code=code)
            # check if attendance record already exists for the date
            if Attendance.objects.filter(date=date, course=course).exists():
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Student.objects.get(course=course), 'myId': user.id, 'error': "Attendance record already exists for the date " + date})
            else:
                for student in students:
                    attendance = Attendance(
                        student=student, course=course, date=date, status=False)
                    attendance.save()

                messages.success(
                    request, 'Attendance record created successfully for the date ' + date)
                return redirect('/attendance/' + str(code))
        else:
            return redirect('/attendance/' + str(code))
    else:
        return redirect('std_login')

@login_required
def loadAttendance(request, code):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        if request.method == 'POST':
            date = request.POST['date']
            course = Course.objects.get(code=code)
            students = Student.objects.filter(course__code=code)
            attendance = Attendance.objects.filter(course=course, date=date)
            # check if attendance record exists for the date
            if attendance.exists():
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Student.objects.get(course=course), 'myId': user.id, 'attendance': attendance, 'date': date})
            else:
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Student.objects.get(course=course), 'myId': user.id, 'error': 'Could not load. Attendance record does not exist for the date ' + date})

    else:
        return redirect('std_login')

@login_required
def submitAttendance(request, code):
    user = myUser.objects.get(username=request.user.username)
    if user.is_teacher == True:
        try:
            students = Student.objects.filter(course__code=code)
            # print(students)
            course = Course.objects.get(code=code)
            if request.method == 'POST':
                date = request.POST['datehidden']
                for student in students:
                    attendance = Attendance.objects.get(
                        student=student, course=course, date=date)
                    if request.POST.get(str(student.id)) == '1':
                        attendance.status = True
                    else:
                        attendance.status = False
                    attendance.save()
                messages.success(
                    request, 'Attendance record submitted successfully for the date ' + date)
                return redirect('/attendance/' + str(code))

            else:
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Student.objects.get(course=course), 'myId': user.id})
        except:
            return render(request, 'attendance/attendance.html', {'code': code, 'error': "Error! could not save", 'students': students, 'course': course, 'faculty': Student.objects.get(course=course), 'myId': user.id})
