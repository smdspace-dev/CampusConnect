import React, { useEffect, useState } from 'react';
import api from '../../api/apiClient';
import { toast } from 'react-toastify';

export default function StaffManagement() {
  const [staff, setStaff] = useState([]);

  useEffect(()=> {
    load();
  }, []);

  const load = async () => {
    try {
      const res = await api.get('admin_system/staff/');
      setStaff(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const toggle = async (id) => {
    try {
      await api.post(`admin_system/staff/${id}/toggle_access/`);
      toast.success('Toggled');
      load();
    } catch (e) {
      toast.error('Error toggling');
    }
  };

  const reset = async (id) => {
    try {
      const res = await api.post(`admin_system/staff/${id}/reset_password/`);
      toast.success('Password reset token generated');
      console.log(res.data);
    } catch (e) {
      toast.error('Error resetting');
    }
  };

  return (
    <div>
      <h3>Staff Management</h3>
      <ul className="list-group">
        {staff.map(s=>(
          <li key={s.id} className="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <strong>{s.user?.username}</strong>
              <div className="text-muted">{s.role}</div>
            </div>
            <div>
              <button className="btn btn-sm btn-outline-secondary me-2" onClick={()=>toggle(s.id)}>Toggle Access</button>
              <button className="btn btn-sm btn-outline-danger" onClick={()=>reset(s.id)}>Reset Password</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
