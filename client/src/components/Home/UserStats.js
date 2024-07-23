import Navbar from "./Navbar";
import axios from "axios";
import { useEffect,useState } from "react";

export default function UserStats(){

    const [favouriteGenres, setFavouriteGenre] = useState()

    async function getFavouriteGenres(){
        axios.post("http://127.0.0.1:8000/api/favourite_genres/",{
            "name" : localStorage.getItem('email')
        })
        .then((response)=>{
            setFavouriteGenre(response.data[0])
            console.log(Object.keys(response.data[0]))
        })
        .catch((error)=>{
            console.log(error)
        })
    }

    useEffect(()=>{
        getFavouriteGenres()
    },[])

    return(
        <div>
            <Navbar/>
        </div>
    )
}