import { useEffect, useState, useRef, useCallback } from "react";
import MovieCard from "@/components/MovieCard";



export default function Home() {
  const [movies, setMovies] = useState([]);
  const [cursor, setCursor] = useState(null);
  const [hasMore, setHasMore] = useState(true);
  const [loading, setLoading] = useState(false)
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const observerRef = useRef(null);
  const loadMoreRef = useCallback(
    (node) => {
      if (loading) return;
      if (observerRef.current) observerRef.current.disconnect();
  
      observerRef.current = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting && hasMore && !loading) {
            fetchDBMovies(cursor)
          }
        },
        { rootMargin: '100px' }
      );
  
      if (node) observerRef.current.observe(node);
    },
    [cursor, hasMore, loading]
  )
  const fetchDBMovies = async (cursorParam = null) => {
    if (loading) return;
    setLoading(true);

    const params = new URLSearchParams({ limit: '24' });
    if (cursorParam) params.set('cursor', cursorParam);
    const URL = `${API_URL}/api/movies?${params}`;
    const res = await fetch(URL);
    const data = await res.json();


    console.log(`Movies from database: ${data}`);
    setMovies((prev) => [...prev, ...data.movies]);
    setCursor(data.nextCursor)
    setHasMore(data.hasMore);
    setLoading(false);
  };
  useEffect(() => {
    // Fetch movies from Flask API
    fetchDBMovies();
  }, []);

  return (
    <div className="p-4">
      <div className="flex flex-col gap-4 p-4 flex-wrap ">
        <h1 className="font-bold text-3xl">National Film Registry</h1>
        <div className="grid lg:grid-cols-4 grid-flow-row">
          {movies.map((movie) => (
            <div key={movie.title} className="flex flex-col group">
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
                // year_inducted={movie.yearInducted}
                // logo={movie.LogoImage}
              />
            </div>
          ))}
        </div>

        <div ref={loadMoreRef} className="h-10">
          {loading && <p>Loading more films... </p>}
          {!hasMore && movies.length > 0 && (
            <p className="text-center text-gray-400"> That's all folks! </p>
          )}
        </div>
      </div>
    </div>
  );
}
