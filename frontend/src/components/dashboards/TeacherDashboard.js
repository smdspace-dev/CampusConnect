import React from 'react';
import { Routes, Route } from 'react-router-dom';
import DashboardLayout from '../shared/DashboardLayout';
import TeacherCourses from '../teacher/TeacherCourses';
import TeacherAssignments from '../teacher/TeacherAssignments';
import TeacherAttendance from '../teacher/TeacherAttendance';
import TeacherGrading from '../teacher/TeacherGrading';

const TeacherDashboard = () => {
  const menuItems = [
    {
      label: 'Dashboard',
      path: '/teacher/dashboard',
      icon: 'fas fa-tachometer-alt'
    },
    {
      label: 'My Classes',
      icon: 'fas fa-chalkboard',
      submenu: [
        { label: 'Current Classes', path: '/teacher/classes', icon: 'fas fa-chalkboard-teacher' },
        { label: 'Class Schedule', path: '/teacher/schedule', icon: 'fas fa-calendar' },
        { label: 'Attendance', path: '/teacher/attendance', icon: 'fas fa-check-circle' }
      ]
    },
    {
      label: 'Academics',
      icon: 'fas fa-book',
      submenu: [
        { label: 'Assignments', path: '/teacher/assignments', icon: 'fas fa-tasks' },
        { label: 'Grades', path: '/teacher/grades', icon: 'fas fa-medal' },
        { label: 'Course Materials', path: '/teacher/materials', icon: 'fas fa-folder-open' }
      ]
    },
    {
      label: 'Students',
      icon: 'fas fa-user-graduate',
      submenu: [
        { label: 'Student List', path: '/teacher/students', icon: 'fas fa-list' },
        { label: 'Performance', path: '/teacher/performance', icon: 'fas fa-chart-line' },
        { label: 'Reports', path: '/teacher/reports', icon: 'fas fa-file-alt' }
      ]
    },
    {
      label: 'Communication',
      icon: 'fas fa-comments',
      submenu: [
        { label: 'Messages', path: '/teacher/messages', icon: 'fas fa-envelope' },
        { label: 'Announcements', path: '/teacher/announcements', icon: 'fas fa-bullhorn' }
      ]
    },
    {
      label: 'Profile',
      path: '/teacher/profile',
      icon: 'fas fa-user'
    }
  ];

  const TeacherDashboardHome = () => (
    <div className="teacher-dashboard">
      {/* Welcome Section */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card border-0 shadow-sm bg-gradient-success text-white">
            <div className="card-body p-4">
              <div className="row align-items-center">
                <div className="col-md-8">
                  <h2 className="h3 mb-2">Good morning, Professor!</h2>
                  <p className="mb-3">Ready to inspire minds and shape the future today?</p>
                  <div className="d-flex gap-4">
                    <div className="stat-item">
                      <strong>5</strong>
                      <small className="d-block">Active Classes</small>
                    </div>
                    <div className="stat-item">
                      <strong>127</strong>
                      <small className="d-block">Total Students</small>
                    </div>
                    <div className="stat-item">
                      <strong>8</strong>
                      <small className="d-block">Pending Grades</small>
                    </div>
                  </div>
                </div>
                <div className="col-md-4 text-center">
                  <i className="fas fa-chalkboard-teacher fa-5x opacity-50"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="row g-4 mb-4">
        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-success bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-chalkboard fa-2x text-success"></i>
              </div>
              <h4 className="h5 mb-2">Today's Classes</h4>
              <h3 className="text-success mb-0">4</h3>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-primary bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-user-graduate fa-2x text-primary"></i>
              </div>
              <h4 className="h5 mb-2">Total Students</h4>
              <h3 className="text-primary mb-0">127</h3>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-warning bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-tasks fa-2x text-warning"></i>
              </div>
              <h4 className="h5 mb-2">Assignments</h4>
              <h3 className="text-warning mb-0">12</h3>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-info bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-medal fa-2x text-info"></i>
              </div>
              <h4 className="h5 mb-2">Pending Grades</h4>
              <h3 className="text-info mb-0">8</h3>
            </div>
          </div>
        </div>
      </div>

      {/* Today's Schedule & Quick Actions */}
      <div className="row g-4 mb-4">
        <div className="col-lg-8">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Today's Teaching Schedule</h5>
            </div>
            <div className="card-body">
              <div className="schedule-list">
                <div className="schedule-item d-flex align-items-center mb-3 p-3 bg-light rounded">
                  <div className="time-badge bg-success text-white px-3 py-2 rounded me-3">
                    <strong>09:00</strong>
                  </div>
                  <div className="schedule-content flex-grow-1">
                    <h6 className="mb-1">Web Development - CSE 301</h6>
                    <p className="text-muted mb-0">Room 101, 35 students • React.js Components</p>
                  </div>
                  <div className="schedule-status">
                    <span className="badge bg-success">In Progress</span>
                  </div>
                </div>

                <div className="schedule-item d-flex align-items-center mb-3 p-3 bg-light rounded">
                  <div className="time-badge bg-warning text-white px-3 py-2 rounded me-3">
                    <strong>11:00</strong>
                  </div>
                  <div className="schedule-content flex-grow-1">
                    <h6 className="mb-1">Database Systems - CSE 401</h6>
                    <p className="text-muted mb-0">Room 205, 42 students • SQL Optimization</p>
                  </div>
                  <div className="schedule-status">
                    <span className="badge bg-warning">Next</span>
                  </div>
                </div>

                <div className="schedule-item d-flex align-items-center mb-3 p-3 bg-light rounded">
                  <div className="time-badge bg-secondary text-white px-3 py-2 rounded me-3">
                    <strong>14:00</strong>
                  </div>
                  <div className="schedule-content flex-grow-1">
                    <h6 className="mb-1">Software Engineering Lab</h6>
                    <p className="text-muted mb-0">Lab 2, 25 students • Project Review</p>
                  </div>
                  <div className="schedule-status">
                    <span className="badge bg-secondary">Later</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Quick Actions</h5>
            </div>
            <div className="card-body">
              <div className="d-grid gap-3">
                <button className="btn btn-success">
                  <i className="fas fa-check-circle me-2"></i>
                  Take Attendance
                </button>
                <button className="btn btn-primary">
                  <i className="fas fa-plus me-2"></i>
                  Create Assignment
                </button>
                <button className="btn btn-warning">
                  <i className="fas fa-medal me-2"></i>
                  Grade Submissions
                </button>
                <button className="btn btn-info">
                  <i className="fas fa-bullhorn me-2"></i>
                  Post Announcement
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity & Student Performance */}
      <div className="row g-4">
        <div className="col-lg-6">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Recent Submissions</h5>
            </div>
            <div className="card-body">
              <div className="submission-list">
                <div className="submission-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded">
                  <div>
                    <h6 className="mb-1">React Portfolio Project</h6>
                    <small className="text-muted">John Doe - CSE 301</small>
                  </div>
                  <div>
                    <span className="badge bg-success me-2">New</span>
                    <button className="btn btn-sm btn-outline-primary">Grade</button>
                  </div>
                </div>

                <div className="submission-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded">
                  <div>
                    <h6 className="mb-1">Database Design Assignment</h6>
                    <small className="text-muted">Jane Smith - CSE 401</small>
                  </div>
                  <div>
                    <span className="badge bg-success me-2">New</span>
                    <button className="btn btn-sm btn-outline-primary">Grade</button>
                  </div>
                </div>

                <div className="submission-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded">
                  <div>
                    <h6 className="mb-1">Software Testing Report</h6>
                    <small className="text-muted">Mike Johnson - CSE 301</small>
                  </div>
                  <div>
                    <span className="badge bg-warning me-2">Late</span>
                    <button className="btn btn-sm btn-outline-primary">Grade</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-6">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Class Performance Overview</h5>
            </div>
            <div className="card-body">
              <div className="performance-list">
                <div className="performance-item mb-4">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="fw-medium">CSE 301 - Web Development</span>
                    <span className="text-success">85% Avg</span>
                  </div>
                  <div className="progress mb-2">
                    <div className="progress-bar bg-success" style={{width: '85%'}}></div>
                  </div>
                  <small className="text-muted">35 students • Last assignment avg: 85%</small>
                </div>

                <div className="performance-item mb-4">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="fw-medium">CSE 401 - Database Systems</span>
                    <span className="text-warning">78% Avg</span>
                  </div>
                  <div className="progress mb-2">
                    <div className="progress-bar bg-warning" style={{width: '78%'}}></div>
                  </div>
                  <small className="text-muted">42 students • Last exam avg: 78%</small>
                </div>

                <div className="performance-item mb-4">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="fw-medium">CSE 501 - Software Engineering</span>
                    <span className="text-success">92% Avg</span>
                  </div>
                  <div className="progress mb-2">
                    <div className="progress-bar bg-success" style={{width: '92%'}}></div>
                  </div>
                  <small className="text-muted">25 students • Project submission avg: 92%</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <DashboardLayout role="teacher" menuItems={menuItems}>
      <Routes>
        <Route path="/dashboard" element={<TeacherDashboardHome />} />
        <Route path="/" element={<TeacherDashboardHome />} />
        <Route path="/classes" element={<TeacherCourses />} />
        <Route path="/assignments" element={<TeacherAssignments />} />
        <Route path="/attendance" element={<TeacherAttendance />} />
        <Route path="/grades" element={<TeacherGrading />} />
      </Routes>
    </DashboardLayout>
  );
};

export default TeacherDashboard;
