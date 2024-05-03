import { useEffect, useRef, useState } from "react";

export default function ChatPage() {
  const [isTyping, setIsTyping] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const Card = ({ suggestion, onClick }) => {
    return (
      <button
        onClick={() => onClick(suggestion)}
        className="border font-bold flex justify-center items-center py-2 px-4 rounded-2xl text-white break-words max-w-[400px] cursor-pointer"
      >
        <p className="text-pretty">{suggestion}</p>
      </button>
    );
  };

  const handleSuggestionClick = async (suggestion) => {
    const newMessage = {
      text: suggestion,
      role: "User",
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setIsTyping(true);
    await processMessage();
  };

  const Hero = () => {
    const suggestionData = [
      "Check my balance?",
      "What are your services ?",
      "What is my transaction history ?",
    ];

    return (
      <div
        className={`w-full h-[350px] text-white flex flex-col justify-center items-center space-y-24 `}
      >
        <div className="">
          <h1 className="text-4xl font-bold">Good evening, Adam.</h1>
          <p className="text-3xl">
            What <span className="text-blue-600 font-semibold">can</span> I help
            you with?
          </p>
        </div>

        <div className="flex gap-2">
          {suggestionData.map((suggestion, index) => (
            <Card
              key={index}
              suggestion={suggestion}
              onClick={() => handleSuggestionClick(suggestion)}
            />
          ))}
        </div>
      </div>
    );
  };
  const handleSendMessage = async (e) => {
    e.preventDefault();

    const newMessage = {
      text: message,
      role: "User",
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    setMessage("");

    //gpt is typing
    setIsTyping(true);
    await processMessage();
  };

  async function processMessage() {
    await new Promise((resolve) => setTimeout(resolve, 3000));
    const botRes = {
      text: "im just hardcoded hahah",
      name: "Assistant",
    };

    setMessages((prevMessages) => [
      ...prevMessages,
      { text: botRes.text, role: "Assistant" },
    ]);
    setIsTyping(false);
  }
  const Message = ({ message }) => {
    const senderLabel = message.role === "Assistant" ? "Assistant" : "You";
    const style = message.role === "Assistant" ? "border" : "bg-[#18181E]";

    return (
      <div
        className={`flex ${
          message.role === "Assistant" ? "justify-start" : "justify-end"
        }`}
      >
        <div className={`${style} p-4 rounded-lg max-w-[400px] text-white`}>
          <p className="text-sm font-bold">{senderLabel}</p>
          <p>{message.text}</p>
        </div>
      </div>
    );
  };

  const Chatbox = ({ messages }) => {
    const messagesEndRef = useRef();

    const scrollToBottom = () => {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    return (
      <div className="w-full p-5 flex flex-col gap-2 pb-20">
        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}
        <div ref={messagesEndRef}></div>
      </div>
    );
  };

  return (
    <main className="">
      <div className="container max-w-4xl mx-auto">
        {/* MESSAGES CONTAINER */}
        {messages.length === 0 ? <Hero /> : <Chatbox messages={messages} />}

        {/* //SEND MESSAGE INPUT */}
        <div>
          <form onSubmit={handleSendMessage}>
            <div className="fixed bottom-0 w-full px-8 py-2 max-w-4xl mb-5">
              <div className="relative w-full">
                <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                  {isTyping && <div className="loading"></div>}
                </div>

                <input
                  type="text"
                  className="grow bg-[#18181E] text-gray-400 text-sm rounded-full py-4 block w-full ps-10 p-2.5 outline-none focus:border-2 border-blue-600 "
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
                    className="w-4 h-4 text-gray-500  hover:text-gray-400"
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
}

// <input
//             className="border-2 border-black"
//             placeholder="Type your message"
//             value={message}
//             onChange={(e) => setMessage(e.target.value)}
//           />
//           <button
//             className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-full"
//             type="submit"
//           >
//             Send
//           </button>
