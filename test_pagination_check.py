import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Employee_task_mgt.settings')
django.setup()

from django.test import RequestFactory
from home.models import CustomUser

factory = RequestFactory()
request = factory.get('/team/team_work_entries/?page=2&start_date=2024-01-01&end_date=2024-01-31')
request.user = CustomUser.objects.filter(role='admin').first()

from home.views import team_work_entries
response = team_work_entries(request)
html = response.content.decode('utf-8')
if "start_date=2024-01-01" in html:
    print("SUCCESS: Found start_date in pagination links.")
else:
    print("FAIL: start_date not found in pagination links.")
if "end_date=2024-01-31" in html:
    print("SUCCESS: Found end_date in pagination links.")
else:
    print("FAIL: end_date not found in pagination links.")
