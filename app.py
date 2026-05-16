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

# ================= FETCH JOBS =================
def fetch_jobs(query, page=1):
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "page": str(page),
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
    page = int(request.args.get("page", 1))

    jobs = fetch_jobs(build_query(search, city, portal), page)

    html = """
    <html>
    <body style="font-family:Arial;background:#f3f2ef;">

    <div style="background:#0a66c2;color:white;padding:15px;">
        🚀 JobNest Job Portal
    </div>

    <div style="background:white;padding:10px;">
        <a href="/">Home</a> |
        <a href="/profile">Profile</a> |
        <a href="/register">Register</a> |
        <a href="/login">Login</a> |
        <a href="/saved">Saved Jobs</a> |
        <a href="/upload">Upload Resume</a>
    </div>

    <div style="padding:20px;">
    """

    for i, job in enumerate(jobs):
        html += f"""
        <div style="background:white;padding:10px;margin:10px;border-radius:8px;">
            <h3>{job.get('job_title')}</h3>
            <p>{job.get('employer_name')}</p>

            <a href="{job.get('job_apply_link')}" target="_blank">Apply</a>
            <a href="/save/{i}">Save</a>
        </div>
        """

    html += "</div></body></html>"
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
            return redirect("/profile")

        return "Invalid Login"

    return """
    <h2>Login</h2>
    <form method="POST">
        <input name="username">
        <input name="password" type="password">
        <button>Login</button>
    </form>
    """

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ================= PROFILE =================
@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    user = session["user"]
    jobs = saved_jobs.get(user, [])

    html = f"""
    <html>
    <body style="font-family:Arial;background:#f3f2ef;">

    <div style="background:#0a66c2;color:white;padding:15px;">
        👤 Welcome {user}
        <a href="/" style="color:white;margin-left:15px;">Home</a>
        <a href="/logout" style="color:white;margin-left:10px;">Logout</a>
    </div>

    <div style="padding:20px;">
        <h3>📌 Saved Jobs</h3>
    """

    if not jobs:
        html += "<p>No saved jobs yet</p>"
    else:
        for j in jobs:
            html += f"""
            <div style="background:white;padding:10px;margin:10px;">
                Saved Job ID: {j}
            </div>
            """

    html += "</div></body></html>"
    return html

# ================= SAVE JOB =================
@app.route("/save/<jobid>")
def save_job(jobid):

    if "user" not in session:
        return redirect("/login")

    user = session["user"]

    if user not in saved_jobs:
        saved_jobs[user] = []

    saved_jobs[user].append(jobid)

    return redirect("/profile")

# ================= SAVED =================
@app.route("/saved")
def saved():

    if "user" not in session:
        return redirect("/login")

    user = session["user"]
    jobs = saved_jobs.get(user, [])

    return f"<h1>Saved Jobs</h1><p>{jobs}</p>"

# ================= UPLOAD =================
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        file = request.files["resume"]
        os.makedirs("uploads", exist_ok=True)
        file.save("uploads/" + file.filename)
        return "Uploaded Successfully"

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