// src/Pages/AboutUs.jsx
import React from "react";

const AboutUs = () => {
  return (
    <div className="bg-black text-white min-h-screen">
      {/* Hero */}
      <section className="text-center py-12 bg-gradient-to-r from-yellow-600 to-yellow-400 text-black">
        <h1 className="text-4xl font-bold py-9">Min. Elistar Ministry</h1>
        <p className="mt-2 text-lg italic">"We stand for the Gospel"</p>
      </section>

      {/* Mission & Vision */}
      <section className="max-w-4xl mx-auto px-4 py-10 space-y-8">
        <div>
          <h2 className="text-2xl font-semibold text-yellow-400">Mission Statement</h2>
          <p className="mt-2">
            Igniting a wave of revival by empowering youths, fostering a deeper relationship with God, 
            and equipping them to transform their communities for Christ.
          </p>
        </div>
        <div>
          <h2 className="text-2xl font-semibold text-yellow-400">Vision Statement</h2>
          <p className="mt-2">
            A movement of young people passionately pursuing God and impacting their world with the Gospel.
          </p>
        </div>
      </section>

      {/* About Us */}
      <section className="bg-gray-900 py-10 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-semibold text-yellow-400">About Us</h2>
          <p className="mt-2">
            The Min. Elistar Ministry is a non-denominational network dedicated to influencing youths 
            with the intent of Christ. The aim of this network is to provide a message of hope and 
            inspiration to the youths in a respectful and inclusive manner.
          </p>
        </div>
      </section>

      {/* Core Values */}
      <section className="max-w-5xl mx-auto px-4 py-10">
        <h2 className="text-2xl font-semibold text-yellow-400 text-center">Core Values</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
          {["Passion for God", "Youth Empowerment", "Biblical Integrity", "Evangelism and Outreach"].map((value, i) => (
            <div key={i} className="bg-gray-800 p-4 rounded-lg shadow hover:scale-105 transition">
              <p className="text-center">{value}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Focused Areas */}
      <section className="bg-gray-900 py-10 px-4">
        <h2 className="text-2xl font-semibold text-yellow-400 text-center">Focused Areas</h2>
        <div className="max-w-4xl mx-auto grid md:grid-cols-3 gap-6 mt-6">
          {["Spiritual Growth", "Community Outreach", "Leadership Development"].map((area, i) => (
            <div key={i} className="bg-gray-800 p-6 rounded-lg text-center shadow hover:scale-105 transition">
              <p>{area}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default AboutUs;
