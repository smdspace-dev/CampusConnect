import React, { useEffect, useState } from 'react';
import api from '../../api/apiClient';
import { toast } from 'react-toastify';

export default function ClusterManagement() {
  const [clusters, setClusters] = useState([]);
  const [name, setName] = useState('');
  const [mentorId, setMentorId] = useState('');
  const [departments, setDepartments] = useState([]);
  const [mentors, setMentors] = useState([]);
  const [file, setFile] = useState(null);

  useEffect(() => {
    fetchClusters();
    fetchDepartments();
    fetchMentors();
  }, []);

  const fetchClusters = async () => {
    try {
      const res = await api.get('admin_system/clusters/');
      setClusters(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchDepartments = async () => {
    try {
      const res = await api.get('admin_system/departments/');
      setDepartments(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchMentors = async () => {
    try {
      const res = await api.get('admin_system/staff/');
      setMentors(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    const form = new FormData();
    form.append('name', name);
    if (mentorId) form.append('mentor_id', mentorId);
    if (file) form.append('file_upload', file);
    try {
      await api.post('admin_system/clusters/', form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      toast.success('Cluster created');
      setName('');
      setMentorId('');
      setFile(null);
      fetchClusters();
    } catch (err) {
      toast.error('Error creating cluster');
      console.error(err);
    }
  };

  return (
    <div>
      <h3>Cluster Management</h3>
      <form onSubmit={handleCreate} className="mb-4">
        <div className="mb-2">
          <label className="form-label">Name</label>
          <input className="form-control" value={name} onChange={(e)=>setName(e.target.value)} required/>
        </div>
        <div className="mb-2">
          <label className="form-label">Mentor</label>
          <select className="form-select" value={mentorId} onChange={(e)=>setMentorId(e.target.value)}>
            <option value="">--none--</option>
            {mentors.map(m => (
              <option key={m.id} value={m.id}>{m.user?.username || m.user?.email}</option>
            ))}
          </select>
        </div>
        <div className="mb-2">
          <label className="form-label">File Upload (optional)</label>
          <input type="file" className="form-control" onChange={(e)=>setFile(e.target.files[0])}/>
        </div>
        <button className="btn btn-primary">Create Cluster</button>
      </form>

      <h5>Existing Clusters</h5>
      <ul className="list-group">
        {clusters.map(c => (
          <li key={c.id} className="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <strong>{c.name || 'Unnamed'}</strong>
              <div className="text-muted">ID: {c.cluster_id}</div>
            </div>
            <div>{c.mentor ? c.mentor.user.username : 'No Mentor'}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
