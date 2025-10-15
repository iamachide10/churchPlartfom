import { useState } from "react";
import Spinner from "../Components/spinser";


function UploadSermon() {
  const [pastorName, setPastorName] = useState("");
  const [sermonTitle, setSermonTitle] = useState("");
  const [sermonDate, setSermonDate] = useState("");
  const [audios, setAudios] = useState([]);
  const [loading, setLoading] = useState(false);
  

  const handleAudioUpload = (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    const newAudios = files.map((file) => ({

  file,
      name: file.name,
      url: URL.createObjectURL(file),
    }));

    setAudios([...audios, ...newAudios]);
  };

const handleSermonSave = async () => {
  
  if (!pastorName || !sermonTitle || !sermonDate || audios.length === 0) {
    alert("Please fill all fields and upload at least one audio.");
    return;
  }

  // Prepare FormData
  const formData = new FormData();
  audios.forEach((audio) => {
    formData.append("audios", audio.file); // all uploaded files
  });
 

  formData.append("preacher", pastorName)
  formData.append("title", sermonTitle)
  formData.append("date", sermonDate)

  try {
    setLoading(true);
    const API_URL = import.meta.env.VITE_API_URL;
    const url = `${API_URL}/uploads/upload-audio`; // show spinner if using one
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      alert(data.message );
      console.log("Uploaded files:", data.success);
    } else {
      alert(`Error: ${data.message || "Upload failed"}`);
    }

    setPastorName("");
    setSermonTitle("");
    setSermonDate("");
    setAudios([]);
  } catch (error) {
    console.error("Upload error:", error);
    alert("Network error. Please try again.");
  } finally {
    setLoading(false); // hide spinner
  }
};


 if(loading){
    return <Spinner/>
  }


  return (
    <div className="min-h-screen bg-gray-900 text-white py-10 px-6">
      <div className="max-w-4xl mx-auto bg-black bg-opacity-60 p-8 rounded-2xl shadow-lg">
        <h1 className="text-3xl font-bold text-yellow-400 text-center mb-8">
          Upload Sermon
        </h1>

        {/* Sermon Info */}
        <div className="space-y-6 mb-10">
          <div>
            <label className="block text-yellow-400 font-semibold mb-2">
              Pastor’s Name
            </label>
            <input
              type="text"
              value={pastorName}
              onChange={(e) => setPastorName(e.target.value)}
              className="w-full px-4 py-2 bg-gray-800 text-white rounded-lg focus:ring-2 focus:ring-yellow-400"
              placeholder="Enter pastor’s name"
            />
          </div>

          <div>
            <label className="block text-yellow-400 font-semibold mb-2">
              Sermon Title
            </label>
            <input
              type="text"
              value={sermonTitle}
              onChange={(e) => setSermonTitle(e.target.value)}
              className="w-full px-4 py-2 bg-gray-800 text-white rounded-lg focus:ring-2 focus:ring-yellow-400"
              placeholder="Enter sermon title"
            />
          </div>

          <div>
            <label className="block text-yellow-400 font-semibold mb-2">
              Date
            </label>
            <input
              type="date"
              value={sermonDate}
              onChange={(e) => setSermonDate(e.target.value)}
              className="w-full px-4 py-2 bg-gray-800 text-white rounded-lg focus:ring-2 focus:ring-yellow-400"
            />
          </div>
        </div>

        {/* Audio Upload Section */}
        <div className="border-t border-gray-700 pt-6">
          <h2 className="text-2xl font-semibold text-yellow-400 mb-4">
            Upload Audios
          </h2>
          
          <input
            type="file"
            accept="audio/*"
            multiple
            onChange={handleAudioUpload}
            className="w-full px-4 py-2 bg-gray-800 text-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400"
          />

          {/* Uploaded Audios */}
          <div className="mt-8">
            <h3 className="text-xl font-semibold text-yellow-300 mb-3">
              Uploaded Audios ({audios.length})
            </h3>
            {audios.length === 0 ? (
              <p className="text-gray-400">No audios uploaded yet.</p>
            ) : (
              <ul className="space-y-4">
                {audios.map((audio, index) => (
                  <li
                    key={audio.id}
                    className="bg-gray-800 p-4 rounded-lg flex flex-col gap-2"
                  >
                    <p className="font-semibold text-yellow-200">
                      Audio {index + 1}: {audio.name}
                    </p>
                    <audio controls src={audio.url} className="w-full rounded" />
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>



        {/* Save Sermon */}
        <div className="mt-10">
          <button
            onClick={handleSermonSave}
            className="w-full bg-yellow-400 text-black font-bold py-3 rounded-lg hover:bg-yellow-500 transition"
          >
            Save Sermon
          </button>
        </div>
      </div>
    </div>
  );
}

export default UploadSermon;
