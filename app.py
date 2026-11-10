from flask import Flask, render_template, request, session, redirect, url_for
import requests

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
                return redirect(url_for("comparison_years"))

        except (TypeError, ValueError):
            pass

    return render_template(
        "solar_payment.html",
        solar_payment=session.get("solar_payment"),
        solar_increase=session.get("solar_increase")
        )

@app.route("/comparison-years", methods=["GET", "POST"])
def comparison_years():

    if "solar_payment" not in session or "solar_increase" not in session:
        return redirect(url_for("solar_payment"))

    if request.method == "POST":
        comparison_years = request.form.get("comparison_years")

        try:
            comparison_years = int(comparison_years)

            if comparison_years > 0:
                session["comparison_years"] = comparison_years
                return redirect(url_for("home_location"))

        except (TypeError, ValueError):
            pass


    return render_template(
        "comparison_years.html",
        comparison_years=session.get("comparison_years")
        )

@app.route("/home-location", methods=["GET", "POST"])
def home_location():

    if "comparison_years" not in session:
        return redirect(url_for("comparison_years"))
    
    error = None
    latitude = None
    longitude = None

    street_address = ""
    city = ""
    state = ""
    zip_code = ""

    if request.method == "POST":
        street_address = request.form.get("street_address", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        zip_code = request.form.get("zip_code", "").strip()

        if street_address and city and state and zip_code:

            url = "https://geocoding.geo.census.gov/geocoder/locations/address"

            params = {
                "street": street_address,
                "city": city,
                "state": state,
                "zip": zip_code,
                "benchmark": "Public_AR_Current",
                "format": "json"
            }

            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                matches = data["result"]["addressMatches"]

                if matches:
                    coordinates = matches[0]["coordinates"]

                    longitude = coordinates["x"]
                    latitude = coordinates["y"]
                    
                    session["street_address"] = street_address
                    session["city"] = city
                    session["state"] = state
                    session["zip_code"] = zip_code
                    session["latitude"] = latitude
                    session["longitude"] = longitude
                    
                    return redirect(url_for("solar_system"))

                else:
                    error = "We could not find this address. Please check the address and try again."

            except (requests.RequestException, ValueError, KeyError):
                error = "There was a problem finding the location. Please try again."

    return render_template(
        "home_location.html",
        street_address=street_address,
        city=city,
        state=state,
        zip_code=zip_code,
        latitude=latitude,
        longitude=longitude,
        error=error
        )

@app.route("/solar-system")
def solar_system():

    if "latitude" not in session or "longitude" not in session:
        return redirect(url_for("home_location"))

    return render_template("solar_system.html")

if __name__ == "__main__":
    app.run(debug=True)