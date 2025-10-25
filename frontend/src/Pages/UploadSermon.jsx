import { createClient } from "@supabase/supabase-js";
import { useState } from "react";

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

// 🔥 Initialize Supabase client
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

console.log("🚀 Supabase URL:", SUPABASE_URL);
console.log("🔑 Supabase ANON KEY:", SUPABASE_KEY.slice(0, 8) + "...");

function UploadSermon() {
  const [pastorName, setPastorName] = useState("");
  const [sermonTitle, setSermonTitle] = useState("");
  const [sermonDate, setSermonDate] = useState("");
  const [audios, setAudios] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleAudioUpload = (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    const newAudios = files.map((file) => ({
      file,
      name: file.name,
      url: URL.createObjectURL(file),
      progress: 0,
      status: "pending",
    }));

    setAudios((prev) => [...prev, ...newAudios]);
  };

  // 🎧 Convert audio to MP3
  const convertToMp3 = async (file) => {
    if (!ffmpegInstance) {
      const ffmpegModule = await import(
        "https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.11.8/dist/ffmpeg.min.js"
      );
      const { createFFmpeg, fetchFile } = ffmpegModule;
      ffmpegInstance = createFFmpeg({ log: true });
      ffmpegInstance.fetchFile = fetchFile;
      await ffmpegInstance.load();
    }

    const ffmpeg = ffmpegInstance;
    const fetchFile = ffmpeg.fetchFile;

    ffmpeg.FS("writeFile", file.name, await fetchFile(file));
    const output = `${file.name.replace(/\.\w+$/, "")}-converted.mp3`;

    await ffmpeg.run("-i", file.name, "-b:a", "192k", output);
    const data = ffmpeg.FS("readFile", output);

    const mp3File = new File([data.buffer], output, { type: "audio/mp3" });

    ffmpeg.FS("unlink", file.name);
    ffmpeg.FS("unlink", output);

    return mp3File;
  };

  const handleSermonSave = async () => {
    if (!pastorName || !sermonTitle || !sermonDate || audios.length === 0) {
      alert("Please fill all fields and upload at least one audio.");
      return;
    }

    try {
      setUploading(true);
      setProgress(0);

      const sermon_id = `SERMON-${crypto.randomUUID().slice(0, 8)}`;
      let uploadedCount = 0;

      for (const audio of audios) {
        try {
          let fileToUpload = audio.file;
          if (!fileToUpload.type.includes("mp3")) {
            fileToUpload = await convertToMp3(fileToUpload);
          }

          const filePath = `sermons/${sermon_id}/${fileToUpload.name}`;

          console.log(`⬆️ Uploading ${filePath}...`);

          const { data, error } = await supabase.storage
            .from("audios")
            .upload(filePath, fileToUpload, {
              cacheControl: "3600",
              upsert: false,
            });

          if (error) {
            console.error("❌ Upload error:", error.message);
            throw error;
          }

          console.log("✅ Uploaded:", data.path);

          uploadedCount++;
          const percent = Math.round((uploadedCount / audios.length) * 100);
          setProgress(percent);

          setAudios((prev) =>
            prev.map((a) =>
              a.name === audio.name
                ? { ...a, status: "done", progress: 100 }
                : a
            )
          );
        } catch (err) {
          console.error(`Error uploading ${audio.name}:`, err);
          setAudios((prev) =>
            prev.map((a) =>
              a.name === audio.name ? { ...a, status: "error" } : a
            )
          );
        }
      }

      alert("✅ All sermons uploaded successfully!");
      setAudios([]);
      setPastorName("");
      setSermonTitle("");
      setSermonDate("");
    } catch (error) {
      console.error("Upload error:", error);
      alert(`❌ Upload failed: ${error.message}`);
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

  return (
    <div className="p-8 text-white bg-gray-900 min-h-screen">
      <h1 className="text-yellow-400 text-3xl font-bold mb-6">Upload Sermon</h1>

      <input
        type="text"
        placeholder="Pastor's Name"
        value={pastorName}
        onChange={(e) => setPastorName(e.target.value)}
        className="block w-full mb-3 p-2 bg-gray-800 rounded"
      />

      <input
        type="text"
        placeholder="Sermon Title"
        value={sermonTitle}
        onChange={(e) => setSermonTitle(e.target.value)}
        className="block w-full mb-3 p-2 bg-gray-800 rounded"
      />

      <input
        type="date"
        value={sermonDate}
        onChange={(e) => setSermonDate(e.target.value)}
        className="block w-full mb-3 p-2 bg-gray-800 rounded"
      />

      <input
        type="file"
        accept="audio/*"
        multiple
        onChange={handleAudioUpload}
        className="block w-full mb-3"
      />

      <button
        onClick={handleSermonSave}
        disabled={uploading}
        className="w-full py-2 bg-yellow-400 text-black font-bold rounded"
      >
        {uploading ? `Uploading... ${progress}%` : "Save Sermon"}
      </button>
    </div>
  );
}

export default UploadSermon;
      await ffmpegInstance.load();
    }

    const ffmpeg = ffmpegInstance;
    const fetchFile = ffmpeg.fetchFile;

    ffmpeg.FS("writeFile", file.name, await fetchFile(file));
    const output = `${file.name.replace(/\.\w+$/, "")}-converted.mp3`;

    await ffmpeg.run("-i", file.name, "-b:a", "192k", output);
    const data = ffmpeg.FS("readFile", output);

    const mp3File = new File([data.buffer], output, { type: "audio/mp3" });

    ffmpeg.FS("unlink", file.name);
    ffmpeg.FS("unlink", output);

    return mp3File;
  };

  const handleSermonSave = async () => {
    if (!pastorName || !sermonTitle || !sermonDate || audios.length === 0) {
      alert("Please fill all fields and upload at least one audio.");
      return;
    }

    try {
      setUploading(true);
      setProgress(0);

      const API_URL = import.meta.env.VITE_API_URL;
      const formData = new FormData();

      audios.forEach((audio) => formData.append("filenames", audio.name));
      formData.append("preacher", pastorName);
      formData.append("title", sermonTitle);
      formData.append("date", sermonDate);

      // 1️⃣ Request signed URLs
      const res = await fetch(`${API_URL}/uploads/get-signed-urls`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Failed to get signed URLs");

      const { sermon_id, urls } = await res.json();

      let uploadedCount = 0;

      const uploadFile = async (audio, uploadUrlObj) => {
        try {
          // 🧩 Convert file to MP3 if not already
          if (!audio.file.type.includes("mp3")) {
            audio.file = await convertToMp3(audio.file);
          }

          const xhr = new XMLHttpRequest();
          xhr.open("PUT", uploadUrlObj.upload_url, true);
          xhr.setRequestHeader("Content-Type", audio.file.type);

          xhr.upload.onprogress = (e) => {
            if (e.lengthComputable) {
              const percent = Math.round((e.loaded / e.total) * 100);
              setAudios((prev) =>
                prev.map((a) =>
                  a.name === audio.name ? { ...a, progress: percent } : a
                )
              );
            }
          };

          await new Promise((resolve, reject) => {
            xhr.onload = () => {
              if (xhr.status >= 200 && xhr.status < 300) resolve();
              else reject(new Error(`Upload failed: ${xhr.status}`));
            };
            xhr.onerror = () => reject(new Error("Network error"));
            xhr.send(audio.file);
          });

          uploadedCount++;
          setProgress(Math.round((uploadedCount / audios.length) * 100));

          setAudios((prev) =>
            prev.map((a) =>
              a.name === audio.name
                ? { ...a, status: "done", progress: 100 }
                : a
            )
          );
        } catch (error) {
          console.error(`Error uploading ${audio.name}:`, error);
          setAudios((prev) =>
            prev.map((a) =>
              a.name === audio.name ? { ...a, status: "error" } : a
            )
          );
        }
      };

      // Batch uploads (5 at a time)
      const batchSize = 5;
      for (let i = 0; i < audios.length; i += batchSize) {
        const batch = audios.slice(i, i + batchSize);
        await Promise.all(
          batch.map((audio) => {
            const urlObj = urls.find((u) => u.filename === audio.name);
            return uploadFile(audio, urlObj);
          })
        );
      }

      // 3️⃣ Register sermon metadata
      const registerBody = {
        sermon_id,
        preacher: pastorName,
        title: sermonTitle,
        timestamp: sermonDate,
        audios: urls,
      };

      const registerRes = await fetch(`${API_URL}/uploads/register-sermon`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(registerBody),
      });

      const result = await registerRes.json();
      if (!registerRes.ok)
        throw new Error(result.message || "Failed to register sermon");

      alert("✅ Sermon uploaded successfully!");
      setAudios([]);
      setPastorName("");
      setSermonTitle("");
      setSermonDate("");
    } catch (error) {
      console.error("Upload error:", error);
      alert(`❌ Upload failed: ${error.message}`);
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

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

          {uploading && (
            <div className="mt-6">
              <p className="text-yellow-300 font-semibold mb-2">
                Overall Progress: {progress}%
              </p>
              <progress
                value={progress}
                max="100"
                className="w-full h-3 rounded-lg"
              />
            </div>
          )}

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
                    key={index}
                    className="bg-gray-800 p-4 rounded-lg flex flex-col gap-2"
                  >
                    <p className="font-semibold text-yellow-200">
                      Audio {index + 1}: {audio.name}
                    </p>
                    <audio controls src={audio.url} className="w-full rounded" />
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          audio.status === "error"
                            ? "bg-red-500"
                            : audio.status === "done"
                            ? "bg-green-500"
                            : "bg-yellow-400"
                        }`}
                        style={{ width: `${audio.progress}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-gray-400">
                      {audio.status === "done"
                        ? "✅ Uploaded"
                        : audio.status === "error"
                        ? "❌ Failed"
                        : `${audio.progress}%`}
                    </p>
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
            disabled={uploading}
            className={`w-full font-bold py-3 rounded-lg transition ${
              uploading
                ? "bg-gray-600 text-gray-300 cursor-not-allowed"
                : "bg-yellow-400 text-black hover:bg-yellow-500"
            }`}
          >
            {uploading ? `Uploading... ${progress}%` : "Save Sermon"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default UploadSermon;
