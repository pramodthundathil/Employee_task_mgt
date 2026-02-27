import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Employee_task_mgt.settings')
django.setup()

from home.models import CustomUser, WorkEntry, Project

semi_admin = CustomUser.objects.get(id=17) # dubai
print(f"Semi-admin: {semi_admin.email}, Location: {semi_admin.work_location}")

work_entries = WorkEntry.objects.filter(employee__work_location=semi_admin.work_location)
print("Entries count:", work_entries.count())
if work_entries.exists():
    for we in work_entries[:5]:
        print(we.employee.email, we.employee.work_location)

other_entries = WorkEntry.objects.exclude(employee__work_location=semi_admin.work_location)
print("Other entries count:", other_entries.count())

