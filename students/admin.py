from django.contrib import admin
from .models import Student, Guardian, EducationalBackground


class GuardianInline(admin.StackedInline):
    model = Guardian
    extra = 0


class BackgroundInline(admin.StackedInline):
    model = EducationalBackground
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "full_name", "course", "year_level", "status")
    search_fields = ("student_id", "first_name", "last_name")
    inlines = [GuardianInline, BackgroundInline]