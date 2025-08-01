# Generated by Django 5.2.4 on 2025-07-24 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_doctorprofile_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorprofile',
            name='working_hours',
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='doctor_pics/'),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='specialty',
            field=models.CharField(choices=[('Orthopedist', 'Orthopedist'), ('Dentist', 'Dentist'), ('Family Doctor', 'Family Doctor')], max_length=50),
        ),
        migrations.CreateModel(
            name='WorkingHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_hours', to='doctors.doctorprofile')),
            ],
            options={
                'ordering': ['day'],
            },
        ),
    ]
