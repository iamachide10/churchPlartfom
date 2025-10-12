import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import Spinner from "../Components/spinser";

const SignIn = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const [resendMessage,setResendMessage]=useState("")
  const [verification, setVerification]=useState(null)
  const [loading,setLoading]=useState(false)


  
  const handleResend = async () => {
    setLoading(true)
    try {
      const res = await fetch(verification, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      });
      const data = await res.json();
      setResendMessage(data.message);
      setError("")
      
    } catch (err) {
      setResendMessage("Something went wrong. Please try again later.");
      setError("")
      console.error("Error :" + err)
    }finally{
      setLoading(false)
    }
  };




  const handleSubmit = async(e) => {
    e.preventDefault();
    setLoading(true)
    const credentials = { email, password };
    const API_URL = import.meta.env.VITE_API_URL;
    const url = `${API_URL}/auth/login`;
    const response=await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(credentials),
    })
    const text= await response.text()
    let data;
    try{
      data=JSON.parse(text)
      
    }catch{
      throw new Error(`Invalid JSON response: ${text}`)
    }finally{
      setLoading(false)
    }

    const {status,message ,resend_verification_url}=data
    if(resend_verification_url){
      setVerification(resend_verification_url)
    }
    if(status==="e"){
      setError(typeof message==="string" ? message :JSON.stringify(message))
    }
    else if(status==="s"){
      setError("")
      login(data.user.userName , data.access_token)
      window.location.href="/"
    } 
  };

  if(loading){
    return <Spinner/>
  }


  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <form
        onSubmit={handleSubmit}
        className="mx-5 bg-black text-white p-8 rounded-2xl shadow-lg w-full max-w-md border border-yellow-400"
      >
        <h2 className="text-2xl font-bold mb-6 text-center text-yellow-400">
          Sign In
        </h2>

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

      
        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}
        

        {verification && (
       <button onClick={handleResend} className="mb-4 text-blue-400 underline">
          Resend Verification Email
       </button>
        )}
         {resendMessage && <p className="text-white-400 text-sm mb-4">{resendMessage}</p>}

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
