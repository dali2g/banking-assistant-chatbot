import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import LoginPage from "./pages/login/LoginPage";
import ChatPage from "./pages/chat/ChatPage";
import { useAuth } from "./context/AuthContext";
import Navbar from "./pages/Navbar";
function App() {
  const { user } = useAuth();
  return (
    <>
      {user && <Navbar />}
      <Routes>
        <Route path="/" index element={user ? <ChatPage /> : <Home />} />
        <Route path="/login" element={user ? <ChatPage /> : <LoginPage />} />
        <Route path="/chat" element={user ? <ChatPage /> : <Home />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </>
  );
}

export default App;
