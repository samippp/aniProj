import Navbar from "./Navbar";
import { useState, useEffect } from "react";
import { useLocation } from "react-router";
import axios from "axios";

export default function AnimeInfoPage({favourited}) {
    const location = useLocation();
    const name = location.state.name;
    const desc = location.state.desc;
    const studios = location.state.studios;
    const genres = location.state.genres;
    const score = location.state.score;
    const img = location.state.img;
    const [ratingModal, setVisible] = useState(false);
    const [userRating, setUserRating] = useState(null)
    const [liked, setLiked] = useState(false)

    async function setRating({rating}){
        axios.patch("http://127.0.0.1:8000/api/search_anime_from_liked/",{
            "name" : localStorage.getItem('email'),
            "anime" : name,
            "rating" : rating
        })
        .then((response)=>{
            setUserRating(response.data['rating'])
        })
        .catch((error)=>{
            console.log(error)
        })
        setVisible(false)
    }

    async function searchLikedExists(){
        axios.post("http://127.0.0.1:8000/api/search_anime_from_liked/",{
            "name": localStorage.getItem('email'),
            "anime" : name
        })
        .then((response)=>{
            response.data['user'] ? setLiked(true) : setLiked(false)
            if(response.data['rating'] !== null)
                setUserRating(response.data['rating'])
        })
        .catch((error)=>{
            console.log(error)
        })
    }

    async function addToLiked(){
        axios.post("http://127.0.0.1:8000/api/add_to_liked_anime/",{
            "name": localStorage.getItem('email'),
            "anime" : name
        })
        .then((response)=>{
            setLiked(true)
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
            setLiked(false)
            setUserRating(null)
        })
        .catch((error)=>{
            console.log(error)
        })
    }
    useEffect(()=>{
        searchLikedExists()
    },[])

    return (
        <>
            <Navbar />
            <div className="mt-[5rem] ml-[22rem]">
                <div className="flex">
                    <img className="rounded-lg" src={img} alt={name}/>
                    <div className="ml-[1rem] mr-[22rem] block relative">
                        <div className="text-2xl mb-[1rem] font-semibold">{name}</div>
                        <div>Studios: {studios.join(', ')}</div>
                        <div>Genres: {genres.join(', ')}</div>
                        <div>Average Rating: {score}/10</div>
                        <button
                            type="button"
                            onClick={(e) => {liked == false? addToLiked():removeFromLiked()}}
                            className="text-white bg-gray-800 hover:bg-gray-900 font-medium rounded-lg text-sm px-5 py-[2%] mt-[5%]"
                        >
                            {liked ? "Unlike": "Like"}
                        </button>
                        <div 
                            className="cursor-pointer rounded-lg border-black border-[1px] mt-4 w-[70%] hover:bg-slate-200"
                            onClick={() => {liked ? setVisible(!ratingModal) : setVisible(ratingModal)}}
                        >
                            <div className="m-1 pl-[4%]">{userRating? "Your Rating: " + userRating: "Rate"}</div>
                        </div>
                        {ratingModal && (
                            <div className="absolute top-[69%] left-0 right-0 border mt-2 p-2 bg-white z-10 shadow-lg">
                                <ul className="w-full">
                                    {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(rating => (
                                        <li key={rating} className="hover:bg-gray-200 p-1 cursor-pointer" onClick={()=>setRating({rating})}>
                                            {rating}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>
                <div className="text-lg mt-[2rem] mr-[22rem]">
                    <div className="mb-[2rem] font-semibold">Synopsis</div>
                    <div>{desc}</div>
                </div>  
            </div>
        </>
    );
}