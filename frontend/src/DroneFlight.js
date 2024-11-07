import React, { useEffect, useState } from "react";

function DroneFlight() {
  const [droneflight, setDroneflight] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/droneflights")
      .then((response) => response.json())
      .then((data) => {
        setDroneflight(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching droneflight data:", error);
        setLoading(false);
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/api/test", {
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
    <div className="queries">
      <form onSubmit={handleSubmit}>
        <label htmlFor="Description">Enter your query</label>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="What is the battery level of the drone during the last image?"
        />
        <button type="submit">Submit</button>
      </form>

      {response && (
        <div className="response">
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}

      {loading ? (
        <p>Loading drone data...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Image ID</th>
              <th>Timestamp</th>
              <th>Altitude (m)</th>
              <th>Battery Level (%)</th>
              <th>Speed (m/s)</th>
              <th>Latitude</th>
              <th>Longitude</th>
              <th>Temperature (°C)</th>
              <th>Signal Strength (dB)</th>
              <th>Drone ID</th>
              <th>Camera Angle (°)</th>
              <th>Orientation</th>
              <th>File Size (MB)</th>
              <th>Image Resolution</th>
              <th>Weather Conditions</th>
              <th>Wind Speed (m/s)</th>
              <th>Location Description</th>
            </tr>
          </thead>
          <tbody>
            {droneflight.map((flight) => (
              <tr key={flight.image_id}>
                <td>{flight.image_id}</td>
                <td>{flight.timestamp}</td>
                <td>{flight.altitude_m}</td>
                <td>{flight.battery_level_pct}</td>
                <td>{flight.drone_speed_mps}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default DroneFlight;
