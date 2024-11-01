import React, { useEffect, useState } from 'react';
import api from '../../api/apiClient';
import { toast } from 'react-toastify';

export default function ClubBrowser() {
  const [clubs, setClubs] = useState([]);

  useEffect(()=> {
    load();
  }, []);

  const load = async () => {
    try {
      const res = await api.get('student_interface/clubs/');
      setClubs(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const join = async (id) => {
    try {
      await api.post(`student_interface/clubs/${id}/join/`);
      toast.success('Joined club');
      load();
    } catch (e) {
      toast.error('Failed to join');
    }
  };

  return (
    <div>
      <h3>Clubs</h3>
      <ul className="list-group">
        {clubs.map(c=>(
          <li key={c.id} className="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <strong>{c.name}</strong>
              <div className="text-muted">ID: {c.club_id}</div>
            </div>
            <div>
              <button className="btn btn-sm btn-primary" onClick={()=>join(c.id)}>Join</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
