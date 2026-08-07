import { useEffect, useState } from "react";
import MovieCard from "@/components/MovieCard";
export default function Home() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    // Fetch movies from Flask API
    const fetchDBMovies = async () => {
      const res = await fetch("http://127.0.0.1:5000/api/movies");
      const data = await res.json();
      console.log(data);
      setMovies(data);
    };

    fetchDBMovies();
  }, []);

  return (
    <div className="p-4 max-w-[100vw]">

    <div className="flex flex-col gap-4 p-4 flex-wrap wrap">
      <h1 className="font-bold text-3xl">National Film Registry</h1>
      <div className="grid grid-cols-3 grid-flow-row gap-4">
        {movies.map((movie, index) => (
          <div key={index} className="flex flex-row">
            <MovieCard
              className=""
              title={movie.title}
              year={movie.year}
              imdb_rating={movie.imDB_Rating}
              movie_data={movie}
            />
          </div>
        ))}
      </div>
    </div>
    </div>
  );
}
