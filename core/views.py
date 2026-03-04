import csv
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from .models import Teacher, ExaminationCenter, Assignment
from .forms import TeacherForm, ExaminationCenterForm, GenerateAssignmentForm

# Dashboard
def dashboard(request):
    assignments = Assignment.objects.all().select_related('teacher', 'center')
    return render(request, 'core/dashboard.html', {'assignments': assignments})

# Teacher CRUD
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'core/teacher_list.html', {'teachers': teachers})

def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Add Teacher'})

def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'core/form.html', {'form': form, 'title': 'Edit Teacher'})

def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully.')
        return redirect('teacher_list')
    return render(request, 'core/confirm_delete.html', {'object': teacher, 'title': 'Delete Teacher'})

# Center CRUD
def center_list(request):
    centers = ExaminationCenter.objects.all()
    return render(request, 'core/center_list.html', {'centers': centers})

def center_create(request):
    if request.method == 'POST':
        form = ExaminationCenterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Center added successfully.')
            return redirect('center_list')
    else:
        form = ExaminationCenterForm()
    return render(request, 'core/form.html', {'form': form, 'title': 'Add Center'})

def center_update(request, pk):
    center = get_object_or_404(ExaminationCenter, pk=pk)
    if request.method == 'POST':
        form = ExaminationCenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            messages.success(request, 'Center updated successfully.')
            return redirect('center_list')
    else:
        form = ExaminationCenterForm(instance=center)
    return render(request, 'core/form.html', {'form': form, 'title': 'Edit Center'})

def center_delete(request, pk):
    center = get_object_or_404(ExaminationCenter, pk=pk)
    if request.method == 'POST':
        center.delete()
        messages.success(request, 'Center deleted successfully.')
        return redirect('center_list')
    return render(request, 'core/confirm_delete.html', {'object': center, 'title': 'Delete Center'})

# Assignment Logic
def generate_assignments(request):
    if request.method == 'POST':
        form = GenerateAssignmentForm(request.POST)
        if form.is_valid():
            # Clear existing assignments? Or keep history?
            # For this simple app, let's clear current assignments to avoid duplicates for the same session.
            # In a real app, we might have 'sessions' or 'exams'.
            Assignment.objects.all().delete()
            
            teachers = list(Teacher.objects.all())
            centers = list(ExaminationCenter.objects.all())
            
            if not teachers or not centers:
                messages.error(request, 'Need teachers and centers to generate assignments.')
                return redirect('dashboard')

            random.shuffle(teachers)
            
            assignments_created = 0
            # Simple logic: Assign teachers to centers until we run out of teachers or capacity
            # This is a basic round-robin or fill-up strategy.
            # Let's try to distribute evenly or just fill up?
            # Requirement: "Random assignment ... without order bias"
            
            # Helper to get a random center that has capacity
            # But wait, centers have 'capacity'. We should respect it.
            
            # Let's create a list of available slots
            slots = []
            for center in centers:
                for _ in range(center.capacity):
                    slots.append(center)
            
            random.shuffle(slots)
            
            with transaction.atomic():
                for teacher in teachers:
                    if not slots:
                        messages.warning(request, 'Not enough capacity in centers for all teachers.')
                        break
                    
                    center = slots.pop()
                    Assignment.objects.create(teacher=teacher, center=center)
                    assignments_created += 1
            
            messages.success(request, f'Successfully assigned {assignments_created} teachers.')
            return redirect('dashboard')
    else:
        form = GenerateAssignmentForm()
    
    return render(request, 'core/generate_assignments.html', {'form': form})

def export_assignments(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assignments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Teacher Name', 'Teacher Email', 'Examination Center', 'Location', 'Date Assigned'])
    
    assignments = Assignment.objects.all().select_related('teacher', 'center')
    for assignment in assignments:
        writer.writerow([
            assignment.teacher.name,
            assignment.teacher.email,
            assignment.center.name,
            assignment.center.location,
            assignment.date_assigned
        ])
    
    return response
