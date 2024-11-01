import React from 'react';
import { Routes, Route } from 'react-router-dom';
import DashboardLayout from '../shared/DashboardLayout';

// Import existing admin components
import ClusterManagement from '../admin/ClusterManagement';
import DepartmentManagement from '../admin/DepartmentManagement';
import StaffManagement from '../admin/StaffManagement';
import StudentBulkUpload from '../admin/StudentBulkUpload';

// Import new admin components
import StudentManagement from '../admin/StudentManagement';
import CourseManagement from '../admin/CourseManagement';
import ReportsManagement from '../admin/ReportsManagement';
import SettingsManagement from '../admin/SettingsManagement';

const AdminDashboard = () => {
  const menuItems = [
    {
      label: 'Dashboard',
      path: '/admin/dashboard',
      icon: 'fas fa-tachometer-alt'
    },
    {
      label: 'Organization',
      icon: 'fas fa-sitemap',
      submenu: [
        { label: 'Clusters', path: '/admin/clusters', icon: 'fas fa-layer-group' },
        { label: 'Departments', path: '/admin/departments', icon: 'fas fa-building' }
      ]
    },
    {
      label: 'User Management',
      icon: 'fas fa-users',
      submenu: [
        { label: 'Staff', path: '/admin/staff', icon: 'fas fa-user-tie' },
        { label: 'Students', path: '/admin/students', icon: 'fas fa-user-graduate' },
        { label: 'Bulk Upload', path: '/admin/bulk-upload', icon: 'fas fa-upload' }
      ]
    },
    {
      label: 'Academic',
      icon: 'fas fa-book',
      submenu: [
        { label: 'Courses', path: '/admin/courses', icon: 'fas fa-book-open' },
        { label: 'Classes', path: '/admin/classes', icon: 'fas fa-chalkboard' },
        { label: 'Schedules', path: '/admin/schedules', icon: 'fas fa-calendar' }
      ]
    },
    {
      label: 'Reports',
      path: '/admin/reports',
      icon: 'fas fa-chart-bar'
    },
    {
      label: 'Settings',
      path: '/admin/settings',
      icon: 'fas fa-cog'
    }
  ];

  const AdminDashboardHome = () => (
    <div className="admin-dashboard">
      {/* Stats Cards */}
      <div className="row g-4 mb-4">
        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h3 className="h2 text-primary mb-1">1,247</h3>
                  <p className="text-muted mb-0">Total Students</p>
                </div>
                <div className="bg-primary bg-opacity-10 p-3 rounded-circle">
                  <i className="fas fa-user-graduate fa-2x text-primary"></i>
                </div>
              </div>
              <div className="mt-3">
                <small className="text-success">
                  <i className="fas fa-arrow-up"></i> 12% increase
                </small>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h3 className="h2 text-success mb-1">89</h3>
                  <p className="text-muted mb-0">Faculty Members</p>
                </div>
                <div className="bg-success bg-opacity-10 p-3 rounded-circle">
                  <i className="fas fa-chalkboard-teacher fa-2x text-success"></i>
                </div>
              </div>
              <div className="mt-3">
                <small className="text-success">
                  <i className="fas fa-arrow-up"></i> 5% increase
                </small>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h3 className="h2 text-warning mb-1">24</h3>
                  <p className="text-muted mb-0">Departments</p>
                </div>
                <div className="bg-warning bg-opacity-10 p-3 rounded-circle">
                  <i className="fas fa-building fa-2x text-warning"></i>
                </div>
              </div>
              <div className="mt-3">
                <small className="text-muted">
                  <i className="fas fa-minus"></i> No change
                </small>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h3 className="h2 text-info mb-1">8</h3>
                  <p className="text-muted mb-0">Active Clusters</p>
                </div>
                <div className="bg-info bg-opacity-10 p-3 rounded-circle">
                  <i className="fas fa-layer-group fa-2x text-info"></i>
                </div>
              </div>
              <div className="mt-3">
                <small className="text-muted">
                  <i className="fas fa-minus"></i> No change
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="row g-4 mb-4">
        <div className="col-lg-8">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Quick Actions</h5>
            </div>
            <div className="card-body">
              <div className="row g-3">
                <div className="col-md-4">
                  <div className="quick-action-card text-center p-3 border rounded">
                    <i className="fas fa-user-plus fa-3x text-primary mb-3"></i>
                    <h6>Add New Student</h6>
                    <button className="btn btn-sm btn-primary">Add Student</button>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="quick-action-card text-center p-3 border rounded">
                    <i className="fas fa-upload fa-3x text-success mb-3"></i>
                    <h6>Bulk Upload</h6>
                    <button className="btn btn-sm btn-success">Upload Data</button>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="quick-action-card text-center p-3 border rounded">
                    <i className="fas fa-chart-bar fa-3x text-warning mb-3"></i>
                    <h6>Generate Report</h6>
                    <button className="btn btn-sm btn-warning">View Reports</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-4">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">System Status</h5>
            </div>
            <div className="card-body">
              <div className="status-item d-flex justify-content-between align-items-center mb-3">
                <span>Server Status</span>
                <span className="badge bg-success">Online</span>
              </div>
              <div className="status-item d-flex justify-content-between align-items-center mb-3">
                <span>Database</span>
                <span className="badge bg-success">Connected</span>
              </div>
              <div className="status-item d-flex justify-content-between align-items-center mb-3">
                <span>Backup Status</span>
                <span className="badge bg-warning">Pending</span>
              </div>
              <div className="status-item d-flex justify-content-between align-items-center">
                <span>Last Login</span>
                <small className="text-muted">Just now</small>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="row">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Recent Activity</h5>
            </div>
            <div className="card-body">
              <div className="activity-feed">
                <div className="activity-item d-flex mb-3">
                  <div className="activity-icon bg-primary bg-opacity-10 rounded-circle p-2 me-3">
                    <i className="fas fa-user-plus text-primary"></i>
                  </div>
                  <div className="activity-content">
                    <p className="mb-1">New student <strong>John Doe</strong> added to Computer Science department</p>
                    <small className="text-muted">2 hours ago</small>
                  </div>
                </div>
                <div className="activity-item d-flex mb-3">
                  <div className="activity-icon bg-success bg-opacity-10 rounded-circle p-2 me-3">
                    <i className="fas fa-upload text-success"></i>
                  </div>
                  <div className="activity-content">
                    <p className="mb-1">Bulk upload completed: 45 students imported successfully</p>
                    <small className="text-muted">4 hours ago</small>
                  </div>
                </div>
                <div className="activity-item d-flex mb-3">
                  <div className="activity-icon bg-warning bg-opacity-10 rounded-circle p-2 me-3">
                    <i className="fas fa-edit text-warning"></i>
                  </div>
                  <div className="activity-content">
                    <p className="mb-1">Department structure updated for Engineering cluster</p>
                    <small className="text-muted">1 day ago</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <DashboardLayout role="admin" menuItems={menuItems}>
      <Routes>
        <Route path="/dashboard" element={<AdminDashboardHome />} />
        <Route path="/clusters" element={<ClusterManagement />} />
        <Route path="/departments" element={<DepartmentManagement />} />
        <Route path="/staff" element={<StaffManagement />} />
        <Route path="/students" element={<StudentManagement />} />
        <Route path="/bulk-upload" element={<StudentBulkUpload />} />
        <Route path="/courses" element={<CourseManagement />} />
        <Route path="/reports" element={<ReportsManagement />} />
        <Route path="/settings" element={<SettingsManagement />} />
        <Route path="/" element={<AdminDashboardHome />} />
      </Routes>
    </DashboardLayout>
  );
};

export default AdminDashboard;
