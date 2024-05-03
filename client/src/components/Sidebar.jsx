import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function Sidebar() {
  const { logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const LogoutButton = () => {
    return (
      <button onClick={logout} className="w-full">
        <div className="flex items-center justify-center pb-" title="Logout">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="1.5"
            stroke="currentColor"
            className="h-6 w-6 cursor-pointer text-gray-500 hover:text-blue-600"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"
            />
          </svg>
        </div>
      </button>
    );
  };

  return (
    <>
      {/* Sidebar */}
      <div
        className={`lg:flex z-50 fixed h-full lg:left-0 justify-center w-24 bg-[#18181E] transition-all duration-300 ${
          isOpen ? "lg:translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        <div className="my-auto flex flex-col items-center space-y-10">
          <div className="flex items-center justify-center rounded-md p-4 text-blue-600 font-bold text-center">
            Banking Bot
          </div>

          <div className="space-y-48 rounded-md">
            <ul>
              <li className="p-5">
                <div className=" cursor-pointer text-gray-500 transition-all hover:text-blue-600">
                  MENU1
                </div>
              </li>

              <li className="p-5 ">
                <div className=" cursor-pointer text-gray-500 transition-all hover:text-blue-600">
                  MENU2
                </div>
              </li>
            </ul>
            <LogoutButton />
          </div>
        </div>
      </div>

      {/* Button for toggling sidebar on mobile */}
      <button
        className="lg:hidden fixed bottom-[50%] right-5 z-50 p-3 bg-blue-600 text-white rounded-full shadow-lg"
        onClick={toggleSidebar}
      >
        {isOpen ? (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16m-7 6h7"
            />
          </svg>
        )}
      </button>
    </>
  );
}
