import React, { useEffect, useState } from 'react';
import api from '../../api/apiClient';

export default function StudentDashboard() {
  const [data, setData] = useState(null);

  useEffect(()=> {
    fetch();
  }, []);

  const fetch = async () => {
    try {
      const res = await api.get('student_interface/dashboard/');
      setData(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h3>Student Dashboard</h3>
      <div className="card mb-3">
        <div className="card-body">
          <h5>{data.user.username}</h5>
          <p>{data.user.first_name} {data.user.last_name} - {data.user.email}</p>
          <p>Cluster: {data.cluster ? data.cluster.name : 'None'}</p>
          <p>Mentors: {data.mentors.join(', ')}</p>
        </div>
      </div>
    </div>
  );
}
