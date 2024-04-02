import random

alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

quizzes_alphabets = {}

for letter in alphabets:
    questions = [f'/{letter}/1.jpg']
    answers = [letter]
    options = [letter]
    
    # Generate three random options (excluding the correct answer)
    while len(options) < 4:
        random_option = random.choice(alphabets)
        if random_option != letter and random_option not in options:
            options.append(random_option)

    # Shuffle the options
    random.shuffle(options)
    
    quizzes_alphabets[letter.lower()] = {'questions': questions, 'answers': answers, 'options': options}

for letter, quiz_info in quizzes_alphabets.items():
    print(f"{quiz_info['options']}")

