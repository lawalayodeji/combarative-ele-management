# Generated by Django 4.0.4 on 2023-06-06 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_course_faculty_alter_course_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='otp_token',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
