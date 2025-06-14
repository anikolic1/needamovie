import { useState } from 'react';
import './App.css';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

function App() {
  const [userName, setUsername] = useState("");
  const [responseMessage, setResponseMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponseMessage("");

    // no empty username
    if (userName.trim() === "") {
      setResponseMessage("Please enter a username");
      return;
    }

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
        setResponseMessage(`Success, Server says: ${data.message}`);
      } else {
        setResponseMessage(`Error: ${data.message}`);
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
    </>
  );
}

export default App;
