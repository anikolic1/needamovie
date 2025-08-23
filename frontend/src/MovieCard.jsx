function MovieCard({ movie }) {

    return (
        <div className="movie-card">
            <h3>{movie.title}</h3>
            <p>{movie.year}</p>
            <img src={movie.poster}></img>
            <p>{movie.director}</p>
            <p>{movie.genre}</p>
            <a href={movie.movie_url} target="_blank" rel="noopener noreferrer">
                View on IMDb
            </a>
            <p>{movie.reason}</p>
        </div>
    );
}

export default MovieCard;