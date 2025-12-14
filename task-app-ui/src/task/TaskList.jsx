import { useEffect, useState } from "react";
import {
  getTasks,
  getTaskById,
  updateTask,
  deleteTask,
} from "./taskService";
import TaskForm from "./TaskForm";
import "../css/ui.css";

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [modal, setModal] = useState(null);
  const [selectedTask, setSelectedTask] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [toast, setToast] = useState("");

  const loadTasks = () => {
    getTasks().then(setTasks);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const openView = async (id) => {
    setSelectedTask(await getTaskById(id));
    setModal("view");
  };

  const openEdit = async (id) => {
    setSelectedTask(await getTaskById(id));
    setModal("edit");
  };

  const handleUpdate = async (data) => {
    await updateTask(selectedTask.id, data);
    setToast("Task updated successfully");
    setModal(null);
    loadTasks();
    setTimeout(() => setToast(""), 2000);
  };

  const handleDelete = async () => {
    await deleteTask(confirmDelete);
    setToast("Task deleted successfully");
    setConfirmDelete(null);
    loadTasks();
    setTimeout(() => setToast(""), 2000);
  };

  return (
    <div className="task-list">
      {toast && <div className="toast right">{toast}</div>}

      <h3>Tasks</h3>

      {tasks.map((task) => (
        <div className="task-card" key={task.id}>
          <div>
            <strong>{task.title}</strong>
            <p>{task.description}</p>
            <span className={`badge ${task.priority}`}>
              {task.priority}
            </span>
          </div>

          <div className="task-actions">
            <button className="btn btn-outline" onClick={() => openView(task.id)}>
              View
            </button>
            <button className="btn" onClick={() => openEdit(task.id)}>
              Edit
            </button>
            <button
              className="btn btn-danger"
              onClick={() => setConfirmDelete(task.id)}
            >
              Delete
            </button>
          </div>
        </div>
      ))}

      {/* VIEW / EDIT MODAL */}
      {modal && (
        <div className="modal-backdrop">
          <div className="modal card">
            <TaskForm
              initialData={selectedTask}
              readOnly={modal === "view"}
              onSubmit={handleUpdate}
              onCancel={() => setModal(null)}
            />
          </div>
        </div>
      )}

      {/* DELETE CONFIRM MODAL */}
      {confirmDelete && (
        <div className="modal-backdrop">
          <div className="modal card">
            <h4>Delete Task?</h4>
            <p>This action cannot be undone.</p>

            <div className="task-actions">
              <button className="btn btn-danger" onClick={handleDelete}>
                Delete
              </button>
              <button
                className="btn btn-outline"
                onClick={() => setConfirmDelete(null)}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskList;
