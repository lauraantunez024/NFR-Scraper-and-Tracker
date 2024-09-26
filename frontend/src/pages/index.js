import { useEffect, useState } from "react";
import MovieCard from "@/components/MovieCard";
import styles from "@/styles/Home.module.css";



export default function Home() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    // Fetch movies from Flask API
    const fetchDBMovies = async () => {
      const res = await fetch("http://localhost:5000/api/movies");
      const data = await res.json();
      console.log(data);
      setMovies(data)
    };


    fetchDBMovies();
  }, []);

  return (
    <div>
      <h1>Movie List</h1>
      {movies.map((movie, index) => (
        <div key={index}>
          <MovieCard class={styles.movie_container} 
            title={movie.title}
            year={movie.year}
            imdb_rating={movie.imDB_Rating}
            movie_data={movie}
          />
        </div>
      ))}
    </div>
  );
}
