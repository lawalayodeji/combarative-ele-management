# Generated by Django 4.0.4 on 2023-06-02 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='email',
            field=models.EmailField(default='ayodeji@gmail.com', max_length=255, unique=True, verbose_name='email address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_teacher',
            field=models.BooleanField(default=False, null=True),
        ),
    ]