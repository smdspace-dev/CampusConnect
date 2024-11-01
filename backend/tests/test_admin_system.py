from django.test import TestCase
from django.contrib.auth.models import User
from admin_system.models import Department, Staff, Cluster, Club, Student

class AdminModelsTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name='Computer Science', code='CS')
        self.user = User.objects.create_user(username='adminuser', password='pass1234', email='admin@example.com')
        self.staff = Staff.objects.create(user=self.user, role='super_admin', department=self.dept)
        self.cluster = Cluster.objects.create(name='Cluster A', mentor=self.staff, department=self.dept)
        self.student_user = User.objects.create_user(username='student1', password='pass1234', email='student@example.com')
        self.student = Student.objects.create(
            user=self.student_user, 
            cluster=self.cluster, 
            department=self.dept,
            roll_number='CS2023001'
        )
        self.club = Club.objects.create(name='Robotics Club', coordinator=self.staff)

    def test_department_active(self):
        self.assertTrue(self.dept.is_active)
        self.dept.is_active = False
        self.dept.save()
        self.assertFalse(Department.objects.get(pk=self.dept.pk).is_active)

    def test_staff_toggle(self):
        before = self.staff.toggle_access
        self.staff.toggle()
        self.assertNotEqual(before, self.staff.toggle_access)

    def test_cluster_str(self):
        self.assertIn('Cluster', str(self.cluster))

    def test_club_membership(self):
        self.club.members.add(self.student)
        self.assertIn(self.student, self.club.members.all())
