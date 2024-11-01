import React, { useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const LoginPage = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loginAs, setLoginAs] = useState('student');
  
  const { login, loading, isAuthenticated, user } = useAuth();
  const navigate = useNavigate();

  // Redirect if already authenticated
  if (isAuthenticated) {
    const role = user?.role || 'student';
    switch (role) {
      case 'admin':
        return <Navigate to="/admin/dashboard" replace />;
      case 'teacher':
        return <Navigate to="/teacher/dashboard" replace />;
      case 'resource_person':
        return <Navigate to="/resource-person/dashboard" replace />;
      default:
        return <Navigate to="/student/dashboard" replace />;
    }
  }

  const handleInputChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await login(credentials);
    
    if (result.success) {
      const role = result.user.role;
      switch (role) {
        case 'admin':
          navigate('/admin/dashboard');
          break;
        case 'teacher':
          navigate('/teacher/dashboard');
          break;
        case 'resource_person':
          navigate('/resource-person/dashboard');
          break;
        default:
          navigate('/student/dashboard');
      }
    }
  };

  // Demo credentials for different roles
  const demoCredentials = {
    admin: { username: 'admin', password: 'admin123' },
    teacher: { username: 'teacher_demo', password: 'teacher123' },
    student: { username: 'student_demo', password: 'student123' },
    resource_person: { username: 'resource_demo', password: 'resource123' }
  };

  const fillDemoCredentials = (role) => {
    setCredentials(demoCredentials[role]);
    setLoginAs(role);
  };

  return (
    <div className="login-page min-vh-100 d-flex align-items-center bg-light">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-10 col-xl-8">
            <div className="row shadow-lg rounded-3 overflow-hidden bg-white">
              {/* Left Side - Form */}
              <div className="col-md-6 p-5">
                <div className="login-form">
                  {/* Header */}
                  <div className="mb-4">
                    <Link to="/" className="text-decoration-none">
                      <h4 className="text-primary fw-bold">
                        <i className="fas fa-graduation-cap me-2"></i>
                        Campus Connect
                      </h4>
                    </Link>
                    <h2 className="h3 mt-3 mb-2">Welcome Back!</h2>
                    <p className="text-muted">Sign in to your account</p>
                  </div>

                  {/* Demo Login Buttons */}
                  <div className="demo-section mb-4">
                    <p className="small text-muted mb-2">Quick Demo Access:</p>
                    <div className="row g-2">
                      <div className="col-6">
                        <button
                          type="button"
                          className="btn btn-outline-danger btn-sm w-100"
                          onClick={() => fillDemoCredentials('admin')}
                        >
                          <i className="fas fa-user-shield me-1"></i>
                          Admin
                        </button>
                      </div>
                      <div className="col-6">
                        <button
                          type="button"
                          className="btn btn-outline-success btn-sm w-100"
                          onClick={() => fillDemoCredentials('teacher')}
                        >
                          <i className="fas fa-chalkboard-teacher me-1"></i>
                          Teacher
                        </button>
                      </div>
                      <div className="col-6">
                        <button
                          type="button"
                          className="btn btn-outline-primary btn-sm w-100"
                          onClick={() => fillDemoCredentials('student')}
                        >
                          <i className="fas fa-user-graduate me-1"></i>
                          Student
                        </button>
                      </div>
                      <div className="col-6">
                        <button
                          type="button"
                          className="btn btn-outline-warning btn-sm w-100"
                          onClick={() => fillDemoCredentials('resource_person')}
                        >
                          <i className="fas fa-users-cog me-1"></i>
                          Resource
                        </button>
                      </div>
                    </div>
                    <hr className="my-4" />
                  </div>

                  {/* Login Form */}
                  <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                      <label htmlFor="username" className="form-label">
                        Username or Email
                      </label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <i className="fas fa-user"></i>
                        </span>
                        <input
                          type="text"
                          className="form-control"
                          id="username"
                          name="username"
                          value={credentials.username}
                          onChange={handleInputChange}
                          placeholder="Enter username or email"
                          autoComplete="username"
                          required
                        />
                      </div>
                    </div>

                    <div className="mb-3">
                      <label htmlFor="password" className="form-label">
                        Password
                      </label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <i className="fas fa-lock"></i>
                        </span>
                        <input
                          type={showPassword ? 'text' : 'password'}
                          className="form-control"
                          id="password"
                          name="password"
                          value={credentials.password}
                          onChange={handleInputChange}
                          placeholder="Enter password"
                          autoComplete="current-password"
                          required
                        />
                        <button
                          type="button"
                          className="btn btn-outline-secondary"
                          onClick={() => setShowPassword(!showPassword)}
                        >
                          <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`}></i>
                        </button>
                      </div>
                    </div>

                    <div className="mb-3 d-flex justify-content-between align-items-center">
                      <div className="form-check">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id="rememberMe"
                        />
                        <label className="form-check-label" htmlFor="rememberMe">
                          Remember me
                        </label>
                      </div>
                      <Link to="/forgot-password" className="text-decoration-none small">
                        Forgot password?
                      </Link>
                    </div>

                    <button
                      type="submit"
                      className="btn btn-primary w-100 py-2 mb-3"
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-2" role="status">
                            <span className="visually-hidden">Loading...</span>
                          </span>
                          Signing in...
                        </>
                      ) : (
                        <>
                          <i className="fas fa-sign-in-alt me-2"></i>
                          Sign In
                        </>
                      )}
                    </button>

                    <div className="text-center">
                      <Link to="/" className="text-decoration-none">
                        <i className="fas fa-arrow-left me-2"></i>
                        Back to Home
                      </Link>
                    </div>
                  </form>
                </div>
              </div>

              {/* Right Side - Info */}
              <div className="col-md-6 bg-gradient-primary text-white p-5 d-flex align-items-center">
                <div className="info-content">
                  <h3 className="h2 mb-4">Access Your Portal</h3>
                  <div className="feature-list">
                    <div className="feature-item mb-3">
                      <i className="fas fa-check-circle me-3 text-warning"></i>
                      <span>Role-based dashboard access</span>
                    </div>
                    <div className="feature-item mb-3">
                      <i className="fas fa-check-circle me-3 text-warning"></i>
                      <span>Secure authentication system</span>
                    </div>
                    <div className="feature-item mb-3">
                      <i className="fas fa-check-circle me-3 text-warning"></i>
                      <span>Real-time data synchronization</span>
                    </div>
                    <div className="feature-item mb-3">
                      <i className="fas fa-check-circle me-3 text-warning"></i>
                      <span>Mobile-responsive design</span>
                    </div>
                  </div>
                  
                  <div className="mt-5 p-3 bg-white bg-opacity-10 rounded">
                    <p className="mb-2 small">
                      <i className="fas fa-info-circle me-2"></i>
                      Demo Access Available
                    </p>
                    <p className="small mb-0 opacity-75">
                      Use the demo buttons above to quickly access different user roles 
                      and explore the system capabilities.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
