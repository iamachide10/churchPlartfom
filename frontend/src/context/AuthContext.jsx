import { createContext,useContext ,useEffect,useState } from "react";

const AuthContext=createContext();
export const AuthProvider=({children})=>{

    const [user,setUser]=useState(null)
    const [access_token,setAccessToken]=useState(null)

    const login = (userData , access_token)=>{
        setUser(userData)
        setAccessToken(access_token)
        localStorage.setItem("user",JSON.stringify(userData))
        localStorage.setItem("access_token",access_token)
    }

    const logout=()=>{
        setUser(null)
        setAccessToken(null)
        localStorage.removeItem("user")
        localStorage.removeItem("access_token")
    }

    useEffect(()=>{
        const storedUser = localStorage.getItem("user")
        if(storedUser){
            setUser(JSON.parse(storedUser))
        }
    },[])

    return(
        <AuthContext.Provider value={{access_token,user , login , logout}}>
            {children}
        </AuthContext.Provider>
    )

}

export const useAuth=()=>{
    return useContext(AuthContext)
}