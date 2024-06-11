import { useNavigate } from "react-router"

export default function AnimePanel({name, studios, genres, score, img}){
    const nav = useNavigate();
    
    const viewItem = (name, studios, genres, score, img) => {
        nav("/AnimeInfo",{state:{
            name: name,
            studios : studios,
            genres : genres,
            score : score, 
            img: img
        }})
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
                onClick={() => viewItem(name, studios, genres, score, img)}
                className="text-white bg-gray-800 hover:bg-gray-900 font-medium rounded-lg text-sm px-5 py-2.5"
            >
                View
            </button>
            <button
                type="button"
                //onClick={(e) => addFavorite()}
                className="text-white bg-gray-800 hover:bg-gray-900 font-medium rounded-lg text-sm px-5 py-2.5"
            >
                Favorite
            </button>
            </div>
        </div>
        </div>
    </> )
}