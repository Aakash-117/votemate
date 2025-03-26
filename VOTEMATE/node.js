const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Connect to SQLite database
const db = new sqlite3.Database("voting.db", (err) => {
    if (err) console.error("Error connecting to database:", err);
    else console.log("Connected to SQLite database.");
});

// Create tables if not exists
db.run(`
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
`);

db.run(`
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        votes INTEGER DEFAULT 0
    )
`);

db.run(`
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        candidate_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    )
`);

// **User Registration**
app.post("/register", (req, res) => {
    const { username, password } = req.body;
    db.run(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        [username, password],
        function (err) {
            if (err) return res.status(400).json({ error: err.message });
            res.json({ message: "User registered successfully", userId: this.lastID });
        }
    );
});

// **User Voting**
app.post("/vote", (req, res) => {
    const { user_id, candidate_id } = req.body;

    // Check if the user has already voted
    db.get("SELECT * FROM votes WHERE user_id = ?", [user_id], (err, row) => {
        if (row) return res.status(400).json({ error: "User has already voted" });

        // Insert vote
        db.run("INSERT INTO votes (user_id, candidate_id) VALUES (?, ?)", [user_id, candidate_id], (err) => {
            if (err) return res.status(500).json({ error: err.message });

            // Update vote count
            db.run("UPDATE candidates SET votes = votes + 1 WHERE id = ?", [candidate_id], (err) => {
                if (err) return res.status(500).json({ error: err.message });
                res.json({ message: "Vote cast successfully" });
            });
        });
    });
});

// **Get Candidates & Vote Counts**
app.get("/candidates", (req, res) => {
    db.all("SELECT * FROM candidates", [], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

// **Add a Candidate**
app.post("/candidates", (req, res) => {
    const { name } = req.body;
    db.run("INSERT INTO candidates (name, votes) VALUES (?, 0)", [name], function (err) {
        if (err) return res.status(400).json({ error: err.message });
        res.json({ message: "Candidate added successfully", candidateId: this.lastID });
    });
});

// **Start Server**
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
