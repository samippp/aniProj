import React from 'react';
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import { Link } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const LoginForm = ({setUser}) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e: { preventDefault: () => void; }) {
    e.preventDefault();
    try {
      if (!email) {
        console.error("You need a email")
        toast.warning("Missing email");
      }
      else if (!password) {
        console.error("You need a password")
        toast.warning("Missing password");
      }
      else {
        const response = await axios.post('http://localhost:5000/login', { "email": email, "password": password });  //go to database and see response
        
        console.log(response);

        const { token, user_id } = response.data;

        // Store the token in localStorage
        localStorage.setItem('token', token);
        setUser(user_id,email);
        
        toast.success("Success!")
        // Redirect to home page
        navigate('/home');

      }
    } catch (error) {
      toast("Incorrect Login");
      console.error("login error:", error);
    }

  }

  return (
    <section>
      <div className="relative items-center w-full px-5 py-40 mx-auto md:px-12 lg:px-20 max-w-7xl">
        <div className="w-full max-w-md mx-auto md:max-w-sm md:px-0 md:w-96 sm:px-4">
          <div className="flex flex-col">
            <div>
              <h2 className="text-4xl text-black text-center">SIGN IN</h2>
            </div>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="mt-4 space-y-6">
              <div className="col-span-full">
                <label className="block mb-3 text-sm font-medium text-gray-600" htmlFor="password">
                  Email
                </label>
                <input
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full px-6 py-3 text-black bg-white border border-gray-200 rounded-full appearance-none placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
                  placeholder="user@email.com"
                  autoComplete="off"
                />
              </div>
              <div className="col-span-full">
                <label className="block mb-3 text-sm font-medium text-gray-600" htmlFor="confirm_password">
                  Password
                </label>
                <input
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full px-6 py-3 text-black bg-white border border-gray-200 rounded-full appearance-none placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
                  placeholder="******"
                  autoComplete="off"
                  type="password"
                />
              </div>

              <div className="col-span-full">
                <button
                  className="items-center justify-center w-full px-6 py-2.5 text-center text-white duration-200 bg-black border-2 border-black rounded-full nline-flex hover:bg-transparent hover:border-black hover:text-black focus:outline-none focus-visible:outline-black text-sm focus-visible:ring-black"
                  type="submit"
                >
                  Sign in
                </button>
                <ToastContainer />
              </div>
              <div className="col-span-full">
                <Link to="/create"
                  className="items-center justify-center w-full px-3 text-center text-black duration-200 hover:text-slate-400 "
                  type="submit"
                >
                  Register for a new Account
                </Link>
              </div>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}

export default LoginForm;
