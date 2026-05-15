from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# =========================
# 🔑 API CONFIG
# =========================
API_KEY = "284e976fecmsh6344107e8f517cep1a8ec9jsnfffbd6a518dd"
BASE_URL = "https://jsearch.p.rapidapi.com/search"

# =========================
# 🧠 MEMORY DB (Demo)
# =========================
users = {}
saved_jobs = {}

# =========================
# 🔎 FETCH JOBS (WITH PAGINATION)
# =========================
def fetch_jobs(query, page=1):

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "page": str(page),
        "num_pages": "1",
        "date_posted": "month"
    }

    try:
        res = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        return res.json().get("data", [])
    except:
        return []

# =========================
# 🧠 SMART QUERY
# =========================
def build_query(search, city, portal):
    q = []

    if search:
        q.append(search + " jobs")
    else:
        q.append("jobs hiring")

    if city:
        q.append("in " + city)

    portals = {
        "world": "linkedin naukri indeed glassdoor monster",
        "linkedin": "linkedin jobs",
        "naukri": "naukri jobs india",
        "indeed": "indeed jobs"
    }

    if portal in portals:
        q.append(portals[portal])

    return " ".join(q)

# =========================
# 🏠 HOME (LINKEDIN STYLE UI + PAGINATION)
# =========================
@app.route("/")
def home():

    search = request.args.get("search", "")
    city = request.args.get("city", "")
    portal = request.args.get("portal", "")
    page = int(request.args.get("page", 1))

    query = build_query(search, city, portal)
    jobs = fetch_jobs(query, page)

    html = f"""
    <html>
    <head>
        <title>JobNest - LinkedIn Style</title>

        <style>
            body {{
                font-family: Arial;
                background: #f3f2ef;
                margin: 0;
                padding: 0;
            }}

            .header {{
                background: #0a66c2;
                color: white;
                padding: 15px;
                font-size: 22px;
                font-weight: bold;
            }}

            .container {{
                width: 60%;
                margin: auto;
                padding: 20px;
            }}

            .card {{
                background: white;
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
                box-shadow: 0px 1px 3px #ccc;
            }}

            .searchbox {{
                margin: 15px 0;
            }}

            input, select {{
                padding: 8px;
                margin: 5px;
            }}

            .btn {{
                background: #0a66c2;
                color: white;
                padding: 8px 12px;
                border: none;
                cursor: pointer;
            }}

            .pagination {{
                text-align: center;
                margin: 20px;
            }}

            .pagination a {{
                padding: 8px 12px;
                margin: 5px;
                background: #0a66c2;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }}
        </style>
    </head>

    <body>

    <div class="header">🌍 JobNest Job Portal)</div>

    <div class="container">

        <form method="GET" class="searchbox">

            <input name="search" placeholder="Search Jobs" value="{search}">
            <input name="city" placeholder="City" value="{city}">

            <select name="portal">
                <option value="">All Portals</option>
                <option value="world">World</option>
                <option value="linkedin">LinkedIn</option>
                <option value="naukri">Naukri</option>
                <option value="indeed">Indeed</option>
            </select>

            <button class="btn" type="submit">Search</button>

        </form>

        <h3>Page: {page}</h3>
    """

    if not jobs:
        html += "<h3>No Jobs Found</h3>"

    for job in jobs:
        html += f"""
        <div class="card">
            <h3>{job.get('job_title')}</h3>
            <p><b>{job.get('employer_name')}</b></p>
            <p>{job.get('job_city')}</p>

            <a href="{job.get('job_apply_link')}" target="_blank">
                Apply Now
            </a>
        </div>
        """

    # =========================
    # 🔥 PAGINATION (BOTTOM)
    # =========================
    next_page = page + 1
    prev_page = page - 1

    html += f"""
    <div class="pagination">
        {"<a href='?page=" + str(prev_page) + "'>⬅ Prev</a>" if page > 1 else ""}
        <a href='?page={next_page}'>Next ➡</a>
    </div>

    </div>
    </body>
    </html>
    """

    return html


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)