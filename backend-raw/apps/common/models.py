# Description: This module contains database models for the application.
import os
import uuid
from django.db import models
from django.utils.deconstruct import deconstructible
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Define a base model class that includes common fields for all models
class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        abstract = True

class BlankModel(models.Model):
    """
    A blank model that can be used as a placeholder or for testing purposes.
    """
    pass
class ModelDocument(BaseModel):
    """
    Model to represent a document with a file field.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents_uploaded'
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"


class ModelMetaInformation(BaseModel):
    """
    Model to store metadata information for documents.
    """
    document = models.ForeignKey(ModelDocument, on_delete=models.CASCADE, related_name='metadata', null=True, blank=True)
    key = models.CharField(max_length=255, help_text="Metadata key, e.g., 'author', 'description'", unique=True, db_index=True, verbose_name="Metadata Key")
    value = models.TextField()
    def __str__(self):
        return f"{self.key}: {self.value}"
    class Meta:
        verbose_name = "Meta Information"
        verbose_name_plural = "Meta Information"



class SetupLine(BaseModel):
    id = models.CharField(max_length=255, unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Setup Line"
        verbose_name_plural = "Setup Lines"

class SetupSalaryPackage(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    package_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
    house_rent = models.DecimalField(max_digits=12, decimal_places=2)
    medical_allowance = models.DecimalField(max_digits=12, decimal_places=2)
    conveyance = models.DecimalField(max_digits=12, decimal_places=2)
    food_allowance = models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self):
        return self.package_id
    class Meta:
        verbose_name = "Salary Package"
        verbose_name_plural = "Salary Packages"
    
class SetupHoliday(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    holiday_name = models.CharField(max_length=255)
    type_of_holiday = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.holiday_name} ({self.holiday_date})"
    
    class Meta:
        verbose_name = "Holiday"
        verbose_name_plural = "Holidays"


class SetupDesignation(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    designation_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
    designation = models.CharField(max_length=255, unique=True, null=False, blank=False)
    designation_category = models.CharField(max_length=255)
    worktype = models.CharField(max_length=255)
    grade = models.IntegerField()
    minimum_gross = models.CharField(max_length=255)
    attendance_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    tiffin_bill = models.DecimalField(max_digits=10, decimal_places=2)
    night_bill = models.DecimalField(max_digits=10, decimal_places=2)
    night_shift_bill = models.DecimalField(max_digits=10, decimal_places=2)
    ifter_bill = models.DecimalField(max_digits=10, decimal_places=2)
    design_type_in_pd = models.CharField(max_length=255)
    designation_type = models.CharField(max_length=255)
    ot_general_duty = models.CharField(max_length=255)
    w_off_allowance_hd = models.CharField(max_length=255)
    w_off_allowance_fd = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    tofsil = models.CharField(max_length=255)

    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = "Designation"
        verbose_name_plural = "Designations"


class SetupSections(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salary_package = models.ForeignKey(
        SetupSalaryPackage,
        on_delete=models.CASCADE,
        related_name='sections',
        null=True,
        blank=True,
        default=None
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Setup Section"
        verbose_name_plural = "Setup Sections"
