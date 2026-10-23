from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "solar-savings-project-key"

@app.route("/", methods=["GET", "POST"])
def home():
    saved = False

    if request.method == "POST":
        monthly_bill = request.form.get("monthly_bill")
        utility_increase = request.form.get("utility_increase")

        try:
            monthly_bill = float(monthly_bill)
            utility_increase = float(utility_increase)

            if monthly_bill > 0 and utility_increase >= 0:
                session["monthly_bill"] = monthly_bill
                session["utility_increase"] = utility_increase
                saved = True

        except (TypeError, ValueError):
            pass

    return render_template(
        "index.html",
        saved=saved,
        monthly_bill=session.get("monthly_bill"),
        utility_increase=session.get("utility_increase")
        )

if __name__ == "__main__":
    app.run(debug=True)