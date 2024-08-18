from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Тестовий відповідь без завантаженої моделі
    response = {"message": "This is a test response from predict_mod"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
