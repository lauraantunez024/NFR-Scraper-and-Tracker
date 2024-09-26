import styles from "@/styles/Home.module.css";
import { useEffect, useState } from "react";

require("dotenv").config({});

export default function MovieCard({ title, imdb_rating, year, movie_data }) {
  const [isLoading, setIsLoading] = useState([false]);
  const [movieData, setMovieData] = useState([]);
  const [posterData, setPosterData] = useState([]);
  const [imagePath, setImagePath] = useState([]);
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

        const image_link = `https://image.tmdb.org/t/p/w500${posterData.posters[0].file_path}`;
        setImagePath(image_link);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchTmDBData();
  }, []);
  return (
    <div class={styles.card}>
      <h1 class={styles.title}>{title}</h1>

      <img class={styles.card_image} src={imagePath} alt="womp" />
      <div class={styles.card_details}>
        <p>imdb rating: {imdb_rating}</p>
        <p>year: {year}</p>
      </div>
    </div>
  );
}
