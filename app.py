from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key'

quizzes = {
    'number': {
        'questions': ['/1/1.jpg', '/2/1.jpg', '/3/1.jpg', '/4/1.jpg','/5/2.jpg', '/6/1.jpg', '/7/1.jpg', '/8/1.jpg', '/9/1.jpg',  ],
        'answers': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],  
        'options': [
            ['1', '5', '2', '7'],
            ['3', '2', '4', '1'],
            ['1', '6', '3', '7'],
            ['0', '9', '4', '2'],
            ['5', '6', '3', '8'],
            ['4', '2', '6', '9'],
            ['2', '3', '8', '7'],
            ['5', '3', '8', '4'],
            ['6', '9', '2', '7'],
        ]
    },
    'alphabet': {
        'questions': ['/A/1.jpg', '/B/1.jpg'], 
        'answers': ['C', 'A'],  
        'options': [
            ['Option 1A', 'Option 1B', 'Option 1C', 'Option 1D'],
            ['Option 2A', 'Option 2B', 'Option 2C', 'Option 2D']
        ]
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz/<category>/<int:question_num>', methods=['GET', 'POST'])
def quiz(category, question_num):
    if request.method == 'POST':
        selected_option = request.form['option']
        if selected_option == quizzes[category]['answers'][question_num - 1]:
            session['score'] = session.get('score', 0) + 1

        if question_num < len(quizzes[category]['questions']):
            return redirect(url_for('quiz', category=category, question_num=question_num + 1))
        else:
            return redirect(url_for('result', category=category))

    question = quizzes[category]['questions'][question_num - 1]
    options = quizzes[category]['options'][question_num - 1]
    return render_template('quiz.html', category=category, question_num=question_num, question=question, options=options)

@app.route('/result/<category>')
def result(category):
    score = session.get('score', 0)
    total_questions = len(quizzes[category]['questions'])
    session.pop('score', None)  
    return render_template('result.html', score=score, total_questions=total_questions, category=category)

@app.route('/review/<category>')
def review(category):
    questions = quizzes[category]['questions']
    answers = quizzes[category]['answers']
    options = quizzes[category]['options']
    enumerated_questions = list(enumerate(questions, start=1))
    return render_template('review.html', category=category, enumerated_questions=enumerated_questions, answers=answers, options=options)


if __name__ == '__main__':
    app.run(debug=True)
