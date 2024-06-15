import { useState } from 'react'
import { Route, Routes, Navigate} from "react-router-dom"
import './App.css'
import Login from "./pages/Login.js"
import Register from './pages/Register.js'
import Dashboard from './components/Home/Dashboard.js'
import ProtecedRoute from './components/ProtecedRoute.jsx'
import TopAnimePage from './components/Home/TopAnimePage.js'
import AnimeInfoPage from './components/Home/AnimeInfoPage.js'
import Favourites from './components/Home/Favourites.js'

function Logout(){
  localStorage.clear()
  return <Navigate to="/login"/>
}
function RegisterAndLogout(){
  localStorage.clear()
  return <Navigate to="/create"/>
}
function App() {

  const [user_id, set_id] = useState("");
  const [email, set_Email] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(user_id !== ""); 

  const setUser = (user_id: string, email: string) => {
    set_id(user_id);
    set_Email(email);
    setIsLoggedIn(user_id !== "");
  }

  return (
    <Routes>

      <Route path="/login" element= {<Login setUser={setUser}/>} />
      <Route path="/create" element= {<Register />} />
      <Route path="/" element= {
        <ProtecedRoute>
          <Dashboard user_id={user_id} email={email}/>
        </ProtecedRoute>
      } />
      <Route path="/archives" element = {<TopAnimePage/>}/>
      <Route path="/AnimeInfo" element = {<AnimeInfoPage/>}/>
      <Route path="/Favourite" element = {<Favourites/>}/>
    </Routes>
  )
}

export default App
