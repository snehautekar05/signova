import os
import mediapipe as mp
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import pyttsx3
from threading import Thread
from flask import Flask, render_template, Response, request, redirect, url_for, session,make_response


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'super_secret_key'


# Load the machine learning model
model_dict = pickle.load(open('./model_4.p', 'rb'))
model = model_dict['model_4']
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True,
                       min_detection_confidence=0.4, max_num_hands=2)

# Global variables for frame skipping optimization
frame_count = 0
frame_skip = 2  # Process every 2nd frame

def extractData(result) -> list:
    dataLeft = []
    dataRight = []
    totalData = []
    for handType, handLms in zip(result.multi_handedness, result.multi_hand_landmarks):
        if handType.classification[0].label == 'Left':
            for i in range(len(handLms.landmark)):
                x = handLms.landmark[i].x
                y = handLms.landmark[i].y
                dataLeft.append(x)
                dataLeft.append(y)
        else:
            for i in range(len(handLms.landmark)):
                x = handLms.landmark[i].x
                y = handLms.landmark[i].y
                dataRight.append(x)
                dataRight.append(y)

    if len(dataLeft) == 0 and len(dataRight) == 42:
        dataLeft = [0] * 42
    if len(dataRight) == 0 and len(dataLeft) == 42:
        dataRight = [0] * 42
    totalData.extend(dataLeft)
    totalData.extend(dataRight)
    return totalData

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def draw(img, result):
    for hand_landmarks in result.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            img,  # image to draw
            hand_landmarks,  # model output
            mp_hands.HAND_CONNECTIONS,  # hand connections
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

def generate_frames():
    global frame_count

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue  # Skip processing this frame

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)
        if result.multi_hand_landmarks:
            draw(frame, result)
            frame_data = extractData(result)
            pred = model.predict([np.asarray(frame_data)])
            cv2.putText(frame, pred[0], (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)
            
            # Start a new thread for text-to-speech
            Thread(target=text_to_speech, args=(pred[0],)).start()

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/translator')
def translator():
    return render_template('translator.html')

@app.route('/learner')
def learner():
    return render_template('learner.html')


# Route to handle user selection and render flashcards
@app.route('/flashcards', methods=['POST'])
def flashcards():
    choice = request.form.get('choice')
    if choice == 'numbers':
        return render_template('flashno.html')
    elif choice == 'alphabets':
        return render_template('flashAlpha.html')
    else:
        return redirect(url_for('learner')) 

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
        'questions': ['/A/A.jpg', '/B/B.jpg', '/C/C.jpg', '/D/D.jpg', '/E/E.jpg', '/F/F.jpg', '/G/G.jpg', '/H/H.jpg', '/I/I.jpg', '/J/J.jpg', '/K/K.jpg', '/L/L.jpg', '/M/M.jpg', '/N/N.jpg', '/O/O.jpg', '/P/P.jpg', '/Q/Q.jpg', '/R/R.jpg', '/S/S.jpg', '/T/T.jpg', '/U/U.jpg', '/V/V.jpg', '/W/W.jpg', '/X/X.jpg', '/Y/Y.jpg', '/Z/Z.jpg'], 
        'answers': ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],  
        'options': [
           ['U', 'A', 'R', 'Z'],
['K', 'C', 'B', 'A'],
['T', 'S', 'R', 'C'],
['D', 'M', 'V', 'Q'],
['T', 'Y', 'F', 'E'],
['O', 'S', 'F', 'Y'],
['G', 'O', 'C', 'Y'],
['E', 'C', 'T', 'H'],
['I', 'K', 'F', 'Q'],
['J', 'W', 'O', 'Q'],
['Q', 'K', 'Z', 'I'],
['L', 'C', 'K', 'Z'],
['M', 'C', 'D', 'E'],
['T', 'N', 'S', 'B'],
['O', 'N', 'I', 'F'],
['O', 'V', 'A', 'P'],
['Q', 'Z', 'X', 'V'],
['J', 'C', 'R', 'H'],
['Q', 'S', 'R', 'I'],
['R', 'H', 'T', 'S'],
['E', 'Q', 'U', 'M'],
['P', 'I', 'V', 'Z'],
['S', 'I', 'W', 'J'],
['S', 'Z', 'K', 'X'],
['Y', 'F', 'J', 'N'],
['Z', 'W', 'J', 'N'],

        ]
    }
}

user_answers = []  # Store user's answers for review

@app.route('/quiz')
def render_quiz():
    return render_template('home.html')

@app.route('/quiz/<category>/<int:question_num>', methods=['GET', 'POST'])
def quiz(category, question_num):
    if request.method == 'POST':
        selected_option = request.form['option']
        user_answers.append({'user_answer': selected_option})
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
    correct_percent = score/total_questions*100
    correct_percent =  round(correct_percent, 2)
    print(correct_percent)
    wrong_percent = 100-correct_percent
    print(wrong_percent)
    session.pop('score', None)  
    return render_template('result.html', score=score, total_questions=total_questions, category=category, correct_percent=correct_percent, wrong_percent=wrong_percent)

@app.route('/review/<category>', methods=['GET','POST'])
def review(category):
    print(user_answers)
    review_data = []
    for item in user_answers:
    #     question_num = item['question_num']
        user_answer=item['user_answer']
    #     answers = quizzes[category]['answers']
    #     questions = quizzes[category]['questions']
    #     enumerated_questions = list(enumerate(questions, start=1))
        review_data.append({'user_answer':user_answer})
    print(review_data)
    # return render_template('review.html', review_data=review_data, category=category)

    questions = quizzes[category]['questions']
    answers = quizzes[category]['answers']
    options = quizzes[category]['options']
    enumerated_questions = list(enumerate(questions, start=1))

    combined_data = []
    for index, question in enumerate(enumerated_questions):
        combined_data.append({
            'question': question[1],
            'review_item': review_data[index],
            'correct_answer': answers[index]
    })
    print(combined_data)
    return render_template('review.html', category=category, combined_data=combined_data, answers=answers, options=options, review_data=review_data)



if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    app.run(debug=True)

    cap.release()
    cv2.destroyAllWindows()