import React, { useState, useEffect } from 'react';
import apiClient from '../../api/apiClient';
import { toast } from 'react-toastify';

const TeacherCourses = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [students, setStudents] = useState([]);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await apiClient.get('/teacher_interface/course-assignments/');
      setCourses(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
      toast.error('Failed to fetch courses');
    } finally {
      setLoading(false);
    }
  };

  const fetchCourseStudents = async (courseId) => {
    try {
      const response = await apiClient.get(`/teacher_interface/course-assignments/${courseId}/students/`);
      setStudents(response.data.data || response.data);
    } catch (error) {
      console.error('Error fetching students:', error);
      toast.error('Failed to fetch students');
    }
  };

  const handleCourseSelect = (course) => {
    setSelectedCourse(course);
    fetchCourseStudents(course.id);
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
    <div className="teacher-courses">
      <h2 className="mb-4">My Courses</h2>

      <div className="row">
        <div className="col-lg-4">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">Assigned Courses</h5>
            </div>
            <div className="card-body p-0">
              <div className="list-group list-group-flush">
                {courses.map((course) => (
                  <div 
                    key={course.id}
                    className={`list-group-item list-group-item-action ${
                      selectedCourse?.id === course.id ? 'active' : ''
                    }`}
                    onClick={() => handleCourseSelect(course)}
                    style={{ cursor: 'pointer' }}
                  >
                    <div className="d-flex w-100 justify-content-between">
                      <h6 className="mb-1">{course.course?.name}</h6>
                      <small className="text-muted">{course.course?.code}</small>
                    </div>
                    <p className="mb-1">{course.course?.department?.name}</p>
                    <small>Semester {course.course?.semester} • {course.course?.credits} Credits</small>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-8">
          {selectedCourse ? (
            <div className="card">
              <div className="card-header">
                <h5 className="card-title mb-0">
                  {selectedCourse.course?.name} - Students
                </h5>
              </div>
              <div className="card-body">
                <div className="row mb-3">
                  <div className="col-md-3">
                    <div className="card border-primary">
                      <div className="card-body text-center">
                        <h4 className="text-primary">{students.length}</h4>
                        <small>Total Students</small>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-3">
                    <div className="card border-success">
                      <div className="card-body text-center">
                        <h4 className="text-success">{selectedCourse.course?.credits}</h4>
                        <small>Credits</small>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-3">
                    <div className="card border-info">
                      <div className="card-body text-center">
                        <h4 className="text-info">{selectedCourse.course?.semester}</h4>
                        <small>Semester</small>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-3">
                    <div className="card border-warning">
                      <div className="card-body text-center">
                        <h4 className="text-warning">{selectedCourse.course?.course_type}</h4>
                        <small>Type</small>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>Roll No.</th>
                        <th>Student Name</th>
                        <th>Email</th>
                        <th>Enrollment Date</th>
                        <th>Current Grade</th>
                      </tr>
                    </thead>
                    <tbody>
                      {students.map((student) => (
                        <tr key={student.id}>
                          <td><strong>{student.roll_number}</strong></td>
                          <td>{student.name}</td>
                          <td>{student.email}</td>
                          <td>{new Date(student.enrollment_date).toLocaleDateString()}</td>
                          <td>
                            <span className={`badge ${
                              student.current_grade >= 80 ? 'bg-success' :
                              student.current_grade >= 60 ? 'bg-warning' : 'bg-danger'
                            }`}>
                              {student.current_grade || 'N/A'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          ) : (
            <div className="card">
              <div className="card-body text-center py-5">
                <i className="fas fa-book-open fa-3x text-muted mb-3"></i>
                <h5 className="text-muted">Select a course to view details</h5>
                <p className="text-muted">Choose a course from the left panel to see enrolled students and course information.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TeacherCourses;