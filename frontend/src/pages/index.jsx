import { useEffect, useState } from "react";
import MovieCard from "@/components/MovieCard";

export default function Home() {
  const [movies, setMovies] = useState([]);
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  useEffect(() => {
    // Fetch movies from Flask API
    const fetchDBMovies = async () => {
      const URL = `${API_URL}/api/movies`;
      console.log(URL);
      const res = await fetch(URL);
      const data = await res.json();
      console.log(`Movies from database: ${data}`);
      setMovies(data);
    };

    fetchDBMovies();
  }, []);

  return (
    <div className="p-4">
      <div className="flex flex-col gap-4 p-4 flex-wrap ">
        <h1 className="font-bold text-3xl">National Film Registry</h1>
        <div className="grid lg:grid-cols-4 grid-flow-row">
          {movies.map((movie, index) => (
            <div key={index} className="flex flex-col group">
              <div className="sprockets flex justify-between px-2 py-1 bg-[#141414]">
                {Array.from({ length: 8 }).map((_, i) => (
                  <span key={i} className="p-2 w-2 h-2 bg-gray-500 rounded-[1px]" />
                ))}
              </div>
              <MovieCard
                className=""
                title={movie.title}
                year={movie.year}
                imdb_rating={movie.imDB_Rating}
                movie_data={movie}
                year_inducted={movie.yearInducted}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
