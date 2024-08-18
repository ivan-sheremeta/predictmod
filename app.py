import os
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import tensorflow as tf

app = Flask(__name__)

# Шлях до моделі
MODEL_PATH = 'model/my_model.keras'

# Завантажуємо модель при старті сервера
model = tf.keras.models.load_model(MODEL_PATH)

# Ensure the 'uploads' folder exists
UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    prediction = request.args.get('prediction')
    image_url = request.args.get('image_url')
    return render_template('index.html', prediction=prediction, image_url=image_url)

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Завантажуємо зображення і перетворюємо його на формат, придатний для моделі
    img = tf.keras.preprocessing.image.load_img(file_path, target_size=(224, 224))  # Змінюємо розмір зображення до 224x224 пікселів
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, 0)  # Додаємо батч
    img_array = img_array / 255.0  # Масштабування пікселів, як у коді з Colab

    # Виконуємо прогноз
    predictions = model.predict(img_array)

    # Визначення класу з найбільшою ймовірністю
    predicted_class = np.argmax(predictions, axis=1)

    # Виведення передбаченого класу
    class_labels = {0: 'Ukraine', 1: 'Russia'}  # Вкажіть відповідні назви класів
    predicted_label = class_labels[predicted_class[0]]

    # Відсоток ймовірності для передбаченого класу
    probability = np.max(predictions) * 100

    # Формуємо відповідь на основі результату
    prediction = f"Сторона: {predicted_label}. Ймовірність: {probability:.2f}%"

    # Зберігаємо результат і перенаправляємо на головну сторінку
    return redirect(url_for('index', prediction=prediction, image_url=url_for('static', filename=f'uploads/{filename}')))

if __name__ == '__main__':
    app.run(debug=True)
