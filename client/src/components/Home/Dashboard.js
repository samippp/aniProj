import { useEffect, useState } from "react";
import axios from 'axios'
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AnimePanel from "./AnimePanel";
import Navbar from "./Navbar";

const Body = ({ user_id }) => {
  const nav = useNavigate()
  const [animeFiveTen, setAnimeTopTen] = useState([]);
  const [favouriteAnime, setFavouriteAnime] = useState([]);
  const [searchAnime, setSearchAnime] = useState(null);
  const [likedAnime, setLikedAnime] = useState([])

  async function addFavorite(e: { preventDefault: () => void; }, userId: string, productId: number) {
    e.preventDefault();
  }

  async function search(e: { preventDefault: () => void; }) {

  }

  async function getFavourites(){
  }
  useEffect(()=>{
    async function fetchTopFive(){
      await axios.get('http://127.0.0.1:8000/api/anime_list/5')
      .then((response) =>{
        setAnimeTopTen(response.data)
      })
      .catch((error)=>{
        console.log(error)
      })
    }
    async function fetchLikedAnimeId(){
      await axios.post('http://127.0.0.1:8000/api/like_anime/',{
        "name" : localStorage.getItem('email')
      })
      .then((response) =>{
        for (const x in response.data){
          setLikedAnime(prev => [...prev, response.data[x]['anime']['id']])
        }
      })
      .catch((error)=>{
        console.log(error)
      })
    }
    fetchLikedAnimeId();
    fetchTopFive();

  },[])

  return (
    <>

          <Navbar/>
      <div className="grid grid-cols-3 my-24">
            <div className="max-w-sm block text-xl ml-[55%]">TOP TEN ANIME</div>
            <div></div>
            <div className="ml-[25%] cursor-pointer text-lg hover:underline" onClick={()=>{nav("/archives")}}>Show more</div>
      </div>
      {animeFiveTen[0] ? (
        <>
          <div>
          <div className="mx-[20%] grid grid-cols-5 space-0">
            {
              animeFiveTen.map((anime)=>{
                const fav = likedAnime.includes(anime.id) ? true : false
                  return (
                    <div className="w-[80%] h-[100%]">
                      <AnimePanel  
                        name={anime.name}
                        studios={anime.studios}
                        genres={anime.genres}
                        score={anime.score}
                        img={anime.img}
                        desc = {anime.desc}
                        favourited = {fav}
                      />
                    </div>
                  )
              })
            }
          </div>
          </div>
        </>
      ) : null}
      <div className="flex flex-wrap justify-center">
        <ToastContainer />
      </div>
    </>
  )
}

export default Body