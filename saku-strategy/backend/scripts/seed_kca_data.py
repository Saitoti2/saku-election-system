#!/usr/bin/env python3
"""
Script to seed KCA University academic structure data
Based on the official SAKU 2025/2026 election document
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from elections.models import Faculty, Department, Course


def create_faculties():
    """Create all 4 faculties"""
    faculties_data = [
        {'code': 'business', 'name': 'School of Business'},
        {'code': 'technology', 'name': 'School of Technology'},
        {'code': 'education', 'name': 'School of Education, Arts & Social Sciences'},
        {'code': 'journalism', 'name': 'School of Journalism and Digital Media'},
    ]
    
    faculties = {}
    for data in faculties_data:
        faculty, created = Faculty.objects.get_or_create(
            code=data['code'],
            defaults={'name': data['name']}
        )
        faculties[data['code']] = faculty
        print(f"{'Created' if created else 'Found'} faculty: {faculty.name}")
    
    return faculties


def create_departments(faculties):
    """Create all departments under their respective faculties"""
    departments_data = [
        # School of Business
        {'faculty': 'business', 'code': 'business_admin', 'name': 'Department of Business Administration and Management'},
        {'faculty': 'business', 'code': 'finance_accounting', 'name': 'Department of Finance & Accounting'},
        {'faculty': 'business', 'code': 'economics_stats', 'name': 'Department of Economics & Statistics'},
        
        # School of Technology
        {'faculty': 'technology', 'code': 'software_dev', 'name': 'Department of Software Development & Information Systems'},
        {'faculty': 'technology', 'code': 'networking', 'name': 'Department of Networking and Applied Computing'},
        {'faculty': 'technology', 'code': 'data_science', 'name': 'Department of Data Science & Artificial Intelligence'},
        
        # School of Education, Arts & Social Sciences
        {'faculty': 'education', 'code': 'education', 'name': 'Department of Education'},
        {'faculty': 'education', 'code': 'social_sciences', 'name': 'Department of Social Sciences'},
        {'faculty': 'education', 'code': 'film_performing', 'name': 'Department of Film Technology and Performing Arts'},
        
        # School of Journalism and Digital Media
        {'faculty': 'journalism', 'code': 'journalism', 'name': 'Department of Journalism and Digital Media'},
        {'faculty': 'journalism', 'code': 'digital_media', 'name': 'Department of Digital Media'},
        {'faculty': 'journalism', 'code': 'communication', 'name': 'Department of Communication'},
    ]
    
    departments = {}
    for data in departments_data:
        department, created = Department.objects.get_or_create(
            code=data['code'],
            defaults={
                'faculty': faculties[data['faculty']],
                'name': data['name']
            }
        )
        departments[data['code']] = department
        print(f"{'Created' if created else 'Found'} department: {department.name}")
    
    return departments


def create_courses(departments):
    """Create all courses under their respective departments"""
    
    # School of Business - Department of Business Administration and Management
    business_admin_courses = [
        'Certificate in Business Management',
        'Certificate in Procurement and Logistics',
        'Diploma in Business Management',
        'Diploma in Procurement and Logistics',
        'Diploma in Public Management',
        'Bachelor in International Business Management',
        'Bachelor in Procurement and Logistics',
        'Bachelor in Public Management',
        'Master of Business Administration (With Specialization)',
        'Master of Business Administration Corporate Management',
        'Master of Science in Knowledge Management and Innovation',
        'Master of Science in Supply Chain Management',
        'PhD in Business Management',
    ]
    
    # School of Business - Department of Finance & Accounting
    finance_accounting_courses = [
        'Bachelor of Commerce',
        'Bachelor of Science in Forensic Accounting',
        'Master of Science in Commerce (Specialization)',
        'Master of Science in Development Finance',
        'PhD in Finance',
    ]
    
    # School of Business - Department of Economics & Statistics
    economics_stats_courses = [
        'Bachelor of Science in Economics and Statistics',
        'Bachelor of Arts in Business Studies',
    ]
    
    # School of Technology - Department of Software Development & Information Systems
    software_dev_courses = [
        'Certificate in Information Technology',
        'Diploma in Information Technology',
        'Bachelor of Science in Software Development',
        'Bachelor of Science in Information Technology',
        'Master of Science Information Systems Management',
        'PhD. Information Systems',
    ]
    
    # School of Technology - Department of Networking and Applied Computing
    networking_courses = [
        'Certificate in Business Information Technology',
        'Diploma in Business Information Technology',
        'Bachelor of Science in Information Security and Forensics',
    ]
    
    # School of Technology - Department of Data Science & Artificial Intelligence
    data_science_courses = [
        'Certificate in Data Science',
        'Diploma in Data Science',
        'Bachelor of Science in Data Science',
        'Bachelor of Science in Artificial Intelligence',
        'Master of Science in Data Science',
        'Master of Science in Artificial Intelligence',
        'PhD in Data Science',
    ]
    
    # School of Education, Arts & Social Sciences - Department of Education
    education_courses = [
        'Certificate in Education',
        'Diploma in Education',
        'Bachelor of Education',
        'Bachelor of Arts in Education',
        'Master of Education',
        'Master of Arts in Education',
        'PhD in Education',
        'Post Graduate Diploma in Education',
    ]
    
    # School of Education, Arts & Social Sciences - Department of Social Sciences
    social_sciences_courses = [
        'Certificate in Social Work',
        'Diploma in Social Work',
        'Bachelor of Arts in Social Work',
        'Bachelor of Arts in Psychology',
        'Master of Arts in Social Work',
        'Master of Arts in Psychology',
    ]
    
    # School of Education, Arts & Social Sciences - Department of Film Technology and Performing Arts
    film_performing_courses = [
        'Certificate in Film Technology',
        'Diploma in Film Technology',
        'Bachelor of Arts in Film Technology',
        'Bachelor of Arts in Performing Arts',
        'Master of Arts in Film Technology',
        'Master of Arts in Performing Arts',
    ]
    
    # School of Journalism and Digital Media - Department of Journalism and Digital Media
    journalism_courses = [
        'Certificate in Journalism',
        'Diploma in Journalism',
        'Bachelor of Arts in Journalism',
        'Bachelor of Arts in Digital Media',
        'Master of Arts in Journalism',
        'Master of Arts in Digital Media',
    ]
    
    # School of Journalism and Digital Media - Department of Digital Media
    digital_media_courses = [
        'Certificate in Digital Marketing',
        'Diploma in Digital Marketing',
        'Bachelor of Science in Digital Marketing',
        'Bachelor of Science in Web Design',
        'Master of Science in Digital Marketing',
    ]
    
    # School of Journalism and Digital Media - Department of Communication
    communication_courses = [
        'Certificate in Communication',
        'Diploma in Communication',
        'Bachelor of Arts in Communication',
        'Bachelor of Arts in Public Relations',
        'Master of Arts in Communication',
        'Master of Arts in Public Relations',
    ]
    
    # Map courses to departments
    courses_mapping = {
        'business_admin': business_admin_courses,
        'finance_accounting': finance_accounting_courses,
        'economics_stats': economics_stats_courses,
        'software_dev': software_dev_courses,
        'networking': networking_courses,
        'data_science': data_science_courses,
        'education': education_courses,
        'social_sciences': social_sciences_courses,
        'film_performing': film_performing_courses,
        'journalism': journalism_courses,
        'digital_media': digital_media_courses,
        'communication': communication_courses,
    }
    
    total_courses = 0
    for dept_code, courses in courses_mapping.items():
        if dept_code in departments:
            department = departments[dept_code]
            for course_name in courses:
                course, created = Course.objects.get_or_create(
                    name=course_name,
                    defaults={'department': department}
                )
                if created:
                    total_courses += 1
                    print(f"Created course: {course_name}")
    
    print(f"\nTotal courses created: {total_courses}")


def main():
    """Main function to seed all data"""
    print("🌱 Seeding KCA University academic structure...")
    print("=" * 50)
    
    # Create faculties
    print("\n📚 Creating Faculties...")
    faculties = create_faculties()
    
    # Create departments
    print("\n🏢 Creating Departments...")
    departments = create_departments(faculties)
    
    # Create courses
    print("\n📖 Creating Courses...")
    create_courses(departments)
    
    print("\n✅ Data seeding completed successfully!")
    print("=" * 50)
    
    # Print summary
    print(f"📊 Summary:")
    print(f"   - Faculties: {Faculty.objects.count()}")
    print(f"   - Departments: {Department.objects.count()}")
    print(f"   - Courses: {Course.objects.count()}")


if __name__ == '__main__':
    main()
