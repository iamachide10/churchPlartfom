import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";

const SignUp = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const [taskMessage,setTaskMessage]=useState("")
  console.log("VITE_API_URL from env:", import.meta.env.VITE_API_URL);

const handleSubmit = async (e) => {
  e.preventDefault();

  // /check password match
  if (password !== confirmPassword) {
    setError("Passwords do not match");
    return;
  }

  const credentials = { name, email, password };

  // get API URL from environment
  const API_URL = import.meta.env.VITE_API_URL;
  const url = `${API_URL}/auth/register`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(credentials),
    });

    // check if backend sent a valid JSON
    const text = await response.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      throw new Error(`Invalid JSON response: ${text}`);
    }

    const { status, message} = data;


    const task_id=data.task_id
    console.log(task_id)
    if(task_id){
      const url=`${API_URL}/task-status/${task_id}`
      const response = await fetch(url)
      const text= await response.text()
      try{
        data=JSON.parse(text)
      }catch{
        throw new Error(`Invalid JSON response: ${text}`)
      }
      setTaskMessage(typeof data.massage==="string" ? data.massage :JSON.stringify(data.message))
    }


    if (status === "e") {
      setError(typeof message === "string" ? message : JSON.stringify(message));
    } else if (status === "s") {
      setSuccess(typeof message === "string" ? message : JSON.stringify(message));
    } else {
      setError("Unexpected response from server");
    }
  } catch (err) {
    console.error("❌ Request failed:", err);
    setError(err.message || "Something went wrong");
  }
};


  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 ">
      <form
        onSubmit={handleSubmit}
        className="mx-5 bg-black text-white p-8 rounded-2xl shadow-lg w-full max-w-md border border-yellow-400"
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
        {taskMessage &&  <p className="text-green-400 text-sm mb-4">{taskMessage}</p>}

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
