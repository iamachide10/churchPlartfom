import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

function SermonPackDetails() {
  const { id } = useParams();
  const [sermon, setSermon] = useState(null);

  useEffect(() => {
    const sermons = JSON.parse(localStorage.getItem("sermons") || "[]");
    const found = sermons.find((s) => s.id.toString() === id);
    setSermon(found);
  }, [id]);

  if (!sermon)
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <p className="text-gray-400">Sermon not found.</p>
      </div>
    );

  return (
    <div className="min-h-screen bg-gray-900 text-white py-10 px-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-yellow-400 mb-4">
          {sermon.sermonTitle}
        </h1>
        <p className="text-gray-300 mb-2">
          <span className="text-yellow-300">Pastor:</span> {sermon.pastorName}
        </p>
        <p className="text-gray-400 mb-6">
          <span className="text-yellow-300">Date:</span> {sermon.sermonDate}
        </p>

        <h2 className="text-2xl font-semibold text-yellow-400 mb-4">
          Audios
        </h2>
        {sermon.audios.map((audio, index) => (
          <div
            key={audio.id}
            className="bg-gray-800 p-4 mb-4 rounded-lg shadow-lg"
          >
            <p className="font-semibold text-yellow-200 mb-2">
              Audio {index + 1}: {audio.name}
            </p>
            <audio controls src={audio.url} className="w-full rounded-lg" />
          </div>
        ))}
      </div>
    </div>
  );
}

export default SermonPackDetails;
