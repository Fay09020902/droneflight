import React, { useEffect, useState } from 'react';

function DroneFlight() {
  const [droneflight, setDroneflight] = useState(null);
  const [loading, setLoading] = useState(true); // Loading state
  const [query, setQuery] = useState(''); // Store user query
  const [response, setResponse] = useState(null); // Store response from API

  // useEffect(() => {
  //   fetch('http://127.0.0.1:5000/api/droneflight')
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setDroneflight(data); // Set the fetched data
  //       setLoading(false);    // Update loading state
  //     })
  //     .catch((error) => {
  //       console.error('Error fetching droneflight data:', error);
  //       setLoading(false); // Stop loading if there’s an error
  //     });
  // }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (response.ok) {
        const data = await response.json();
        setResponse(data.response);
      }
    } catch (error) {
      console.error("Network error: ", error);
      setResponse("Network error occurred. Please try again later.");
    }
  };

  return (
    <div className='queries'>
      {/* Input Form for User Query */}
      <form onSubmit={handleSubmit}>
        <label htmlFor="Description">Enter your query</label>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder='What is the battery level of the drone during the last image?'
        />
        <button type="submit">Submit</button>
      </form>

      {/* Display Query Response */}
      {response && (
        <div className="response">
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}
{/*
      Display Drone Data
      {loading ? (
        <p>Loading drone data...</p>
      ) : (
        droneflight && (
          <div>
            <h1>Drone Flight Details</h1>
            <p>Image ID: {droneflight.image_id}</p>
            <p>Timestamp: {droneflight.timestamp}</p>
            <p>Altitude: {droneflight.altitude_m} meters</p>
          </div>
        )
      )} */}
    </div>
  );
}

export default DroneFlight;
