import { useState, useEffect } from "react";
import api from "../api/axios";

const NoteForm = ({ currentNote, fetchNotes, setCurrentNote }) => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (currentNote) {
      setTitle(currentNote.title);
      setContent(currentNote.content);
    } else {
      setTitle("");
      setContent("");
    }
  }, [currentNote]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (currentNote) {
        await api.put(`/notes/${currentNote._id}`, { title, content });
        setMessage("Note updated successfully!");
      } else {
        await api.post("/notes/", { title, content });
        setMessage("Note created successfully!");
      }
      setTitle("");
      setContent("");
      setCurrentNote(null);
      fetchNotes();
      setTimeout(() => setMessage(""), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || "Operation failed");
      setTimeout(() => setError(""), 3000);
    }
  };

  return (
    <div style={{ marginBottom: "20px", padding: "15px", border: "1px solid #ddd", borderRadius: "5px" }}>
      <h3>{currentNote ? "Edit Note" : "Create Note"}</h3>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          style={{ padding: "8px" }}
        />
        <textarea
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
          rows="4"
          style={{ padding: "8px" }}
        />
        <div style={{ display: 'flex', gap: '10px' }}>
          <button type="submit" style={{ padding: "8px 15px", backgroundColor: currentNote ? "#ffc107" : "#007bff", color: currentNote ? "black" : "white", border: "none", cursor: "pointer" }}>
            {currentNote ? "Update" : "Create"}
          </button>
          {currentNote && (
            <button type="button" onClick={() => setCurrentNote(null)} style={{ padding: "8px 15px", backgroundColor: "#6c757d", color: "white", border: "none", cursor: "pointer" }}>
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default NoteForm;
