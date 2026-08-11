import { useEffect, useState } from "react";

require("dotenv").config({});

export default function MovieCard({ title, imdb_rating, year, movie_data }) {
  const [isLoading, setIsLoading] = useState([false]);
  const [movieData, setMovieData] = useState([]);
  const [posterData, setPosterData] = useState([]);
  const [imagePath, setImagePath] = useState([]);
  const [logoPath, setLogoPath] = useState([]);
  const api_key = process.env.NEXT_PUBLIC_TMDB_API_KEY;
  // const api_key = process.env.TMDB_API_KEY;
  const movieUrl = `https://api.themoviedb.org/3/find/${movie_data.imDB_ID}?external_source=imdb_id&api_key=${api_key}`;

  useEffect(() => {
    const fetchTmDBData = async () => {
      setIsLoading(true);
      try {
        const movieDataResponse = await fetch(movieUrl);

        const movieData = await movieDataResponse.json();

        setMovieData(movieData);
        const posterDataResponse = await fetch(
          `https://api.themoviedb.org/3/movie/${movieData.movie_results[0].id}/images?include_image_language=en&api_key=${api_key}`
        );
        const posterData = await posterDataResponse.json();
        setPosterData(posterData);
        if (posterData.logos[0] == null || movieData.imDB_ID === null) {
          setLogoPath(null)
        } else {
          const image_link = `https://image.tmdb.org/t/p/w500${posterData.posters[0].file_path}`;
          setImagePath(image_link);
          const logo_link = `https://image.tmdb.org/t/p/w200${posterData.logos[0].file_path}`
          setLogoPath(logo_link)
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchTmDBData();
  }, []);
  return (
    <div className="min-w-[10vw] p-2 h-[40vh] bg-[#6776b5] group-hover:bg-[#6776b5]/50 justify-around text-(--primary) rounded-md border-[#141414] border-x-4 border-y-2 border flex flex-col gap-4">

      {logoPath ? (
        <img className="p-4 flex text-center shrink text-white group-hover:hidden max-h-[30vh] max-w-[18vw] m-auto text-2xl" onerror="this.style.display='none'" src={logoPath} alt={title} />
      ) : (
        <h2 className="text-center text-2xl text-white group-hover:hidden">{title}</h2>

      )}
      <div className="hidden group-hover:block flex flex-col justify-evenly text-white">

        <h1 className="text-center text-lg font-bold">{title}</h1>
        {/* <img className="p-4 flex shrink" src={logoPath} alt={title} /> */}
        <div className="flex flex-row gap-4 m-auto">
          <p>imdb rating: {imdb_rating}</p>
          <p>year: {year}</p>
        </div>
          <span>
            movie description: {movie_data.plot}
          </span>
      </div>
    </div>
  );
}

