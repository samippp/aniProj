import React, { useState } from "react";

export default function Modal( {visible, email} ) {

    if(!visible)
        return null
    else{
        return (
            <>
            <div className="bg-white text-wrap overflow-hidden absolute top-28 w-[300px] border-2 rounded-lg p-4">
                <div className="inline-block w-64 ">
                    <p className="cursor-pointer py-2 group/item hover:bg-slate-100 rounded-lg p-4">{email}</p>
                    <p className="cursor-pointer py-2 group/item hover:bg-slate-100 rounded-lg p-4">Home Page</p>
                    <p className="cursor-pointer py-2 group/item hover:bg-slate-100 rounded-lg p-4">Favourite Items</p>
                    <p className="cursor-pointer py-2 group/item hover:bg-slate-100 rounded-lg p-4">Account Details</p>
                    <p className="cursor-pointer py-2 group/item hover:bg-slate-100 rounded-lg p-4">Logout</p>
                </div>
            </div>
            </>
        )
    }

}