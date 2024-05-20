import { useState } from 'react'
import { Route, Routes } from "react-router-dom"
import './App.css'
import Login from "./pages/Login.js"
import Register from './pages/Register.js'
import Dashboard from './components/Home/Dashboard.js'

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
      <Route path="/" element= {<Login setUser={setUser}/>} />
      <Route path="/create" element= {<Register />} />
      <Route path="/home" element= {<Dashboard user_id={user_id} email={email}/>} />
    </Routes>
  )
}

export default App
