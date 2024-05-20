import { useEffect, useState } from "react";
import axios from 'axios'
import { json } from "react-router-dom";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


const Body = ({ user_id }) => {
  const [item, setItem] = useState("")
  const [gender, setGender] = useState("")
  const [dataSet, setData] = useState([])
  const [fav, setFav]  = useState(false);
  
  async function addFavorite(e: { preventDefault: () => void; }, userId: string, productId: number) {
    e.preventDefault();

    if (gender === "men") {
      await axios.post('http://localhost:5000/add_fav_male', { "user_id": userId, "product_id": productId })
        .then((response) => {
          toast.success("Item added to favorites");
          console.log(response);
        })
        .catch((error) => {
          toast.warning("Already added");
          console.log(error)
        })
    }
    else {
      await axios.post('http://localhost:5000/add_fav_female', { "user_id": userId, "product_id": productId })
        .then((response) => {
          toast.success("Item added to favorites");
          console.log(response);
        })
        .catch((error) => {
          toast.warning("Something went wrong");
          console.log(error)
        })
    }

  }

  async function search(e: { preventDefault: () => void; }) {
    e.preventDefault();
    console.log(item)
    console.log()
    await axios.post('http://localhost:5000/searchItems', { "item": item, "gender": gender })
      .then((response) => {
        console.log(response);
        const itemData = (response.data).rows
        setData(itemData)

      })
      .catch((error) => {
        console.log(error)
      })

  }

  async function viewItem(brand: string, name: string, id: number, seller: string) {
    if (seller == "ss")
      window.open(`https://www.ssense.com/en-ca/${gender}/product/${brand}/${name}/${id}`, '_blank');
    else
      window.open(`https://www.farfetch.com/ca/shopping/${gender}/${brand} ${name} ${id}.aspx`);
  }

  async function getMaleItems() {
    setGender("men")
    await axios.get('http://localhost:5000/getMaleItems')
      .then((response) => {
        const itemData = (response.data).rows
        setData(itemData)
        console.log(itemData[1]['img'])
      })
      .catch((error) => {
        console.error(error)
      })
      
  }

  async function getFemaleItems() {
    setGender("women")
    await axios.get('http://localhost:5000/getFemaleItems')
      .then((response) => {
        const itemData = (response.data).rows
        console.log(itemData)
        setData(itemData)
      })
      .catch((error) => {
        console.error(error)
      })

  }

  async function getFavourites(){
    await axios.post('http://localhost:5000/get_fav_male',{"user_id" :user_id})
    .then((response) => {
      const itemData = (response.data).rows
      console.log(Array.isArray(itemData))
      setData(itemData)
    })
    .catch((error) => {
      console.error(error)
    })


  }
  return (
    <>
      <div className="pl-[18.5%] my-12 grid grid-cols-2">
        <div className="flex">
          <div className="cursor-pointer max-w-sm w-24 hover:text-blue-600"
            onClick={() => { getMaleItems() }}
          >MEN</div>
          <div className="cursor-pointer max-w-sm w-28 hover:text-blue-600"
            onClick={() => { getFemaleItems() }}
          >WOMEN</div>
          <div className="cursor-pointer max-w-sm hover:text-blue-600"
            onClick={() => {getFavourites()}}
          >FAVOURITES</div>
        </div>
        <div className="ml-48 flex centered-item">
          <form onSubmit={search}>
            <input
              value={item}
              onChange={(e) => setItem(e.target.value)}
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
        {dataSet[0] ? (
          <div className="grid grid-cols-3 justify-items-center gap-9 py-8  mx-auto max-w-7xl">
            {dataSet.slice(0, 9).map((itemData, index) => (
              <div key={index} className="shadow-md rounded relative p-2 mb-4">
                <img src={itemData.img} className="object-contain h-96 w-56" alt="Product" />
                <div className="truncate text-ellipsis opacity-0 hover:opacity-100 bg-zinc-50/[.4] duration-[450ms] backdrop-blur-[10px] backdrop-opacity-100 absolute inset-0 flex flex-col justify-center items-center text-slate-950 font-semibold">
                  <span>{itemData.name}</span>
                  <span>${itemData.price}</span>
                  <span>{itemData.brand}</span>
                  <br />
                  <button type="button" onClick={() => viewItem(itemData.brand, itemData.name, itemData.product_id, itemData.seller)} className="text-white bg-gray-800 hover:bg-gray-900 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700">
                    View
                  </button>
                  <button type="button" onClick={(e) => addFavorite(e, user_id,itemData.product_id)} className="text-white bg-gray-800 hover:bg-gray-900  font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700">
                    Favorite
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : null}
        <ToastContainer />
      </div>
    </>
  )
}

export default Body