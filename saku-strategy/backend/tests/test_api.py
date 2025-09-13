from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from elections.models import Department, Course, Delegate, Gender


class DepartmentAPITest(APITestCase):
    def setUp(self):
        self.dept = Department.objects.create(
            code='ict',
            name='Information Technology'
        )

    def test_list_departments(self):
        url = reverse('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Information Technology')

    def test_create_department(self):
        url = reverse('department-list')
        data = {
            'code': 'business',
            'name': 'Business Administration'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 2)


class DelegateAPITest(APITestCase):
    def setUp(self):
        self.dept = Department.objects.create(
            code='ict',
            name='Information Technology'
        )
        self.course = Course.objects.create(
            department=self.dept,
            name='Computer Science'
        )

    def test_create_delegate(self):
        url = reverse('delegate-list')
        data = {
            'full_name': 'John Doe',
            'gender': 'Male',
            'department_id': self.dept.id,
            'course_id': self.course.id,
            'year_of_study': 2,
            'student_id': 'CS001',
            'contacts': {'phone': '1234567890'}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Delegate.objects.count(), 1)
        
        delegate = Delegate.objects.first()
        self.assertEqual(delegate.full_name, 'John Doe')
        self.assertTrue(delegate.is_qualified)  # Should be auto-qualified

    def test_metrics_endpoint(self):
        # Create a qualified delegate
        Delegate.objects.create(
            full_name='John Doe',
            gender=Gender.MALE,
            department=self.dept,
            course=self.course,
            year_of_study=2,
            student_id='CS001',
            is_qualified=True
        )
        
        url = reverse('delegate-metrics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('departments', response.data)
        self.assertIn('score', response.data)
        self.assertEqual(len(response.data['departments']), 1)
        
        dept_data = response.data['departments'][0]
        self.assertEqual(dept_data['qualified'], 1)
        self.assertEqual(dept_data['total_candidates'], 1)

    def test_risks_endpoint(self):
        # Create an unqualified delegate (below minimum)
        Delegate.objects.create(
            full_name='John Doe',
            gender=Gender.MALE,
            department=self.dept,
            course=self.course,
            year_of_study=2,
            student_id='CS001',
            is_qualified=False
        )
        
        url = reverse('delegate-risks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('risks', response.data)
        self.assertEqual(len(response.data['risks']), 1)
        
        risk = response.data['risks'][0]
        self.assertEqual(risk['code'], 'ict')
        self.assertIn('under_minimum', [r['type'] for r in risk['risks']])

    def test_simulate_endpoint(self):
        url = reverse('delegate-simulate')
        data = {
            'actions': [
                {
                    'department': 'ict',
                    'add_candidates': 2,
                    'gender': 'Female'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('before', response.data)
        self.assertIn('after', response.data)
        self.assertIn('delta', response.data)
        self.assertIn('features', response.data)
