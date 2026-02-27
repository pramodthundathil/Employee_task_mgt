import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Employee_task_mgt.settings')
django.setup()

from home.models import CustomUser, WorkEntry, Project

semi_admin = CustomUser.objects.filter(role='semi-admin').first()
print("Semi admin:", semi_admin.email, semi_admin.work_location)

team_members = CustomUser.objects.filter(
    work_entries__employee__work_location=semi_admin.work_location
).distinct()

print("Team members by my logic:", [tm.email for tm in team_members])

correct = CustomUser.objects.filter(work_location=semi_admin.work_location)
print("Team members by correct logic:", [tm.email for tm in correct])

work_entries = WorkEntry.objects.filter(employee__work_location=semi_admin.work_location)
print("Work entries by my logic:", work_entries.count())

