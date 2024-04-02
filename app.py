from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle user selection and render flashcards
@app.route('/flashcards', methods=['POST'])
def flashcards():
    choice = request.form.get('choice')
    if choice == 'numbers':
        return render_template('flashNo.html')
    elif choice == 'alphabets':
        return render_template('flashAlpha.html')
    else:
        return redirect(url_for('home'))  # Redirect to home if invalid choice

if __name__ == '__main__':
    app.run(debug=True)
