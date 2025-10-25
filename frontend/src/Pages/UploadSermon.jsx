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
