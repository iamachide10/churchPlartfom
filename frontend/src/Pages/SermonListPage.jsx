import { useEffect, useState } from "react";
import SermonCard from "../Components/SermonCard";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Spinner from "../Components/spinser";


export const SermonListPage = () => {
 const [sermons, setSermons] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { user,access_token } = useAuth();

  useEffect(() => {
    const fetchSermons = async () => {
      console.log(access_token);
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const url = `${API_URL}/uploads/get-sermons`;
        // const response = await fetch(url, {
        //   headers: {
        //     "Authorization": `Bearer ${access_token}`,
        //   },
        // });
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error("Failed to fetch sermons");
        }
        const data = await response.json();
        setSermons(data.sermons || []);
        console.log(data.sermons);
      } catch (error) {
        console.error("Error fetching sermons:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchSermons();
  }, [user]);

  if (loading) {
    return <Spinner />;
  }

  if(!user) {
  return (
    <p className="min-h-screen bg-gray-900 text-white px-4 sm:px-6 lg:px-12 py-10 font-bold text-lg text-center mt-9">
      Please Signin first
    </p>
  );
  }


  return (
    <div className="min-h-screen bg-gray-900 text-white px-4 sm:px-6 lg:px-12 py-10">
      <h1 className="text-3xl font-bold text-yellow-400 mb-8 text-center">
        Sermons
      </h1>

      {sermons.length === 0 ? (
        <p className="text-center text-gray-400">
          No sermons uploaded yet. Go to Upload Page to add one.
        </p>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {sermons.map((sermon) => (
            <div
              key={sermon.id}
              onClick={() => navigate(`/sermons/${sermon.title}`)}
              className="cursor-pointer"
            >
              <SermonCard
                preacher={sermon.pastorName}
                title={sermon.sermonTitle}
                date={sermon.sermonDate}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
