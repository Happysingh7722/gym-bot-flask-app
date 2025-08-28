from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    height = db.Column(db.Float, nullable=False)  # inches
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    bmi_category = db.Column(db.String(30), nullable=False)
    diet_type = db.Column(db.String(20), nullable=False)
    recommended_protein = db.Column(db.Float, nullable=False)
    protein_total = db.Column(db.Float, nullable=False)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)

def calculate_bmi(weight, height_m):
    return round(weight / (height_m ** 2), 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_protein_factor(goal):
    factors = {
        "Weight Gain & Muscle Building": 1.8,
        "Maintenance & Healthy Living": 1.2,
        "Weight Loss & Fat Reduction": 1.5,
        "Significant Weight Loss": 1.5,
    }
    return factors.get(goal, 1.2)

def get_diet_plan(bmi_category, diet_type):
    diet_plans = {
        "Underweight": {
            "veg": {
                "goal": "Weight Gain & Muscle Building",
                "daily_calories": "2500-3000",
                "meals": {
                    "breakfast": [("Banana & Peanut Butter Smoothie (400 cal)", 12),
                                  ("2 Whole Wheat Parathas with Ghee (350 cal)", 10),
                                  ("Mixed nuts & Almonds (200 cal)", 6),
                                  ("Green Tea (5 cal)", 0)],
                    "mid_morning": [("Mixed fruit bowl with honey (150 cal)", 2),
                                    ("8-10 Almonds & 4 Walnuts (180 cal)", 6)],
                    "lunch": [("2 Cups Brown Rice (220 cal)", 10),
                              ("1 Cup Dal/Rajma/Chickpea Curry (200 cal)", 15),
                              ("Paneer Curry - 100g (265 cal)", 18),
                              ("Mixed Vegetable Sabzi (100 cal)", 3),
                              ("Curd - 1 cup (150 cal)", 8),
                              ("Salad with olive oil dressing (80 cal)", 2)],
                    "evening": [("Protein Smoothie with banana & oats (300 cal)", 20),
                                ("Handful of mixed nuts (200 cal)", 6)],
                    "dinner": [("3 Whole Wheat Rotis (210 cal)", 9),
                               ("Palak Paneer (200 cal)", 15),
                               ("Mixed Vegetable Curry (120 cal)", 3),
                               ("1 Cup Milk (150 cal)", 8)],
                },
                "tips": [
                    "Eat every 2-3 hours",
                    "Include healthy fats like ghee, nuts, avocado",
                    "Drink protein smoothies between meals",
                    "Stay hydrated with 3-4 liters water daily"
                ],
            },
            "nonveg": {
                "goal": "Weight Gain & Muscle Building",
                "daily_calories": "2500-3000",
                "meals": {
                    "breakfast": [("3 Egg Omelette with vegetables (300 cal)", 18),
                                  ("2 Whole Wheat Toast (140 cal)", 6),
                                  ("Banana Milkshake (250 cal)", 8),
                                  ("Mixed nuts (200 cal)", 6)],
                    "mid_morning": [("Greek Yogurt with fruits (200 cal)", 12),
                                    ("Almonds & Walnuts (150 cal)", 6)],
                    "lunch": [("2 Cups Brown Rice (220 cal)", 10),
                              ("Grilled Chicken Breast - 150g (250 cal)", 31),
                              ("Dal - 1 cup (150 cal)", 15),
                              ("Mixed Vegetables (100 cal)", 3),
                              ("Curd (100 cal)", 8),
                              ("Salad (50 cal)", 2)],
                    "evening": [("Protein Shake with milk (300 cal)", 25),
                                ("4 Boiled Eggs (280 cal)", 24)],
                    "dinner": [("3 Whole Wheat Rotis (210 cal)", 9),
                               ("Fish/Chicken Curry - 150g (300 cal)", 30),
                               ("Vegetable Sabzi (100 cal)", 3),
                               ("1 Cup Milk (150 cal)", 8)],
                },
                "tips": [
                    "Include lean protein in every meal",
                    "Eat 6-8 meals per day",
                    "Combine carbs with protein",
                    "Stay hydrated and exercise regularly"
                ],
            },
        },
        "Normal": {
            "veg": {
                "goal": "Maintenance & Healthy Living",
                "daily_calories": "2000-2200",
                "meals": {
                    "breakfast": [("Oats with fruits & nuts (300 cal)", 12),
                                  ("Green Tea (5 cal)", 0),
                                  ("Mixed seeds - 1 tbsp (50 cal)", 4)],
                    "mid_morning": [("1 Apple with 6 almonds (120 cal)", 4)],
                    "lunch": [("1.5 Cups Brown Rice (165 cal)", 8),
                              ("Dal - 1 cup (150 cal)", 15),
                              ("Paneer Sabzi - 80g (200 cal)", 12),
                              ("Mixed Vegetables (80 cal)", 3),
                              ("Curd - 1/2 cup (75 cal)", 4),
                              ("Green Salad (40 cal)", 2)],
                    "evening": [("Green Tea (5 cal)", 0),
                                ("Sprouts Chat (100 cal)", 6)],
                    "dinner": [("2 Whole Wheat Rotis (140 cal)", 8),
                               ("Vegetable Curry (100 cal)", 3),
                               ("Dal - 1/2 cup (75 cal)", 7),
                               ("Salad (40 cal)", 2)],
                },
               "tips": [
                        "Maintain balanced macronutrients",
                        "Include variety of colorful vegetables",
                        "Exercise 4-5 times per week",
                        "Stay hydrated with 8-10 glasses water",
                        "Incorporate regular cardio exercises like jogging, cycling, or swimming",
                        "Focus on high-intensity interval training (HIIT) to boost fat loss",
                        "Combine strength training with cardio for optimal fat burning",
                        "Keep active throughout the day to increase overall calorie expenditure"
                    ],

            },
            "nonveg": {
                "goal": "Maintenance & Healthy Living",
                "daily_calories": "2000-2200",
                "meals": {
                    "breakfast": [("2 Egg Omelette with vegetables (200 cal)", 12),
                                  ("1 Whole Wheat Toast (70 cal)", 4),
                                  ("Green Tea (5 cal)", 0)],
                    "mid_morning": [("1 Apple with almonds (120 cal)", 4)],
                    "lunch": [("1.5 Cups Brown Rice (165 cal)", 8),
                              ("Grilled Chicken - 100g (165 cal)", 31),
                              ("Dal - 1 cup (150 cal)", 15),
                              ("Mixed Vegetables (80 cal)", 3),
                              ("Curd (75 cal)", 4),
                              ("Salad (40 cal)", 2)],
                    "evening": [("Green Tea (5 cal)", 0),
                                ("Boiled Eggs - 2 (140 cal)", 12)],
                    "dinner": [("2 Whole Wheat Rotis (140 cal)", 8),
                               ("Fish/Chicken Curry - 100g (200 cal)", 25),
                               ("Vegetable Sabzi (80 cal)", 3),
                               ("Salad (40 cal)", 2)],
                },
                "tips": [
                    "Choose lean protein sources",
                    "Include omega-3 rich fish twice a week",
                    "Regular exercise and strength training",
                    "Monitor portion sizes"
                ],
            },
        },
        "Overweight": {
            "veg": {
                "goal": "Weight Loss & Fat Reduction",
                "daily_calories": "1500-1800",
                "meals": {
                    "breakfast": [("Vegetable Poha with minimal oil (200 cal)", 6),
                                  ("Green Tea (5 cal)", 0),
                                  ("6 Almonds (42 cal)", 4)],
                    "mid_morning": [("1 Orange or seasonal fruit (60 cal)", 1)],
                    "lunch": [("1 Cup Brown Rice (110 cal)", 6),
                              ("Mixed Dal - 3/4 cup (110 cal)", 12),
                              ("Mixed Vegetable Curry (60 cal)", 3),
                              ("Large Green Salad with lemon (50 cal)", 2),
                              ("Buttermilk - 1 glass (60 cal)", 3)],
                    "evening": [("Green Tea (5 cal)", 0),
                                ("Roasted Chana - handful (100 cal)", 8)],
                    "dinner": [("2 Whole Wheat Rotis (140 cal)", 8),
                               ("Mixed Vegetable Curry (80 cal)", 3),
                               ("Dal - 1/2 cup (75 cal)", 7),
                               ("Large Salad (40 cal)", 2)],
                },
                "tips": [
                    "Control portion sizes",
                    "Eat slowly and mindfully",
                    "Increase fiber intake",
                    "Exercise daily - cardio + strength training",
                    "Drink water before meals"
                ],
            },
            "nonveg": {
                "goal": "Weight Loss & Fat Reduction",
                "daily_calories": "1500-1800",
                "meals": {
                    "breakfast": [("2 Egg White Omelette with vegetables (120 cal)", 10),
                                  ("1 Whole Wheat Toast (70 cal)", 4),
                                  ("Green Tea (5 cal)", 0)],
                    "mid_morning": [("1 Apple (80 cal)", 1)],
                    "lunch": [("1 Cup Brown Rice (110 cal)", 6),
                              ("Grilled Chicken Breast - 80g (130 cal)", 25),
                              ("Dal - 3/4 cup (110 cal)", 12),
                              ("Steamed Vegetables (40 cal)", 3),
                              ("Large Salad (50 cal)", 2)],
                    "evening": [("Green Tea (5 cal)", 0),
                                ("2 Boiled Egg Whites (34 cal)", 7)],
                    "dinner": [("2 Whole Wheat Rotis (140 cal)", 8),
                               ("Grilled Fish/Chicken - 80g (150 cal)", 26),
                               ("Steamed Vegetables (60 cal)", 3),
                               ("Salad (40 cal)", 2)],
                },
                "tips": [
                    "Choose lean cuts of meat",
                    "Grill, bake, or steam instead of frying",
                    "Include protein in every meal",
                    "Regular cardio exercise",
                    "Track your food intake"
                ],
            },
        },
        "Obese": {
            "veg": {
                "goal": "Significant Weight Loss",
                "daily_calories": "1200-1500",
                "meals": {
                    "breakfast": [("Vegetable Daliya/Oats (180 cal)", 6),
                                  ("Green Tea (5 cal)", 0),
                                  ("4 Almonds (28 cal)", 3)],
                    "mid_morning": [("1 Small apple (60 cal)", 1)],
                    "lunch": [("3/4 Cup Brown Rice (85 cal)", 4),
                              ("Dal - 3/4 cup (110 cal)", 13),
                              ("Steamed Vegetables - large portion (50 cal)", 3),
                              ("Large Green Salad (40 cal)", 2),
                              ("Buttermilk (50 cal)", 3)],
                    "evening": [("Green Tea (5 cal)", 0),
                                ("Cucumber/Carrot sticks (20 cal)", 1)],
                    "dinner": [("2 Small Whole Wheat Rotis (120 cal)", 7),
                               ("Mixed Vegetable Curry (low oil) (60 cal)", 3),
                               ("Clear Dal - 1/2 cup (60 cal)", 6),
                               ("Large Salad (40 cal)", 2)],
                },
                "tips": [
                    "Strict portion control",
                    "Eat vegetables first, then proteins, then carbs",
                    "Daily exercise minimum 45 minutes",
                    "Drink warm water with lemon",
                    "Avoid processed foods completely",
                    "Consult a nutritionist"
                ],
            },
            "nonveg": {
                "goal": "Significant Weight Loss",
                "daily_calories": "1200-1500",
                "meals": {
                    "breakfast": [("2 Egg White Scramble with vegetables (100 cal)", 10),
                                  ("Green Tea (5 cal)", 0)],
                    "mid_morning": [("1 Small seasonal fruit (50 cal)", 1)],
                    "lunch": [("3/4 Cup Brown Rice (85 cal)", 4),
                              ("Grilled Chicken/Fish - 60g (100 cal)", 20),
                              ("Clear Dal (80 cal)", 7),
                              ("Large portion steamed vegetables (50 cal)", 3),
                              ("Large Salad (40 cal)", 2)],
                    "evening": [("Green Tea (5 cal)", 0),
                                ("1 Boiled Egg White (17 cal)", 4)],
                    "dinner": [("1.5 Small Rotis (90 cal)", 6),
                               ("Grilled Fish/Chicken - 60g (120 cal)", 24),
                               ("Steamed/Boiled Vegetables (50 cal)", 3),
                               ("Large Salad (40 cal)", 2)],
                },
                "tips": [
                    "High protein, low carb approach",
                    "Intensive exercise program",
                    "Meal prep and planning",
                    "Regular health check-ups",
                    "Consider professional guidance",
                    "Track progress weekly"
                ],
            },
        }
    }
    return diet_plans.get(bmi_category, {}).get(diet_type, {})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        height_feet = int(request.form['height_feet'])
        height_inch = int(request.form['height_inch'])
        height_inches = height_feet * 12 + height_inch
        height_meters = height_inches * 0.0254

        weight = float(request.form['weight'])
        diet_type = request.form['diet_type']

        bmi = calculate_bmi(weight, height_meters)
        bmi_category = get_bmi_category(bmi)
        diet_plan = get_diet_plan(bmi_category, diet_type) or {}

        protein_factor = get_protein_factor(diet_plan.get('goal', 'Maintenance & Healthy Living'))
        recommended_protein = round(weight * protein_factor, 1)

        meals = diet_plan.get("meals", {})
        # Flatten meals for template access
        diet_plan.update(meals)

        protein_total = 0
        protein_meal_breakdown = {}
        if meals:
            for meal_name, foods in meals.items():
                meal_protein = sum([protein for _, protein in foods])
                protein_meal_breakdown[meal_name] = round(meal_protein, 1)
                protein_total += meal_protein
            protein_total = round(protein_total, 1)
        else:
            protein_meal_breakdown = {}
            protein_total = 0

        user_entry = UserEntry(
            name=name,
            age=age,
            gender=gender,
            height=height_inches,
            weight=weight,
            bmi=bmi,
            bmi_category=bmi_category,
            diet_type=diet_type,
            recommended_protein=recommended_protein,
            protein_total=protein_total
        )
        db.session.add(user_entry)
        db.session.commit()

        height_formatted = f"{height_feet} ft {height_inch} in"  # Convert inches to feet

        result = {
            "name": name,
            "age": age,
            "height": height_formatted,  # height in feet now
            "weight": weight,
            "diet_type": diet_type.title(),
            "gender": gender.title(),
            "bmi": bmi,
            "bmi_category": bmi_category,
            "diet_plan": diet_plan,
            "recommended_protein": recommended_protein,
            "protein_total": protein_total,
            "protein_meal_breakdown": protein_meal_breakdown,
        }

        return render_template('result.html', result=result)

    except Exception as e:
        return f"Error: {str(e)}", 400




@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form.get('name')
        entries = UserEntry.query.filter_by(name=name).all()
        return render_template('search_result.html', entries=entries, search_name=name)
    return render_template('search.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
