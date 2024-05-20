import React from 'react';
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { Link } from 'react-router-dom';
import LoginForm from '../components/login/LoginForm'

const Login = ({setUser}) => {
  return (
    <>
        <LoginForm setUser={setUser}/>
    </>
  )
}

export default Login