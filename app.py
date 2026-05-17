# from flask import Flask, request, redirect, session
# import requests
# import os
#
# app = Flask(__name__)
# app.secret_key = "jobnestsecret"
#
# # =========================
# # 🔑 API CONFIG
# # =========================
# API_KEY = "284e976fecmsh6344107e8f517cep1a8ec9jsnfffbd6a518dd"
#
# BASE_URL = "https://jsearch.p.rapidapi.com/search"
#
# # =========================
# # 🧠 MEMORY DB
# # =========================
# users = {}
# saved_jobs = {}
#
# # =========================
# # 🔎 FETCH JOBS
# # =========================
# def fetch_jobs(query, page=1):
#
#     headers = {
#         "X-RapidAPI-Key": API_KEY,
#         "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
#     }
#
#     params = {
#         "query": query,
#         "page": str(page),
#         "num_pages": "1",
#         "date_posted": "month"
#     }
#
#     try:
#         res = requests.get(
#             BASE_URL,
#             headers=headers,
#             params=params,
#             timeout=10
#         )
#
#         return res.json().get("data", [])
#
#     except:
#         return []
#
# # =========================
# # 🧠 SMART QUERY
# # =========================
# def build_query(search, city, portal):
#
#     q = []
#
#     if search:
#         q.append(search + " jobs")
#     else:
#         q.append("jobs hiring")
#
#     if city:
#         q.append("in " + city)
#
#     portals = {
#         "world": "linkedin naukri indeed glassdoor",
#         "linkedin": "linkedin jobs",
#         "naukri": "naukri jobs india",
#         "indeed": "indeed jobs"
#     }
#
#     if portal in portals:
#         q.append(portals[portal])
#
#     return " ".join(q)
#
# # =========================
# # 🏠 HOME PAGE
# # =========================
# @app.route("/")
# def home():
#
#     search = request.args.get("search", "")
#     city = request.args.get("city", "")
#     portal = request.args.get("portal", "")
#     page = int(request.args.get("page", 1))
#
#     query = build_query(search, city, portal)
#
#     jobs = fetch_jobs(query, page)
#
#     html = f"""
#     <!DOCTYPE html>
#
#     <html>
#
#     <head>
#
#         <title>JobNest</title>
#
#         <style>
#
#             body {{
#                 font-family: Arial;
#                 background: #f3f2ef;
#                 margin: 0;
#                 padding: 0;
#             }}
#
#             .header {{
#                 background: #0a66c2;
#                 color: white;
#                 padding: 15px;
#                 font-size: 24px;
#                 font-weight: bold;
#             }}
#
#             .navbar {{
#                 background: white;
#                 padding: 10px;
#                 box-shadow: 0px 1px 5px #ccc;
#             }}
#
#             .navbar a {{
#                 margin-right: 15px;
#                 text-decoration: none;
#                 color: #0a66c2;
#                 font-weight: bold;
#             }}
#
#             .container {{
#                 width: 60%;
#                 margin: auto;
#                 padding: 20px;
#             }}
#
#             .card {{
#                 background: white;
#                 padding: 15px;
#                 margin: 15px 0;
#                 border-radius: 10px;
#                 box-shadow: 0px 1px 5px #ccc;
#             }}
#
#             input, select {{
#                 padding: 10px;
#                 margin: 5px;
#             }}
#
#             .btn {{
#                 background: #0a66c2;
#                 color: white;
#                 border: none;
#                 padding: 10px 15px;
#                 cursor: pointer;
#                 border-radius: 5px;
#             }}
#
#             .btn:hover {{
#                 opacity: 0.9;
#             }}
#
#             .pagination {{
#                 text-align: center;
#                 margin-top: 20px;
#             }}
#
#             .pagination a {{
#                 background: #0a66c2;
#                 color: white;
#                 padding: 8px 15px;
#                 text-decoration: none;
#                 margin: 5px;
#                 border-radius: 5px;
#             }}
#
#         </style>
#
#     </head>
#
#     <body>
#
#         <div class="header">
#             🚀 JobNest Job Portal
#         </div>
#
#         <div class="navbar">
#
#             <a href="/">Home</a>
#
#             <a href="/register">Register</a>
#
#             <a href="/login">Login</a>
#
#             <a href="/saved">Saved Jobs</a>
#
#             <a href="/upload">Upload Resume</a>
#
#         </div>
#
#         <div class="container">
#
#             <form method="GET">
#
#                 <input
#                     type="text"
#                     name="search"
#                     placeholder="Search Jobs"
#                     value="{search}"
#                 >
#
#                 <input
#                     type="text"
#                     name="city"
#                     placeholder="City"
#                     value="{city}"
#                 >
#
#                 <select name="portal">
#
#                     <option value="">All Portals</option>
#
#                     <option value="world">World</option>
#
#                     <option value="linkedin">LinkedIn</option>
#
#                     <option value="naukri">Naukri</option>
#
#                     <option value="indeed">Indeed</option>
#
#                 </select>
#
#                 <button class="btn" type="submit">
#                     Search
#                 </button>
#
#             </form>
#
#             <h3>Page: {page}</h3>
#     """
#
#     if not jobs:
#
#         html += """
#         <h2>No Jobs Found</h2>
#         """
#
#     for idx, job in enumerate(jobs):
#
#         html += f"""
#
#         <div class="card">
#
#             <h2>{job.get('job_title')}</h2>
#
#             <p>
#                 <b>Company:</b>
#                 {job.get('employer_name')}
#             </p>
#
#             <p>
#                 <b>Location:</b>
#                 {job.get('job_city')}
#             </p>
#
#             <br>
#
#             <a
#                 href="{job.get('job_apply_link')}"
#                 target="_blank"
#             >
#                 <button class="btn">
#                     Apply Now
#                 </button>
#             </a>
#
#             <a href="/save/{idx}">
#                 <button class="btn">
#                     Save Job
#                 </button>
#             </a>
#
#         </div>
#         """
#
#     prev_page = page - 1
#     next_page = page + 1
#
#     html += f"""
#
#         <div class="pagination">
#
#             {"<a href='?page=" + str(prev_page) + "'>⬅ Prev</a>" if page > 1 else ""}
#
#             <a href='?page={next_page}'>
#                 Next ➡
#             </a>
#
#         </div>
#
#         </div>
#
#     </body>
#
#     </html>
#     """
#
#     return html
#
# # =========================
# # 🔐 REGISTER
# # =========================
# @app.route("/register", methods=["GET", "POST"])
# def register():
#
#     if request.method == "POST":
#
#         username = request.form["username"]
#         password = request.form["password"]
#
#         users[username] = password
#
#         return redirect("/login")
#
#     return """
#
#     <h2>Register</h2>
#
#     <form method="POST">
#
#         <input
#             type="text"
#             name="username"
#             placeholder="Username"
#         >
#
#         <br><br>
#
#         <input
#             type="password"
#             name="password"
#             placeholder="Password"
#         >
#
#         <br><br>
#
#         <button type="submit">
#             Register
#         </button>
#
#     </form>
#     """
#
# # =========================
# # 🔑 LOGIN
# # =========================
# @app.route("/login", methods=["GET", "POST"])
# def login():
#
#     if request.method == "POST":
#
#         username = request.form["username"]
#         password = request.form["password"]
#
#         if username in users and users[username] == password:
#
#             session["user"] = username
#
#             return redirect("/")
#
#         return "Invalid Login"
#
#     return """
#
#     <h2>Login</h2>
#
#     <form method="POST">
#
#         <input
#             type="text"
#             name="username"
#             placeholder="Username"
#         >
#
#         <br><br>
#
#         <input
#             type="password"
#             name="password"
#             placeholder="Password"
#         >
#
#         <br><br>
#
#         <button type="submit">
#             Login
#         </button>
#
#     </form>
#     """
#
# # =========================
# # ❤️ SAVE JOB
# # =========================
# @app.route("/save/<jobid>")
# def save_job(jobid):
#
#     if "user" not in session:
#         return redirect("/login")
#
#     username = session["user"]
#
#     if username not in saved_jobs:
#         saved_jobs[username] = []
#
#     saved_jobs[username].append(jobid)
#
#     return redirect("/saved")
#
# # =========================
# # 📌 SAVED JOBS
# # =========================
# @app.route("/saved")
# def saved():
#
#     if "user" not in session:
#         return redirect("/login")
#
#     username = session["user"]
#
#     jobs = saved_jobs.get(username, [])
#
#     html = f"""
#     <h1>Saved Jobs</h1>
#
#     <h3>User: {username}</h3>
#
#     <ul>
#     """
#
#     for job in jobs:
#         html += f"<li>Saved Job ID: {job}</li>"
#
#     html += "</ul>"
#
#     return html
#
# # =========================
# # 📄 UPLOAD RESUME
# # =========================
# @app.route("/upload", methods=["GET", "POST"])
# def upload():
#
#     if request.method == "POST":
#
#         file = request.files["resume"]
#
#         os.makedirs("uploads", exist_ok=True)
#
#         file.save("uploads/" + file.filename)
#
#         return "Resume Uploaded Successfully"
#
#     return """
#
#     <h2>Upload Resume</h2>
#
#     <form method="POST" enctype="multipart/form-data">
#
#         <input
#             type="file"
#             name="resume"
#         >
#
#         <br><br>
#
#         <button type="submit">
#             Upload
#         </button>
#
#     </form>
#     """
#
# # =========================
# # 🚀 RUN APP
# # =========================
# if __name__ == "__main__":
#
#     port = int(os.environ.get("PORT", 5000))
#
#     app.run(host="0.0.0.0", port=port)



# _________________________________________________!!!!!___________________________________________________

from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # frontend access fix

API_KEY = "284e976fecmsh6344107e8f517cep1a8ec9jsnfffbd6a518dd"
URL = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

@app.route("/jobs")
def jobs():
    query = request.args.get("query", "developer")

    params = {
        "query": query,
        "page": "1",
        "num_pages": "1"
    }

    res = requests.get(URL, headers=headers, params=params)
    data = res.json()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)