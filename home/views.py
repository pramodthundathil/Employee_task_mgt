from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
import json
from .models import User, Project, Task, WorkEntry
from .forms import *


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    # Dashboard statistics
    total_employees = User.objects.filter(role='user', is_active=True).count()
    total_projects = Project.objects.filter(status='active').count()
    total_tasks = Task.objects.count()
    
    # Recent work entries
    recent_entries = WorkEntry.objects.select_related('employee', 'project').order_by('-created_at')[:5]
    
    # Active projects
    active_projects = Project.objects.filter(status='active').order_by('-created_at')[:5]
    
    context = {
        'total_employees': total_employees,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'recent_entries': recent_entries,
        'active_projects': active_projects,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def employee_dashboard(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    
    # Employee's active projects
    active_projects = Project.objects.filter(status='active')[:5]
    
    # Employee's recent work entries
    recent_entries = WorkEntry.objects.filter(employee=request.user).order_by('-work_date')[:5]
    
    # Employee's assigned tasks
    assigned_tasks = Task.objects.filter(assigned_to=request.user).order_by('-created_at')[:5]
    
    context = {
        'active_projects': active_projects,
        'recent_entries': recent_entries,
        'assigned_tasks': assigned_tasks,
    }
    return render(request, 'employee/dashboard.html', context)

# Admin Views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import User
from .forms import CustomUserForm
import json
from django.views.decorators.csrf import csrf_exempt



@login_required
def employee_management(request):
    """Display employee management page with all employees"""
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    employees = User.objects.filter(role='user').order_by('-date_joined')
    form = CustomUserForm()  # For the add employee modal
    
    context = {
        'employees': employees,
        'form': form,
    }
    return render(request, 'admin/employee_management.html', context)


@login_required
def add_employee(request):
    """Add new employee"""
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('employee_management')
        else:
            # Return form errors for AJAX handling
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserForm()
    
    return render(request, 'admin/employee_management.html', {'form': form})


@login_required
@csrf_exempt
def edit_employee(request, user_id):
    """Edit employee details"""
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    employee = get_object_or_404(User, id=user_id, role='user')
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Employee updated successfully!'
                })
            
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_management')
        else:
            # Return form errors for AJAX handling
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserForm(instance=employee)
    
    # For AJAX requests, return the form HTML
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form_html = render_to_string('admin/employee_edit_form.html', {
            'form': form,
            'employee': employee
        })
        return JsonResponse({'form_html': form_html})
    
    return render(request, 'admin/edit_employee.html', {
        'form': form,
        'employee': employee
    })


@login_required
def view_employee(request, user_id):
    """View employee details"""
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    employee = get_object_or_404(User, id=user_id, role='user')
    
    # For AJAX requests, return the employee details HTML
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        details_html = render_to_string('admin/employee_details.html', {
            'employee': employee
        })
        return JsonResponse({'details_html': details_html})
    
    return render(request, 'admin/employee_details.html', {'employee': employee})


@login_required
@csrf_protect
def toggle_employee_status(request, user_id):
    """Toggle employee active/inactive status"""
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    if request.method == 'POST':
        employee = get_object_or_404(User, id=user_id, role='user')
        employee.is_active = not employee.is_active
        employee.save()
        
        status = 'activated' if employee.is_active else 'deactivated'
        return JsonResponse({
            'success': True,
            'message': f'Employee {status} successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
@csrf_protect
def delete_employee(request, user_id):
    """Delete employee"""
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    if request.method == 'POST':
        employee = get_object_or_404(User, id=user_id, role='user')
        employee_name = f"{employee.first_name} {employee.last_name}"
        employee.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Employee {employee_name} deleted successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def employee_search(request):
    """Search employees with filters"""
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    query = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    
    employees = User.objects.filter(role='user')
    
    # Apply search filter
    if query:
        employees = employees.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(designation__icontains=query)
        )
    
    # Apply role filter
    if role_filter:
        employees = employees.filter(role=role_filter)
    
    # Apply status filter
    if status_filter:
        is_active = status_filter == 'active'
        employees = employees.filter(is_active=is_active)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(employees, 10)
    employees_page = paginator.get_page(page)
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        employees_data = []
        for employee in employees_page:
            employees_data.append({
                'id': employee.id,
                'name': f"{employee.first_name} {employee.last_name or ''}",
                'email': employee.email,
                'phone': employee.phone_number or '-',
                'designation': employee.designation or '-',
                'role': employee.role,
                'is_active': employee.is_active,
                'date_joined': employee.date_joined.strftime('%b %d, %Y'),
                'profile_picture': employee.profile_picture.url if employee.profile_picture else None
            })
        
        return JsonResponse({
            'success': True,
            'employees': employees_data,
            'total_pages': paginator.num_pages,
            'current_page': employees_page.number,
            'total_count': paginator.count
        })
    
    return render(request, 'admin/employee_management.html', {
        'employees': employees_page,
        'query': query,
        'role_filter': role_filter,
        'status_filter': status_filter
    })

@login_required
def project_management(request):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    projects = Project.objects.all().order_by('-created_at')
    paginator = Paginator(projects, 10)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    form = ProjectForm()
    
    return render(request, 'admin/project_management.html', {'projects': projects, 'form':form})

@login_required
def add_project(request):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('project_management')
    else:
        form = ProjectForm()
    
    return render(request, 'admin/add_project.html', {'form': form})

@login_required
def edit_project(request, project_id):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_management')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'admin/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, project_id):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    project = get_object_or_404(Project, id=project_id)
    project_name = project.name
    project.delete()
    messages.success(request, f'Project "{project_name}" deleted successfully!')
    return redirect('project_management')

@login_required
def project_details(request, project_id):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)
    work_entries = WorkEntry.objects.filter(project=project)
    return render(request, 'admin/project_details.html', {
        'project': project,
        'tasks': tasks,
        'work_entries': work_entries,
    })

@login_required
def close_project(request, project_id):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    project = get_object_or_404(Project, id=project_id)
    if project.status == "active":
        project.status = 'closed'

        messages.success(request, f'Project "{project.name}" has been closed.')

    else:
        project.status = "active"
        messages.success(request, f'Project "{project.name}" has been Re Opened.')

    project.save()
    return redirect('project_management')

@login_required
def work_entry_management(request):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    work_entries = WorkEntry.objects.select_related('employee', 'project').order_by('-work_date')
    
    # Filters
    employee_filter = request.GET.get('employee')
    project_filter = request.GET.get('project')
    date_filter = request.GET.get('date')
    
    if employee_filter:
        work_entries = work_entries.filter(employee_id=employee_filter)
    if project_filter:
        work_entries = work_entries.filter(project_id=project_filter)
    if date_filter:
        work_entries = work_entries.filter(work_date=date_filter)
    
    paginator = Paginator(work_entries, 20)
    page = request.GET.get('page')
    work_entries = paginator.get_page(page)
    
    employees = User.objects.filter(role='employee', is_active=True)
    projects = Project.objects.all()
    
    context = {
        'work_entries': work_entries,
        'employees': employees,
        'projects': projects,
    }
    return render(request, 'admin/work_entry_management.html', context)

@login_required
def edit_work_entry(request, entry_id):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    work_entry = get_object_or_404(WorkEntry, id=entry_id)
    
    if request.method == 'POST':
        form = WorkEntryForm(request.POST, instance=work_entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.updated_by = request.user
            entry.save()
            messages.success(request, 'Work entry updated successfully!')
            return redirect('work_entry_management')
    else:
        form = WorkEntryForm(instance=work_entry)
    
    return render(request, 'admin/edit_work_entry.html', {'form': form, 'work_entry': work_entry})

# Employee Views
@login_required
def add_work_entry(request):
    projects = Project.objects.filter(status = "active")
    if request.user.role != 'user':
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = WorkEntryForm(request.POST)
        if form.is_valid():
            work_entry = form.save(commit=False)
            work_entry.employee = request.user
            
            # Check if work date is within allowed range
            today = date.today()
            if (today - work_entry.work_date).days > 2:
                messages.error(request, 'You can only add work entries for today or yesterday.')
                return redirect('add_work_entry')
            
            work_entry.save()
            messages.success(request, 'Work entry added successfully!')
            return redirect('add_work_entry')
        else:
            errors = []
            for field, error_list in form.errors.items():
                for error in error_list:
                    errors.append(f" {error}")



            messages.info(request, " | ".join(errors))
            return redirect('add_work_entry')

    else:
        form = WorkEntryForm()
    
    return render(request, 'employee/add_work_entry.html', {'form': form, "projects":projects})

@login_required
def my_work_entries(request):
    if request.user.role != 'user':
        return redirect('admin_dashboard')
    
    # Base queryset
    work_entries = WorkEntry.objects.filter(employee=request.user).select_related('project').order_by('-work_date', '-created_at')
    
    # Filters
    project_filter = request.GET.get('project')
    date_filter = request.GET.get('date')
    
    if project_filter:
        work_entries = work_entries.filter(project_id=project_filter)
        
    if date_filter:
        work_entries = work_entries.filter(work_date=date_filter)
    
    # Pagination
    paginator = Paginator(work_entries, 20)
    page = request.GET.get('page')
    work_entries = paginator.get_page(page)
    
    # Get active projects for filter dropdown
    projects = Project.objects.filter(status='active').order_by('name')
    
    # Calculate summary stats for the current filter
    total_entries = work_entries.paginator.count if work_entries else 0
    total_hours = WorkEntry.objects.filter(employee=request.user).aggregate(
        total=Sum('working_hours')
    )['total'] or 0
    
    # Get recent activity summary
    today = date.today()
    recent_entries = WorkEntry.objects.filter(
        employee=request.user,
        work_date__gte=today - timedelta(days=7)
    ).count()
    
    context = {
        'work_entries': work_entries,
        'projects': projects,
        'total_entries': total_entries,
        'total_hours': total_hours,
        'recent_entries': recent_entries,
        'current_filters': {
            'project': project_filter,
            'date': date_filter,
        },
        'today': today,
    }
    
    return render(request, 'employee/my_work_entries.html', context)

@login_required
def view_work_entry(request, entry_id):
    """View for viewing work entry details"""
    if request.user.role != 'user':
        return redirect('admin_dashboard')
    
    try:
        entry = WorkEntry.objects.get(id=entry_id, employee=request.user)
    except WorkEntry.DoesNotExist:
        messages.error(request, 'Work entry not found.')
        return redirect('my_work_entries')
    
    return render(request, 'employee/view_work_entry.html', {'entry': entry})

@login_required
def view_work_entry_admin(request, entry_id):
    """View for viewing work entry details"""
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    try:
        entry = WorkEntry.objects.get(id=entry_id)
    except WorkEntry.DoesNotExist:
        messages.info(request, 'Work entry not found.')
        return redirect('work_entry_management')
    
    return render(request, 'admin/view_work_entry.html', {'entry': entry})


@login_required
def reports(request):
    if request.user.role != 'admin':
        return redirect('employee_dashboard')
    
    # Default date range - current month
    today = date.today()
    start_date = today.replace(day=1)
    end_date = today
    
    # Get parameters
    report_type = request.GET.get('type', 'employee')
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')
    employee_id = request.GET.get('employee')
    project_id = request.GET.get('project')
    
    if start_date_param:
        start_date = date.fromisoformat(start_date_param)
    if end_date_param:
        end_date = date.fromisoformat(end_date_param)
    
    # Base query
    work_entries = WorkEntry.objects.filter(
        work_date__range=[start_date, end_date]
    ).select_related('employee', 'project')
    
    if employee_id:
        work_entries = work_entries.filter(employee_id=employee_id)
    if project_id:
        work_entries = work_entries.filter(project_id=project_id)
    
    # Generate report data
    if report_type == 'employee':
        report_data = work_entries.values('employee__email', 'employee__first_name', 'employee__last_name').annotate(
            total_hours=Sum('working_hours')
        ).order_by('employee__id')
    else:  # project
        report_data = work_entries.values('project__name').annotate(
            total_hours=Sum('working_hours')
        ).order_by('project__name')
    
    employees = User.objects.filter(role='employee', is_active=True)
    projects = Project.objects.all()
    
    context = {
        'report_data': report_data,
        'work_entries': work_entries,
        'employees': employees,
        'projects': projects,
        'report_type': report_type,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'admin/reports.html', context)

# API Views
@login_required
def get_available_dates(request):
    """Return available dates for work entry (today and yesterday)"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    dates = [
        {'value': today.isoformat(), 'label': f'Today ({today.strftime("%B %d, %Y")})'},
        {'value': yesterday.isoformat(), 'label': f'Yesterday ({yesterday.strftime("%B %d, %Y")})'},
    ]
    
    return JsonResponse({'dates': dates})

@login_required
def get_active_projects(request):
    """Return active projects for dropdown"""
    projects = Project.objects.filter(status='active').values('id', 'name')
    return JsonResponse({'projects': list(projects)})