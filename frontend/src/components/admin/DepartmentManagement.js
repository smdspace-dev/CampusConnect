import React, { useEffect, useState } from 'react';
import api from '../../api/apiClient';
import { toast } from 'react-toastify';

export default function DepartmentManagement() {
  const [departments, setDepartments] = useState([]);
  const [name, setName] = useState('');

  useEffect(()=> {
    load();
  }, []);

  const load = async () => {
    try {
      const res = await api.get('admin_system/departments/');
      setDepartments(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const create = async (e) => {
    e.preventDefault();
    try {
      await api.post('admin_system/departments/', { name });
      toast.success('Department created');
      setName('');
      load();
    } catch (e) {
      toast.error('Error');
    }
  };

  const toggle = async (id) => {
    try {
      await api.post(`admin_system/departments/${id}/toggle/`);
      toast.success('Toggled');
      load();
    } catch (e) {
      toast.error('Error toggling');
    }
  };

  return (
    <div>
      <h3>Department Management</h3>
      <form onSubmit={create} className="mb-3">
        <input className="form-control mb-2" value={name} onChange={e=>setName(e.target.value)} placeholder="Department name" required/>
        <button className="btn btn-primary">Create</button>
      </form>
      <ul className="list-group">
        {departments.map(d=>(
          <li key={d.id} className="list-group-item d-flex justify-content-between align-items-center">
            {d.name}
            <div>
              <span className={`me-3 ${d.is_active ? 'text-success' : 'text-danger'}`}>{d.is_active ? 'Active' : 'Inactive'}</span>
              <button className="btn btn-sm btn-outline-secondary" onClick={()=>toggle(d.id)}>Toggle</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
