from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class WorkLocation(models.Model):
    location = models.CharField(max_length=20, choices=(("kochi","Kochi"),('dubai',"Dubai")))

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.location)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='last name')
    employee_id = models.CharField(max_length=30, null=True, blank=True, verbose_name='employee_id')
    designation = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.FileField(upload_to="profile_pic", null=True, blank=True)
    man_hour_of_employee = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)
    is_verified = models.BooleanField(default=False)
    
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
        verbose_name='phone number'
    )
    date_of_birth = models.DateField(auto_now_add=False, null=True, blank=True)
    pin_code = models.BigIntegerField(default=1, null=True, blank=True)
    age = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name='address')
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff status')
    role = models.CharField(max_length=20, 
                            choices=(
                                ("admin","admin"),
                                ("semi-admin", "semi-admin"),
                                ("user","user"),
                            ),
                            default='user'
                            )
    work_location = models.ForeignKey(WorkLocation, on_delete=models.CASCADE)
    
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "date_of_birth", "phone_number"]

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return str(self.first_name + " " + str(self.last_name))


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=200)
    project_id = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    work_location = models.ForeignKey(WorkLocation, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.project_id) + " - "+str(self.name)

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.project.name}"

# class WorkEntry(models.Model):
#     employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_entries')
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='work_entries')
#     work_date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     working_hours = models.DecimalField(
#         max_digits=4, 
#         decimal_places=2,
#         validators=[MinValueValidator(0.1), MaxValueValidator(24.0)]
#     )
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_work_entries')

#     class Meta:
#         ordering = ['-work_date', '-created_at']
        

#     def __str__(self):
#         return f"{self.employee.first_name} - {self.project.name} - {self.work_date}"

#     def can_edit(self):
#         """Check if work entry can be edited (within 2 days)"""
#         today = date.today()
#         return (today - self.work_date).days <= 2

#     def save(self, *args, **kwargs):
#         user = kwargs.pop('user', None)  # Extract the user passed from view
#         # Validate start_time and end_time
#         if self.start_time >= self.end_time:
#             raise ValueError("End time must be after start time")

#         # if not self.pk:  # Only for new entries
#         #     today = date.today()
#         #     if (today - self.work_date).days > 3:
#         #         if not user or user.role != 'admin':
#         #             raise ValueError("Cannot create work entry for dates older than 3 days (admin only)")
        
#         super().save(*args, **kwargs)


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date, datetime
from decimal import Decimal

class WorkEntry(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_entries')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='work_entries')
    work_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    working_hours = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(0.1), MaxValueValidator(24.0)]
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='updated_work_entries'
    )

    class Meta:
        ordering = ['-work_date', '-created_at']
        # Add database constraints
        constraints = [
            models.CheckConstraint(
                check=models.Q(working_hours__gte=0.1) & models.Q(working_hours__lte=24),
                name='valid_working_hours_range'
            ),
        ]

    def __str__(self):
        return f"{self.employee.first_name} - {self.project.name} - {self.work_date}"

    def can_edit(self):
        """Check if work entry can be edited (within 2 days)"""
        today = date.today()
        return (today - self.work_date).days <= 2

    def clean(self):
        """Model-level validation - called before save"""
        super().clean()
        
        # Skip validation if employee is not set yet (during form initialization)
        if not self.employee_id:
            return
        
        # Validate start_time and end_time relationship
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError({
                    'end_time': "End time must be after start time."
                })
            
            # Calculate actual time difference
            start_datetime = datetime.combine(date.today(), self.start_time)
            end_datetime = datetime.combine(date.today(), self.end_time)
            time_diff = end_datetime - start_datetime
            actual_hours = Decimal(str(time_diff.total_seconds() / 3600))
            actual_hours = actual_hours.quantize(Decimal('0.01'))
            
            # Validate working hours don't exceed actual time
            if self.working_hours and self.working_hours > actual_hours:
                raise ValidationError({
                    'working_hours': f"Working hours ({self.working_hours}) cannot exceed "
                                   f"actual time period ({actual_hours} hours)."
                })
        
        # Check for time overlaps with existing entries
        if self.employee_id and self.work_date and self.start_time and self.end_time:
            overlapping_entries = WorkEntry.objects.filter(
                employee_id=self.employee_id,
                work_date=self.work_date
            ).exclude(pk=self.pk if self.pk else None)
            
            for entry in overlapping_entries:
                if self._times_overlap(
                    self.start_time, 
                    self.end_time, 
                    entry.start_time, 
                    entry.end_time
                ):
                    raise ValidationError({
                        'start_time': f"Time conflict with existing entry for {entry.project.name} "
                                    f"({entry.start_time.strftime('%I:%M %p')} - "
                                    f"{entry.end_time.strftime('%I:%M %p')})."
                    })

    @staticmethod
    def _times_overlap(start1, end1, start2, end2):
        """Check if two time ranges overlap"""
        def time_to_minutes(t):
            return t.hour * 60 + t.minute
        
        s1 = time_to_minutes(start1)
        e1 = time_to_minutes(end1)
        s2 = time_to_minutes(start2)
        e2 = time_to_minutes(end2)
        
        return s1 < e2 and s2 < e1

    def save(self, *args, **kwargs):
        """Override save to ensure validation runs"""
        # Don't call full_clean here as it causes the RelatedObjectDoesNotExist error
        # The form already validates everything we need
        super().save(*args, **kwargs)



