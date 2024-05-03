import React from "react";
import { Link } from "react-router-dom";
import Navbar from "./Navbar";
const Home = () => {
  return (
    <>
      <Navbar />
      <div className="bg-[#0F0F15] text-white flex min-h-screen flex-col items-center pt-40 sm:justify-center sm:pt-0">
        <h1 className="text-4xl sm:text-6xl font-bold mb-8 text-center">
          Welcome to the &nbsp;
          <span className="text-blue-600 font-semibold">
            Banking Chatbot App!
          </span>
        </h1>
        <p className="text-lg sm:text-2xl mb-8 text-center">
          Chat with our intelligent banking assistant for all your banking
          needs. 💬💼
        </p>
        <Link
          to="/login"
          className="font-semibold w-full max-w-sm hover:bg-black hover:text-white hover:ring hover:ring-white transition duration-300 inline-flex items-center justify-center rounded-md text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-white text-black h-10 px-4 py-2"
        >
          Log in
        </Link>
      </div>
    </>
  );
};

export default Home;
