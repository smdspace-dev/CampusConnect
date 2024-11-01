import React, { useState, useEffect } from 'react';
import apiClient from '../../api/apiClient';
import { toast } from 'react-toastify';

const ReportsManagement = () => {
  const [dashboardStats, setDashboardStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [reportType, setReportType] = useState('overview');

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await apiClient.get('/admin_system/dashboard/stats/');
      setDashboardStats(response.data);
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      toast.error('Failed to fetch reports data');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async (type) => {
    try {
      const response = await apiClient.get(`/admin_system/reports/export/?type=${type}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${type}_report_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success(`${type} report downloaded successfully`);
    } catch (error) {
      console.error('Error downloading report:', error);
      toast.error('Failed to download report');
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '400px' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="reports-management">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Reports & Analytics</h2>
        <div className="btn-group">
          <button 
            className={`btn ${reportType === 'overview' ? 'btn-primary' : 'btn-outline-primary'}`}
            onClick={() => setReportType('overview')}
          >
            Overview
          </button>
          <button 
            className={`btn ${reportType === 'detailed' ? 'btn-primary' : 'btn-outline-primary'}`}
            onClick={() => setReportType('detailed')}
          >
            Detailed
          </button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="row g-4 mb-4">
        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h3 className="h2 text-primary mb-1">{dashboardStats?.total_students || 0}</h3>
                  <p className="text-muted mb-0">Total Students</p>
                </div>
                <div className="bg-primary bg-opacity-10 p-3 rounded-circle">
                  <i className="fas fa-user-graduate fa-2x text-primary"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h3 className="h2 text-success mb-1">{dashboardStats?.total_faculty || 0}</h3>
                  <p className="text-muted mb-0">Faculty Members</p>
                </div>
                <div className="bg-success bg-opacity-10 p-3 rounded-circle">
                  <i className="fas fa-chalkboard-teacher fa-2x text-success"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h3 className="h2 text-info mb-1">{dashboardStats?.total_departments || 0}</h3>
                  <p className="text-muted mb-0">Departments</p>
                </div>
                <div className="bg-info bg-opacity-10 p-3 rounded-circle">
                  <i className="fas fa-building fa-2x text-info"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h3 className="h2 text-warning mb-1">{dashboardStats?.total_courses || 0}</h3>
                  <p className="text-muted mb-0">Courses</p>
                </div>
                <div className="bg-warning bg-opacity-10 p-3 rounded-circle">
                  <i className="fas fa-book fa-2x text-warning"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Report Generation */}
      <div className="row">
        <div className="col-lg-8">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">Generate Reports</h5>
            </div>
            <div className="card-body">
              <div className="row g-3">
                <div className="col-md-6">
                  <div className="card border">
                    <div className="card-body text-center">
                      <i className="fas fa-users fa-3x text-primary mb-3"></i>
                      <h5>Student Report</h5>
                      <p className="text-muted">Complete student enrollment and academic data</p>
                      <button 
                        className="btn btn-primary"
                        onClick={() => downloadReport('students')}
                      >
                        <i className="fas fa-download me-2"></i>Download
                      </button>
                    </div>
                  </div>
                </div>

                <div className="col-md-6">
                  <div className="card border">
                    <div className="card-body text-center">
                      <i className="fas fa-chalkboard-teacher fa-3x text-success mb-3"></i>
                      <h5>Faculty Report</h5>
                      <p className="text-muted">Staff details and department assignments</p>
                      <button 
                        className="btn btn-success"
                        onClick={() => downloadReport('faculty')}
                      >
                        <i className="fas fa-download me-2"></i>Download
                      </button>
                    </div>
                  </div>
                </div>

                <div className="col-md-6">
                  <div className="card border">
                    <div className="card-body text-center">
                      <i className="fas fa-book fa-3x text-info mb-3"></i>
                      <h5>Course Report</h5>
                      <p className="text-muted">Course details and enrollment statistics</p>
                      <button 
                        className="btn btn-info"
                        onClick={() => downloadReport('courses')}
                      >
                        <i className="fas fa-download me-2"></i>Download
                      </button>
                    </div>
                  </div>
                </div>

                <div className="col-md-6">
                  <div className="card border">
                    <div className="card-body text-center">
                      <i className="fas fa-building fa-3x text-warning mb-3"></i>
                      <h5>Department Report</h5>
                      <p className="text-muted">Department-wise statistics and data</p>
                      <button 
                        className="btn btn-warning"
                        onClick={() => downloadReport('departments')}
                      >
                        <i className="fas fa-download me-2"></i>Download
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-4">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">Quick Analytics</h5>
            </div>
            <div className="card-body">
              {dashboardStats?.department_statistics && (
                <div className="mb-4">
                  <h6>Department Distribution</h6>
                  {dashboardStats.department_statistics.slice(0, 5).map((dept, index) => (
                    <div key={index} className="d-flex justify-content-between align-items-center mb-2">
                      <span className="small">{dept.name}</span>
                      <span className="badge bg-primary">{dept.student_count}</span>
                    </div>
                  ))}
                </div>
              )}

              {dashboardStats?.recent_activities && (
                <div>
                  <h6>Recent Activities</h6>
                  {dashboardStats.recent_activities.slice(0, 3).map((activity, index) => (
                    <div key={index} className="d-flex align-items-start mb-2">
                      <div className="flex-shrink-0">
                        <i className="fas fa-circle text-primary" style={{ fontSize: '8px' }}></i>
                      </div>
                      <div className="flex-grow-1 ms-2">
                        <p className="small mb-0">{activity.description}</p>
                        <small className="text-muted">{activity.timestamp}</small>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportsManagement;