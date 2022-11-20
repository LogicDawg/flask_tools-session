from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app =Flask(__name__)
app.config['SECRET_KEY'] = "dogos"

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route("/")
def show_home_page():
    return render_template('home.html',survey=survey)

@app.route("/start", methods=['POST'])
def start_survey():
    session[RESPONSES_KEY] = []

    return redirect('/questions/0')

@app.route("/answer", methods=["POST"])
def question_answer():

    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
      
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:id>")
def show_question(id):
    
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[id]
    return render_template(
        "question.html", question_num=id, question=question)


@app.route("/complete")
def complete():

    return render_template("complete.html")
