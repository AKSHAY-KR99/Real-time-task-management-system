import { useState } from "react";
import { registerUser } from "./authService";
import { useNavigate } from "react-router-dom";
import "../css/auth.css";
import "../css/notification.css";

const Register = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: "",
    password: "",
    full_name: "",
    role: "user",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerUser(form);
      setMessage("Registration successful");
      setTimeout(() => navigate("/login"), 1500);
    } catch {
      setMessage("Registration failed");
      setTimeout(() => setMessage(""), 3000);
    }
  };

  return (
    <div className="auth-container fade-in">
      {message && <div className="notification">{message}</div>}

      <div className="auth-card">
        <h2>Register</h2>

        <form onSubmit={handleSubmit}>
          <input
            className="input"
            name="full_name"
            placeholder="Full Name"
            onChange={handleChange}
          />

          <input
            className="input"
            name="email"
            placeholder="Email"
            onChange={handleChange}
          />

          <input
            className="input"
            name="password"
            type="password"
            placeholder="Password"
            onChange={handleChange}
          />

          <select className="input" name="role" onChange={handleChange}>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
                    <div className="form-actions">
  <button className="btn" type="submit">Register</button>
</div>
        </form>

        <p onClick={() => navigate("/")}>Go to Login</p>
      </div>
    </div>
  );
};

export default Register;
