import React from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Dashboard</h1>
      <p>Welcome to AI Pension Assistant</p>
      
      {/* Chat Button */}
      <button
        style={{ padding: "10px 20px", marginTop: "20px", fontSize: "16px" }}
        onClick={() => navigate("/chat")}
      >
        Open AI Chatbot
      </button>
    </div>
  );
}

export default Dashboard;