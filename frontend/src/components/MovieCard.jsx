import { useState } from "react";
import MovieModal from './MovieDoc'

require("dotenv").config({});

export default function MovieCard({ title, imdb_rating, year, movie_data }) {
  const [showDetails, setShowDetails] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const logoPath = movie_data?.LogoImage;
  return (
    <div className="min-w-[10vw] p-2 h-[30vh] max-h-[15rem] bg-[#6776b5] lg:group-hover:bg-[#6776b5]/50 justify-around text-(--primary) rounded-md border-[#141414] border-x-4 border-y-2 border flex flex-col gap-4"
    onClick={() => setShowDetails((prev) => !prev)} tabIndex={0}>

      {logoPath ? (
        <img className={`p-4 flex text-center shrink text-white lg:group-hover:hidden group-focus:hidden max-h-[10rem] lg:max-w-[18vw] m-auto text-2xl ${showDetails ? "max-lg:hidden" : ""}`} onerror="this.style.display='none'" src={logoPath} alt={title} />
      ) : (
        <h2 className={`text-center text-2xl text-white lg:group-hover:hidden ${showDetails ? "max-lg:hidden" : ""}`}>{title}</h2>

      )}
<div
  className={`
    hidden flex-col content-around p-2 text-white
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
          <button type="button" onClick={(e) => { e.stopPropagation(); setShowModal(true)}}> button right here </button>
      </div>

          <MovieModal 
          title={title}
          open={showModal}
          plot={movie_data?.plot}
          poster={movie_data?.posterImage}
          onClose={() => setShowModal(false)}/>
    </div>
  );
}

