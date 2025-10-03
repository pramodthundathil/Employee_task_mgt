from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, WorkLocation
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter New Password',
                'id': 'password1'
            }
        ),
        required=False,
        label="Password"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password',
                'id': 'password2'
            }
        ),
        required=False,
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'employee_id', 'designation', 
            'work_location', 'profile_picture', 'man_hour_of_employee', 
            'phone_number', 'date_of_birth', 'pin_code', 'age', 'district', 
            'state', 'address', 'role'
        ]
        labels = {
            'man_hour_of_employee': 'Man Hour Rate (USD)',
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email',
                'id': 'email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter First Name',
                'id': 'first_name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Last Name',
                'id': 'last_name'
            }),
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Employee Id',
                'id': 'employee_id'
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Designation',
                'id': 'designation'
            }),
            'work_location': forms.Select(attrs={
                'class': 'form-control',
                'id': 'work_location'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'profile_picture'
            }),
            'man_hour_of_employee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Man Hour',
                'id': 'man_hour_of_employee'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
                'id': 'phone_number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
                'id': 'date_of_birth',
                'type': 'date'
            }),
            'pin_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PIN Code',
                'id': 'pin_code'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Age',
                'id': 'age'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter District',
                'id': 'district'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter State',
                'id': 'state'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
                'id': 'address',
                'rows': 3
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
                'id': 'role'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make work_location required in the form
        self.fields['work_location'].required = True
        self.fields['work_location'].queryset = WorkLocation.objects.all()
        self.fields['work_location'].empty_label = "Select Work Location"

    def clean_password2(self):
        """Validate that the two password entries match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        
        return password2

    def clean_password1(self):
        """Validate password strength."""
        password1 = self.cleaned_data.get("password1")
        
        if password1:
            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long")
        
        return password1

    def save(self, commit=True):
        """Save the user with properly hashed password."""
        user = super().save(commit=False)
        
        # Handle password if provided
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        
        return user
# from django import forms
# from django.core.exceptions import ValidationError
# from .models import CustomUser, WorkLocation

# class CustomUserForm(forms.ModelForm):
#     password1 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter New Password',
#                 'id': 'password1'
#             }
#         ),
#         required=True,  # Make password required for new users
#         label="Password"
#     )

#     password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Confirm Password',
#                 'id': 'password2'
#             }
#         ),
#         required=True,  # Make password required for new users
#         label="Confirm Password"
#     )

#     class Meta:
#         model = CustomUser
#         fields = [
#             'email', 'first_name', 'last_name','employee_id', 'designation', 'profile_picture',
#             'man_hour_of_employee', 'phone_number', 'date_of_birth',
#             'pin_code', 'age', 'district', 'state', 'address', 'role'
#         ]
#         labels = {
#             'man_hour_of_employee': 'Man Hour Rate (USD)',
#             'work_location': 'Work Location',
#         }
#         widgets = {
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Email',
#                 'id': 'email',
#                 'required': 'required'
#             }),
#             'first_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter First Name',
#                 'id': 'first_name',
#                 'required': 'required'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Last Name',
#                 'id': 'last_name'
#             }),
#             'employee_id': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Employee Id',
#                 'id': 'employee_id'
#             }),
#             'designation': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Designation',
#                 'id': 'designation'
#             }),
#             'profile_picture': forms.FileInput(attrs={
#                 'class': 'form-control',
#                 'id': 'profile_picture'
#             }),
#             'man_hour_of_employee': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Man Hour',
#                 'id': 'man_hour_of_employee'
#             }),
#             'phone_number': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Phone Number',
#                 'id': 'phone_number',
#                 'required': 'required'
#             }),
#             'date_of_birth': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'YYYY-MM-DD',
#                 'id': 'date_of_birth',
#                 'type': 'date',
#                 'required': 'required'
#             }),
#             'pin_code': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter PIN Code',
#                 'id': 'pin_code'
#             }),
#             'age': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Age',
#                 'id': 'age'
#             }),
#             'district': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter District',
#                 'id': 'district'
#             }),
#             'state': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter State',
#                 'id': 'state'
#             }),
#             'address': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Address',
#                 'id': 'address',
#                 'rows': 3
#             }),
#             'role': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'role'
#             }),
#             # 'work_location': forms.Select(attrs={
#             #     'class': 'form-control',
#             #     'id': 'work_location',
#             #     'required': 'required'
#             # }),
#         }

#     def __init__(self, *args, **kwargs):
#         self.request_user = kwargs.pop('user', None)
#         self.is_edit = kwargs.pop('is_edit', False)
#         super().__init__(*args, **kwargs)
        
#         # Make passwords optional for editing existing users
#         if self.is_edit:
#             self.fields['password1'].required = False
#             self.fields['password2'].required = False
        
#         # Populate work_location choices
#         self.fields['work_location'].queryset = WorkLocation.objects.all()
#         self.fields['work_location'].empty_label = "Select Work Location"
        
#         # Restrict role choices if user is not admin
#         if self.request_user and self.request_user.role != 'admin':
#             self.fields['role'].choices = [('user', 'user')]
#             self.fields['role'].widget.attrs['readonly'] = True

#     def clean_email(self):
#         """Validate email is unique"""
#         email = self.cleaned_data.get('email')
#         if email:
#             # Check if email exists for other users (exclude current user if editing)
#             qs = CustomUser.objects.filter(email=email)
#             if self.instance.pk:
#                 qs = qs.exclude(pk=self.instance.pk)
#             if qs.exists():
#                 raise ValidationError("This email is already registered")
#         return email

#     def clean_work_location(self):
#         """Ensure work_location is provided"""
#         work_location = self.cleaned_data.get('work_location')
#         if not work_location:
#             raise ValidationError("Work location is required")
#         return work_location

#     def clean_role(self):
#         """Restrict role assignment based on user permissions"""
#         role = self.cleaned_data.get('role')
        
#         # Only admins can assign admin or semi-admin roles
#         if role in ['admin', 'semi-admin']:
#             if not self.request_user or self.request_user.role != 'admin':
#                 raise ValidationError("Only administrators can assign admin or semi-admin roles")
        
#         return role

#     def clean_password2(self):
#         """Validate that the two password entries match."""
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
        
#         # If editing and no password provided, skip validation
#         if self.is_edit and not password1 and not password2:
#             return password2
        
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords don't match")
        
#         return password2

#     def clean_password1(self):
#         """Validate password strength."""
#         password1 = self.cleaned_data.get("password1")
        
#         # If editing and no password provided, skip validation
#         if self.is_edit and not password1:
#             return password1
        
#         if password1:
#             if len(password1) < 8:
#                 raise ValidationError("Password must be at least 8 characters long")
        
#         return password1

#     def clean(self):
#         """Additional form-level validation"""
#         cleaned_data = super().clean()
        
#         # Ensure password is provided for new users
#         if not self.is_edit:
#             password1 = cleaned_data.get("password1")
#             if not password1:
#                 raise ValidationError("Password is required for new users")
        
#         return cleaned_data

#     def save(self, commit=True):
#         """Save the user with properly hashed password."""
#         user = super().save(commit=False)
        
#         # Handle password if provided
#         password = self.cleaned_data.get("password1")
#         if password:
#             user.set_password(password)
        
#         # Set default role if not provided
#         if not user.role:
#             user.role = 'user'
        
#         if commit:
#             user.save()
        
#         return user

class CustomUserFormEdit(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name','employee_id', 'designation', 'profile_picture',
            'man_hour_of_employee', 'is_verified', 'phone_number', 'date_of_birth',
            'pin_code', 'age', 'district', 'state', 'address', 'is_active',
            'is_staff', 'role', 'password'
        ]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name','employee_id', 'designation', 'profile_picture',
            'man_hour_of_employee', 'is_verified', 'phone_number', 'date_of_birth',
            'pin_code', 'age', 'district', 'state', 'address', 'is_active',
            'is_staff', 'role'
        ]

class ProfileUpdateForm(forms.Form):
    profile_picture = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text="Upload a new profile picture (optional)"
    )
    
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Check file size (limit to 5MB)
            if picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            
            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = os.path.splitext(picture.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Invalid file type. Please upload a valid image file.")
        
        return picture

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Current Password'
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        })
    )


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import User, Project, Task, WorkEntry

# class UserForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)
#     email = forms.EmailField(required=True)
#     employee_id = forms.CharField(max_length=20, required=True)
#     phone = forms.CharField(max_length=15, required=False)

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'employee_id', 'phone', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add Bootstrap classes
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             if field_name == 'password1':
#                 field.help_text = None
#             elif field_name == 'password2':
#                 field.help_text = None

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name','project_id', 'description','work_location', 'start_date', 'end_date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', "placeholder":"Project Title"}),
            'project_id': forms.TextInput(attrs={'class': 'form-control', "placeholder":"Project Id"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,"placeholder":"Enter Project Description"}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
             'work_location': forms.Select(attrs={
                'class' :'form-control',
                'id': 'work_location'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date must be after start date.")

        return cleaned_data

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('project', 'assigned_to', 'title', 'description', 'priority', 'due_date')
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter projects to show only active ones
        self.fields['project'].queryset = Project.objects.filter(status='active')
        # Filter assigned_to to show only employees
        self.fields['assigned_to'].queryset = User.objects.filter(role='employee', is_active=True)

# class WorkEntryForm(forms.ModelForm):
#     class Meta:
#         model = WorkEntry
#         fields = ('project', 'work_date', 'start_time', 'end_time', 'working_hours', 'description')
#         widgets = {
#             'project': forms.Select(attrs={'class': 'form-control'}),
#             'work_date': forms.Select(attrs={'class': 'form-control'}),
#             'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
#             'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
#             'working_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.1', 'max': '24'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Filter projects to show only active ones
#         self.fields['project'].queryset = Project.objects.filter(status='active')
        
#         # Set work_date choices to today and previous 2 days (3 days total)
#         today = date.today()
#         day_1 = today - timedelta(days=1)
        
        
#         date_choices = [
#             (today.isoformat(), f'Today ({today.strftime("%B %d, %Y")})'),
#             (day_1.isoformat(), f'Yesterday ({day_1.strftime("%B %d, %Y")})'),
            
#         ]
        
#         self.fields['work_date'] = forms.ChoiceField(
#             choices=date_choices,
#             widget=forms.Select(attrs={'class': 'form-control'})
#         )

#     def clean_work_date(self):
#         work_date = self.cleaned_data.get('work_date')
#         if isinstance(work_date, str):
#             work_date = date.fromisoformat(work_date)
        
#         # Check if date is within allowed range (today or previous 2 days)
#         today = date.today()
#         if (today - work_date).days > 2:
#             raise ValidationError("You can only add work entries for today or the previous 2 days.")
        
#         return work_date

#     def clean_working_hours(self):
#         working_hours = self.cleaned_data.get('working_hours')
#         if working_hours is not None:
#             if working_hours < 0.1:
#                 raise ValidationError("Working hours must be at least 0.1 hours.")
#             if working_hours > 24:
#                 raise ValidationError("Working hours cannot exceed 24 hours.")
#         return working_hours

#     def clean(self):
#         cleaned_data = super().clean()
#         start_time = cleaned_data.get('start_time')
#         end_time = cleaned_data.get('end_time')

#         if start_time and end_time and start_time >= end_time:
#             raise ValidationError("End time must be after start time.")

#         return cleaned_data


from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta, datetime, time as dt_time
from decimal import Decimal


class WorkEntryForm(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = ('project', 'work_date', 'start_time', 'end_time', 'working_hours', 'description')
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'work_date': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'working_hours': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.1', 
                'min': '0.1', 
                'max': '24',
                'placeholder': 'Enter hours (e.g., 5.5)'
            }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # Extract user from kwargs
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter projects based on user's location and active status
        if self.user and hasattr(self.user, 'work_location'):
            self.fields['project'].queryset = Project.objects.filter(
                status='active',
                work_location=self.user.work_location
            )
        else:
            self.fields['project'].queryset = Project.objects.filter(status='active')
        
        # Set work_date choices to today and yesterday
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        date_choices = [
            (today.isoformat(), f'Today ({today.strftime("%B %d, %Y")})'),
            (yesterday.isoformat(), f'Yesterday ({yesterday.strftime("%B %d, %Y")})'),
        ]
        
        self.fields['work_date'] = forms.ChoiceField(
            choices=date_choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Work Date'
        )

    def clean_work_date(self):
        """Validate and convert work_date"""
        work_date = self.cleaned_data.get('work_date')
        
        # Convert string to date object
        if isinstance(work_date, str):
            work_date = date.fromisoformat(work_date)
        
        # Check if date is within allowed range
        today = date.today()
        days_diff = (today - work_date).days
        
        if days_diff > 1:
            raise ValidationError("You can only add work entries for today or yesterday.")
        
        if days_diff < 0:
            raise ValidationError("You cannot add work entries for future dates.")
        
        return work_date

    def clean_working_hours(self):
        """Validate working hours"""
        working_hours = self.cleaned_data.get('working_hours')
        
        if working_hours is not None:
            if working_hours < 0.1:
                raise ValidationError("Working hours must be at least 0.1 hours (6 minutes).")
            if working_hours > 24:
                raise ValidationError("Working hours cannot exceed 24 hours in a day.")
        
        return working_hours

    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        working_hours = cleaned_data.get('working_hours')
        work_date = cleaned_data.get('work_date')
        project = cleaned_data.get('project')

        # Convert work_date string to date object if needed
        if isinstance(work_date, str):
            work_date = date.fromisoformat(work_date)
            cleaned_data['work_date'] = work_date

        # Validate start and end time relationship
        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError({
                    'end_time': "End time must be after start time."
                })
            
            # Calculate actual time difference in hours
            start_datetime = datetime.combine(date.today(), start_time)
            end_datetime = datetime.combine(date.today(), end_time)
            time_diff = end_datetime - start_datetime
            actual_hours = Decimal(str(time_diff.total_seconds() / 3600))
            
            # Round to 2 decimal places for comparison
            actual_hours = actual_hours.quantize(Decimal('0.01'))
            
            # Validate that working_hours doesn't exceed actual time difference
            if working_hours:
                if working_hours > actual_hours:
                    raise ValidationError({
                        'working_hours': f"Working hours ({working_hours}) cannot exceed the actual "
                                       f"time period ({actual_hours} hours) between "
                                       f"{start_time.strftime('%I:%M %p')} and {end_time.strftime('%I:%M %p')}."
                    })

        # Check for time overlap with existing entries
        if self.user and work_date and start_time and end_time:
            # Query existing work entries for this user on this date
            existing_entries = WorkEntry.objects.filter(
                employee=self.user,
                work_date=work_date
            )
            
            # Exclude current entry if we're editing
            if self.instance and self.instance.pk:
                existing_entries = existing_entries.exclude(pk=self.instance.pk)
            
            # Check each existing entry for time overlap
            for entry in existing_entries:
                if self._times_overlap(start_time, end_time, entry.start_time, entry.end_time):
                    raise ValidationError({
                        'start_time': f"Time conflict! You already have a work entry for "
                                    f"'{entry.project.name}' from "
                                    f"{entry.start_time.strftime('%I:%M %p')} to "
                                    f"{entry.end_time.strftime('%I:%M %p')} on this date.",
                        'end_time': "Please choose a different time period."
                    })

        return cleaned_data

    @staticmethod
    def _times_overlap(start1, end1, start2, end2):
        """
        Check if two time ranges overlap.
        Returns True if there is any overlap between the two time periods.
        
        Example:
        - (9:00, 12:00) overlaps with (11:00, 14:00) -> True
        - (9:00, 12:00) does not overlap with (12:00, 14:00) -> False (touching endpoints don't count)
        """
        # Convert times to minutes since midnight for easier comparison
        def time_to_minutes(t):
            return t.hour * 60 + t.minute
        
        s1 = time_to_minutes(start1)
        e1 = time_to_minutes(end1)
        s2 = time_to_minutes(start2)
        e2 = time_to_minutes(end2)
        
        # Two ranges overlap if one starts before the other ends
        # AND the other starts before the first ends
        return s1 < e2 and s2 < e1
    

class WorkEntryFormAdmin(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = ['employee', 'project', 'work_date', 'start_time', 'end_time', 'working_hours', 'description']
        widgets = {
            'employee': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'project': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'work_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': 'required'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': 'required'
            }),
            'working_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.1',
                'max': '24',
                'required': 'required'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'required': 'required'
            }),
        }
        labels = {
            'work_date': 'Work Date',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'working_hours': 'Working Hours',
            'description': 'Work Description',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.location = kwargs.pop('location', None)
        super().__init__(*args, **kwargs)
        
        # Filter employees based on user role and location
        if self.user:
            if self.user.role == 'semi-admin' and self.location:
                # Semi-admin sees only employees from their location
                self.fields['employee'].queryset = User.objects.filter(
                    role='user',
                    is_active=True,
                    work_location=self.location
                ).order_by('first_name', 'last_name')
                
                # Semi-admin sees only projects from their location
                self.fields['project'].queryset = Project.objects.filter(
                    status='active',
                    work_location=self.location
                ).order_by('name')
            else:
                # Admin sees all active employees and projects
                self.fields['employee'].queryset = User.objects.filter(
                    role='user',
                    is_active=True
                ).order_by('first_name', 'last_name')
                
                self.fields['project'].queryset = Project.objects.filter(
                    status='active'
                ).order_by('name')
        
        # Set empty labels
        self.fields['employee'].empty_label = "Select Employee"
        self.fields['project'].empty_label = "Select Project"
    
    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        project = cleaned_data.get('project')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        # Validate start and end time
        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError("End time must be after start time")
        
        # Validate location matching for semi-admin
        if self.user and self.user.role == 'semi-admin' and self.location:
            if employee and employee.work_location != self.location:
                raise ValidationError(
                    f"Employee must be from {self.location.get_location_display()} location"
                )
            
            if project and project.work_location != self.location:
                raise ValidationError(
                    f"Project must be from {self.location.get_location_display()} location"
                )
        
        return cleaned_data
    
    def save(self, commit=True):
        """Save the work entry"""
        instance = super().save(commit=False)
        
        # Set updated_by if user is available
        if self.user:
            instance.updated_by = self.user
        
        if commit:
            instance.save()
        
        return instance