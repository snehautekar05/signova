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
    # Add more questions here
]

scoreboard = {
    'correct': 0,
    'total': len(questions)
}

user_answers = []  # Store user's answers for review

@app.route('/')
def index():
    question_index = request.args.get('question_index', default=0, type=int)
    return render_template('index.html', question=questions[question_index], question_index=question_index)

@app.route('/answer', methods=['POST'])
def answer():
    user_answer = request.form['option']
    question_index = int(request.form['question_index'])

    user_answers.append({'question_index': question_index, 'user_answer': user_answer})

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

@app.route('/review')
def review():
    review_data = []
    for item in user_answers:
        question_index = item['question_index']
        user_answer = item['user_answer']
        correct_answer = questions[question_index]['correct_answer']
        image_url = questions[question_index]['image_url']
        review_data.append({'image_url': image_url, 'user_answer': user_answer, 'correct_answer': correct_answer})
    return render_template('review.html', review_data=review_data)

if __name__ == '__main__':
    app.run(debug=True)
