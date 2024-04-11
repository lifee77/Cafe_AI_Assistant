# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests 

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['CORS_HEADERS'] = 'Content-Type'

#a next field that determines the next question based on the answer.
questions = {
  "1": { "text": "Do you prefer a cozy atmosphere or a trendy vibe?", "options": ["Cozy", "Trendy"], "next": {"Cozy": "2", "Trendy": "3"} },
  "2": { "text": "Coffee or tea?", "options": ["Coffee", "Tea"], "next": {} },
  "3": { "text": "Do you like quiet places or a bit of a buzz?", "options": ["Quiet", "Buzz"], "next": {} }
}

@app.route('/questions/<id>', methods=['GET'])
def get_question(id):
    return jsonify(questions[id])

@app.route('/questions/<id>', methods=['POST'])
def get_next_question(id):
    answer = request.json.get('answer')
    next_id = questions[id]['next'].get(answer)
    if next_id:
        return jsonify(questions[next_id])
    else:
        return jsonify({"message": "No more questions"})

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/questions/<id>', methods=['POST'])
def get_next_question(id):
    # ... your existing logic for handling question flow ...

    if next_id:
        return jsonify(questions[next_id])
    else:
        user_answers =  # ... Gather accumulated answers
        response = requests.post('http://localhost:5001/recommend',  # Assuming port 5001
                                json={'answers': user_answers})
        if response.status_code == 200:
            recommendations = response.json().get('cafes', [])  
            # ... Display recommendations in your frontend ...
        else:
            # ... Handle error in getting recommendations ...