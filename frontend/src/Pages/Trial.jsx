import { useState } from "react"


export const UploadSermon=()=>{
    const [pastorName,setPastorName]=useState("")



return(
<div className="min-h-screen bg-gray-800 text-white py-10 px-6">
    <div className="max-w-4xl mx-auto bg-black bg-opacity-60 p-8 rounded-2xl shadow-lg">
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
                className="w-full px-4 bg-gray-800 text-white rounded-lg focus:ring-2"
                
                />

            </div>
        </div>

        

    </div>

</div>)    
}
