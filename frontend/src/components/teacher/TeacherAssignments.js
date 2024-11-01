import React, { useState, useEffect } from 'react';
import apiClient from '../../api/apiClient';
import { toast } from 'react-toastify';

const TeacherAssignments = () => {
  const [assignments, setAssignments] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    course_assignment: '',
    due_date: '',
    max_marks: 100,
    instructions: ''
  });

  useEffect(() => {
    fetchAssignments();
    fetchCourses();
  }, []);

  const fetchAssignments = async () => {
    try {
      const response = await apiClient.get('/teacher_interface/assignments/');
      setAssignments(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching assignments:', error);
      toast.error('Failed to fetch assignments');
    } finally {
      setLoading(false);
    }
  };

  const fetchCourses = async () => {
    try {
      const response = await apiClient.get('/teacher_interface/course-assignments/');
      setCourses(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const fetchSubmissions = async (assignmentId) => {
    try {
      const response = await apiClient.get(`/teacher_interface/assignments/${assignmentId}/submissions/`);
      setSubmissions(response.data.data || response.data);
    } catch (error) {
      console.error('Error fetching submissions:', error);
      toast.error('Failed to fetch submissions');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedAssignment) {
        await apiClient.put(`/teacher_interface/assignments/${selectedAssignment.id}/`, formData);
        toast.success('Assignment updated successfully');
      } else {
        await apiClient.post('/teacher_interface/assignments/', formData);
        toast.success('Assignment created successfully');
      }
      setShowModal(false);
      resetForm();
      fetchAssignments();
    } catch (error) {
      console.error('Error saving assignment:', error);
      toast.error(error.response?.data?.detail || 'Failed to save assignment');
    }
  };

  const handleEdit = (assignment) => {
    setSelectedAssignment(assignment);
    setFormData({
      title: assignment.title || '',
      description: assignment.description || '',
      course_assignment: assignment.course_assignment?.id || '',
      due_date: assignment.due_date || '',
      max_marks: assignment.max_marks || 100,
      instructions: assignment.instructions || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (assignmentId) => {
    if (window.confirm('Are you sure you want to delete this assignment?')) {
      try {
        await apiClient.delete(`/teacher_interface/assignments/${assignmentId}/`);
        toast.success('Assignment deleted successfully');
        fetchAssignments();
      } catch (error) {
        console.error('Error deleting assignment:', error);
        toast.error('Failed to delete assignment');
      }
    }
  };

  const handleViewSubmissions = (assignment) => {
    setSelectedAssignment(assignment);
    fetchSubmissions(assignment.id);
  };

  const handleGradeSubmission = async (submissionId, grade, feedback) => {
    try {
      await apiClient.post(`/teacher_interface/assignments/${selectedAssignment.id}/grade_submission/`, {
        submission_id: submissionId,
        grade: grade,
        feedback: feedback
      });
      toast.success('Submission graded successfully');
      fetchSubmissions(selectedAssignment.id);
    } catch (error) {
      console.error('Error grading submission:', error);
      toast.error('Failed to grade submission');
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      course_assignment: '',
      due_date: '',
      max_marks: 100,
      instructions: ''
    });
    setSelectedAssignment(null);
  };

  const handleAddNew = () => {
    resetForm();
    setShowModal(true);
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
    <div className="teacher-assignments">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Assignments</h2>
        <button className="btn btn-primary" onClick={handleAddNew}>
          <i className="fas fa-plus me-2"></i>Create Assignment
        </button>
      </div>

      <div className="card">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Course</th>
                  <th>Due Date</th>
                  <th>Max Marks</th>
                  <th>Submissions</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {assignments.map((assignment) => (
                  <tr key={assignment.id}>
                    <td><strong>{assignment.title}</strong></td>
                    <td>{assignment.course_assignment?.course?.name}</td>
                    <td>{new Date(assignment.due_date).toLocaleDateString()}</td>
                    <td>{assignment.max_marks}</td>
                    <td>
                      <button 
                        className="btn btn-sm btn-outline-info"
                        onClick={() => handleViewSubmissions(assignment)}
                      >
                        View Submissions
                      </button>
                    </td>
                    <td>
                      <button 
                        className="btn btn-sm btn-outline-primary me-2"
                        onClick={() => handleEdit(assignment)}
                      >
                        <i className="fas fa-edit"></i>
                      </button>
                      <button 
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => handleDelete(assignment.id)}
                      >
                        <i className="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Assignment Modal */}
      {showModal && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-lg">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  {selectedAssignment ? 'Edit Assignment' : 'Create New Assignment'}
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label">Title</label>
                    <input
                      type="text"
                      className="form-control"
                      name="title"
                      value={formData.title}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Course</label>
                    <select
                      className="form-select"
                      name="course_assignment"
                      value={formData.course_assignment}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select Course</option>
                      {courses.map((course) => (
                        <option key={course.id} value={course.id}>
                          {course.course?.name} ({course.course?.code})
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="row">
                    <div className="col-md-6">
                      <div className="mb-3">
                        <label className="form-label">Due Date</label>
                        <input
                          type="datetime-local"
                          className="form-control"
                          name="due_date"
                          value={formData.due_date}
                          onChange={handleInputChange}
                          required
                        />
                      </div>
                    </div>
                    <div className="col-md-6">
                      <div className="mb-3">
                        <label className="form-label">Max Marks</label>
                        <input
                          type="number"
                          className="form-control"
                          name="max_marks"
                          min="1"
                          value={formData.max_marks}
                          onChange={handleInputChange}
                          required
                        />
                      </div>
                    </div>
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Description</label>
                    <textarea
                      className="form-control"
                      name="description"
                      rows="3"
                      value={formData.description}
                      onChange={handleInputChange}
                      required
                    ></textarea>
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Instructions</label>
                    <textarea
                      className="form-control"
                      name="instructions"
                      rows="4"
                      value={formData.instructions}
                      onChange={handleInputChange}
                    ></textarea>
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {selectedAssignment ? 'Update Assignment' : 'Create Assignment'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Submissions Modal */}
      {selectedAssignment && submissions.length > 0 && (
        <div className="mt-4 card">
          <div className="card-header">
            <h5 className="card-title mb-0">
              Submissions for: {selectedAssignment.title}
            </h5>
          </div>
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Student</th>
                    <th>Roll No.</th>
                    <th>Submitted At</th>
                    <th>Status</th>
                    <th>Grade</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {submissions.map((submission) => (
                    <tr key={submission.id}>
                      <td>{submission.student_name}</td>
                      <td>{submission.student_roll}</td>
                      <td>{new Date(submission.submitted_at).toLocaleString()}</td>
                      <td>
                        <span className={`badge ${
                          submission.status === 'GRADED' ? 'bg-success' :
                          submission.status === 'SUBMITTED' ? 'bg-warning' : 'bg-secondary'
                        }`}>
                          {submission.status}
                        </span>
                      </td>
                      <td>{submission.grade || 'Not Graded'}</td>
                      <td>
                        <button 
                          className="btn btn-sm btn-outline-primary"
                          onClick={() => {
                            const grade = prompt('Enter grade:');
                            const feedback = prompt('Enter feedback:');
                            if (grade !== null) {
                              handleGradeSubmission(submission.id, grade, feedback);
                            }
                          }}
                        >
                          Grade
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeacherAssignments;