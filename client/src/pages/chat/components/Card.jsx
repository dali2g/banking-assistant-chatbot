import React from "react";

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

export default Card;
