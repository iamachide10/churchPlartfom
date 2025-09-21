import React from "react";

const SermonCard = ({ preacher, title, date }) => {
  return (
    <div className="bg-black text-white rounded-2xl shadow-lg p-6 w-full max-w-md mx-auto border border-yellow-400">
      {/* Sermon Title */}
      <h2 className="text-2xl font-bold text-yellow-400 mb-2">{title}</h2>

      {/* Preacher */}
      <p className="text-lg text-gray-200 mb-1">
        <span className="font-semibold">Preacher:</span> {preacher}
      </p>

      {/* Date */}
      <p className="text-sm text-gray-400">
        <span className="font-semibold text-yellow-300">Date:</span> {date}
      </p>
    </div>
  );
};

export default SermonCard;
