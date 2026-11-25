from django import forms
from .models import Student, Guardian, EducationalBackground

INPUT = (
    "w-full rounded-lg border border-line bg-white/60 px-4 py-2.5 text-sm "
    "text-ink placeholder:text-muted focus:outline-none focus:ring-2 focus:ring-navy/40"
)


class StyledForm(forms.ModelForm):
    """Adds the Tailwind classes to every input."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs["class"] = "text-sm"
            else:
                field.widget.attrs["class"] = INPUT


class StudentForm(StyledForm):
    class Meta:
        model = Student
        fields = [
            "student_id", "first_name", "middle_name", "last_name",
            "birth_date", "sex", "email", "phone", "address", "photo",
            "course", "year_level", "status",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }


class GuardianForm(StyledForm):
    class Meta:
        model = Guardian
        fields = ["name", "relationship", "contact_number", "occupation"]


class BackgroundForm(StyledForm):
    class Meta:
        model = EducationalBackground
        fields = ["last_school", "school_address", "year_graduated", "honors"]