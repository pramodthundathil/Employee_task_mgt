import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Employee_task_mgt.settings')
django.setup()

from django.template.loader import render_to_string
from django.test import RequestFactory
from home.models import CustomUser

factory = RequestFactory()
request = factory.get('/team/team_work_entries/?page=2&start_date=2024-01-01&end_date=2024-01-31')
request.user = CustomUser.objects.filter(role='admin').first()

from home.views import team_work_entries
response = team_work_entries(request)
print("Response status:", response.status_code)
# Search for pagination links in the response content
html = response.content.decode('utf-8')
if "start_date=2024-01-01" in html:
    print("Found start_date in rendered pagination logic")
else:
    print("Did not find start_date in rendered HTML. Check pagination logic.")
