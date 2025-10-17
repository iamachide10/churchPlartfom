import { useState } from "react"


export const UploadSermonTrial=()=>{
    const [pastorName,setPastorName]=useState("")
    const [title, setTitle]=useState("")
    const [sermonDate,setSermonDate]=useState("")
    const [audios,setAudios]=useState([])

    const handleAudioUpload=(e)=>{
        const files=Array.from(e.target.files)
        if(files.length===0) return;

        const newAudios =files.map((file)=>({
            name: file.name,
            url:URL.createObjectURL(file)
        }))
        setAudios([...audios, ...newAudios])
    }


return(
<div className="min-h-screen bg-gray-800 text-white py-10 px-6">
    <div className="max-w-4xl mx-auto bg-black bg-opacity-60 p-8 rounded-2xl shadow-lg mt-8">
        <h1 className="text-3xl font-bold text-yellow-400 text-center mb-8">
            Upload Sermon
        </h1>

        <div className="space-y-6 mb-10">
            <div>
                <label className="block text-yellow-400 font-semibold mb-2">
                    Pastor's Name
                </label>
                <input type="text"
                value={pastorName}
                onChange={e=>setPastorName(e.target.value)}
                className="mb-3 w-full px-4 py-2 bg-gray-800 text-white rounded-lg focus:ring-2 focus:ring-yellow-400"
                placeholder="Enter Preacher's name"
                />
            </div>

            <div>
            <label className="block text-yellow-400 font-semibold mb-2">Sermon Title</label>
            <input type="text"
            placeholder="Enter sermon title"
            className="py-2 px-4 focus:ring-2 focus:ring-yellow-400 bg-gray-800 w-full rounded-md"
            onChange={e=>setTitle(e.target.value)}
            value={title}
            />
            </div>

            <div>
                <label className="block text-yellow-400 font-semibold md-2">
                    Date
                </label>
                <input type="date"
                value={sermonDate}
                className="w-full bg-gray-800 px-6 py-2 rounded-lg text-white focus:ring-2 focus:ring-yellow-300"
                onChange={e=>setSermonDate(e.target.value)}
                 />
            </div>

            <div className="border-t border-gray-600 pt-6">
                <h2 className="text-yellow-400 font-semibold text-2xl mb-2">Upload Audios</h2>

                <input type="file" accept="audio/*" multiple 
                onChange={handleAudioUpload}
                className="w-full rounded-lg text-white mb-2 py-2 px-4 bg-gray-800"
                />

                <p className="text-yellow-300  text-xl font-semibold mb-2 pt-2">Uploaded Audios ({audios.length})</p>
                {audios.length===0 ?(<p className="text-gray-400 mt-2 mb-2">No audios uploaded yet.</p>):
                (<ul className="space-y-4">
                {audios.map((audio,i)=>(
                    <li key={i}
                    className="bg-gray-800 p-4 rounded-lg flex flex-col gap-2"
                    >
                        <p className="font-semibold text-yellow-200">
                            Audio {i+1 }: {audio.name}
                        </p>

                        <audio controls src={audio.url} className="w-full rounded"></audio>
                    </li>
                ))}
                 </ul>)}

                <button className="mt-3 bg-yellow-400 w-full rounded-lg text-center text-gray-800 font-semibold py-2 px-4">Upload Sermos </button>

            </div>
        </div>
    </div>

</div>)    
}
