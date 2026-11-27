from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Student
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from .forms import StudentForm, GuardianForm, BackgroundForm, PhotoForm


def student_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(student_id__icontains=query)
        )
    return render(
        request, "students/student_list.html", {"students": students, "query": query}
    )


def student_detail(request, pk):
    student = get_object_or_404(
        Student.objects.select_related("guardian", "background"), pk=pk
    )
    return render(request, "students/student_detail.html", {"student": student})


def student_save(request, pk=None):
    """Handles both Add (no pk) and Edit (with pk)."""
    student = get_object_or_404(Student, pk=pk) if pk else None
    guardian = getattr(student, "guardian", None)
    background = getattr(student, "background", None)

    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    guardian_form = GuardianForm(request.POST or None, instance=guardian, prefix="g")
    background_form = BackgroundForm(
        request.POST or None, instance=background, prefix="b"
    )

    if request.method == "POST":
        valid = [form.is_valid(), guardian_form.is_valid(), background_form.is_valid()]
        if all(valid):
            with transaction.atomic():
                saved = form.save()

                guardian_obj = guardian_form.save(commit=False)
                guardian_obj.student = saved
                guardian_obj.save()

                background_obj = background_form.save(commit=False)
                background_obj.student = saved
                background_obj.save()

            messages.success(request, f"{saved.full_name} was saved.")
            return redirect("students:detail", pk=saved.pk)

    return render(
        request,
        "students/student_form.html",
        {
            "student": student,
            "form": form,
            "guardian_form": guardian_form,
            "background_form": background_form,
        },
    )


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        name = student.full_name
        student.delete()
        messages.success(request, f"{name} was deleted.")
        return redirect("students:list")
    return render(request, "students/student_confirm_delete.html", {"student": student})


def student_photo(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        if "remove" in request.POST:
            student.photo.delete(save=True)
            messages.success(request, "Photo removed.")
        else:
            form = PhotoForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, "Photo updated.")
            else:
                messages.error(request, form.errors["photo"][0])

    return redirect("students:detail", pk=pk)
