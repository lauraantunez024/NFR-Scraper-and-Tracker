import { useEffect, useState } from "react";

require("dotenv").config({});

export default function MovieCard({ title, imdb_rating, year, movie_data, logoPath }) {
  const [showDetails, setShowDetails] = useState(false);
  const logoPath = movie_data?.LogoImage;
  return (
    <div className="min-w-[10vw] p-2 h-[40vh] bg-[#6776b5] lg:group-hover:bg-[#6776b5]/50 justify-around text-(--primary) rounded-md border-[#141414] border-x-4 border-y-2 border flex flex-col gap-4"
    onClick={() => setShowDetails((prev) => !prev)} tabIndex={0}>

      {logoPath ? (
        <img className={`p-4 flex text-center shrink text-white lg:group-hover:hidden group-focus:hidden max-h-[30vh] lg:max-w-[18vw] m-auto text-2xl ${showDetails ? "max-lg:hidden" : ""}`} onerror="this.style.display='none'" src={logoPath} alt={title} />
      ) : (
        <h2 className={`text-center text-2xl text-white lg:group-hover:hidden ${showDetails ? "max-lg:hidden" : ""}`}>{title}</h2>

      )}
<div
  className={`
    hidden flex-col justify-evenly text-white
    ${showDetails ? "max-lg:flex" : ""}
    lg:group-hover:flex
  `}
>
        <h1 className="text-center text-lg font-bold">{title}</h1>
        {/* <img className="p-4 flex shrink" src={logoPath} alt={title} /> */}
        <div className="flex flex-row gap-4 m-auto">
          <p>imdb rating: {imdb_rating}</p>
          <p>year: {year}</p>
        </div>
          <span>
            movie description: {plot}
          </span>
      </div>
    </div>
  );
}

