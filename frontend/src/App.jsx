import { useEffect, useState } from "react";

function App() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_URL = import.meta.env.VITE_API_URL;
  const TOKEN = import.meta.env.VITE_API_TOKEN;

  useEffect(() => {
    console.log("Fetching from:", `${API_URL}/api/v3/resumes/`);

    fetch(`${API_URL}/api/v3/resumes/`, {
      headers: {
        "Authorization": `Bearer ${TOKEN}`,
        "Content-Type": "application/json",
      },
    })
      .then(res => {
        console.log("Status:", res.status);
        if (!res.ok) throw new Error("HTTP error " + res.status);
        return res.json();
      })
      .then(data => {
        console.log("DATA:", data);
        setResumes(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Fetch error:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <h2>Loading resumes...</h2>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Resumes</h1>

      {resumes.length === 0 && <p>No resumes found.</p>}

      {resumes.map((resume) => (
        <div
          key={resume.id}
          style={{
            border: "1px solid #ddd",
            borderRadius: "10px",
            padding: "15px",
            marginBottom: "10px",
            backgroundColor: "#fafafa",
          }}
        >
          <h2>{resume.name}</h2>
          <p><strong>Bio:</strong> {resume.bio}</p>
          <p><strong>Skills:</strong> {resume.skills}</p>
          <p><strong>Address:</strong> {resume.address}</p>
          <p><strong>Job History:</strong> {resume.job_history}</p>
          <p><strong>Education:</strong> {resume.education_history}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
