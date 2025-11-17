import { useEffect, useState } from "react";

function App() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    console.log("Fetching from:", `${API_URL}/resumes/`);
    fetch(`${API_URL}/resumes/`)
      .then(res=> res.json())
      .then(data => {
        setResumes(data);
        setLoading(false);
        });
      }, []);

      
  return (
    <div>
      <h1>Resumes</h1>
      {loading ? <p>Loading...</p> : null}
      {resumes.length === 0 ? <p>No resumes found.</p> : null}
    </div>
  );
}

export default App;
