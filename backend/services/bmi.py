class BMICalculator:
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height

    def calculate_bmi(self):
        height_m = self.height / 100
        bmi = self.weight / (height_m ** 2)
        return round(bmi, 2)

    def get_category(self, bmi):
        if bmi < 18.5:
            return "저체중"
        elif bmi < 23:
            return "정상"
        elif bmi < 25:
            return "과체중"
        else:
            return "비만"

    def get_result(self):
        bmi = self.calculate_bmi()
        category = self.get_category(bmi)

        return {
            "bmi": bmi,
            "category": category
        }