from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

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

    clil = ", ".join(components)
    prompt = (
        f"Мектеп мұғалімі ретінде {grade}-сыныпқа арналған информатика сабағы бойынша рефлексия сұрақтарын құрастыр. "
        f"Тақырып: {topic}. CLIL компоненттері: {clil}. Bloom таксономиясы: {bloom}. "
        f"Рефлексия әдісі: {reflex_type}. 5 сұрақ бер және соңында 3 цифрлық құрал ұсын (сілтемелерімен)."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        answer = response.choices[0].message.content

        # HTML-инструменты
        tools_html = "<h4>🔧 Ұсынылатын цифрлық құралдар:</h4><ul>"
        for name, url in TOOLS.items():
            tools_html += f'<li><a href="{url}" target="_blank">{name}</a></li>'
        tools_html += "</ul>"

        return jsonify({"questions": answer + tools_html})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
