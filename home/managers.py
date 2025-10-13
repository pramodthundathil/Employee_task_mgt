# managers.py
from django.db import models
from django.db.models import Q

def get_current_user():
    """Import from middleware"""
    from .middleware import get_current_user as _get_user
    return _get_user()


class AutoFilterQuerySet(models.QuerySet):
    """Custom QuerySet that applies automatic filtering"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._auto_filter_disabled = False
    
    def _clone(self):
        """Ensure cloned querysets maintain the filter state"""
        clone = super()._clone()
        clone._auto_filter_disabled = self._auto_filter_disabled
        return clone
    
    def disable_auto_filter(self):
        """Disable automatic filtering for this queryset"""
        clone = self._clone()
        clone._auto_filter_disabled = True
        return clone
    
    def _filter_by_user(self, user):
        """Override this in model-specific managers"""
        return self


class ProjectQuerySet(AutoFilterQuerySet):
    def _filter_by_user(self, user):
        if not user or not user.is_authenticated:
            return self.none()
        
        if user.role == 'admin':
            return self
        elif user.role == 'semi-admin':
            return self.filter(work_location=user.work_location)
        else:  # regular user
            # Users see projects they're involved in
            return self.filter(
                Q(tasks__assigned_to=user) | 
                Q(work_entries__employee=user) |
                Q(created_by=user)
            ).distinct()


class TaskQuerySet(AutoFilterQuerySet):
    def _filter_by_user(self, user):
        if not user or not user.is_authenticated:
            return self.none()
        
        if user.role == 'admin':
            return self
        elif user.role == 'semi-admin':
            return self.filter(project__work_location=user.work_location)
        else:  # regular user
            return self.filter(assigned_to=user)


class WorkEntryQuerySet(AutoFilterQuerySet):
    def _filter_by_user(self, user):
        if not user or not user.is_authenticated:
            return self.none()
        
        if user.role == 'admin':
            return self
        elif user.role == 'semi-admin':
            return self.filter(project__work_location=user.work_location)
        else:  # regular user
            return self.filter(employee=user)


class CustomUserQuerySet(AutoFilterQuerySet):
    def _filter_by_user(self, user):
        if not user or not user.is_authenticated:
            return self.none()
        
        if user.role == 'admin':
            return self
        elif user.role == 'semi-admin':
            return self.filter(work_location=user.work_location)
        else:  # regular user
            return self.filter(id=user.id)


class AutoFilterManager(models.Manager):
    """
    Manager that automatically applies role-based filtering.
    NO CODE CHANGES NEEDED - filtering happens automatically!
    """
    
    def get_queryset(self):
        """Override to apply automatic filtering"""
        qs = super().get_queryset()
        
        # Get queryset class (e.g., ProjectQuerySet)
        if hasattr(self, '_queryset_class'):
            qs = self._queryset_class(self.model, using=self._db)
        
        # Check if auto-filter is disabled
        if getattr(qs, '_auto_filter_disabled', False):
            return qs
        
        # Get current user from thread local
        user = get_current_user()
        
        # Apply filtering based on user
        if user and user.is_authenticated:
            return qs._filter_by_user(user)
        
        return qs
    
    def all_unfiltered(self):
        """Get all records without filtering (for admin purposes)"""
        return self.get_queryset().disable_auto_filter()
    
    def for_user(self, user):
        """Manually specify a user (useful for background tasks)"""
        return self.get_queryset()._filter_by_user(user)


class ProjectManager(AutoFilterManager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)
    
    _queryset_class = ProjectQuerySet


class TaskManager(AutoFilterManager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)
    
    _queryset_class = TaskQuerySet


class WorkEntryManager(AutoFilterManager):
    def get_queryset(self):
        return WorkEntryQuerySet(self.model, using=self._db)
    
    _queryset_class = WorkEntryQuerySet


class FilteredCustomUserManager(AutoFilterManager):
    """Separate manager for filtering users"""
    def get_queryset(self):
        return CustomUserQuerySet(self.model, using=self._db)
    
    _queryset_class = CustomUserQuerySet