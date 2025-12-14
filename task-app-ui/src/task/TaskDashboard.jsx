import { useEffect, useState } from "react";
import { getCurrentUser, logoutUser } from "../auth/authService";
import { useNavigate } from "react-router-dom";
import { createTask } from "./taskService";
import TaskForm from "./TaskForm";
import TaskList from "./TaskList";

import "../css/dashboard.css";
import "../css/ui.css";
import "../css/web_not.css";

import {
  connectWebSocket,
  disconnectWebSocket,
} from "../websocket/socket";

const TaskDashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [showCreate, setShowCreate] = useState(false);
  const [notification, setNotification] = useState("");

  useEffect(() => {
    getCurrentUser()
      .then((userData) => {
        setUser(userData);

        connectWebSocket(userData.id, (message) => {
          setNotification(message);
          setTimeout(() => setNotification(""), 5000);
        });
      })
      .catch(() => {
        logoutUser();
        navigate("/login");
      });

    return () => disconnectWebSocket();
  }, []);

  const handleLogout = () => {
    disconnectWebSocket();
    logoutUser();
    navigate("/login");
  };

  const handleCreateTask = async (data) => {
    await createTask(data);
    setNotification("Task created successfully");
    setShowCreate(false);

    setTimeout(() => {
      setNotification("");
      window.location.reload();
    }, 1500);
  };

  return (
    <div className="dashboard">
      {notification && <div className="toast center">{notification}</div>}

      <div className="dashboard-header">
        <div className="user-info">
          <strong>{user?.full_name}</strong>
          <span>{user?.email}</span>
          <span>{user?.role}</span>
        </div>

        <button className="btn btn-outline" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div className="dashboard-actions">
        <button className="btn" onClick={() => setShowCreate(true)}>
          + Add Task
        </button>
      </div>

      {showCreate && (
        <div className="modal-backdrop">
          <div className="modal card">
            <TaskForm
              onSubmit={handleCreateTask}
              onCancel={() => setShowCreate(false)}
            />
          </div>
        </div>
      )}

      <TaskList />
    </div>
  );
};

export default TaskDashboard;
