import React from 'react';
import { Routes, Route } from 'react-router-dom';
import DashboardLayout from '../shared/DashboardLayout';

// Import existing student components
import Dashboard from '../student/Dashboard';
import ClubBrowser from '../student/ClubBrowser';

const StudentDashboard = () => {
  const menuItems = [
    {
      label: 'Dashboard',
      path: '/student/dashboard',
      icon: 'fas fa-tachometer-alt'
    },
    {
      label: 'Academics',
      icon: 'fas fa-book',
      submenu: [
        { label: 'My Courses', path: '/student/courses', icon: 'fas fa-book-open' },
        { label: 'Assignments', path: '/student/assignments', icon: 'fas fa-tasks' },
        { label: 'Grades', path: '/student/grades', icon: 'fas fa-medal' },
        { label: 'Schedule', path: '/student/schedule', icon: 'fas fa-calendar' }
      ]
    },
    {
      label: 'Activities',
      icon: 'fas fa-users',
      submenu: [
        { label: 'Clubs', path: '/student/clubs', icon: 'fas fa-users-cog' },
        { label: 'Events', path: '/student/events', icon: 'fas fa-calendar-alt' },
        { label: 'Attendance', path: '/student/attendance', icon: 'fas fa-check-circle' }
      ]
    },
    {
      label: 'Resources',
      icon: 'fas fa-folder',
      submenu: [
        { label: 'Library', path: '/student/library', icon: 'fas fa-book-reader' },
        { label: 'Downloads', path: '/student/downloads', icon: 'fas fa-download' },
        { label: 'Links', path: '/student/links', icon: 'fas fa-external-link-alt' }
      ]
    },
    {
      label: 'Profile',
      path: '/student/profile',
      icon: 'fas fa-user'
    }
  ];

  const StudentDashboardHome = () => (
    <div className="student-dashboard">
      {/* Welcome Section */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card border-0 shadow-sm bg-gradient-primary text-white">
            <div className="card-body p-4">
              <div className="row align-items-center">
                <div className="col-md-8">
                  <h2 className="h3 mb-2">Welcome back, Student!</h2>
                  <p className="mb-3">Here's what's happening with your academic journey today.</p>
                  <div className="d-flex gap-3">
                    <div className="stat-item">
                      <strong>4.2</strong>
                      <small className="d-block">GPA</small>
                    </div>
                    <div className="stat-item">
                      <strong>85%</strong>
                      <small className="d-block">Attendance</small>
                    </div>
                    <div className="stat-item">
                      <strong>3</strong>
                      <small className="d-block">Active Courses</small>
                    </div>
                  </div>
                </div>
                <div className="col-md-4 text-center">
                  <i className="fas fa-user-graduate fa-5x opacity-50"></i>
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
              <div className="bg-primary bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-book-open fa-2x text-primary"></i>
              </div>
              <h4 className="h5 mb-2">Current Courses</h4>
              <h3 className="text-primary mb-0">6</h3>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-success bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-tasks fa-2x text-success"></i>
              </div>
              <h4 className="h5 mb-2">Pending Tasks</h4>
              <h3 className="text-success mb-0">3</h3>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-warning bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-users-cog fa-2x text-warning"></i>
              </div>
              <h4 className="h5 mb-2">Joined Clubs</h4>
              <h3 className="text-warning mb-0">2</h3>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-info bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-calendar-alt fa-2x text-info"></i>
              </div>
              <h4 className="h5 mb-2">Upcoming Events</h4>
              <h3 className="text-info mb-0">5</h3>
            </div>
          </div>
        </div>
      </div>

      {/* Today's Schedule & Recent Activity */}
      <div className="row g-4 mb-4">
        <div className="col-lg-8">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Today's Schedule</h5>
            </div>
            <div className="card-body">
              <div className="schedule-list">
                <div className="schedule-item d-flex align-items-center mb-3 p-3 bg-light rounded">
                  <div className="time-badge bg-primary text-white px-3 py-2 rounded me-3">
                    <strong>09:00</strong>
                  </div>
                  <div className="schedule-content flex-grow-1">
                    <h6 className="mb-1">Data Structures & Algorithms</h6>
                    <p className="text-muted mb-0">Room 301, Computer Science Block</p>
                  </div>
                  <div className="schedule-status">
                    <span className="badge bg-success">In Progress</span>
                  </div>
                </div>

                <div className="schedule-item d-flex align-items-center mb-3 p-3 bg-light rounded">
                  <div className="time-badge bg-secondary text-white px-3 py-2 rounded me-3">
                    <strong>11:00</strong>
                  </div>
                  <div className="schedule-content flex-grow-1">
                    <h6 className="mb-1">Database Management Systems</h6>
                    <p className="text-muted mb-0">Room 205, IT Block</p>
                  </div>
                  <div className="schedule-status">
                    <span className="badge bg-warning">Upcoming</span>
                  </div>
                </div>

                <div className="schedule-item d-flex align-items-center mb-3 p-3 bg-light rounded">
                  <div className="time-badge bg-secondary text-white px-3 py-2 rounded me-3">
                    <strong>14:00</strong>
                  </div>
                  <div className="schedule-content flex-grow-1">
                    <h6 className="mb-1">Web Development Lab</h6>
                    <p className="text-muted mb-0">Lab 1, Computer Science Block</p>
                  </div>
                  <div className="schedule-status">
                    <span className="badge bg-secondary">Scheduled</span>
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
                <button className="btn btn-primary">
                  <i className="fas fa-book-open me-2"></i>
                  View Assignments
                </button>
                <button className="btn btn-success">
                  <i className="fas fa-medal me-2"></i>
                  Check Grades
                </button>
                <button className="btn btn-warning">
                  <i className="fas fa-users-cog me-2"></i>
                  Browse Clubs
                </button>
                <button className="btn btn-info">
                  <i className="fas fa-calendar me-2"></i>
                  View Schedule
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Notifications & Assignments */}
      <div className="row g-4">
        <div className="col-lg-6">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Recent Notifications</h5>
            </div>
            <div className="card-body">
              <div className="notification-list">
                <div className="notification-item d-flex mb-3">
                  <div className="notification-icon bg-primary bg-opacity-10 rounded-circle p-2 me-3">
                    <i className="fas fa-bell text-primary"></i>
                  </div>
                  <div className="notification-content">
                    <p className="mb-1">Assignment deadline approaching: Web Development Project</p>
                    <small className="text-muted">2 hours ago</small>
                  </div>
                </div>

                <div className="notification-item d-flex mb-3">
                  <div className="notification-icon bg-success bg-opacity-10 rounded-circle p-2 me-3">
                    <i className="fas fa-check text-success"></i>
                  </div>
                  <div className="notification-content">
                    <p className="mb-1">Grade posted for Database Quiz #2</p>
                    <small className="text-muted">4 hours ago</small>
                  </div>
                </div>

                <div className="notification-item d-flex mb-3">
                  <div className="notification-icon bg-warning bg-opacity-10 rounded-circle p-2 me-3">
                    <i className="fas fa-calendar text-warning"></i>
                  </div>
                  <div className="notification-content">
                    <p className="mb-1">New event: Tech Club Meeting scheduled</p>
                    <small className="text-muted">1 day ago</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-6">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Upcoming Assignments</h5>
            </div>
            <div className="card-body">
              <div className="assignment-list">
                <div className="assignment-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded">
                  <div>
                    <h6 className="mb-1">React Portfolio Project</h6>
                    <small className="text-muted">Web Development</small>
                  </div>
                  <span className="badge bg-danger">Due: 2 days</span>
                </div>

                <div className="assignment-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded">
                  <div>
                    <h6 className="mb-1">Algorithm Analysis Report</h6>
                    <small className="text-muted">Data Structures</small>
                  </div>
                  <span className="badge bg-warning">Due: 5 days</span>
                </div>

                <div className="assignment-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded">
                  <div>
                    <h6 className="mb-1">Database Design Project</h6>
                    <small className="text-muted">DBMS</small>
                  </div>
                  <span className="badge bg-success">Due: 1 week</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <DashboardLayout role="student" menuItems={menuItems}>
      <Routes>
        <Route path="/dashboard" element={<StudentDashboardHome />} />
        <Route path="/clubs" element={<ClubBrowser />} />
        <Route path="/" element={<StudentDashboardHome />} />
      </Routes>
    </DashboardLayout>
  );
};

export default StudentDashboard;
