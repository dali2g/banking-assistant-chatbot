import React from "react";
import Card from "./Card";
import { useAuth } from "../../../context/AuthContext";

const Hero = ({ suggestionData, handleSuggestionClick }) => {
  const { user } = useAuth();
  let name = user?.username;
  name = name[0].toUpperCase() + name.slice(1);

  return (
    <div
      className={`w-full h-[350px] text-white flex flex-col justify-center items-center sm:space-y-24 sm:mt-0 space-y-20 mt-2 `}
    >
      <div className="">
        <h1 className="text-4xl font-bold">Good evening, {name}.</h1>
        <p className="text-3xl">
          What <span className="text-blue-600 font-semibold">can</span> I help
          you with?
        </p>
      </div>

      <div className="sm:flex sm:gap-2 grid gap-4">
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

export default Hero;
