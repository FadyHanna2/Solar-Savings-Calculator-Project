from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "solar-savings-project-key"

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        monthly_bill = request.form.get("monthly_bill")
        utility_increase = request.form.get("utility_increase")

        try:
            monthly_bill = float(monthly_bill)
            utility_increase = float(utility_increase)

            if monthly_bill > 0 and utility_increase >= 0:
                session["monthly_bill"] = monthly_bill
                session["utility_increase"] = utility_increase
                return redirect(url_for("solar_payment"))

        except (TypeError, ValueError):
            pass

    return render_template(
        "index.html",
        monthly_bill=session.get("monthly_bill"),
        utility_increase=session.get("utility_increase")
        )

@app.route("/solar-payment", methods=["GET", "POST"])
def solar_payment():

    if "monthly_bill" not in session or "utility_increase" not in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        solar_payment = request.form.get("solar_payment")
        solar_increase = request.form.get("solar_increase")

        try:
            solar_payment = float(solar_payment)
            solar_increase = float(solar_increase)

            if solar_payment > 0 and solar_increase >= 0:
                session["solar_payment"] = solar_payment
                session["solar_increase"] = solar_increase
                return redirect(url_for("solar_payment"))

        except (TypeError, ValueError):
            pass

    return render_template(
        "solar_payment.html",
        solar_payment=session.get("solar_payment"),
        solar_increase=session.get("solar_increase")
        )

if __name__ == "__main__":
    app.run(debug=True)