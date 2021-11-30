from indeed import get_jobs as get_indeed_jobs
from stackof import get_jobs as get_stackof_jobs
from save import save_to_file
from flask import Flask, render_template, request, redirect

app = Flask("Scrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_indeed_jobs(word) + get_stackof_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html", searchingBy=word, resultNum=len(jobs), jobs=jobs)


app.run()
