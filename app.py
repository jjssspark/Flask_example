from flask import Flask, render_template, request
from bmi import BMICalculator
from db import Database

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        if weight <= 0 or height <= 0:
            return render_template('index.html', error="체중과 신장은 양수여야 합니다.")

        calculator = BMICalculator(weight, height)
        result = calculator.get_result()

        db = Database()
        saved = db.save_bmi_record(weight, height, result["bmi"], result["category"])
        print("DB 저장 결과:", saved)
        db.close()

        return render_template(
            'result.html',
            bmi=result["bmi"],
            category=result["category"],
            weight=weight,
            height=height
        )

    except ValueError:
        return render_template('index.html', error="유효한 숫자를 입력해주세요.")

@app.route('/history')
def history():
    db = Database()
    records = db.get_bmi_records(10)
    print("history records:", records)
    db.close()

    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)