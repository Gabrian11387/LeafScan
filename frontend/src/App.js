import React, { useState } from "react";
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setSelectedImage(file);
    setPreviewImage(URL.createObjectURL(file));
    setPrediction("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedImage) return;

    const formData = new FormData();
    formData.append("image", selectedImage);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setPrediction(data.prediction);
    } catch (error) {
      console.error("Eroare la trimiterea imaginii:", error);
      setPrediction("A apărut o eroare.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App" style={{ padding: "20px", textAlign: "center" }}>
      <header className="App-header">
        <h2 style={{ marginBottom: "20px" }}>Detecție Boli la Plante 🌿</h2>
        <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleImageChange} 
            style={{ marginBottom: "10px", padding: "5px" }}
          />
          <br />
          <button 
            type="submit" 
            disabled={loading} 
            style={{
              padding: "10px 20px",
              backgroundColor: "#4CAF50",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer"
            }}
          >
            {loading ? "Se procesează..." : "Trimite imagine"}
          </button>
        </form>

        {previewImage && (
          <div style={{ position: "relative", display: "inline-block" }}>
            <img 
              src={previewImage} 
              alt="Preview" 
              style={{ width: "300px", height: "300px", objectFit: "cover", borderRadius: "10px" }}
            />
            {prediction && (
              <div 
                style={{
                  position: "absolute",
                  top: "10px",
                  left: "10px",
                  right: "10px",
                  padding: "10px",
                  backgroundColor: prediction.toLowerCase().includes("healthy") ? "rgba(0, 128, 0, 0.7)" : "rgba(255, 0, 0, 0.7)",
                  color: "white",
                  fontWeight: "bold",
                  borderRadius: "10px",
                }}
              >
                {prediction}
              </div>
            )}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
