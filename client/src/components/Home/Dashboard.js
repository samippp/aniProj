import React from 'react'
import { useState } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from './Navbar';
import Body from './Body';

const Home = ({user_id,email}) => {
  const [isOpen, setIsOpen] = useState(false);
  //get email from login page
  const urlParams = new URLSearchParams(window.location.search);
  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };


  return (
    <> 
    <div className='mt-40'>
      <Body user_id={user_id}/>
    </div>
    
      <div className='justify-center flex'>
        <div className='absolute w-[150rem] top-0'>
          <Navbar email={email}/>
        </div>
      </div>
    </>
  )
}

export default Home