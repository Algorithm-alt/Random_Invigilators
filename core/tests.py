from django.test import TestCase
from django.urls import reverse
from .models import Teacher, ExaminationCenter, Assignment

class InvigilationTests(TestCase):
    def setUp(self):
        self.t1 = Teacher.objects.create(name='T1', email='t1@example.com')
        self.t2 = Teacher.objects.create(name='T2', email='t2@example.com')
        self.c1 = ExaminationCenter.objects.create(name='C1', location='L1', capacity=1)
        self.c2 = ExaminationCenter.objects.create(name='C2', location='L2', capacity=1)

    def test_assignment_generation(self):
        # Post to generate assignments
        response = self.client.post(reverse('generate_assignments'), {'confirm': True})
        self.assertEqual(response.status_code, 302) # Redirects to dashboard
        
        # Check assignments count
        self.assertEqual(Assignment.objects.count(), 2)
        
        # Check uniqueness of teachers
        assigned_teachers = Assignment.objects.values_list('teacher', flat=True)
        self.assertEqual(len(assigned_teachers), len(set(assigned_teachers)))
        
    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
