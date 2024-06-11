import Navbar from "./Navbar";
import { useLocation } from "react-router";

export default function AnimeInfoPage(){
    const location = useLocation();
    const name = location.state.name
    const studios = location.state.studios
    const genres = location.state.genres
    const score = location.state.score
    const img = location.state.img
    
    console.log(img)
    return (
        <>
            <Navbar/>
            <div className="mt-[5rem] ml-[22rem] text-xl">
                <img className="rounded-lg" src={img}/>
                <div className="m-[1rem]">{name}</div>
                <div>{studios}</div>
            </div>
        </>
    )
}