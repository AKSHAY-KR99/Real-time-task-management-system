import { useState } from "react";
import { loginUser } from "./authService";
import { useNavigate } from "react-router-dom";
import "../css/auth.css";
import "../css/notification.css";

const Login = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await loginUser(form);
      localStorage.setItem("access_token", res.access_token);
      navigate("/dashboard");
    } catch {
      setMessage("Invalid credentials");
      setTimeout(() => setMessage(""), 3000);
    }
  };

  return (
    <div className="auth-container fade-in">
      {message && <div className="notification">{message}</div>}

      <div className="auth-card">
        <h2>Login</h2>

        <form onSubmit={handleSubmit}>
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

          <div className="form-actions">
  <button className="btn" type="submit">Login</button>
</div>
        </form>

        <p onClick={() => navigate("/register")}>Go to Register</p>
      </div>
    </div>
  );
};

export default Login;
