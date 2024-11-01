import React, { useState, useEffect } from 'react';
import apiClient from '../../api/apiClient';
import { toast } from 'react-toastify';

const StudentAssignments = () => {
  const [assignments, setAssignments] = useState([]);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('pending');
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [showSubmissionModal, setShowSubmissionModal] = useState(false);
  const [submissionData, setSubmissionData] = useState({
    content: '',
    attachment: null
  });

  useEffect(() => {
    fetchAssignments();
    fetchSubmissions();
  }, []);

  const fetchAssignments = async () => {
    try {
      const response = await apiClient.get('/student_interface/assignments/');
      setAssignments(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching assignments:', error);
      toast.error('Failed to fetch assignments');
    } finally {
      setLoading(false);
    }
  };

  const fetchSubmissions = async () => {
    try {
      const response = await apiClient.get('/student_interface/submissions/');
      setSubmissions(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching submissions:', error);
    }
  };

  const handleSubmissionUpload = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('assignment', selectedAssignment.id);
    formData.append('content', submissionData.content);
    if (submissionData.attachment) {
      formData.append('attachment', submissionData.attachment);
    }

    try {
      await apiClient.post('/student_interface/submissions/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      toast.success('Assignment submitted successfully');
      setShowSubmissionModal(false);
      resetSubmissionForm();
      fetchAssignments();
      fetchSubmissions();
    } catch (error) {
      console.error('Error submitting assignment:', error);
      toast.error(error.response?.data?.detail || 'Failed to submit assignment');
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSubmissionData(prev => ({
      ...prev,
      attachment: file
    }));
  };

  const resetSubmissionForm = () => {
    setSubmissionData({
      content: '',
      attachment: null
    });
    setSelectedAssignment(null);
  };

  const openSubmissionModal = (assignment) => {
    setSelectedAssignment(assignment);
    setShowSubmissionModal(true);
  };

  const getAssignmentStatus = (assignment) => {
    const submission = submissions.find(sub => sub.assignment.id === assignment.id);
    if (!submission) return 'NOT_SUBMITTED';
    return submission.status;
  };

  const getSubmissionForAssignment = (assignment) => {
    return submissions.find(sub => sub.assignment.id === assignment.id);
  };

  const getDaysUntilDue = (dueDate) => {
    const due = new Date(dueDate);
    const now = new Date();
    const diffTime = due - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'NOT_SUBMITTED': { class: 'bg-warning', text: 'Not Submitted' },
      'SUBMITTED': { class: 'bg-info', text: 'Submitted' },
      'GRADED': { class: 'bg-success', text: 'Graded' },
      'LATE': { class: 'bg-danger', text: 'Late Submission' }
    };
    const config = statusConfig[status] || statusConfig['NOT_SUBMITTED'];
    return <span className={`badge ${config.class}`}>{config.text}</span>;
  };

  const filterAssignments = () => {
    switch (activeTab) {
      case 'pending':
        return assignments.filter(assignment => {
          const status = getAssignmentStatus(assignment);
          return status === 'NOT_SUBMITTED' && new Date(assignment.due_date) > new Date();
        });
      case 'submitted':
        return assignments.filter(assignment => {
          const status = getAssignmentStatus(assignment);
          return ['SUBMITTED', 'GRADED', 'LATE'].includes(status);
        });
      case 'overdue':
        return assignments.filter(assignment => {
          const status = getAssignmentStatus(assignment);
          return status === 'NOT_SUBMITTED' && new Date(assignment.due_date) < new Date();
        });
      default:
        return assignments;
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

  const filteredAssignments = filterAssignments();

  return (
    <div className="student-assignments">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>My Assignments</h2>
        <div className="d-flex align-items-center">
          <span className="text-muted me-3">
            Total: {assignments.length} assignments
          </span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'pending' ? 'active' : ''}`}
            onClick={() => setActiveTab('pending')}
          >
            <i className="fas fa-clock me-2"></i>
            Pending 
            <span className="badge bg-warning ms-2">
              {assignments.filter(a => getAssignmentStatus(a) === 'NOT_SUBMITTED' && new Date(a.due_date) > new Date()).length}
            </span>
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'submitted' ? 'active' : ''}`}
            onClick={() => setActiveTab('submitted')}
          >
            <i className="fas fa-check-circle me-2"></i>
            Submitted
            <span className="badge bg-success ms-2">
              {assignments.filter(a => ['SUBMITTED', 'GRADED', 'LATE'].includes(getAssignmentStatus(a))).length}
            </span>
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'overdue' ? 'active' : ''}`}
            onClick={() => setActiveTab('overdue')}
          >
            <i className="fas fa-exclamation-triangle me-2"></i>
            Overdue
            <span className="badge bg-danger ms-2">
              {assignments.filter(a => getAssignmentStatus(a) === 'NOT_SUBMITTED' && new Date(a.due_date) < new Date()).length}
            </span>
          </button>
        </li>
      </ul>

      {/* Assignment List */}
      <div className="row">
        {filteredAssignments.length === 0 ? (
          <div className="col-12">
            <div className="card">
              <div className="card-body text-center py-5">
                <i className="fas fa-tasks fa-3x text-muted mb-3"></i>
                <h5>No {activeTab} assignments</h5>
                <p className="text-muted">
                  {activeTab === 'pending' && 'You\'re all caught up! No pending assignments.'}
                  {activeTab === 'submitted' && 'You haven\'t submitted any assignments yet.'}
                  {activeTab === 'overdue' && 'Great! No overdue assignments.'}
                </p>
              </div>
            </div>
          </div>
        ) : (
          filteredAssignments.map((assignment) => {
            const status = getAssignmentStatus(assignment);
            const submission = getSubmissionForAssignment(assignment);
            const daysUntilDue = getDaysUntilDue(assignment.due_date);
            
            return (
              <div key={assignment.id} className="col-lg-6 col-xl-4 mb-4">
                <div className="card h-100 shadow-sm">
                  <div className="card-header d-flex justify-content-between align-items-center">
                    <h6 className="card-title mb-0">{assignment.course_assignment?.course?.code}</h6>
                    {getStatusBadge(status)}
                  </div>
                  <div className="card-body">
                    <h5 className="card-title">{assignment.title}</h5>
                    <p className="text-muted mb-3">{assignment.description}</p>
                    
                    <div className="mb-3">
                      <div className="row">
                        <div className="col-6">
                          <small className="text-muted">Due Date:</small>
                          <div>
                            <i className="fas fa-calendar me-1"></i>
                            {new Date(assignment.due_date).toLocaleDateString()}
                          </div>
                          <div>
                            <i className="fas fa-clock me-1"></i>
                            {new Date(assignment.due_date).toLocaleTimeString()}
                          </div>
                        </div>
                        <div className="col-6">
                          <small className="text-muted">Max Marks:</small>
                          <div>
                            <i className="fas fa-trophy me-1"></i>
                            {assignment.max_marks} points
                          </div>
                          {submission?.grade && (
                            <div className="mt-1">
                              <span className="badge bg-success">
                                Grade: {submission.grade}/{assignment.max_marks}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {daysUntilDue <= 3 && daysUntilDue > 0 && status === 'NOT_SUBMITTED' && (
                      <div className="alert alert-warning py-2 mb-3">
                        <i className="fas fa-exclamation-triangle me-2"></i>
                        Due in {daysUntilDue} day{daysUntilDue !== 1 ? 's' : ''}
                      </div>
                    )}

                    {daysUntilDue < 0 && status === 'NOT_SUBMITTED' && (
                      <div className="alert alert-danger py-2 mb-3">
                        <i className="fas fa-exclamation-circle me-2"></i>
                        Overdue by {Math.abs(daysUntilDue)} day{Math.abs(daysUntilDue) !== 1 ? 's' : ''}
                      </div>
                    )}

                    {submission && (
                      <div className="mb-3">
                        <small className="text-muted">Submitted:</small>
                        <div>{new Date(submission.submitted_at).toLocaleString()}</div>
                        {submission.feedback && (
                          <div className="mt-2">
                            <small className="text-muted">Feedback:</small>
                            <div className="bg-light p-2 rounded">
                              {submission.feedback}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {assignment.instructions && (
                      <div className="mb-3">
                        <small className="text-muted">Instructions:</small>
                        <div className="bg-light p-2 rounded">
                          {assignment.instructions}
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="card-footer bg-transparent">
                    {status === 'NOT_SUBMITTED' ? (
                      <button 
                        className="btn btn-primary w-100"
                        onClick={() => openSubmissionModal(assignment)}
                      >
                        <i className="fas fa-upload me-2"></i>Submit Assignment
                      </button>
                    ) : (
                      <div className="d-flex gap-2">
                        <button className="btn btn-outline-primary flex-fill" disabled>
                          <i className="fas fa-check me-2"></i>Submitted
                        </button>
                        {submission?.attachment_url && (
                          <a 
                            href={submission.attachment_url} 
                            className="btn btn-outline-info"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            <i className="fas fa-download"></i>
                          </a>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Submission Modal */}
      {showSubmissionModal && selectedAssignment && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-lg">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  Submit Assignment: {selectedAssignment.title}
                </h5>
                <button 
                  type="button" 
                  className="btn-close" 
                  onClick={() => setShowSubmissionModal(false)}
                ></button>
              </div>
              <form onSubmit={handleSubmissionUpload}>
                <div className="modal-body">
                  <div className="mb-3">
                    <h6>Assignment Details</h6>
                    <div className="bg-light p-3 rounded">
                      <p><strong>Course:</strong> {selectedAssignment.course_assignment?.course?.name}</p>
                      <p><strong>Due Date:</strong> {new Date(selectedAssignment.due_date).toLocaleString()}</p>
                      <p><strong>Max Marks:</strong> {selectedAssignment.max_marks}</p>
                      <p className="mb-0"><strong>Description:</strong> {selectedAssignment.description}</p>
                    </div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Submission Content</label>
                    <textarea
                      className="form-control"
                      rows="5"
                      value={submissionData.content}
                      onChange={(e) => setSubmissionData(prev => ({ ...prev, content: e.target.value }))}
                      placeholder="Enter your assignment content or explanation here..."
                      required
                    ></textarea>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Attachment (Optional)</label>
                    <input
                      type="file"
                      className="form-control"
                      onChange={handleFileChange}
                      accept=".pdf,.doc,.docx,.txt,.zip"
                    />
                    <div className="form-text">
                      Supported formats: PDF, DOC, DOCX, TXT, ZIP (Max 10MB)
                    </div>
                  </div>
                </div>
                <div className="modal-footer">
                  <button 
                    type="button" 
                    className="btn btn-secondary" 
                    onClick={() => setShowSubmissionModal(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    <i className="fas fa-upload me-2"></i>Submit Assignment
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentAssignments;