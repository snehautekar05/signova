from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

questions = [
    {
        'image_url': '/numbers/1/1.jpg',
        'options': ['1', '5', '2', '7'],
        'correct_answer': '1'
    },
    {
        'image_url': '/numbers/2/1.jpg',
        'options': ['3', '2', '4', '1'],
        'correct_answer': '2'
    },
        {
        'image_url': '/numbers/3/1.jpg',
        'options': ['1', '6', '3', '7'],
        'correct_answer': '3'
    },
        {
        'image_url': '/numbers/4/1.jpg',
        'options': ['0', '9', '4', '2'],
        'correct_answer': '4'
    },
        {
        'image_url': '/numbers/5/2.jpg',
        'options': ['5', '6', '3', '8'],
        'correct_answer': '5'
    },
        {
        'image_url': '/numbers/6/1.jpg',
        'options': ['4', '2', '6', '9'],
        'correct_answer': '6'
    },
        {
        'image_url': '/numbers/7/1.jpg',
        'options': ['2', '3', '8', '7'],
        'correct_answer': '7'
    },
        {
        'image_url': '/numbers/8/1.jpg',
        'options': ['5', '3', '8', '4'],
        'correct_answer': '8'
    },
        {
        'image_url': '/numbers/9/1.jpg',
        'options': ['6', '9', '2', '7'],
        'correct_answer': '9'
    },
]

scoreboard = {
    'correct': 0,
    'total': len(questions)
}

@app.route('/')
def index():
    question_index = request.args.get('question_index', default=0, type=int)
    return render_template('index.html', question=questions[question_index], question_index=question_index)

@app.route('/answer', methods=['POST'])
def answer():
    user_answer = request.form['option']
    question_index = int(request.form['question_index'])

    if user_answer == questions[question_index]['correct_answer']:
        scoreboard['correct'] += 1

    next_question_index = question_index + 1

    if next_question_index < len(questions):
        return redirect(url_for('index', question_index=next_question_index))
    else:
        return redirect(url_for('score'))

@app.route('/score')
def score():
    return render_template('score.html', scoreboard=scoreboard)

if __name__ == '__main__':
    app.run(debug=True)
