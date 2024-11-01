import React, { useState, useEffect } from 'react';
import apiClient from '../../api/apiClient';
import { toast } from 'react-toastify';

const TeacherGrading = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [gradingPeriods, setGradingPeriods] = useState([]);
  const [selectedPeriod, setSelectedPeriod] = useState('');
  const [students, setStudents] = useState([]);
  const [grades, setGrades] = useState({});
  const [loading, setLoading] = useState(false);
  const [gradeStats, setGradeStats] = useState({});
  const [showCreatePeriod, setShowCreatePeriod] = useState(false);
  const [newPeriod, setNewPeriod] = useState({
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    weightage: 100
  });

  useEffect(() => {
    fetchCourses();
  }, []);

  useEffect(() => {
    if (selectedCourse) {
      fetchGradingPeriods();
      fetchStudents();
    }
  }, [selectedCourse]);

  useEffect(() => {
    if (selectedCourse && selectedPeriod) {
      fetchGrades();
      fetchGradeStats();
    }
  }, [selectedCourse, selectedPeriod]);

  const fetchCourses = async () => {
    try {
      const response = await apiClient.get('/teacher_interface/course-assignments/');
      setCourses(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
      toast.error('Failed to fetch courses');
    }
  };

  const fetchGradingPeriods = async () => {
    try {
      const response = await apiClient.get(`/teacher_interface/grading-periods/`, {
        params: { course_assignment: selectedCourse }
      });
      setGradingPeriods(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching grading periods:', error);
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

  const fetchGrades = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get(`/teacher_interface/grades/`, {
        params: {
          course_assignment: selectedCourse,
          grading_period: selectedPeriod
        }
      });
      
      const gradeRecords = response.data.results || response.data;
      const gradeMap = {};
      
      gradeRecords.forEach(grade => {
        if (!gradeMap[grade.student.id]) {
          gradeMap[grade.student.id] = {};
        }
        gradeMap[grade.student.id][grade.component] = {
          id: grade.id,
          marks: grade.marks,
          max_marks: grade.max_marks,
          feedback: grade.feedback || ''
        };
      });
      
      setGrades(gradeMap);
    } catch (error) {
      console.error('Error fetching grades:', error);
      setGrades({});
    } finally {
      setLoading(false);
    }
  };

  const fetchGradeStats = async () => {
    try {
      const response = await apiClient.get(`/teacher_interface/grades/stats/`, {
        params: {
          course_assignment: selectedCourse,
          grading_period: selectedPeriod
        }
      });
      setGradeStats(response.data.data || {});
    } catch (error) {
      console.error('Error fetching grade stats:', error);
    }
  };

  const handleGradeChange = (studentId, component, field, value) => {
    setGrades(prev => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        [component]: {
          ...prev[studentId]?.[component],
          [field]: value
        }
      }
    }));
  };

  const handleCreatePeriod = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post('/teacher_interface/grading-periods/', {
        ...newPeriod,
        course_assignment: selectedCourse
      });
      toast.success('Grading period created successfully');
      setShowCreatePeriod(false);
      setNewPeriod({
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        weightage: 100
      });
      fetchGradingPeriods();
    } catch (error) {
      console.error('Error creating grading period:', error);
      toast.error('Failed to create grading period');
    }
  };

  const handleSubmitGrades = async () => {
    if (!selectedCourse || !selectedPeriod) {
      toast.error('Please select course and grading period');
      return;
    }

    const gradeRecords = [];
    const components = ['ASSIGNMENT', 'TEST', 'PROJECT', 'PARTICIPATION', 'FINAL_EXAM'];

    students.forEach(student => {
      components.forEach(component => {
        const gradeData = grades[student.id]?.[component];
        if (gradeData && gradeData.marks !== undefined && gradeData.marks !== '') {
          gradeRecords.push({
            student: student.id,
            course_assignment: selectedCourse,
            grading_period: selectedPeriod,
            component: component,
            marks: parseFloat(gradeData.marks),
            max_marks: parseFloat(gradeData.max_marks) || 100,
            feedback: gradeData.feedback || ''
          });
        }
      });
    });

    try {
      await apiClient.post('/teacher_interface/grades/bulk_create/', {
        grade_records: gradeRecords
      });
      toast.success('Grades saved successfully');
      fetchGradeStats();
    } catch (error) {
      console.error('Error saving grades:', error);
      toast.error(error.response?.data?.detail || 'Failed to save grades');
    }
  };

  const calculateTotalGrade = (studentId) => {
    const studentGrades = grades[studentId] || {};
    let totalMarks = 0;
    let totalMaxMarks = 0;

    Object.values(studentGrades).forEach(grade => {
      if (grade.marks !== undefined && grade.marks !== '') {
        totalMarks += parseFloat(grade.marks);
        totalMaxMarks += parseFloat(grade.max_marks) || 100;
      }
    });

    if (totalMaxMarks === 0) return '0%';
    return `${Math.round((totalMarks / totalMaxMarks) * 100)}%`;
  };

  const getGradeColor = (percentage) => {
    if (percentage >= 90) return 'text-success';
    if (percentage >= 80) return 'text-info';
    if (percentage >= 70) return 'text-warning';
    if (percentage >= 60) return 'text-primary';
    return 'text-danger';
  };

  const components = [
    { key: 'ASSIGNMENT', label: 'Assignment', maxMarks: 25 },
    { key: 'TEST', label: 'Test', maxMarks: 25 },
    { key: 'PROJECT', label: 'Project', maxMarks: 20 },
    { key: 'PARTICIPATION', label: 'Participation', maxMarks: 10 },
    { key: 'FINAL_EXAM', label: 'Final Exam', maxMarks: 20 }
  ];

  return (
    <div className="teacher-grading">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Grade Management</h2>
        <button 
          className="btn btn-primary"
          onClick={() => setShowCreatePeriod(true)}
          disabled={!selectedCourse}
        >
          <i className="fas fa-plus me-2"></i>Create Grading Period
        </button>
      </div>

      {/* Course and Period Selection */}
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
              <label className="form-label">Grading Period</label>
              <select
                className="form-select"
                value={selectedPeriod}
                onChange={(e) => setSelectedPeriod(e.target.value)}
                disabled={!selectedCourse}
              >
                <option value="">Choose grading period...</option>
                {gradingPeriods.map((period) => (
                  <option key={period.id} value={period.id}>
                    {period.name} ({period.weightage}%)
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Grade Statistics */}
      {selectedCourse && selectedPeriod && Object.keys(gradeStats).length > 0 && (
        <div className="card mb-4">
          <div className="card-body">
            <h6 className="card-title">Grade Statistics</h6>
            <div className="row">
              <div className="col-md-3">
                <div className="text-center">
                  <h4 className="text-success">{gradeStats.average || '0'}%</h4>
                  <small className="text-muted">Class Average</small>
                </div>
              </div>
              <div className="col-md-3">
                <div className="text-center">
                  <h4 className="text-info">{gradeStats.highest || '0'}%</h4>
                  <small className="text-muted">Highest Grade</small>
                </div>
              </div>
              <div className="col-md-3">
                <div className="text-center">
                  <h4 className="text-warning">{gradeStats.lowest || '0'}%</h4>
                  <small className="text-muted">Lowest Grade</small>
                </div>
              </div>
              <div className="col-md-3">
                <div className="text-center">
                  <h4 className="text-primary">{gradeStats.total_students || '0'}</h4>
                  <small className="text-muted">Total Students</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {selectedCourse && selectedPeriod && students.length > 0 && (
        <>
          {/* Save Button */}
          <div className="card mb-4">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <h6 className="mb-0">Grade Entry</h6>
                <button className="btn btn-primary" onClick={handleSubmitGrades}>
                  <i className="fas fa-save me-2"></i>Save All Grades
                </button>
              </div>
            </div>
          </div>

          {/* Grading Table */}
          <div className="card">
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
                        <th rowSpan="2">Student</th>
                        <th rowSpan="2">Roll No.</th>
                        {components.map(component => (
                          <th key={component.key} colSpan="2" className="text-center">
                            {component.label}
                            <br />
                            <small className="text-muted">(Max: {component.maxMarks})</small>
                          </th>
                        ))}
                        <th rowSpan="2">Total</th>
                      </tr>
                      <tr>
                        {components.map(component => (
                          <React.Fragment key={component.key}>
                            <th className="text-center">Marks</th>
                            <th className="text-center">Feedback</th>
                          </React.Fragment>
                        ))}
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
                              </div>
                            </div>
                          </td>
                          <td>{student.roll_number}</td>
                          {components.map(component => (
                            <React.Fragment key={component.key}>
                              <td>
                                <input
                                  type="number"
                                  className="form-control form-control-sm"
                                  min="0"
                                  max={component.maxMarks}
                                  step="0.5"
                                  value={grades[student.id]?.[component.key]?.marks || ''}
                                  onChange={(e) => handleGradeChange(student.id, component.key, 'marks', e.target.value)}
                                  onBlur={(e) => handleGradeChange(student.id, component.key, 'max_marks', component.maxMarks)}
                                />
                              </td>
                              <td>
                                <input
                                  type="text"
                                  className="form-control form-control-sm"
                                  placeholder="Feedback..."
                                  value={grades[student.id]?.[component.key]?.feedback || ''}
                                  onChange={(e) => handleGradeChange(student.id, component.key, 'feedback', e.target.value)}
                                />
                              </td>
                            </React.Fragment>
                          ))}
                          <td>
                            <span className={`badge fs-6 ${getGradeColor(parseInt(calculateTotalGrade(student.id)))}`}>
                              {calculateTotalGrade(student.id)}
                            </span>
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

      {/* Create Grading Period Modal */}
      {showCreatePeriod && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Create Grading Period</h5>
                <button type="button" className="btn-close" onClick={() => setShowCreatePeriod(false)}></button>
              </div>
              <form onSubmit={handleCreatePeriod}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label">Name</label>
                    <input
                      type="text"
                      className="form-control"
                      value={newPeriod.name}
                      onChange={(e) => setNewPeriod(prev => ({ ...prev, name: e.target.value }))}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Description</label>
                    <textarea
                      className="form-control"
                      rows="3"
                      value={newPeriod.description}
                      onChange={(e) => setNewPeriod(prev => ({ ...prev, description: e.target.value }))}
                    ></textarea>
                  </div>
                  <div className="row">
                    <div className="col-md-6">
                      <div className="mb-3">
                        <label className="form-label">Start Date</label>
                        <input
                          type="date"
                          className="form-control"
                          value={newPeriod.start_date}
                          onChange={(e) => setNewPeriod(prev => ({ ...prev, start_date: e.target.value }))}
                          required
                        />
                      </div>
                    </div>
                    <div className="col-md-6">
                      <div className="mb-3">
                        <label className="form-label">End Date</label>
                        <input
                          type="date"
                          className="form-control"
                          value={newPeriod.end_date}
                          onChange={(e) => setNewPeriod(prev => ({ ...prev, end_date: e.target.value }))}
                          required
                        />
                      </div>
                    </div>
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Weightage (%)</label>
                    <input
                      type="number"
                      className="form-control"
                      min="1"
                      max="100"
                      value={newPeriod.weightage}
                      onChange={(e) => setNewPeriod(prev => ({ ...prev, weightage: parseInt(e.target.value) }))}
                      required
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowCreatePeriod(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Create Period
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Empty States */}
      {!selectedCourse && (
        <div className="card">
          <div className="card-body text-center">
            <i className="fas fa-book fa-3x text-muted mb-3"></i>
            <h5>Select a Course</h5>
            <p className="text-muted">Please select a course to manage grades.</p>
          </div>
        </div>
      )}

      {selectedCourse && !selectedPeriod && (
        <div className="card">
          <div className="card-body text-center">
            <i className="fas fa-calendar fa-3x text-muted mb-3"></i>
            <h5>Select Grading Period</h5>
            <p className="text-muted">Please select a grading period to enter grades.</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeacherGrading;