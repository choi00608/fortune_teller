from flask import Flask, render_template, request
import saju_core
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    hour = request.form['hour']
    location = request.form['location']
    question = request.form['question']

    birth_info = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "location": location,
        "question": question,
    }

    prompt = saju_core.generate_saju_prompt(birth_info)
    saju_data = saju_core.get_saju_analysis_from_gemini(prompt)
    print(f"--- Gemini API Raw Response ---\n{saju_data}\n---------------------------------")
    
    try:
        final_data = json.loads(saju_core.extract_json_from_string(saju_data))
    except (json.JSONDecodeError, TypeError):
        final_data = {"error": "결과를 처리하는 중 오류가 발생했습니다. 유효한 JSON 형식이 아닙니다."}
    return render_template('result.html', saju_result=final_data)

if __name__ == '__main__':
    app.run(debug=True)
