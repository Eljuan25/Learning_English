from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Ruta para cargar la lección desde el JSON
def cargar_leccion(lesson_id):
    ruta = os.path.join('lessons', f'lesson{lesson_id}.json')
    with open(ruta, 'r', encoding='utf-8') as archivo:
        leccion = json.load(archivo)
    return leccion

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lesson/<int:lesson_id>', methods=['GET', 'POST'])
def lesson(lesson_id):
    leccion = cargar_leccion(lesson_id)

    if request.method == 'POST':
        # Recoger respuestas enviadas
        respuestas_usuario = []
        for i in range(len(leccion['practice'])):
            r = request.form.get(f'q{i}')
            respuestas_usuario.append(r)

        # Comparar respuestas y contar aciertos
        correctas = 0
        total = len(leccion['practice'])
        feedback = []

        for i, p in enumerate(leccion['practice']):
            correcta = p['answer']
            user = respuestas_usuario[i]
            acierto = (user == correcta)
            if acierto:
                correctas += 1
            feedback.append({
                'question': p['question'],
                'your_answer': user,
                'correct_answer': correcta,
                'correct': acierto
            })

        puntaje = f"{correctas} de {total} correctas"

        return render_template('lesson.html', lesson=leccion, feedback=feedback, score=puntaje)

    # Si es GET, mostrar solo la lección sin feedback
    return render_template('lesson.html', lesson=leccion)

if __name__ == '__main__':
    app.run(debug=True)
