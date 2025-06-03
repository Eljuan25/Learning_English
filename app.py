from flask import Flask, render_template, request, redirect, url_for, abort
import json
import os

app = Flask(__name__)

def cargar_leccion(lesson_id):
    ruta = os.path.join('lessons', f'lesson{lesson_id}.json')
    if not os.path.exists(ruta):
        abort(404, description=f"Lección {lesson_id} no encontrada")
    with open(ruta, 'r', encoding='utf-8') as archivo:
        leccion = json.load(archivo)
    return leccion

@app.route('/')
def index():
    # Aquí podrías listar las lecciones disponibles dinámicamente si quieres
    return render_template('index.html')

@app.route('/lesson/<int:lesson_id>', methods=['GET', 'POST'])
def lesson(lesson_id):
    leccion = cargar_leccion(lesson_id)

    if request.method == 'POST':
        respuestas_usuario = []
        for i in range(len(leccion.get('practice', []))):
            r = request.form.get(f'q{i}')
            respuestas_usuario.append(r)

        correctas = 0
        total = len(leccion.get('practice', []))
        feedback = []

        for i, p in enumerate(leccion.get('practice', [])):
            correcta = p.get('answer')
            user = respuestas_usuario[i]
            acierto = (user == correcta)
            if acierto:
                correctas += 1
            feedback.append({
                'question': p.get('question'),
                'your_answer': user,
                'correct_answer': correcta,
                'correct': acierto
            })

        puntaje = f"{correctas} de {total} correctas"

        return render_template('lesson.html', lesson=leccion, feedback=feedback, score=puntaje)

    # GET request solo muestra la lección
    return render_template('lesson.html', lesson=leccion)

if __name__ == '__main__':
    app.run(debug=True)
