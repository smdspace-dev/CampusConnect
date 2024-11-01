import React, { useState, useEffect } from 'react';
import apiClient from '../../api/apiClient';
import { toast } from 'react-toastify';

const SettingsManagement = () => {
  const [settings, setSettings] = useState({
    institution_name: 'College Management System',
    institution_address: '',
    institution_phone: '',
    institution_email: '',
    academic_year: '2024-2025',
    semester_system: 'semester',
    grading_system: 'percentage',
    email_notifications: true,
    sms_notifications: false,
    auto_backup: true,
    backup_frequency: 'daily',
    max_login_attempts: 3,
    session_timeout: 30
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await apiClient.get('/admin_system/settings/');
      if (response.data) {
        setSettings(prev => ({ ...prev, ...response.data }));
      }
    } catch (error) {
      console.error('Error fetching settings:', error);
      // Use default settings if API fails
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await apiClient.post('/admin_system/settings/', settings);
      toast.success('Settings saved successfully');
    } catch (error) {
      console.error('Error saving settings:', error);
      toast.error('Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  const handleReset = () => {
    if (window.confirm('Are you sure you want to reset to default settings?')) {
      setSettings({
        institution_name: 'College Management System',
        institution_address: '',
        institution_phone: '',
        institution_email: '',
        academic_year: '2024-2025',
        semester_system: 'semester',
        grading_system: 'percentage',
        email_notifications: true,
        sms_notifications: false,
        auto_backup: true,
        backup_frequency: 'daily',
        max_login_attempts: 3,
        session_timeout: 30
      });
      toast.info('Settings reset to defaults');
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

  return (
    <div className="settings-management">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>System Settings</h2>
        <div>
          <button className="btn btn-outline-secondary me-2" onClick={handleReset}>
            <i className="fas fa-undo me-2"></i>Reset to Defaults
          </button>
          <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
            {saving ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                Saving...
              </>
            ) : (
              <>
                <i className="fas fa-save me-2"></i>Save Settings
              </>
            )}
          </button>
        </div>
      </div>

      <div className="row">
        {/* Institution Settings */}
        <div className="col-lg-6 mb-4">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">
                <i className="fas fa-building me-2"></i>Institution Information
              </h5>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <label className="form-label">Institution Name</label>
                <input
                  type="text"
                  className="form-control"
                  name="institution_name"
                  value={settings.institution_name}
                  onChange={handleInputChange}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Address</label>
                <textarea
                  className="form-control"
                  name="institution_address"
                  rows="3"
                  value={settings.institution_address}
                  onChange={handleInputChange}
                ></textarea>
              </div>
              <div className="mb-3">
                <label className="form-label">Phone Number</label>
                <input
                  type="tel"
                  className="form-control"
                  name="institution_phone"
                  value={settings.institution_phone}
                  onChange={handleInputChange}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Email</label>
                <input
                  type="email"
                  className="form-control"
                  name="institution_email"
                  value={settings.institution_email}
                  onChange={handleInputChange}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Academic Settings */}
        <div className="col-lg-6 mb-4">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">
                <i className="fas fa-graduation-cap me-2"></i>Academic Configuration
              </h5>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <label className="form-label">Academic Year</label>
                <input
                  type="text"
                  className="form-control"
                  name="academic_year"
                  value={settings.academic_year}
                  onChange={handleInputChange}
                  placeholder="2024-2025"
                />
              </div>
              <div className="mb-3">
                <label className="form-label">System Type</label>
                <select
                  className="form-select"
                  name="semester_system"
                  value={settings.semester_system}
                  onChange={handleInputChange}
                >
                  <option value="semester">Semester System</option>
                  <option value="annual">Annual System</option>
                  <option value="trimester">Trimester System</option>
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label">Grading System</label>
                <select
                  className="form-select"
                  name="grading_system"
                  value={settings.grading_system}
                  onChange={handleInputChange}
                >
                  <option value="percentage">Percentage</option>
                  <option value="gpa">GPA (4.0 Scale)</option>
                  <option value="letter">Letter Grades</option>
                  <option value="cgpa">CGPA (10.0 Scale)</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="col-lg-6 mb-4">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">
                <i className="fas fa-bell me-2"></i>Notification Settings
              </h5>
            </div>
            <div className="card-body">
              <div className="form-check mb-3">
                <input
                  className="form-check-input"
                  type="checkbox"
                  name="email_notifications"
                  checked={settings.email_notifications}
                  onChange={handleInputChange}
                />
                <label className="form-check-label">
                  Enable Email Notifications
                </label>
              </div>
              <div className="form-check mb-3">
                <input
                  className="form-check-input"
                  type="checkbox"
                  name="sms_notifications"
                  checked={settings.sms_notifications}
                  onChange={handleInputChange}
                />
                <label className="form-check-label">
                  Enable SMS Notifications
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Security & Backup Settings */}
        <div className="col-lg-6 mb-4">
          <div className="card">
            <div className="card-header">
              <h5 className="card-title mb-0">
                <i className="fas fa-shield-alt me-2"></i>Security & Backup
              </h5>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <label className="form-label">Max Login Attempts</label>
                <input
                  type="number"
                  className="form-control"
                  name="max_login_attempts"
                  min="1"
                  max="10"
                  value={settings.max_login_attempts}
                  onChange={handleInputChange}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Session Timeout (minutes)</label>
                <input
                  type="number"
                  className="form-control"
                  name="session_timeout"
                  min="5"
                  max="120"
                  value={settings.session_timeout}
                  onChange={handleInputChange}
                />
              </div>
              <div className="form-check mb-3">
                <input
                  className="form-check-input"
                  type="checkbox"
                  name="auto_backup"
                  checked={settings.auto_backup}
                  onChange={handleInputChange}
                />
                <label className="form-check-label">
                  Enable Automatic Backup
                </label>
              </div>
              {settings.auto_backup && (
                <div className="mb-3">
                  <label className="form-label">Backup Frequency</label>
                  <select
                    className="form-select"
                    name="backup_frequency"
                    value={settings.backup_frequency}
                    onChange={handleInputChange}
                  >
                    <option value="hourly">Hourly</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                  </select>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* System Information */}
      <div className="card">
        <div className="card-header">
          <h5 className="card-title mb-0">
            <i className="fas fa-info-circle me-2"></i>System Information
          </h5>
        </div>
        <div className="card-body">
          <div className="row">
            <div className="col-md-3">
              <strong>System Version:</strong>
              <p className="text-muted">v1.0.0</p>
            </div>
            <div className="col-md-3">
              <strong>Database:</strong>
              <p className="text-muted">SQLite 3</p>
            </div>
            <div className="col-md-3">
              <strong>Last Backup:</strong>
              <p className="text-muted">{new Date().toLocaleDateString()}</p>
            </div>
            <div className="col-md-3">
              <strong>System Status:</strong>
              <p className="text-success">
                <i className="fas fa-circle me-1"></i>Operational
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsManagement;