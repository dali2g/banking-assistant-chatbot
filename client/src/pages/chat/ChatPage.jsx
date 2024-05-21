import React, { useState } from "react";
import { Hero, Chatbox } from "./components/index";
import { useAuth } from "../../context/AuthContext";
import { useTheme } from "../../hooks/ThemeProvider";

const ChatPage = () => {
  const { generate } = useAuth();
  const [isTyping, setIsTyping] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const { isDarkMode } = useTheme();
  const handleSuggestionClick = async (suggestion) => {
    const newMessage = {
      text: suggestion,
      role: "User",
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setIsTyping(true);
    await processMessage(suggestion);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    const newMessage = {
      text: message,
      role: "User",
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setMessage("");
    setIsTyping(true);
    await processMessage(message);
  };

  async function processMessage(message) {
    try {
      const response = await generate(message);
      let textResponse = response.message;
      if (textResponse === "") {
        textResponse = "Error while handling the query";
      }
      // set generated response
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: textResponse, role: "Assistant" },
      ]);
      setIsTyping(false);
    } catch (error) {
      console.error("Error generating response:", error);
    }
  }

  return (
    <main className="">
      <div className="container max-w-4xl mx-auto">
        {/* MESSAGES CONTAINER */}
        {messages.length === 0 ? (
          <Hero
            suggestionData={[
              "Check my current balance",
              "What are your services?",
              "What is my transaction history?",
            ]}
            handleSuggestionClick={handleSuggestionClick}
          />
        ) : (
          <Chatbox messages={messages} />
        )}

        {/* SEND MESSAGE INPUT */}
        <div>
          <form onSubmit={handleSendMessage}>
            <div className="fixed bottom-0 w-full px-8 py-2 max-w-4xl mb-5">
              <div className="relative w-full">
                <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                  {isTyping && <div className="loading"></div>}
                </div>

                <input
                  type="text"
                  className="grow bg-[#18181E] text-gray-400 text-sm rounded-full py-4 block w-full ps-10 p-2.5 outline-none focus:border-2 border-blue-600"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Start here to talk or chat"
                  disabled={isTyping}
                  required
                />

                <button
                  type="submit"
                  className="absolute inset-y-0 end-0 flex items-center pe-3"
                >
                  <svg
                    className="w-4 h-4 text-gray-500 hover:text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                    fill="none"
                  >
                    <path
                      d="M21.707 2.293a1 1 0 0 0-1.069-.225l-18 7a1 1 0 0 0 .145 1.909l8.379 1.861 1.862 8.379a1 1 0 0 0 .9.78L14 22a1 1 0 0 0 .932-.638l7-18a1 1 0 0 0-.225-1.069zm-7.445 15.275L13.1 12.319l2.112-2.112a1 1 0 0 0-1.414-1.414L11.681 10.9 6.432 9.738l12.812-4.982z"
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </main>
  );
};

export default ChatPage;
