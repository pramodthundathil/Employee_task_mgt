from django.urls import path 
from .import views 

urlpatterns = [
     # Authentication
    path("",views.login_view,name="login_view"),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.profile_update, name='profile_update'),

    # Dashboards
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # # Employee Management (Admin)
    # path('employees/', views.employee_management, name='employee_management'),
    # path('employees/add/', views.add_employee, name='add_employee'),
    # path('employees/<int:user_id>/edit/', views.edit_employee, name='edit_employee'),

     # Employee Management URLs
    path('employees/', views.employee_management, name='employee_management'),
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/<int:user_id>/', views.view_employee, name='view_employee'),
    path('employee/<int:user_id>/edit/', views.edit_employee, name='edit_employee'),
    path('employee/<int:user_id>/toggle-status/', views.toggle_employee_status, name='toggle_employee_status'),
    path('employee/<int:user_id>/delete/', views.delete_employee, name='delete_employee'),
    path('employees/search/', views.employee_search, name='employee_search'),
     path('employee/<int:employee_id>/work-entries/', views.employee_work_entries, name='employee_work_entries'),
    path('employee/<int:employee_id>/work-entries/download/', views.download_employee_work_excel, name='download_employee_work_excel'),
    

    # Project Management (Admin)
    path('projects/', views.project_management, name='project_management'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/close/', views.close_project, name='close_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('projects/<int:project_id>/', views.project_details, name='project_details'),

    # Work Entry Management (Admin)
    path('work-entries/', views.work_entry_management, name='work_entry_management'),
    path('work-entries/<int:entry_id>/edit/', views.edit_work_entry, name='edit_work_entry'),
    path('view/<int:entry_id>/work-entry',views.view_work_entry_admin,name="view_work_entry_admin"),
    path("work-entry-admin/<int:project_id>/add", views.add_work_entry_admin, name='add_work_entry_admin'),
    # Reports (Admin)
    path('reports/', views.reports, name='reports'),

    # Work Entries (Employee)
    path('employee/work-entries/add/', views.add_work_entry, name='add_work_entry'),
    path('employee/work-entries/', views.my_work_entries, name='my_work_entries'),
    path('work-entries/<int:entry_id>/view/', views.view_work_entry, name='view_work_entry'),
    path('work-entries/employee/<int:entry_id>/edit/', views.edit_work_entry_employee, name='edit_work_entry_employee'),


    # APIs
    path('api/available-dates/', views.get_available_dates, name='get_available_dates'),
    path('api/active-projects/', views.get_active_projects, name='get_active_projects'),

    # workhour reports 
    path("work-summery/",views.all_projects_work_summary,name="all_projects_work_summary"),
    path("work-hour/report/<int:project_id>/",views.project_work_hours_report,name="project_work_hours_report"),
    path("work-hour/Excel/report/<int:project_id>/",views.export_project_report_excel,name="export_project_report_excel"),
    path("employee-work/report/<int:employee_id>/",views.employee_work_report,name="employee_work_report"),
    path("work-summery/excel",views.export_all_projects_excel,name="export_all_projects_excel"),

    path("reports/download",views.download_reports,name="download_reports"),
     path('reports/generate/', views.generate_report, name='generate_report'),
    path('reports/summary/', views.get_report_summary, name='get_report_summary'),

]

handler404 = views.custom_page_not_found_view
handler500 = views.custom_server_error_view
handler403 = views.custom_permission_denied_view
handler400 = views.custom_bad_request_view