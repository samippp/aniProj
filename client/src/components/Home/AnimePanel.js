import { useNavigate } from "react-router"
import { useEffect, useState } from "react";
import axios from "axios";

export default function AnimePanel({name, studios, genres, score, img ,desc, favourited}){
    const nav = useNavigate();
    const initLikedState = favourited == true ? 'Unlike' : 'Like'
    const [liked, setLiked] = useState(initLikedState)

    const viewItem = (name, studios, genres, score, img, desc) => {
        nav("/AnimeInfo",{state:{
            name: name,
            studios : studios,
            genres : genres,
            score : score, 
            img: img,
            desc : desc,
            likedState : liked
        }})
    }

    async function addToLiked(){
        axios.post("http://127.0.0.1:8000/api/add_to_liked_anime/",{
            "name": localStorage.getItem('email'),
            "anime" : name
        })
        .then((response)=>{
            setLiked('Unlike')
        })
        .catch((error)=>{
            console.log(error)
        })
    }
    async function removeFromLiked(){
        axios.post("http://127.0.0.1:8000/api/remove_from_liked_anime/",{
            "name": localStorage.getItem('email'),
            "anime" : name
        })
        .then((response)=>{
            setLiked('Like')
        })
        .catch((error)=>{
            console.log(error)
        })
    }
    
    return ( <>
        <div className="relative">
        <img className="h-[18rem] rounded-lg" src={img} alt="item" />
        <div className="font-medium">{name}</div>
        <div className="font-medium">{score}</div>
        <div className="absolute inset-0 flex items-center justify-center bg-opacity-50 bg-black opacity-0 hover:opacity-100 transition-opacity duration-300 rounded-lg m-[-0.5rem]">
            <div className="flex flex-col space-y-2">
            <button
                type="button"
                onClick={() => viewItem(name, studios, genres, score, img, desc)}
                className="text-white bg-gray-800 hover:bg-gray-900 font-medium rounded-lg text-sm px-5 py-2.5"
            >
                View
            </button>
            <button
                type="button"
                onClick={(e) => {liked == 'Like'? addToLiked():removeFromLiked()}}
                className="text-white bg-gray-800 hover:bg-gray-900 font-medium rounded-lg text-sm px-5 py-2.5"
            >
                {liked}
            </button>
            </div>
        </div>
        </div>
    </> )
}