import Navbar from "./Navbar";
import { useEffect, useState } from "react";
import axios from "axios";
import AnimePanel from "./AnimePanel";
import {FaArrowCircleUp} from 'react-icons/fa'; 

export default function TopAnimePage(){
    const [animeDataset, setAnimeDataset] = useState([]);
    const [visible, setVisible] = useState(false);
    
    const toggleVisible = () => { 
        const scrolled = document.documentElement.scrollTop; 
        if (scrolled > 300){ 
          setVisible(true) 
        }  
        else if (scrolled <= 300){ 
          setVisible(false) 
        } 
    }; 

    const scrollToTop = () =>{ 
        window.scrollTo({ 
          top: 0,  
          behavior: 'smooth'
        }); 
    }; 

    useEffect(()=>{
        async function fetchAnime(){
          await axios.get('http://127.0.0.1:8000/api/anime_list/50')
          .then((response) =>{
            setAnimeDataset(response.data)
            console.log(response.data)
          })
          .catch((error)=>{
            console.log(error)
          })
        }
        fetchAnime();
    },[])

    window.addEventListener('scroll',toggleVisible);
    
    return(
        <>
            <Navbar/>
            <div className="max-w-sm block text-xl ml-[20%] my-[5%]">TOP TEN ANIME</div>
            {animeDataset[0] ? (
            <div>
            <div className="mx-[20%] grid grid-cols-5 space-0 my-[5%]">
                {
                animeDataset.map((anime)=>{
                    return (
                    <div className="w-[80%] h-[100%]">
                        <AnimePanel  
                        name={anime.name}
                        studios={anime.studios}
                        genres={anime.genres}
                        score={anime.score}
                        img={anime.img}
                        />
                    </div>
                    )
                })
                }
            </div>
            </div>
            ) : null}

            {visible ? 
                <FaArrowCircleUp onClick={scrollToTop} className="cursor-pointer fixed bottom-0 right-[12rem] content-center size-[3rem] m-[2%]"/>
            : null}
        </>
    )
}