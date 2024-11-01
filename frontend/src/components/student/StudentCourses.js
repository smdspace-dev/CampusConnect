import React, { useState, useEffect } from 'react';
import apiClient from '../../api/apiClient';
import { toast } from 'react-toastify';

const StudentCourses = () => {
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [availableCourses, setAvailableCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('enrolled');
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [showCourseDetails, setShowCourseDetails] = useState(false);

  useEffect(() => {
    fetchEnrolledCourses();
    fetchAvailableCourses();
  }, []);

  const fetchEnrolledCourses = async () => {
    try {
      const response = await apiClient.get('/student_interface/enrolled-courses/');
      setEnrolledCourses(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching enrolled courses:', error);
      toast.error('Failed to fetch enrolled courses');
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailableCourses = async () => {
    try {
      const response = await apiClient.get('/student_interface/available-courses/');
      setAvailableCourses(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching available courses:', error);
    }
  };

  const handleEnrollment = async (courseId) => {
    try {
      await apiClient.post('/student_interface/enroll/', {
        course_id: courseId
      });
      toast.success('Successfully enrolled in course');
      fetchEnrolledCourses();
      fetchAvailableCourses();
    } catch (error) {
      console.error('Error enrolling in course:', error);
      toast.error(error.response?.data?.detail || 'Failed to enroll in course');
    }
  };

  const handleViewCourseDetails = async (course) => {
    setSelectedCourse(course);
    setShowCourseDetails(true);
  };

  const handleDropCourse = async (enrollmentId) => {
    if (window.confirm('Are you sure you want to drop this course? This action cannot be undone.')) {
      try {
        await apiClient.delete(`/student_interface/enrolled-courses/${enrollmentId}/`);
        toast.success('Course dropped successfully');
        fetchEnrolledCourses();
        fetchAvailableCourses();
      } catch (error) {
        console.error('Error dropping course:', error);
        toast.error('Failed to drop course');
      }
    }
  };

  const getCreditProgress = () => {
    const totalCredits = enrolledCourses.reduce((sum, course) => 
      sum + (course.course?.credits || 0), 0
    );
    const maxCredits = 18; // Typical max credits per semester
    return { current: totalCredits, max: maxCredits, percentage: (totalCredits / maxCredits) * 100 };
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

  const creditProgress = getCreditProgress();

  return (
    <div className="student-courses">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>My Courses</h2>
        <div className="d-flex align-items-center">
          <div className="me-3">
            <small className="text-muted">Credits: {creditProgress.current}/{creditProgress.max}</small>
            <div className="progress" style={{ width: '120px', height: '6px' }}>
              <div 
                className="progress-bar bg-primary" 
                style={{ width: `${Math.min(creditProgress.percentage, 100)}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'enrolled' ? 'active' : ''}`}
            onClick={() => setActiveTab('enrolled')}
          >
            <i className="fas fa-book me-2"></i>
            Enrolled Courses ({enrolledCourses.length})
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'available' ? 'active' : ''}`}
            onClick={() => setActiveTab('available')}
          >
            <i className="fas fa-plus-circle me-2"></i>
            Available Courses ({availableCourses.length})
          </button>
        </li>
      </ul>

      {/* Enrolled Courses Tab */}
      {activeTab === 'enrolled' && (
        <div className="row">
          {enrolledCourses.length === 0 ? (
            <div className="col-12">
              <div className="card">
                <div className="card-body text-center py-5">
                  <i className="fas fa-book-open fa-3x text-muted mb-3"></i>
                  <h5>No Enrolled Courses</h5>
                  <p className="text-muted">You haven't enrolled in any courses yet. Check the available courses tab to get started.</p>
                  <button 
                    className="btn btn-primary"
                    onClick={() => setActiveTab('available')}
                  >
                    Browse Available Courses
                  </button>
                </div>
              </div>
            </div>
          ) : (
            enrolledCourses.map((enrollment) => (
              <div key={enrollment.id} className="col-lg-6 col-xl-4 mb-4">
                <div className="card h-100 shadow-sm">
                  <div className="card-header bg-primary text-white">
                    <div className="d-flex justify-content-between align-items-center">
                      <h6 className="card-title mb-0">{enrollment.course?.code}</h6>
                      <span className="badge bg-light text-primary">
                        {enrollment.course?.credits} Credits
                      </span>
                    </div>
                  </div>
                  <div className="card-body">
                    <h5 className="card-title">{enrollment.course?.name}</h5>
                    <p className="text-muted mb-3">{enrollment.course?.description}</p>
                    
                    <div className="mb-3">
                      <div className="row text-center">
                        <div className="col-4">
                          <div className="border-end">
                            <h6 className="text-primary mb-1">{enrollment.attendance_percentage || '0'}%</h6>
                            <small className="text-muted">Attendance</small>
                          </div>
                        </div>
                        <div className="col-4">
                          <div className="border-end">
                            <h6 className="text-success mb-1">{enrollment.current_grade || 'N/A'}</h6>
                            <small className="text-muted">Grade</small>
                          </div>
                        </div>
                        <div className="col-4">
                          <h6 className="text-info mb-1">{enrollment.assignments_completed || '0'}</h6>
                          <small className="text-muted">Assignments</small>
                        </div>
                      </div>
                    </div>

                    <div className="mb-3">
                      <small className="text-muted">Instructor:</small>
                      <div className="d-flex align-items-center mt-1">
                        <i className="fas fa-user-tie me-2 text-secondary"></i>
                        <span>{enrollment.instructor_name || 'TBA'}</span>
                      </div>
                    </div>

                    <div className="mb-3">
                      <small className="text-muted">Schedule:</small>
                      <div className="d-flex align-items-center mt-1">
                        <i className="fas fa-clock me-2 text-secondary"></i>
                        <span>{enrollment.schedule || 'TBA'}</span>
                      </div>
                    </div>
                  </div>
                  <div className="card-footer bg-transparent">
                    <div className="d-flex gap-2">
                      <button 
                        className="btn btn-outline-primary btn-sm flex-fill"
                        onClick={() => handleViewCourseDetails(enrollment.course)}
                      >
                        <i className="fas fa-eye me-1"></i>Details
                      </button>
                      <button 
                        className="btn btn-outline-danger btn-sm"
                        onClick={() => handleDropCourse(enrollment.id)}
                      >
                        <i className="fas fa-trash me-1"></i>Drop
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Available Courses Tab */}
      {activeTab === 'available' && (
        <div className="row">
          {availableCourses.length === 0 ? (
            <div className="col-12">
              <div className="card">
                <div className="card-body text-center py-5">
                  <i className="fas fa-graduation-cap fa-3x text-muted mb-3"></i>
                  <h5>No Available Courses</h5>
                  <p className="text-muted">There are no courses available for enrollment at this time.</p>
                </div>
              </div>
            </div>
          ) : (
            availableCourses.map((course) => (
              <div key={course.id} className="col-lg-6 col-xl-4 mb-4">
                <div className="card h-100 shadow-sm">
                  <div className="card-header bg-light">
                    <div className="d-flex justify-content-between align-items-center">
                      <h6 className="card-title mb-0">{course.code}</h6>
                      <span className="badge bg-primary">
                        {course.credits} Credits
                      </span>
                    </div>
                  </div>
                  <div className="card-body">
                    <h5 className="card-title">{course.name}</h5>
                    <p className="text-muted mb-3">{course.description}</p>
                    
                    <div className="mb-3">
                      <div className="row">
                        <div className="col-6">
                          <small className="text-muted">Department:</small>
                          <div>{course.department?.name}</div>
                        </div>
                        <div className="col-6">
                          <small className="text-muted">Type:</small>
                          <div>
                            <span className={`badge ${
                              course.course_type === 'CORE' ? 'bg-success' :
                              course.course_type === 'ELECTIVE' ? 'bg-info' : 'bg-secondary'
                            }`}>
                              {course.course_type}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="mb-3">
                      <small className="text-muted">Prerequisites:</small>
                      <div>{course.prerequisites || 'None'}</div>
                    </div>

                    <div className="mb-3">
                      <small className="text-muted">Semester:</small>
                      <div>Semester {course.semester}</div>
                    </div>

                    {course.max_students && (
                      <div className="mb-3">
                        <small className="text-muted">Capacity:</small>
                        <div className="d-flex align-items-center">
                          <span>{course.enrolled_students || 0}/{course.max_students}</span>
                          <div className="progress ms-2 flex-fill" style={{ height: '8px' }}>
                            <div 
                              className="progress-bar bg-info" 
                              style={{ 
                                width: `${((course.enrolled_students || 0) / course.max_students) * 100}%` 
                              }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="card-footer bg-transparent">
                    <div className="d-flex gap-2">
                      <button 
                        className="btn btn-outline-info btn-sm flex-fill"
                        onClick={() => handleViewCourseDetails(course)}
                      >
                        <i className="fas fa-info-circle me-1"></i>View Details
                      </button>
                      <button 
                        className="btn btn-primary btn-sm"
                        onClick={() => handleEnrollment(course.id)}
                        disabled={course.max_students && course.enrolled_students >= course.max_students}
                      >
                        <i className="fas fa-plus me-1"></i>Enroll
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Course Details Modal */}
      {showCourseDetails && selectedCourse && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-lg">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  {selectedCourse.code} - {selectedCourse.name}
                </h5>
                <button 
                  type="button" 
                  className="btn-close" 
                  onClick={() => setShowCourseDetails(false)}
                ></button>
              </div>
              <div className="modal-body">
                <div className="row">
                  <div className="col-md-6">
                    <h6>Course Information</h6>
                    <ul className="list-unstyled">
                      <li><strong>Code:</strong> {selectedCourse.code}</li>
                      <li><strong>Credits:</strong> {selectedCourse.credits}</li>
                      <li><strong>Department:</strong> {selectedCourse.department?.name}</li>
                      <li><strong>Type:</strong> {selectedCourse.course_type}</li>
                      <li><strong>Semester:</strong> {selectedCourse.semester}</li>
                    </ul>
                  </div>
                  <div className="col-md-6">
                    <h6>Additional Details</h6>
                    <ul className="list-unstyled">
                      <li><strong>Prerequisites:</strong> {selectedCourse.prerequisites || 'None'}</li>
                      {selectedCourse.max_students && (
                        <li><strong>Max Students:</strong> {selectedCourse.max_students}</li>
                      )}
                      {selectedCourse.syllabus_url && (
                        <li>
                          <strong>Syllabus:</strong> 
                          <a href={selectedCourse.syllabus_url} target="_blank" rel="noopener noreferrer">
                            Download
                          </a>
                        </li>
                      )}
                    </ul>
                  </div>
                </div>
                <div className="mt-3">
                  <h6>Description</h6>
                  <p>{selectedCourse.description}</p>
                </div>
              </div>
              <div className="modal-footer">
                <button 
                  type="button" 
                  className="btn btn-secondary" 
                  onClick={() => setShowCourseDetails(false)}
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentCourses;