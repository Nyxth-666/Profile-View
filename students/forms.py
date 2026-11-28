from django import forms
from .models import Student, Guardian, EducationalBackground
from io import BytesIO
from PIL import Image, ImageOps

MAX_PHOTO_SIZE = 2 * 1024 * 1024

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
    photo = forms.ImageField(required=False)

    class Meta:
        model = Student
        fields = [
            "student_id", "first_name", "middle_name", "last_name",
            "birth_date", "sex", "email", "phone", "address",
            "course", "year_level", "status",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if photo and photo.size > MAX_PHOTO_SIZE:
            raise forms.ValidationError("Photo must be 2 MB or smaller.")
        return photo

    def save(self, commit=True):
        student = super().save(commit=False)
        photo = self.cleaned_data.get("photo")
        if photo:
            student.photo_data = process_photo(photo)
            student.photo_type = "image/jpeg"
        if commit:
            student.save()
        return student


class GuardianForm(StyledForm):
    class Meta:
        model = Guardian
        fields = ["name", "relationship", "contact_number", "occupation"]


class BackgroundForm(StyledForm):
    class Meta:
        model = EducationalBackground
        fields = ["last_school", "school_address", "year_graduated", "honors"]


class PhotoForm(forms.Form):
    photo = forms.ImageField()

    def clean_photo(self):
        photo = self.cleaned_data["photo"]
        if photo.size > MAX_PHOTO_SIZE:
            raise forms.ValidationError("Photo must be 2 MB or smaller.")
        return photo


def process_photo(upload):
    """Fix rotation, shrink to 500x500 max, return JPEG bytes."""
    image = ImageOps.exif_transpose(Image.open(upload)).convert("RGB")
    image.thumbnail((500, 500))
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()