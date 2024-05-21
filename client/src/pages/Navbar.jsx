import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../hooks/ThemeProvider";

export default function Navbar() {
  const { logout, user } = useAuth();
  const { isDarkMode, toggleDarkMode } = useTheme();
  return (
    <header
      className={`sticky top-0 h-[80px] flex justify-between items-center px-8 ${
        isDarkMode ? "bg-white" : "bg-[#18181E]"
      }`}
    >
      <span
        className={`text-2xl font-bold uppercase  ${
          isDarkMode ? "text-black" : "text-white"
        }`}
      >
        Banking <span className="text-blue-600 font-semibold">Assistant</span>
      </span>
      <div className="flex gap-5">
        <button
          className={`font-semibold hover:ring hover:ring-white transition duration-300 inline-flex items-center justify-center rounded-md text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 h-10 px-4 py-2 ${
            isDarkMode ? "bg-black text-white" : "bg-white text-black"
          }`}
          onClick={toggleDarkMode}
        >
          {isDarkMode ? "Light" : "Dark"}
        </button>
        {user ? (
          <button
            className={`font-semibold hover:ring hover:ring-white transition duration-300 inline-flex items-center justify-center rounded-md text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 h-10 px-4 py-2 ${
              isDarkMode ? "bg-black text-white" : "bg-white text-black"
            }`}
            onClick={logout}
          >
            Log out
          </button>
        ) : (
          <Link
            className={`font-semibold hover:ring hover:ring-white transition duration-300 inline-flex items-center justify-center rounded-md text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 h-10 px-4 py-2 ${
              isDarkMode ? "bg-black text-white" : "bg-white text-black"
            }`}
            to="/login"
          >
            Log in
          </Link>
        )}
      </div>
    </header>
  );
}
