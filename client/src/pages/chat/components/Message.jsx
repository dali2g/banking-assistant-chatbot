import React from "react";

const Message = ({ message }) => {
  const senderLabel = message.role === "Assistant" ? "Assistant" : "You";
  const style = message.role === "Assistant" ? "bg-[#18181E]" : "bg-[#18181E]";

  return (
    <div
      className={`flex ${
        message.role === "Assistant" ? "justify-start" : "justify-end"
      }`}
    >
      <div
        className={`${style} p-4 rounded-lg max-w-[400px] min-w-[100px] text-white`}
      >
        <p className="text-sm font-bold pb-3">{senderLabel}</p>
        <p className="text-balance list-decimal ml-4 whitespace-pre-line">
          {message.text}
        </p>
      </div>
    </div>
  );
};

export default Message;
