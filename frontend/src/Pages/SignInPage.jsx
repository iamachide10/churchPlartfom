import React, { useState } from "react";

const SignIn = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSignedIn, setIsSignedIn] = useState(false);

  // Dummy credentials
  const validUser = {
    email: "test@example.com",
    password: "123456",
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const user=localStorage.getItem("users")
    if (email === validUser.email && password === validUser.password) {
      setIsSignedIn(true);
      setError("");
    } else {
      setError("❌ Invalid email or password");
      setIsSignedIn(false);
    }
  };

  if (isSignedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
        <h1 className="text-2xl font-bold text-green-400">
          ✅ Signed in successfully! Welcome back 
        </h1>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <form
        onSubmit={handleSubmit}
        className="bg-black text-white p-8 rounded-2xl shadow-lg w-full max-w-md border border-yellow-400"
      >
        <h2 className="text-2xl font-bold mb-6 text-center text-yellow-400">
          Sign In
        </h2>

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

        {/* Error */}
        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        {/* Button */}
        <button
          type="submit"
          className="w-full bg-yellow-400 text-black py-2 rounded font-bold hover:bg-yellow-500 transition"
        >
          Sign In
        </button>
      </form>
    </div>
  );
};

export default SignIn;
