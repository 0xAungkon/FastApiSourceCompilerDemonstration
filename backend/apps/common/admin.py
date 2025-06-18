from django.contrib import admin
from .models import (
    ModelDocument,
    ModelMetaInformation,
    SetupSections,
    SetupLine,
    SetupSalaryPackage,
    SetupHoliday,
    SetupDesignation

)

@admin.register(ModelDocument)
class ModelDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uploaded_by', 'created_at', 'updated_at', 'is_deleted')
    search_fields = ('name', 'uploaded_by__username')
    list_filter = ('is_deleted', 'created_at', 'uploaded_by')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ModelMetaInformation)
class ModelMetaInformationAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'document', 'created_at', 'updated_at', 'is_deleted')
    search_fields = ('key', 'value', 'document__name')
    list_filter = ('is_deleted', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SetupSections)
class SetupSectionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'unit', 'company_name','salary_package', 'created_at', 'updated_at', 'is_deleted')
    search_fields = ('name', 'company_name')
    list_filter = ('is_deleted', 'type', 'unit', 'company_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SetupLine)
class SetupLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at', 'is_deleted')
    search_fields = ('name',)
    list_filter = ('is_deleted',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SetupSalaryPackage)
class SetupSalaryPackageAdmin(admin.ModelAdmin):
    list_display = ('package_id', 'house_rent', 'medical_allowance', 'conveyance', 'food_allowance', 'created_at', 'updated_at', 'is_deleted')
    search_fields = ('package_id',)
    list_filter = ('is_deleted',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SetupHoliday)
class SetupHolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday_name', 'type_of_holiday', 'date_from', 'date_to', 'created_at', 'updated_at', 'is_deleted')
    search_fields = ('holiday_name', 'type_of_holiday')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SetupDesignation)
class SetupDesignationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'designation', 'designation_category', 'worktype', 'grade',
        'attendance_bonus', 'tiffin_bill', 'night_bill', 'night_shift_bill',
        'ifter_bill', 'design_type_in_pd', 'designation_type',
        'ot_general_duty', 'w_off_allowance_hd', 'w_off_allowance_fd',
        'rank', 'tofsil', 'created_at', 'updated_at', 'is_deleted'
    )
    search_fields = ('designation', 'designation_category', 'rank')
    list_filter = ('designation_type', 'worktype', 'is_deleted')
    readonly_fields = ('created_at', 'updated_at')