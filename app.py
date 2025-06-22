from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://cliledu.kz"}})

# 🗝️ OpenAI клиент
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Онлайн құралдар
TOOLS = {
    "Padlet": "https://padlet.com",
    "Mentimeter": "https://www.mentimeter.com",
    "Kahoot": "https://kahoot.com",
    "Wordwall": "https://wordwall.net",
    "Google Forms": "https://forms.google.com"
}

@app.route("/generate_reflection", methods=["POST"])
def generate_reflection():
    data = request.get_json()

    topic = data.get("topic", "")
    grade = data.get("grade", "")
    bloom = data.get("bloom", "")
    reflex_type = data.get("reflexType", "")
    components = data.get("components", [])

    clil_components = ", ".join(components)

    prompt = (
        f"Мұғалім ретінде {grade}-сыныпқа арналған информатика сабағына арналған рефлексия сұрақтарын дайында. "
        f"Тақырып: {topic}. CLIL компоненттері: {clil_components}. Bloom таксономиясы: {bloom}. "
        f"Рефлексия әдісі: {reflex_type}. 5 нақты сұрақ дайында және соңында 3 онлайн құралды ұсын (сілтемелерімен)."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content

        tools_html = "<h4>🔧 Ұсынылатын цифрлық құралдар:</h4><ul>"
        for name, url in TOOLS.items():
            tools_html += f'<li><a href="{url}" target="_blank">{name}</a></li>'
        tools_html += "</ul>"

        return jsonify({"questions": answer + tools_html})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
