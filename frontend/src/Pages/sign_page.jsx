import React, { useState } from "react";

const SignUp = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");


  
  const handleSubmit = (e) => {
    e.preventDefault();

    // Get existing users from localStorage (if any)
    let users = JSON.parse(localStorage.getItem("users")) || [];

    // Check if email already exists
    const userExists = users.some((user) => user.email === email);
    if (userExists) {
      setError("❌ Email already registered. Please sign in.");
      return;
    }

    if(password !==confirmPassword) return setError("Password mismatch")

      
    const newUser = { name, email, password };
    users.push(newUser);
    localStorage.setItem("users", JSON.stringify(users));

    setSuccess("✅ Account created successfully! You can now sign in.");
    setError("");
    setName("");
    setEmail("");
    setPassword("");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <form
        onSubmit={handleSubmit}
        className="bg-black text-white p-8 rounded-2xl shadow-lg w-full max-w-md border border-yellow-400"
      >
        <h2 className="text-2xl font-bold mb-6 text-center text-yellow-400">
          Sign Up
        </h2>

        {/* Name */}
        <div className="mb-4">
          <label className="block text-gray-300 mb-1">Full Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-400"
          />
        </div>

        {/* Email */}
        <div className="mb-4">
          <label className="block text-gray-300 mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-400"
          />
        </div>

        {/* Password */}
        <div className="mb-4">
          <label className="block text-gray-300 mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-400"
          />
        </div>
        {/* Confirm Password */}
        <div className="mb-4">
          <label className="block text-gray-300 mb-1">Confirm Password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            className="w-full p-2 rounded bg-gray-800 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-400"
          />
        </div>

        {/* Success & Error Messages */}
        {success && <p className="text-green-400 text-sm mb-4">{success}</p>}
        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        {/* Button */}
        <button
          type="submit"
          className="w-full bg-yellow-400 text-black py-2 rounded font-bold hover:bg-yellow-500 transition"
        >
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default SignUp;
