import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const DashboardLayout = ({ children, role, menuItems }) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const getRoleColor = (role) => {
    const colors = {
      admin: 'danger',
      teacher: 'success',
      student: 'primary',
      resource_person: 'warning'
    };
    return colors[role] || 'secondary';
  };

  const getRoleIcon = (role) => {
    const icons = {
      admin: 'fa-user-shield',
      teacher: 'fa-chalkboard-teacher',
      student: 'fa-user-graduate',
      resource_person: 'fa-users-cog'
    };
    return icons[role] || 'fa-user';
  };

  const isActiveRoute = (path) => {
    return location.pathname === path || location.pathname.startsWith(path);
  };

  return (
    <div className="dashboard-layout d-flex">
      {/* Sidebar */}
      <div className={`sidebar bg-dark text-white ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
        <div className="sidebar-header p-3 border-bottom border-secondary">
          <div className="d-flex align-items-center">
            <div className={`sidebar-brand ${sidebarCollapsed ? 'd-none' : ''}`}>
              <h5 className="mb-0">
                <i className="fas fa-graduation-cap me-2 text-primary"></i>
                Campus Connect
              </h5>
            </div>
          </div>
        </div>

        <div className="sidebar-content flex-grow-1 p-0">
          {/* User Info */}
          <div className="user-info p-3 border-bottom border-secondary">
            <div className="d-flex align-items-center">
              <div className={`avatar bg-${getRoleColor(role)} rounded-circle d-flex align-items-center justify-content-center me-3`} 
                   style={{ width: '40px', height: '40px' }}>
                <i className={`fas ${getRoleIcon(role)}`}></i>
              </div>
              {!sidebarCollapsed && (
                <div className="user-details flex-grow-1">
                  <div className="fw-bold">{user?.first_name || user?.username}</div>
                  <small className={`text-${getRoleColor(role)}`}>
                    {role.charAt(0).toUpperCase() + role.slice(1).replace('_', ' ')}
                  </small>
                </div>
              )}
            </div>
          </div>

          {/* Navigation Menu */}
          <nav className="sidebar-nav">
            <ul className="nav flex-column">
              {menuItems.map((item, index) => (
                <li key={index} className="nav-item">
                  {item.submenu ? (
                    <div className="nav-submenu">
                      <div className="nav-link text-muted px-3 py-2">
                        <i className={`${item.icon} me-3`}></i>
                        {!sidebarCollapsed && item.label}
                      </div>
                      <ul className="nav flex-column ms-3">
                        {item.submenu.map((subitem, subindex) => (
                          <li key={subindex} className="nav-item">
                            <Link
                              to={subitem.path}
                              className={`nav-link px-3 py-2 ${isActiveRoute(subitem.path) ? 'active bg-primary' : ''}`}
                            >
                              <i className={`${subitem.icon} me-3`}></i>
                              {!sidebarCollapsed && subitem.label}
                            </Link>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : (
                    <Link
                      to={item.path}
                      className={`nav-link px-3 py-3 ${isActiveRoute(item.path) ? 'active bg-primary' : ''}`}
                    >
                      <i className={`${item.icon} me-3`}></i>
                      {!sidebarCollapsed && item.label}
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </nav>
        </div>

        {/* Sidebar Footer */}
        <div className="sidebar-footer p-3 border-top border-secondary">
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="btn btn-outline-light btn-sm w-100 mb-2"
          >
            <i className={`fas ${sidebarCollapsed ? 'fa-expand' : 'fa-compress'}`}></i>
            {!sidebarCollapsed && <span className="ms-2">Collapse</span>}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content flex-grow-1">
        {/* Top Header */}
        <header className="main-header bg-white border-bottom px-4 py-3">
          <div className="d-flex justify-content-between align-items-center">
            <div className="header-left">
              <button
                className="btn btn-outline-secondary btn-sm me-3 d-lg-none"
                onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              >
                <i className="fas fa-bars"></i>
              </button>
              <h4 className="mb-0 text-dark">
                {role.charAt(0).toUpperCase() + role.slice(1).replace('_', ' ')} Dashboard
              </h4>
            </div>
            
            <div className="header-right d-flex align-items-center">
              {/* Notifications */}
              <div className="dropdown me-3">
                <button className="btn btn-outline-secondary position-relative">
                  <i className="fas fa-bell"></i>
                  <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                    3
                  </span>
                </button>
              </div>

              {/* User Dropdown */}
              <div className="dropdown">
                <button
                  className="btn btn-outline-secondary dropdown-toggle"
                  onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                >
                  <i className={`fas ${getRoleIcon(role)} me-2`}></i>
                  {user?.first_name || user?.username}
                </button>
                {userDropdownOpen && (
                  <div className="dropdown-menu dropdown-menu-end show">
                    <Link className="dropdown-item" to={`/${role}/profile`}>
                      <i className="fas fa-user me-2"></i>
                      Profile
                    </Link>
                    <Link className="dropdown-item" to={`/${role}/settings`}>
                      <i className="fas fa-cog me-2"></i>
                      Settings
                    </Link>
                    <div className="dropdown-divider"></div>
                    <button className="dropdown-item" onClick={handleLogout}>
                      <i className="fas fa-sign-out-alt me-2"></i>
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="page-content p-4">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
