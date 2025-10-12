import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";

function SermonPackDetails() {
  const { id } = useParams();
  const { user } = useAuth();
  const [sermon, setSermon] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSermonDetails = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const response = await fetch(`${API_URL}/uploads/get-sermon-audios/${id}`, {
          headers: {
            "Authorization": `Bearer ${user?.access_token}`,
          },
        });

        if (!response.ok) throw new Error("Failed to fetch sermon details");

        const data = await response.json();
        setSermon(data.sermon);
      } catch (error) {
        console.error("Error fetching sermon:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchSermonDetails();
  }, [id, user]);

  if (loading)
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <p className="text-gray-400 animate-pulse">Loading sermon...</p>
      </div>
    );

  if (!sermon)
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <p className="text-gray-400">Sermon not found.</p>
      </div>
    );

  return (
    <div className="min-h-screen bg-gray-900 text-white py-10 px-6 mt-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-yellow-400 mb-7">
          {sermon.title}
        </h1>
        <p className="text-gray-300 mb-2">
          <span className="text-yellow-300">Pastor:</span> {sermon.preacher}
        </p>
        <p className="text-gray-400 mb-6">
          <span className="text-yellow-300">Date:</span> {sermon.timestamp}
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
