import { useState } from "react";
import { useAuth } from "../context/AuthContext";



function LandingPage() {
  const {user}=useAuth();

  return (
    <div className="bg-gray-900 text-white">
      {/* Hero Section */}
      <section className="h-screen flex flex-col items-center justify-center text-center bg-black bg-opacity-70">
        <h1 className="text-4xl md:text-6xl font-bold text-yellow-400">Welcome to Min. Elistar Ministry</h1>
        <p className="mt-4 text-lg text-gray-300">Faith. Hope. Love.</p>


      {user ?  <button className="mt-6 bg-yellow-400 text-black px-6 py-3 rounded-lg font-bold hover:bg-yellow-500">
          <a href="/sermons">
          Listen To Sermons
          </a>
        </button> :  <p  className="mt-10 text-lg text-gray-300">Kindly Sign Up to Join the Family.</p>}
       
      </section>
      {/* About */}
      <section className="py-16 px-6 text-center max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold text-yellow-400 mb-4">About Us</h2>
        <p className="text-gray-300">
          We are a family of believers dedicated to sharing God’s love and message 
          with the world. Join us for worship, fellowship, and service.
        </p>
      </section>
      {/* Events, Prayer Requests, Pastor’s Message ... */}
    </div>
  );
}

 
export default LandingPage;