import React from 'react';
import { Routes, Route } from 'react-router-dom';
import DashboardLayout from '../shared/DashboardLayout';

const ResourcePersonDashboard = () => {
  const menuItems = [
    {
      label: 'Dashboard',
      path: '/resource-person/dashboard',
      icon: 'fas fa-tachometer-alt'
    },
    {
      label: 'Placements',
      icon: 'fas fa-briefcase',
      submenu: [
        { label: 'Job Opportunities', path: '/resource-person/jobs', icon: 'fas fa-search' },
        { label: 'Company Relations', path: '/resource-person/companies', icon: 'fas fa-building' },
        { label: 'Placement Drive', path: '/resource-person/drives', icon: 'fas fa-calendar-check' }
      ]
    },
    {
      label: 'Students',
      icon: 'fas fa-user-graduate',
      submenu: [
        { label: 'Student Database', path: '/resource-person/students', icon: 'fas fa-database' },
        { label: 'Career Counseling', path: '/resource-person/counseling', icon: 'fas fa-comments' },
        { label: 'Resume Review', path: '/resource-person/resumes', icon: 'fas fa-file-alt' }
      ]
    },
    {
      label: 'Training',
      icon: 'fas fa-graduation-cap',
      submenu: [
        { label: 'Skill Development', path: '/resource-person/training', icon: 'fas fa-tools' },
        { label: 'Workshops', path: '/resource-person/workshops', icon: 'fas fa-chalkboard-teacher' },
        { label: 'Industry Connect', path: '/resource-person/industry', icon: 'fas fa-handshake' }
      ]
    },
    {
      label: 'Reports',
      icon: 'fas fa-chart-bar',
      submenu: [
        { label: 'Placement Stats', path: '/resource-person/stats', icon: 'fas fa-chart-pie' },
        { label: 'Company Analysis', path: '/resource-person/analysis', icon: 'fas fa-analytics' },
        { label: 'Performance Reports', path: '/resource-person/performance', icon: 'fas fa-chart-line' }
      ]
    },
    {
      label: 'Profile',
      path: '/resource-person/profile',
      icon: 'fas fa-user'
    }
  ];

  const ResourcePersonDashboardHome = () => (
    <div className="resource-person-dashboard">
      {/* Welcome Section */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card border-0 shadow-sm bg-gradient-primary text-white">
            <div className="card-body p-4">
              <div className="row align-items-center">
                <div className="col-md-8">
                  <h2 className="h3 mb-2">Welcome back, Career Counselor!</h2>
                  <p className="mb-3">Building bridges between talent and opportunity.</p>
                  <div className="d-flex gap-4">
                    <div className="stat-item">
                      <strong>85%</strong>
                      <small className="d-block">Placement Rate</small>
                    </div>
                    <div className="stat-item">
                      <strong>15</strong>
                      <small className="d-block">Active Companies</small>
                    </div>
                    <div className="stat-item">
                      <strong>3</strong>
                      <small className="d-block">Ongoing Drives</small>
                    </div>
                  </div>
                </div>
                <div className="col-md-4 text-center">
                  <i className="fas fa-briefcase fa-5x opacity-50"></i>
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
                <i className="fas fa-user-tie fa-2x text-success"></i>
              </div>
              <h4 className="h5 mb-2">Placed Students</h4>
              <h3 className="text-success mb-0">124</h3>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-primary bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-building fa-2x text-primary"></i>
              </div>
              <h4 className="h5 mb-2">Partner Companies</h4>
              <h3 className="text-primary mb-0">35</h3>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-warning bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-calendar-check fa-2x text-warning"></i>
              </div>
              <h4 className="h5 mb-2">Active Drives</h4>
              <h3 className="text-warning mb-0">3</h3>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body text-center">
              <div className="bg-info bg-opacity-10 rounded-circle p-3 mx-auto mb-3" style={{width: '60px', height: '60px'}}>
                <i className="fas fa-graduation-cap fa-2x text-info"></i>
              </div>
              <h4 className="h5 mb-2">Training Programs</h4>
              <h3 className="text-info mb-0">8</h3>
            </div>
          </div>
        </div>
      </div>

      {/* Current Activities & Quick Actions */}
      <div className="row g-4 mb-4">
        <div className="col-lg-8">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Current Placement Drives</h5>
            </div>
            <div className="card-body">
              <div className="drive-list">
                <div className="drive-item d-flex align-items-center mb-3 p-3 bg-light rounded">
                  <div className="company-logo bg-primary text-white rounded-circle p-3 me-3" style={{width: '50px', height: '50px'}}>
                    <i className="fas fa-building"></i>
                  </div>
                  <div className="drive-content flex-grow-1">
                    <h6 className="mb-1">TCS Campus Drive</h6>
                    <p className="text-muted mb-0">Software Engineer • 25 positions • Ends in 3 days</p>
                  </div>
                  <div className="drive-status">
                    <span className="badge bg-success">Active</span>
                  </div>
                </div>

                <div className="drive-item d-flex align-items-center mb-3 p-3 bg-light rounded">
                  <div className="company-logo bg-info text-white rounded-circle p-3 me-3" style={{width: '50px', height: '50px'}}>
                    <i className="fas fa-laptop-code"></i>
                  </div>
                  <div className="drive-content flex-grow-1">
                    <h6 className="mb-1">Infosys PowerProgrammer</h6>
                    <p className="text-muted mb-0">Systems Engineer • 30 positions • Applications open</p>
                  </div>
                  <div className="drive-status">
                    <span className="badge bg-primary">Recruiting</span>
                  </div>
                </div>

                <div className="drive-item d-flex align-items-center mb-3 p-3 bg-light rounded">
                  <div className="company-logo bg-success text-white rounded-circle p-3 me-3" style={{width: '50px', height: '50px'}}>
                    <i className="fas fa-chart-line"></i>
                  </div>
                  <div className="drive-content flex-grow-1">
                    <h6 className="mb-1">Wipro Elite NTH</h6>
                    <p className="text-muted mb-0">Business Analyst • 15 positions • Selection ongoing</p>
                  </div>
                  <div className="drive-status">
                    <span className="badge bg-warning">In Progress</span>
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
                  <i className="fas fa-plus me-2"></i>
                  Schedule Interview
                </button>
                <button className="btn btn-primary">
                  <i className="fas fa-building me-2"></i>
                  Add Company
                </button>
                <button className="btn btn-warning">
                  <i className="fas fa-file-alt me-2"></i>
                  Review Resume
                </button>
                <button className="btn btn-info">
                  <i className="fas fa-calendar-plus me-2"></i>
                  Plan Workshop
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activities & Placement Analytics */}
      <div className="row g-4">
        <div className="col-lg-6">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Recent Placements</h5>
            </div>
            <div className="card-body">
              <div className="placement-list">
                <div className="placement-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded">
                  <div>
                    <h6 className="mb-1">Rahul Sharma</h6>
                    <small className="text-muted">Placed at Microsoft • ₹18 LPA</small>
                  </div>
                  <div>
                    <span className="badge bg-success">Confirmed</span>
                  </div>
                </div>

                <div className="placement-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded">
                  <div>
                    <h6 className="mb-1">Priya Patel</h6>
                    <small className="text-muted">Selected at Amazon • ₹22 LPA</small>
                  </div>
                  <div>
                    <span className="badge bg-warning">Pending</span>
                  </div>
                </div>

                <div className="placement-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded">
                  <div>
                    <h6 className="mb-1">Amit Kumar</h6>
                    <small className="text-muted">Joined Accenture • ₹6.5 LPA</small>
                  </div>
                  <div>
                    <span className="badge bg-success">Confirmed</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-6">
          <div className="card border-0 shadow-sm">
            <div className="card-header bg-white border-bottom">
              <h5 className="card-title mb-0">Department-wise Placement Rate</h5>
            </div>
            <div className="card-body">
              <div className="department-stats">
                <div className="stat-item mb-4">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="fw-medium">Computer Science</span>
                    <span className="text-success">92%</span>
                  </div>
                  <div className="progress mb-2">
                    <div className="progress-bar bg-success" style={{width: '92%'}}></div>
                  </div>
                  <small className="text-muted">154 students • 142 placed</small>
                </div>

                <div className="stat-item mb-4">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="fw-medium">Information Technology</span>
                    <span className="text-success">88%</span>
                  </div>
                  <div className="progress mb-2">
                    <div className="progress-bar bg-success" style={{width: '88%'}}></div>
                  </div>
                  <small className="text-muted">120 students • 106 placed</small>
                </div>

                <div className="stat-item mb-4">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="fw-medium">Electronics & Communication</span>
                    <span className="text-warning">75%</span>
                  </div>
                  <div className="progress mb-2">
                    <div className="progress-bar bg-warning" style={{width: '75%'}}></div>
                  </div>
                  <small className="text-muted">98 students • 74 placed</small>
                </div>

                <div className="stat-item">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="fw-medium">Mechanical Engineering</span>
                    <span className="text-info">68%</span>
                  </div>
                  <div className="progress mb-2">
                    <div className="progress-bar bg-info" style={{width: '68%'}}></div>
                  </div>
                  <small className="text-muted">85 students • 58 placed</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <DashboardLayout role="resource-person" menuItems={menuItems}>
      <Routes>
        <Route path="/dashboard" element={<ResourcePersonDashboardHome />} />
        <Route path="/" element={<ResourcePersonDashboardHome />} />
      </Routes>
    </DashboardLayout>
  );
};

export default ResourcePersonDashboard;
