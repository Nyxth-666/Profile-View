from datetime import date
from django.db import models


class Student(models.Model):
    SEX_CHOICES = [("M", "Male"), ("F", "Female")]
    STATUS_CHOICES = [
        ("enrolled", "Enrolled"),
        ("pending", "Pending"),
        ("dropped", "Dropped"),
    ]
    YEAR_CHOICES = [(1, "1st Year"), (2, "2nd Year"), (3, "3rd Year"), (4, "4th Year")]

    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to="students/", blank=True)  # needs Pillow

    course = models.CharField(max_length=100)
    year_level = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        had_birthday = (today.month, today.day) >= (self.birth_date.month, self.birth_date.day)
        return today.year - self.birth_date.year - (0 if had_birthday else 1)


class Guardian(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="guardian")
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.relationship})"


class EducationalBackground(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="background")
    last_school = models.CharField(max_length=150)
    school_address = models.CharField(max_length=255, blank=True)
    year_graduated = models.PositiveSmallIntegerField()
    honors = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.last_school