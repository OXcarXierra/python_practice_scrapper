from flask import Flask, render_template, request, redirect
from exporter import save_to_file
from scrapper import get_jobs

app = Flask("Flask Scrapper")

db= {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word= word.lower()
        fromdB = db.get(word)
        if(fromdB):
            jobs = fromdB
        else : 
            jobs= get_jobs(word)
            db[word] = jobs
        job_length = len(jobs)
    else:
        return redirect("/")
    return render_template("report.html", jobLength = job_length, searchingBy=word, jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return f"Generate CSV for {word}"
    except:
        return redirect("/")
app.run(host="0.0.0.0")