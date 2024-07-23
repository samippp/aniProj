import { useEffect, useState } from "react";
import axios from 'axios'
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AnimePanel from "./AnimePanel";
import Navbar from "./Navbar";
import {FaArrowCircleUp} from 'react-icons/fa'; 

const Body = ({ user_id }) => {
  const nav = useNavigate()
  const [animelist, setAnimelist] = useState([]);
  const [favouriteAnime, setFavouriteAnime] = useState([]);
  const [searchAnime, setSearchAnime] = useState(null);
  const [likedAnime, setLikedAnime] = useState([])
  const [arrow, setVisibleArrow] = useState(false);


  const toggleVisible = () => { 
    const scrolled = document.documentElement.scrollTop; 
    if (scrolled > 300){ 
      setVisibleArrow(true) 
    }  
    else if (scrolled <= 300){ 
      setVisibleArrow(false) 
    } 
  }; 

  window.addEventListener('scroll',toggleVisible);

const scrollToTop = () =>{ 
    window.scrollTo({ 
      top: 0,  
      behavior: 'smooth'
    }); 
}; 

  async function search(e: { preventDefault: () => void; }) {

  }

  async function fetchTopX(num){
    await axios.get('http://127.0.0.1:8000/api/anime_list/'+num)
    .then((response) =>{
      setAnimelist(response.data)
    })
    .catch((error)=>{
      console.log(error)
    })
  }
  useEffect(()=>{
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
    fetchTopX(5);

  },[])


  return (
    <>

          <Navbar/>
      <div className="grid grid-cols-3 my-24">
            <div className="max-w-sm block text-xl ml-[55%]">TOP TEN ANIME</div>
            <div></div>
            <div className="ml-[25%] cursor-pointer text-lg hover:underline" onClick={()=>{ animelist.length== 5 ? fetchTopX(50) : fetchTopX(5)}}>
              {animelist.length== 5 ? "Show more": "Show Less"}
            </div>
      </div>
      {animelist[0] ? (
        <>
          <div>
          <div className="mx-[20%] grid grid-cols-5 space-0">
            {
              animelist.map((anime,index)=>{
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
      {arrow ? 
                <FaArrowCircleUp onClick={scrollToTop} className="cursor-pointer fixed bottom-0 right-[12rem] content-center size-[3rem] m-[2%]"/>
            : null}
    </>
  )
}

export default Body