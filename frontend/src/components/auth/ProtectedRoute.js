import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-vh-100 d-flex align-items-center justify-content-center">
        <div className="text-center">
          <div className="spinner-border text-primary mb-3" role="status" style={{ width: '3rem', height: '3rem' }}>
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="text-muted">Verifying authentication...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Check if user has required role
  if (allowedRoles && !allowedRoles.includes(user?.role)) {
    return (
      <div className="min-vh-100 d-flex align-items-center justify-content-center">
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-lg-6">
              <div className="card border-0 shadow-lg">
                <div className="card-body text-center p-5">
                  <div className="mb-4">
                    <i className="fas fa-exclamation-triangle fa-4x text-warning"></i>
                  </div>
                  <h3 className="h4 mb-3">Access Denied</h3>
                  <p className="text-muted mb-4">
                    You don't have permission to access this section. 
                    Your current role: <strong>{user?.role}</strong>
                  </p>
                  <div className="d-flex gap-3 justify-content-center">
                    <button 
                      onClick={() => window.history.back()} 
                      className="btn btn-secondary"
                    >
                      <i className="fas fa-arrow-left me-2"></i>
                      Go Back
                    </button>
                    <Navigate to={`/${user?.role}/dashboard`} replace />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return children;
};

export default ProtectedRoute;
