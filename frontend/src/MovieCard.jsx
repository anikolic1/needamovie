function MovieCard({ movie }) {

    return (
        <div className="movie-card">
            <h3>{movie.title}</h3>
            <p>{movie.rating}</p>
            <a href={movie.movie_url} target="_blank" rel="noopener noreferrer">
                View on Letterboxd
            </a>
        </div>
    )
}

export default MovieCard;