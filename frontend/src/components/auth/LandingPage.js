import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-primary text-white py-5">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-6">
              <h1 className="display-4 fw-bold mb-4">Welcome to Campus Connect</h1>
              <p className="lead mb-4">
                A comprehensive college management system designed to streamline academic operations,
                enhance student engagement, and empower educational institutions.
              </p>
              <Link to="/login" className="btn btn-warning btn-lg me-3">
                <i className="fas fa-sign-in-alt me-2"></i>Login Now
              </Link>
            </div>
            <div className="col-lg-6 text-center">
              <i className="fas fa-graduation-cap fa-5x mb-3"></i>
              <h4>Modern Education Management</h4>
            </div>
          </div>
        </div>
      </section>

      {/* Demo Login Options */}
      <section className="py-5 bg-light">
        <div className="container">
          <div className="row">
            <div className="col-12 text-center mb-5">
              <h2 className="fw-bold mb-3">Try Our Demo</h2>
              <p className="text-muted">Experience different user perspectives</p>
            </div>
          </div>
          <div className="row g-4">
            <div className="col-lg-3 col-md-6">
              <div className="card text-center h-100">
                <div className="card-body">
                  <i className="fas fa-user-shield fa-3x text-danger mb-3"></i>
                  <h5>Admin Login</h5>
                  <p className="small text-muted">admin@college.edu / admin123</p>
                  <Link to="/login" className="btn btn-danger">Try Admin</Link>
                </div>
              </div>
            </div>
            <div className="col-lg-3 col-md-6">
              <div className="card text-center h-100">
                <div className="card-body">
                  <i className="fas fa-chalkboard-teacher fa-3x text-success mb-3"></i>
                  <h5>Teacher Login</h5>
                  <p className="small text-muted">teacher@college.edu / teacher123</p>
                  <Link to="/login" className="btn btn-success">Try Teacher</Link>
                </div>
              </div>
            </div>
            <div className="col-lg-3 col-md-6">
              <div className="card text-center h-100">
                <div className="card-body">
                  <i className="fas fa-user-graduate fa-3x text-primary mb-3"></i>
                  <h5>Student Login</h5>
                  <p className="small text-muted">student@college.edu / student123</p>
                  <Link to="/login" className="btn btn-primary">Try Student</Link>
                </div>
              </div>
            </div>
            <div className="col-lg-3 col-md-6">
              <div className="card text-center h-100">
                <div className="card-body">
                  <i className="fas fa-users-cog fa-3x text-warning mb-3"></i>
                  <h5>Resource Login</h5>
                  <p className="small text-muted">resource@college.edu / resource123</p>
                  <Link to="/login" className="btn btn-warning">Try Resource</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
