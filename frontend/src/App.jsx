import { useState } from 'react';
import './App.css';
import MovieCard from './MovieCard';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

/* main app component, contains username and response message state
variables, user submits username and then a post request is sent
to backend to scrape profile */
function App() {
  const [userName, setUsername] = useState("");
  const [responseMessage, setResponseMessage] = useState("");
  const [movies, setMovies] = useState([]);

  // handler for when user clicks button to submit username
  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponseMessage("");
    setMovies([]);

    // username validation logic
    if (userName.trim() === "") {
      setResponseMessage("Please enter a username");
      return;
    }
    else if (!isValidUsername(userName)) {
      setResponseMessage("Invalid username, please try again.");
      setUsername("");
      return;
    }

    // post request for the username
    try {
      const response = await fetch(BACKEND_URL + "api/scrape", {
        method: "POST",
        headers: {
          "Content-Type" : "application/json"
        },
        body: JSON.stringify({userName}),
      });

      const data = await response.json();

      if (response.ok) {
        setMovies(data.movies);
        const movieTitles = data.movies.map(movie => movie.title).join(", ");
        setResponseMessage(`Success! ${movieTitles}`);
        setUsername("");
      } else {
        setResponseMessage(`Error: ${data.error}`);
      }
    } catch(error) {
      setResponseMessage("Network error."); 
    }
  };

  return (
    <>
      <h1>Enter your Letterboxd username:</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={userName}
          onChange={e => setUsername(e.target.value)}
        />
        <button type="submit">
          Submit
        </button>
      </form>
      {responseMessage && <p>{responseMessage}</p>}
      <div className="movie-grid">
        {movies[0] && <MovieCard key={movies[0].title} movie={movies[0]} />}
      </div>
    </>
  );
}

function isValidUsername(username) {
  // letterboxd username rules are: a-z, A-Z, 0-9, _, and 2-15 chars long
  const regex = /^[a-zA-Z0-9_]{2,15}$/;
  if (!username) return false;
  if (!regex.test(username)) return false;

  return true;
}

export default App;