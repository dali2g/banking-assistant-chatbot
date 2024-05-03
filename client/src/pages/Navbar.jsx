import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { logout, user } = useAuth();
  return (
    <header className="bg-[#18181E] sticky top-0 h-[80px] flex justify-between items-center px-8">
      <span className="text-2xl font-bold uppercase text-white">
        Banking <span className="text-blue-600 font-semibold">Assistant</span>
      </span>
      <div>
        {user ? (
          <button
            className="font-semibold   hover:ring hover:ring-white transition duration-300 inline-flex items-center justify-center rounded-md text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-white text-black h-10 px-4 py-2"
            onClick={logout}
          >
            Log out
          </button>
        ) : (
          <Link
            className="font-semibold   hover:ring hover:ring-white transition duration-300 inline-flex items-center justify-center rounded-md text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-white text-black h-10 px-4 py-2"
            to="/login"
          >
            Log in
          </Link>
        )}
      </div>
    </header>
  );
}
