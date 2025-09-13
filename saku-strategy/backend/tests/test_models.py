from django.test import TestCase
from django.core.exceptions import ValidationError
from elections.models import Department, Course, Delegate, VettingStatus, Gender


class DepartmentModelTest(TestCase):
    def test_department_creation(self):
        dept = Department.objects.create(
            code='ict',
            name='Information Technology'
        )
        self.assertEqual(str(dept), 'Information Technology')
        self.assertEqual(dept.code, 'ict')


class CourseModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(
            code='ict',
            name='Information Technology'
        )

    def test_course_creation(self):
        course = Course.objects.create(
            department=self.dept,
            name='Computer Science'
        )
        self.assertEqual(str(course), 'Computer Science')
        self.assertEqual(course.department, self.dept)


class DelegateModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(
            code='ict',
            name='Information Technology'
        )
        self.course = Course.objects.create(
            department=self.dept,
            name='Computer Science'
        )

    def test_delegate_creation(self):
        delegate = Delegate.objects.create(
            full_name='John Doe',
            gender=Gender.MALE,
            department=self.dept,
            course=self.course,
            year_of_study=2,
            student_id='CS001',
            contacts={'phone': '1234567890', 'email': 'john@example.com'}
        )
        self.assertEqual(str(delegate), 'John Doe (CS001)')
        self.assertEqual(delegate.gender, Gender.MALE)
        self.assertEqual(delegate.vetting_status, VettingStatus.NOT_STARTED)
        self.assertFalse(delegate.is_qualified)

    def test_delegate_unique_student_id(self):
        Delegate.objects.create(
            full_name='John Doe',
            gender=Gender.MALE,
            department=self.dept,
            course=self.course,
            year_of_study=2,
            student_id='CS001'
        )
        
        with self.assertRaises(Exception):  # IntegrityError
            Delegate.objects.create(
                full_name='Jane Doe',
                gender=Gender.FEMALE,
                department=self.dept,
                course=self.course,
                year_of_study=2,
                student_id='CS001'  # Duplicate student_id
            )

