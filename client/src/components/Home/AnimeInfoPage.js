import Navbar from "./Navbar";
import { useLocation } from "react-router";

export default function AnimeInfoPage(){
    const location = useLocation();
    const name = location.state.name
    const desc = location.state.desc
    const studios = location.state.studios
    const genres = location.state.genres
    const score = location.state.score
    const img = location.state.img
    
    console.log(genres)
    return (
        <>
            <Navbar/>
            <div className="mt-[5rem] ml-[22rem]">
                <div className="flex">
                    <img className="rounded-lg" src={img}/>
                    <div className="ml-[1rem] mr-[22rem] block">
                        <div className="text-2xl mb-[1rem] font-semibold">{name}</div>
                        <div>Studios: {studios}</div>
                        <div>Genres: {genres}</div>
                        <div>{score}/10</div>
                    </div>
                </div>
                <div className="text-lg mt-[2rem] mr-[22rem]">
                    <div className="mb-[2rem] font-semibold">Synopsis</div>
                    <div>{desc}</div>
                </div>
            </div>
        </>
    )
}