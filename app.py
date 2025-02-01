import pickle
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


with open("model\model.pkl", "rb") as f:
    model = pickle.load(f)

features = model.feature_names_in_


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        age = float(request.form["age"])
        num_of_products = int(request.form["num_of_products"])
        geography = request.form["geography"]
        is_active_member = float(request.form["is_active_member"])
        gender = request.form["gender"]
        balance = float(request.form["balance"])

        geography_germany = True if geography == "Germany" else False
        geography_france = True if geography == "France" else False
        gender_female = True if gender == "Female" else False
        gender_male = True if gender == "Male" else False

        input_data = pd.DataFrame([[age, num_of_products, geography_germany, is_active_member,
                                  gender_female, gender_male, geography_france, balance]],
                                  columns=features)
        prediction = model.predict(input_data)[0]

        result = "The customer is likely to churn." if prediction == 1 else "The customer is not likely to churn."
        bg_class = "failure-background" if prediction == 1 else "success-background"
        return render_template('home.html', predicted_result=result, bg_class=bg_class)

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
