import React, { useEffect, useRef } from "react";
import Message from "./Message";

const Chatbox = ({ messages }) => {
  const messagesEndRef = useRef();

  const scrollToBottom = () => {
    messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  return (
    <div className="w-full px-10  flex flex-col gap-4 pb-32 pt-20">
      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}
      <div ref={messagesEndRef}></div>
    </div>
  );
};

export default Chatbox;
