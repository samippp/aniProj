import {useState} from "react"
import Modal from "./Modal"
import { useNavigate } from "react-router";

export default function Navbar( { getFavourites, search, searchAnime, setSearchAnime} ){
  const [showModal, setModal] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const nav = useNavigate()
  
    return (
        <>
        <div className="w-full mx-auto bg-white border-b 2xl:max-w-7xl">
          <div className="relative flex flex-col w-full p-5 mx-auto bg-white md:items-center md:justify-between md:flex-row md:px-6 lg:px-8">
            <div className="flex flex-row items-center justify-between lg:justify-start">
              <a className="text-lg tracking-tight text-black uppercase focus:outline-none focus:ring lg:text-2xl" >
                <span className="lg:text-lg uppecase focus:ring-0 text-1xl">
                  KONGSTER
                </span>
              </a>
            </div>
            <nav className={isOpen ? 'flex-col items-center flex-grow md:flex md:justify-end md:flex-row' : 'hidden md:flex md:justify-end md:flex-row'}>
              <a className="cursor-pointer px-2 py-2 text-sm text-gray-500 lg:px-6 md:px-3 hover:text-blue-600 lg:ml-auto" >
                About
              </a>
              <a className="cursor-pointer px-2 py-2 text-sm text-gray-500 lg:px-6 md:px-3 mr-3 hover:text-blue-600" >
                Contact
              </a>
              <button 
              onClick={() => setModal(!showModal)}
              className="inline-flex p-2 rounded-full bg-gray-300 focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 hover:bg-gray-700 focus-visible:outline-blue-900">
                <svg xmlns="http://www.w3.org/2000/svg" height="23" viewBox="0 -960 960 960" width="23"><path d="M480-480q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM160-160v-112q0-34 17.5-62.5T224-378q62-31 126-46.5T480-440q66 0 130 15.5T736-378q29 15 46.5 43.5T800-272v112H160Zm80-80h480v-32q0-11-5.5-20T700-306q-54-27-109-40.5T480-360q-56 0-111 13.5T260-306q-9 5-14.5 14t-5.5 20v32Zm240-320q33 0 56.5-23.5T560-640q0-33-23.5-56.5T480-720q-33 0-56.5 23.5T400-640q0 33 23.5 56.5T480-560Zm0-80Zm0 400Z"/></svg>
              </button>
              <Modal visible={showModal}/>
            </nav>
          </div>
        </div>
        <div className="pl-[18.5%] my-12 grid grid-cols-2">
          <div className="flex">
            <div className="cursor-pointer max-w-sm w-24 hover:text-blue-600"
              onClick={() => {nav("/")}}
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
            </form>
          </div>
        </div>
        </>
    )
}