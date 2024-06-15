import Navbar from "./Navbar";
import axios from "axios";
import { useEffect ,useState } from "react";
import AnimePanel from "./AnimePanel";

export default function Favourites({}){
    const [likedAnime, setLikedAnime] = useState([])

    useEffect(()=>{
        async function fetchLikedAnime(){
          await axios.post('http://127.0.0.1:8000/api/like_anime/',{
            "name" : localStorage.getItem('email')
          })
          .then((response) =>{
            setLikedAnime(response.data)
          })
          .catch((error)=>{
            console.log(error)
          })
        }
        fetchLikedAnime();
      },[])
    return (
        <>
            <Navbar/>
            <div className="max-w-sm block text-xl ml-[22rem] my-[6rem] mb-[6rem]">YOUR LIKED ANIME</div>
            {likedAnime ? (
                <>
                <div>
                <div className="mx-[20%] grid grid-cols-5 space-0">
                    {
                    likedAnime.map((data)=>{
                        return (    
                        <div className="w-[80%] h-[100%]">
                            <AnimePanel  
                            name={data.anime.name}
                            studios={data.anime.studios}
                            genres={data.anime.genres}
                            score={data.anime.score}
                            img={data.anime.img}
                            desc = {data.anime.desc}
                            favourited={true}
                            />
                        </div>
                        )
                    })
                    }
                </div>
                </div>
                </>
            ) : null}
        </>
    )
}