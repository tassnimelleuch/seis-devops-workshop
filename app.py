import sqlite3
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
DB = "data.db"


TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevOps Workshop</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Inter', sans-serif;
      background: #eef0f8;
      color: #1a1a2e;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 3rem 1rem;
    }

    /* ── corner-bracket frame (signature SEIS element) ── */
    .frame {
      position: relative;
      width: 100%;
      max-width: 560px;
      background: #f4f6fc;
      border: 2px solid #3a3aff;
      padding: 2.5rem 2rem 2rem;
      margin-bottom: 2rem;
    }

    .frame::before, .frame::after,
    .frame .corner-br, .frame .corner-bl {
      content: '';
      position: absolute;
      width: 18px;
      height: 18px;
      border-color: #3a3aff;
      border-style: solid;
    }
    .frame::before  { top: -6px;    left: -6px;    border-width: 3px 0 0 3px; }
    .frame::after   { top: -6px;    right: -6px;   border-width: 3px 3px 0 0; }
    .frame .corner-br { bottom: -6px; right: -6px;  border-width: 0 3px 3px 0; }
    .frame .corner-bl { bottom: -6px; left: -6px;   border-width: 0 0 3px 3px; }

    /* ── header ── */
    header {
      width: 100%;
      max-width: 560px;
      margin-bottom: 1.8rem;
    }

    .seis-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #3a3aff;
      margin-bottom: 0.8rem;
    }

    .seis-badge .dot {
      width: 6px; height: 6px;
      background: #ff6b35;
      border-radius: 50%;
    }

    h1 {
      font-size: 2rem;
      font-weight: 900;
      color: #1a1a2e;
      line-height: 1.1;
      letter-spacing: -0.03em;
    }

    h1 .accent { color: #3a3aff; }

    .subtitle {
      font-size: 0.8rem;
      color: #6b7280;
      margin-top: 0.5rem;
      letter-spacing: 0.02em;
    }

    /* ── form ── */
    label {
      display: block;
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #3a3aff;
      margin-bottom: 0.35rem;
    }

    input, textarea {
      width: 100%;
      background: #fff;
      border: 1.5px solid #c7cdf0;
      border-radius: 0;
      color: #1a1a2e;
      font-family: inherit;
      font-size: 0.9rem;
      padding: 0.6rem 0.8rem;
      margin-bottom: 1.2rem;
      transition: border-color 0.2s;
      outline: none;
    }

    input:focus, textarea:focus { border-color: #3a3aff; }
    textarea { resize: vertical; min-height: 80px; }

    button {
      width: 100%;
      background: red;
      color: #fff;
      border: none;
      font-family: inherit;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 0.75rem;
      cursor: pointer;
      transition: background 0.2s;
      border-radius: 0;
    }

    button:hover { background: #1a1acc; }

    /* ── entries ── */
    .entries {
      width: 100%;
      max-width: 560px;
    }

    .entries-header {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 1rem;
    }

    .entries-header h2 {
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #6b7280;
    }

    .entries-header .line {
      flex: 1;
      height: 1px;
      background: #c7cdf0;
    }

    .entry {
      background: #fff;
      border-left: 3px solid #3a3aff;
      padding: 0.7rem 1rem;
      margin-bottom: 0.7rem;
    }

    .entry .name {
      font-size: 0.75rem;
      font-weight: 700;
      color: #3a3aff;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 0.2rem;
    }

    .entry .msg {
      font-size: 0.9rem;
      color: #1a1a2e;
    }

    .empty {
      font-size: 0.85rem;
      color: #9ca3af;
      text-align: center;
      padding: 1.5rem;
      border: 1.5px dashed #c7cdf0;
      background: #fff;
    }
  </style>
</head>
<body>

  <header>
    <div class="seis-badge"><span class="dot"></span> SEIS 2026 &mdash; Hands-On</div>
    <h1>Introduction to <span class="accent">DevOps</span></h1>
  </header>

  <div class="frame">
    <div class="corner-br"></div>
    <div class="corner-bl"></div>

    <form method="POST" action="/submit">
      <label for="name">Your name</label>
      <input id="name" name="name" type="text"  required>

      <label for="message">Message</label>
      <textarea id="message" name="message" placeholder="Hello, DevOps!" required></textarea>

      <button type="submit">Submit &rarr;</button>
    </form>
  </div>

  <div class="entries">
    <div class="entries-header">
      <h2>{{ entries|length }} entr{{ 'y' if entries|length == 1 else 'ies' }}</h2>
      <div class="line"></div>
    </div>

    {% if entries %}
      {% for e in entries %}
        <div class="entry">
          <div class="name">{{ e['name'] }}</div>
          <div class="msg">{{ e['message'] }}</div>
        </div>
      {% endfor %}
    {% else %}
      <div class="empty">No entries yet — be the first!</div>
    {% endif %}
  </div>

</body>
</html>
"""

def get_db():
    """Open and return a connection to the SQLite database.
    
    Sets row_factory to sqlite3.Row so columns are accessible by name.
    The caller is responsible for closing the connection.
    """
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create the messages table if it does not already exist.
    
    Called once at startup before the server begins accepting requests.
    Safe to call multiple times — uses CREATE TABLE IF NOT EXISTS.
    """
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)

@app.route("/")
def index():
    """Render the home page with the submission form and all past entries.
    
    Fetches all rows from the messages table, newest first,
    and passes them to the HTML template for rendering.
    """
    with get_db() as db:
        entries = db.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    return render_template_string(TEMPLATE, entries=entries)

@app.route("/submit", methods=["POST"])
def submit():
    """Handle form submission and save a new message to the database.
    
    Reads 'name' and 'message' from the POST body.
    Silently ignores the submission if either field is empty.
    Redirects back to the home page after processing.
    """
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()
    if name and message:
        with get_db() as db:
            db.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
