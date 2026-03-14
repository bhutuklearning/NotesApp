import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";
import NoteForm from "../components/NoteForm";
import "./Dashboard.css";

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [notes, setNotes] = useState([]);
  const [currentNote, setCurrentNote] = useState(null);
  const [error, setError] = useState("");

  const fetchNotes = async () => {
    try {
      const response = await api.get("/notes/");
      setNotes(response.data);
    } catch (err) {
      setError("Failed to fetch notes");
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const handleDelete = async (noteId) => {
    try {
      await api.delete(`/notes/${noteId}`);
      fetchNotes();
    } catch (err) {
      setError("Failed to delete note");
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-content">
        <div className="dashboard-header">
          <h2 className="welcome-text">
            Welcome, {user.username}! 
            {user.role === "admin" && <span className="admin-badge">Admin</span>}
          </h2>
          <button onClick={logout} className="btn-logout">Logout</button>
        </div>

        {error && <div className="status-message status-error">{error}</div>}

        <NoteForm currentNote={currentNote} fetchNotes={fetchNotes} setCurrentNote={setCurrentNote} />

        <div className="notes-section">
          <h3>Your Notes</h3>
          {notes.length === 0 ? (
            <div className="empty-state">No notes found. Create your first note above!</div>
          ) : (
            <div className="notes-grid">
              {notes.map(note => (
                <div key={note._id} className="note-card">
                  <h4 className="note-title">{note.title}</h4>
                  <div className="note-content">{note.content}</div>
                  <div className="note-meta">
                    <span>Created: {new Date(note.created_at).toLocaleString()}</span>
                    {user.role === "admin" && <span>Owner ID: {note.owner_id}</span>}
                  </div>
                  
                  <div className="note-actions">
                    <button onClick={() => setCurrentNote(note)} className="btn-edit">Edit</button>
                    <button onClick={() => handleDelete(note._id)} className="btn-delete">Delete</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
