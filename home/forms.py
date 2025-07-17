from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
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
            'email', 'first_name', 'last_name','employee_id', 'designation', 'profile_picture',
            'man_hour_of_employee', 'phone_number', 'date_of_birth',
            'pin_code', 'age', 'district', 'state', 'address', 'role'
        ]  # Removed password1 and password2 from here
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
        fields = ('name','project_id', 'description', 'start_date', 'end_date')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', "placeholder":"Project Title"}),
            'project_id': forms.TextInput(attrs={'class': 'form-control', "placeholder":"Project Id"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,"placeholder":"Enter Project Description"}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
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

class WorkEntryForm(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = ('project', 'work_date', 'start_time', 'end_time', 'working_hours', 'description')
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'work_date': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'working_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.1', 'max': '24'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter projects to show only active ones
        self.fields['project'].queryset = Project.objects.filter(status='active')
        
        # Set work_date choices to today and previous 2 days (3 days total)
        today = date.today()
        day_1 = today - timedelta(days=1)
        day_2 = today - timedelta(days=2)
        
        date_choices = [
            (today.isoformat(), f'Today ({today.strftime("%B %d, %Y")})'),
            (day_1.isoformat(), f'Yesterday ({day_1.strftime("%B %d, %Y")})'),
            (day_2.isoformat(), f'{day_2.strftime("%A, %B %d, %Y")}'),
        ]
        
        self.fields['work_date'] = forms.ChoiceField(
            choices=date_choices,
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    def clean_work_date(self):
        work_date = self.cleaned_data.get('work_date')
        if isinstance(work_date, str):
            work_date = date.fromisoformat(work_date)
        
        # Check if date is within allowed range (today or previous 2 days)
        today = date.today()
        if (today - work_date).days > 2:
            raise ValidationError("You can only add work entries for today or the previous 2 days.")
        
        return work_date

    def clean_working_hours(self):
        working_hours = self.cleaned_data.get('working_hours')
        if working_hours is not None:
            if working_hours < 0.1:
                raise ValidationError("Working hours must be at least 0.1 hours.")
            if working_hours > 24:
                raise ValidationError("Working hours cannot exceed 24 hours.")
        return working_hours

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be after start time.")

        return cleaned_data
class WorkEntryFormAdmin(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = ('project','employee', 'work_date', 'start_time', 'end_time', 'working_hours', 'description')
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'employee':forms.Select(attrs={'class': 'form-control'}),
            'work_date': forms.DateInput(attrs={'class': 'form-control', "type":"date"}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'working_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.1', 'max': '24'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }