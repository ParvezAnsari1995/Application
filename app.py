from flask import Flask, request, redirect, session
import requests
import os

app = Flask(__name__)
app.secret_key = "jobnestsecret"

# ================= API =================
API_KEY = "YOUR_RAPIDAPI_KEY"
BASE_URL = "https://jsearch.p.rapidapi.com/search"

# ================= MEMORY DB =================
users = {}
saved_jobs = {}

# ================= JOB FETCH =================
def fetch_jobs(query):
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "page": "1",
        "num_pages": "1"
    }

    try:
        res = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        return res.json().get("data", [])
    except:
        return []

# ================= QUERY BUILDER =================
def build_query(search, city, portal):
    query = search if search else "jobs hiring"

    if city:
        query += f" in {city}"

    if portal == "linkedin":
        query += " linkedin"
    elif portal == "naukri":
        query += " naukri india"
    elif portal == "indeed":
        query += " indeed"

    return query

# ================= HOME =================
@app.route("/")
def home():
    search = request.args.get("search", "")
    city = request.args.get("city", "")
    portal = request.args.get("portal", "")

    query = build_query(search, city, portal)
    jobs = fetch_jobs(query)

    html = """
    <h1>🚀 JobNest Portal</h1>

    <form>
        <input name="search" placeholder="Job title">
        <input name="city" placeholder="City">

        <select name="portal">
            <option value="">All</option>
            <option value="linkedin">LinkedIn</option>
            <option value="naukri">Naukri</option>
            <option value="indeed">Indeed</option>
        </select>

        <button type="submit">Search</button>
    </form>

    <hr>
    """

    for i, job in enumerate(jobs):
        html += f"""
        <div style="border:1px solid #ccc; padding:10px; margin:10px;">
            <h3>{job.get('job_title')}</h3>
            <p>{job.get('employer_name')}</p>
            <a href="{job.get('job_apply_link')}" target="_blank">Apply</a>
            <a href="/save/{i}">Save</a>
        </div>
        """

    return html

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users[request.form["username"]] = request.form["password"]
        return redirect("/login")

    return """
    <h2>Register</h2>
    <form method="POST">
        <input name="username">
        <input name="password" type="password">
        <button>Register</button>
    </form>
    """

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if u in users and users[u] == p:
            session["user"] = u
            return redirect("/")
        return "Invalid login"

    return """
    <h2>Login</h2>
    <form method="POST">
        <input name="username">
        <input name="password" type="password">
        <button>Login</button>
    </form>
    """

# ================= SAVE JOB =================
@app.route("/save/<jobid>")
def save(jobid):
    if "user" not in session:
        return redirect("/login")

    user = session["user"]

    if user not in saved_jobs:
        saved_jobs[user] = []

    saved_jobs[user].append(jobid)

    return redirect("/saved")

# ================= SAVED JOBS =================
@app.route("/saved")
def saved():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]
    jobs = saved_jobs.get(user, [])

    html = f"<h1>Saved Jobs - {user}</h1>"

    for j in jobs:
        html += f"<p>Saved Job ID: {j}</p>"

    return html

# ================= UPLOAD RESUME =================
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["resume"]
        os.makedirs("uploads", exist_ok=True)
        file.save("uploads/" + file.filename)
        return "Uploaded successfully"

    return """
    <h2>Upload Resume</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="resume">
        <button>Upload</button>
    </form>
    """

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)