from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)

# Inicializa el cliente de OpenAI correctamente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["pregunta"]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return jsonify({"respuesta": response.choices[0].message.content})
        except Exception as e:
            return jsonify({"respuesta": f"Error: {str(e)}"})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
