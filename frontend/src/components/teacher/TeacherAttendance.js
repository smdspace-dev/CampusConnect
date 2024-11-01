import React, { useState, useEffect } from 'react';
import apiClient from '../../api/apiClient';
import { toast } from 'react-toastify';

const TeacherAttendance = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [students, setStudents] = useState([]);
  const [attendanceData, setAttendanceData] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(false);
  const [attendanceStats, setAttendanceStats] = useState({});

  useEffect(() => {
    fetchCourses();
  }, []);

  useEffect(() => {
    if (selectedCourse) {
      fetchStudents();
      fetchAttendanceStats();
    }
  }, [selectedCourse]);

  useEffect(() => {
    if (selectedCourse && selectedDate) {
      fetchAttendanceForDate();
    }
  }, [selectedCourse, selectedDate]);

  const fetchCourses = async () => {
    try {
      const response = await apiClient.get('/teacher_interface/course-assignments/');
      setCourses(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
      toast.error('Failed to fetch courses');
    }
  };

  const fetchStudents = async () => {
    try {
      const response = await apiClient.get(`/teacher_interface/course-assignments/${selectedCourse}/students/`);
      setStudents(response.data.data || response.data);
    } catch (error) {
      console.error('Error fetching students:', error);
      toast.error('Failed to fetch students');
    }
  };

  const fetchAttendanceForDate = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get(`/teacher_interface/attendance/`, {
        params: {
          course_assignment: selectedCourse,
          date: selectedDate
        }
      });
      
      const attendanceRecords = response.data.results || response.data;
      const attendanceMap = {};
      
      attendanceRecords.forEach(record => {
        attendanceMap[record.student.id] = {
          id: record.id,
          status: record.status,
          remarks: record.remarks || ''
        };
      });
      
      setAttendanceData(attendanceMap);
    } catch (error) {
      console.error('Error fetching attendance:', error);
      if (error.response?.status !== 404) {
        toast.error('Failed to fetch attendance data');
      }
      setAttendanceData({});
    } finally {
      setLoading(false);
    }
  };

  const fetchAttendanceStats = async () => {
    try {
      const response = await apiClient.get(`/teacher_interface/attendance/stats/`, {
        params: { course_assignment: selectedCourse }
      });
      setAttendanceStats(response.data.data || {});
    } catch (error) {
      console.error('Error fetching attendance stats:', error);
    }
  };

  const handleAttendanceChange = (studentId, status) => {
    setAttendanceData(prev => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        status: status
      }
    }));
  };

  const handleRemarksChange = (studentId, remarks) => {
    setAttendanceData(prev => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        remarks: remarks
      }
    }));
  };

  const handleSubmitAttendance = async () => {
    if (!selectedCourse || !selectedDate) {
      toast.error('Please select course and date');
      return;
    }

    const attendanceRecords = students.map(student => ({
      student: student.id,
      course_assignment: selectedCourse,
      date: selectedDate,
      status: attendanceData[student.id]?.status || 'PRESENT',
      remarks: attendanceData[student.id]?.remarks || ''
    }));

    try {
      await apiClient.post('/teacher_interface/attendance/bulk_create/', {
        attendance_records: attendanceRecords
      });
      toast.success('Attendance saved successfully');
      fetchAttendanceStats();
    } catch (error) {
      console.error('Error saving attendance:', error);
      toast.error(error.response?.data?.detail || 'Failed to save attendance');
    }
  };

  const markAllPresent = () => {
    const newAttendanceData = {};
    students.forEach(student => {
      newAttendanceData[student.id] = {
        ...attendanceData[student.id],
        status: 'PRESENT'
      };
    });
    setAttendanceData(newAttendanceData);
  };

  const markAllAbsent = () => {
    const newAttendanceData = {};
    students.forEach(student => {
      newAttendanceData[student.id] = {
        ...attendanceData[student.id],
        status: 'ABSENT'
      };
    });
    setAttendanceData(newAttendanceData);
  };

  const getAttendancePercentage = (studentId) => {
    const stats = attendanceStats[studentId];
    if (!stats) return '0%';
    const total = stats.present + stats.absent + stats.late;
    if (total === 0) return '0%';
    return `${Math.round((stats.present / total) * 100)}%`;
  };

  return (
    <div className="teacher-attendance">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Attendance Management</h2>
      </div>

      {/* Course and Date Selection */}
      <div className="card mb-4">
        <div className="card-body">
          <div className="row">
            <div className="col-md-6">
              <label className="form-label">Select Course</label>
              <select
                className="form-select"
                value={selectedCourse}
                onChange={(e) => setSelectedCourse(e.target.value)}
              >
                <option value="">Choose a course...</option>
                {courses.map((course) => (
                  <option key={course.id} value={course.id}>
                    {course.course?.name} ({course.course?.code})
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-6">
              <label className="form-label">Date</label>
              <input
                type="date"
                className="form-control"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>

      {selectedCourse && students.length > 0 && (
        <>
          {/* Quick Actions */}
          <div className="card mb-4">
            <div className="card-body">
              <div className="d-flex gap-2 flex-wrap">
                <button className="btn btn-success btn-sm" onClick={markAllPresent}>
                  <i className="fas fa-check me-1"></i>Mark All Present
                </button>
                <button className="btn btn-danger btn-sm" onClick={markAllAbsent}>
                  <i className="fas fa-times me-1"></i>Mark All Absent
                </button>
                <button className="btn btn-primary" onClick={handleSubmitAttendance}>
                  <i className="fas fa-save me-1"></i>Save Attendance
                </button>
              </div>
            </div>
          </div>

          {/* Attendance Table */}
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">
                Attendance for {selectedDate}
              </h5>
            </div>
            <div className="card-body">
              {loading ? (
                <div className="text-center">
                  <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                </div>
              ) : (
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>Student Name</th>
                        <th>Roll Number</th>
                        <th>Attendance %</th>
                        <th>Status</th>
                        <th>Remarks</th>
                      </tr>
                    </thead>
                    <tbody>
                      {students.map((student) => (
                        <tr key={student.id}>
                          <td>
                            <div className="d-flex align-items-center">
                              <div className="me-2">
                                <i className="fas fa-user-circle fa-2x text-secondary"></i>
                              </div>
                              <div>
                                <strong>{student.user?.first_name} {student.user?.last_name}</strong>
                                <br />
                                <small className="text-muted">{student.user?.email}</small>
                              </div>
                            </div>
                          </td>
                          <td>{student.roll_number}</td>
                          <td>
                            <span className={`badge ${
                              parseInt(getAttendancePercentage(student.id)) >= 75 ? 'bg-success' : 
                              parseInt(getAttendancePercentage(student.id)) >= 50 ? 'bg-warning' : 'bg-danger'
                            }`}>
                              {getAttendancePercentage(student.id)}
                            </span>
                          </td>
                          <td>
                            <div className="btn-group btn-group-sm" role="group">
                              <input
                                type="radio"
                                className="btn-check"
                                name={`attendance-${student.id}`}
                                id={`present-${student.id}`}
                                checked={attendanceData[student.id]?.status === 'PRESENT'}
                                onChange={() => handleAttendanceChange(student.id, 'PRESENT')}
                              />
                              <label className="btn btn-outline-success" htmlFor={`present-${student.id}`}>
                                Present
                              </label>

                              <input
                                type="radio"
                                className="btn-check"
                                name={`attendance-${student.id}`}
                                id={`absent-${student.id}`}
                                checked={attendanceData[student.id]?.status === 'ABSENT'}
                                onChange={() => handleAttendanceChange(student.id, 'ABSENT')}
                              />
                              <label className="btn btn-outline-danger" htmlFor={`absent-${student.id}`}>
                                Absent
                              </label>

                              <input
                                type="radio"
                                className="btn-check"
                                name={`attendance-${student.id}`}
                                id={`late-${student.id}`}
                                checked={attendanceData[student.id]?.status === 'LATE'}
                                onChange={() => handleAttendanceChange(student.id, 'LATE')}
                              />
                              <label className="btn btn-outline-warning" htmlFor={`late-${student.id}`}>
                                Late
                              </label>
                            </div>
                          </td>
                          <td>
                            <input
                              type="text"
                              className="form-control form-control-sm"
                              placeholder="Add remarks..."
                              value={attendanceData[student.id]?.remarks || ''}
                              onChange={(e) => handleRemarksChange(student.id, e.target.value)}
                            />
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </>
      )}

      {selectedCourse && students.length === 0 && !loading && (
        <div className="card">
          <div className="card-body text-center">
            <i className="fas fa-users fa-3x text-muted mb-3"></i>
            <h5>No Students Found</h5>
            <p className="text-muted">No students are enrolled in this course.</p>
          </div>
        </div>
      )}

      {!selectedCourse && (
        <div className="card">
          <div className="card-body text-center">
            <i className="fas fa-book fa-3x text-muted mb-3"></i>
            <h5>Select a Course</h5>
            <p className="text-muted">Please select a course to view and manage attendance.</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeacherAttendance;