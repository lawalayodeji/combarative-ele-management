from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Announcement, Assignment, Material, Student,StudentChoice,myUser,Course, Department


from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  

import smtplib
from email.mime.text import MIMEText
  
CHOICES_DEP = (
    ('COMPUTER SCIENCE','COMPUTER SCIENCE'),
    ('BIOCHEMISTRY','BIOCHEMISTRY'),
    ('CHEMISTRY','CHEMISTRY'),
    ('MICROBOLOGY','MICROBOLOGY'),
)

arr = []
def get_departmentf():
    depv= Department.objects.all()
    
    for dep in depv:
        arr.append((dep.name, dep.name))
    CHOICES_DEP = tuple(arr)
    return CHOICES_DEP


depv= Department.objects.all()
if len(depv) > len(CHOICES_DEP):
    CHOICES_DEP = get_departmentf()


class CustomUserCreationForm(forms.ModelForm):  
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    email = forms.EmailField(label='email')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
    # is_teacher = forms.BooleanField()
    class Meta:
        model = myUser
        fields = ['username','email','password1', 'password2']
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class StudentRegDep(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentRegDep, self).__init__(*args, **kwargs)
        self.fields['department'].required = True
        self.fields['department'].label = ''

    department = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control mt-1'}), choices=CHOICES_DEP)

    class Meta:
        model = StudentChoice
        fields = ['department']
        
class TeacherCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeacherCourseForm, self).__init__(*args, **kwargs)
        self.fields['code'].required = True
        self.fields['code'].label = ''
        self.fields['name'].required = True
        self.fields['name'].label = ''

    
    class Meta:
        model = Course
        fields = ['code','name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-1', 'id': 'mycourse_name', 'placeholder': 'course name'}),
            'code': forms.NumberInput(attrs={'class': 'form-control mt-1', 'id': 'marksCode', 'name': 'code', 'placeholder': 'course code'}),

        }



class AnnouncementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = True
        self.fields['description'].label = ''

    class Meta:
        model = Announcement
        fields = ['description']
        widgets = {
            'description': FroalaEditor(),
        }


class AssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.label = ''
        self.fields['file'].required = False

    class Meta:
        model = Assignment
        fields = ('title', 'description', 'deadline', 'marks', 'file')
        widgets = {
            'description': FroalaEditor(),
            'title': forms.TextInput(attrs={'class': 'form-control mt-1', 'id': 'title', 'name': 'title', 'placeholder': 'Title'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control mt-1', 'id': 'deadline', 'name': 'deadline', 'type': 'datetime-local'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control mt-1', 'id': 'marks', 'name': 'marks', 'placeholder': 'Marks'}),
            'file': forms.FileInput(attrs={'class': 'form-control mt-1', 'id': 'file', 'name': 'file', 'aria-describedby': 'file', 'aria-label': 'Upload'}),
        }

class DepartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args,**kwargs)

    class Meta:
        model = Department
        fields = ('name',"description")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-1', 'id': 'department_name', 'name': 'name', 'placeholder': 'Name of department'}),
            'description': FroalaEditor()

        }


class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.label = ""
        self.fields['file'].required = False

    class Meta:
        model = Material
        fields = ('description', 'file')
        widgets = {
            'description': FroalaEditor(),
            'file': forms.FileInput(attrs={'class': 'form-control', 'id': 'file', 'name': 'file', 'aria-describedby': 'file', 'aria-label': 'Upload'}),
        }

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    return True
