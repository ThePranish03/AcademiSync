# Generated by Django 5.1.5 on 2025-03-29 18:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('teacher_code', models.CharField(editable=False, max_length=10, unique=True)),
                ('student_code', models.CharField(editable=False, max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_users', to='users.batch')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_code', models.CharField(max_length=20, unique=True)),
                ('college_name', models.CharField(max_length=255)),
                ('num_classes', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='school',
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('trainer', 'Trainer'), ('student', 'Student')], default='student', max_length=10),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='batch',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='users.school'),
        ),
    ]
