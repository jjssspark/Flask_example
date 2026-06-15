from flask import Blueprint, render_template, request
from backend.services.bmi import BMICalculator
from backend.models.db import Database

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/calculate', methods=['POST'])
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

@main_bp.route('/history')
def history():
    db = Database()
    records = db.get_bmi_records(10)
    print("history records:", records)
    db.close()

    return render_template('history.html', records=records)