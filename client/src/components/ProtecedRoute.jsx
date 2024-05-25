import api from '../api'
import { REFRESH_TOEKN, ACCESS_TOKEN } from '../constants'
import { useState, useEffect } from 'react'

function ProtecedRoute({children}) {
    const [ isAuthorized, setIsAuthorized] = useState(null)

    useEffect(()=>{
        auth().catch(()=>setIsAuthorized(false))
    }, [])

    const refreshToken = async () =>{
        const refreshToken = localStorage.getItem(REFRESH_TOEKN);
        try{
            const res = await api.post("/api/token/refresh/", {
                refresh : refreshToken
            });
            if(res.status === 200){
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                setIsAuthorized(true)
            }
            else{
                setIsAuthorized(false)
            }
        }
        catch (error){
            console.log(error)
            setIsAuthorized(false)
        }
    }
    const auth = async () =>{
        const token = localStorage.getItem(ACCESS_TOKEN)
        if(! token){
            setIsAuthorized(false)
            return
        }
        const decoded = jwtDecode(token)
        const tokenExpiration = decoded.exp
        const now = Date.now() / 10000
        //check if token is expired
        if(tokenExpiration < now){
            await refreshToken()
        }
        else{
            setIsAuthorized(true)
        }
    }
    if(isAuthorized === null ){
        return <div>Loading...</div>;
    }

    return isAuthorized ? children : <Navigate to="/"/>;
}

export default ProtecedRoute;