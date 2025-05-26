import os
import requests
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Cliente de OpenAI actualizado
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

def get_airtable_data():
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json().get("records", [])
        texto = ""
        for rec in records:
            fields = rec.get("fields", {})
            texto += " | ".join([f"{k}: {v}" for k, v in fields.items()]) + "\n"
        return texto
    else:
        return "No se pudieron obtener los datos de Airtable."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():
    pregunta = request.json.get("pregunta")
    datos = get_airtable_data()

    prompt = f"""Sos un experto en caballos de polo. Estos son los datos de la base:
{datos}

Pregunta: {pregunta}
Respondé en lenguaje claro, profesional y directo.
"""

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return jsonify({"respuesta": respuesta.choices[0].message.content})
    except Exception as e:
        return jsonify({"respuesta": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
