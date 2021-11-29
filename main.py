from indeed import get_jobs as get_indeed_jobs
from stackof import get_jobs as get_stackof_jobs
from save import save_to_file
from flask import Flask, render_template, request

app = Flask("Scrapper")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    return render_template("report.html", searchingBy=word)


app.run()


indeed_jobs = get_indeed_jobs()
so_jobs = get_stackof_jobs()

jobs = indeed_jobs + so_jobs

save_to_file(jobs)
