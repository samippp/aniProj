import { useEffect, useState } from "react";
import axios from 'axios'
import { json } from "react-router-dom";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


const Body = ({ user_id }) => {
  const [animeTopTen, setAnimeTopTen] = useState(null);
  const [searchAnime, setSearchAnime] = useState(null);
  
  async function addFavorite(e: { preventDefault: () => void; }, userId: string, productId: number) {
    e.preventDefault();
  }

  async function search(e: { preventDefault: () => void; }) {

  }

  async function getFavourites(){
  }
  useEffect(()=>{
    async function fetchTopTen(){
      await axios.get('http://127.0.0.1:8000/api/anime_list/10')
      .then((response) =>{
        console.log(response)
      })
      .catch((error)=>{
        console.log(error)
      })
    }
    fetchTopTen();
  },[])

  return (
    <>
      <div className="pl-[18.5%] my-12 grid grid-cols-2">
        <div className="flex">
          <div className="cursor-pointer max-w-sm w-24 hover:text-blue-600"
            onClick={() => {}}
          >HOME</div>
          <div className="cursor-pointer max-w-sm w-36 hover:text-blue-600"
            onClick={() => {}}
          >USER STATISTICS</div>
          <div className="cursor-pointer max-w-sm hover:text-blue-600"
            onClick={() => {getFavourites()}}
          >FAVOURITES</div>
        </div>
        <div className="ml-48 flex centered-item">
          <form onSubmit={search}>
            <input
              value={searchAnime}
              onChange={(e) => setSearchAnime(e.target.value)}
              type="Item"
              placeholder="Search"
              className="block l-12 w-64 p-2 text-black bg-white border border-gray-500 rounded-lg appearance-none placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
              autoComplete="off"
            />
            <button
              type="submit"
            >Search</button>
          </form>
        </div>
      </div>
      <div className="flex flex-wrap justify-center">
        
        <ToastContainer />
      </div>
    </>
  )
}

export default Body