import React, { useState } from 'react';
import api from '../../api/apiClient';
import { toast } from 'react-toastify';

export default function StudentBulkUpload() {
  const [file, setFile] = useState(null);
  const [created, setCreated] = useState([]);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return toast.error('Select a file first');
    const form = new FormData();
    form.append('file', file);
    try {
      const res = await api.post('admin_system/students/bulk_upload/', form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setCreated(res.data.created || []);
      toast.success('Upload complete');
    } catch (e) {
      toast.error('Upload failed');
    }
  };

  return (
    <div>
      <h3>Student Bulk Upload (Excel)</h3>
      <form onSubmit={handleUpload}>
        <div className="mb-2">
          <input type="file" accept=".xlsx, .xls" onChange={(e)=>setFile(e.target.files[0])} className="form-control" />
        </div>
        <button className="btn btn-primary">Upload</button>
      </form>

      {created.length > 0 && (
        <>
          <h5 className="mt-3">Created Users</h5>
          <ul className="list-group">
            {created.map(u => <li className="list-group-item" key={u}>{u}</li>)}
          </ul>
        </>
      )}
    </div>
  );
}
