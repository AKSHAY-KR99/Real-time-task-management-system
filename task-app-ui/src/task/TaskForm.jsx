import { useState, useEffect } from "react";
import "../css/ui.css";

const TaskForm = ({ initialData, onSubmit, onCancel, readOnly }) => {
  const [form, setForm] = useState({
    title: "",
    description: "",
    priority: "low",
  });

  useEffect(() => {
    if (initialData) setForm(initialData);
  }, [initialData]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const submit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form className="card" onSubmit={submit}>
      <input
        name="title"
        placeholder="Title"
        value={form.title}
        onChange={handleChange}
        disabled={readOnly}
      />

      <textarea
        name="description"
        placeholder="Description"
        value={form.description}
        onChange={handleChange}
        disabled={readOnly}
      />

      <select
        name="priority"
        value={form.priority}
        onChange={handleChange}
        disabled={readOnly}
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>

      <div className="task-actions">
        {!readOnly && <button className="btn">Save</button>}
        <button type="button" className="btn btn-outline" onClick={onCancel}>
          Close
        </button>
      </div>
    </form>
  );
};

export default TaskForm;
