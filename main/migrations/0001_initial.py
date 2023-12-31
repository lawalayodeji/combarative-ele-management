# Generated by Django 4.0.4 on 2023-06-02 22:34

from django.db import migrations, models
import django.db.models.deletion
import froala_editor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('studentKey', models.IntegerField(unique=True)),
                ('facultyKey', models.IntegerField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='myUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('is_teacher', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, default='Student', max_length=100)),
                ('photo', models.ImageField(blank=True, default='profile_pics/default_student.png', upload_to='profile_pics')),
                ('course', models.ManyToManyField(blank=True, related_name='students', to='main.course')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='main.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserStudent', to='main.myuser')),
            ],
            options={
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='StudentChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('COMPUTER SCIENCE', 'COMPUTER SCIENCE'), ('BIOCHEMISTRY', 'BIOCHEMISTRY'), ('CHEMISTRY', 'CHEMISTRY'), ('MICROBOLOGY', 'MICROBOLOGY')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=2000)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='materials/')),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
            ],
            options={
                'verbose_name_plural': 'Materials',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, default='Faculty', max_length=100)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty', to='main.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserFaculty', to='main.myuser')),
            ],
            options={
                'verbose_name_plural': 'Faculty',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='main.department'),
        ),
        migrations.AddField(
            model_name='course',
            name='faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.faculty'),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('file', models.FileField(blank=True, null=True, upload_to='assignments/')),
                ('marks', models.DecimalField(decimal_places=2, max_digits=6)),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
            ],
            options={
                'verbose_name_plural': 'Assignments',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('description', froala_editor.fields.FroalaField()),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course')),
            ],
            options={
                'verbose_name_plural': 'Announcements',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='submissions/')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('marks', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
            options={
                'verbose_name_plural': 'Submissions',
                'ordering': ['datetime'],
                'unique_together': {('assignment', 'student')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('code', 'department', 'name')},
        ),
    ]
