import React, { useState, useEffect } from "react";
import axios from "axios";
import styles from "./GestureMapping.module.css";

const GestureMapping = () => {
  const [gestures, setGestures] = useState([]);
  const [selectedGesture, setSelectedGesture] = useState("");
  const [action, setAction] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    const fetchGestures = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/gestures");
        setGestures(response.data);
      } catch (error) {
        console.error("Error fetching gestures:", error);
      }
    };

    fetchGestures();
  }, []);

  const handleGestureChange = (event) => {
    setSelectedGesture(event.target.value);
  };

  const handleActionChange = (event) => {
    setAction(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSaving(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/map-gesture", {
        gesture: selectedGesture,
        action: action,
      });
      console.log(response.data);
      alert("Gesture mapped successfully!");
    } catch (error) {
      console.error("Error mapping gesture:", error);
      alert("Failed to map gesture!");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Map Gesture to Action</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.inputGroup}>
          <label>
            Gesture:
            <select
              value={selectedGesture}
              onChange={handleGestureChange}
              className={styles.input}
            >
              {gestures.map((gesture) => (
                <option key={gesture} value={gesture}>
                  {gesture}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div className={styles.inputGroup}>
          <label>
            Action:
            <input
              type="text"
              value={action}
              onChange={handleActionChange}
              className={styles.input}
            />
          </label>
        </div>
        <button type="submit" className={styles.button} disabled={isSaving}>
          Map Gesture
        </button>
      </form>
    </div>
  );
};

export default GestureMapping;
