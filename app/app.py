import os
from flask import Flask, render_template, request

from forms import MortgageForm
from calculator import MortgageCalculator

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def calculate():
    form = MortgageForm()
    form.validate_on_submit()
    if request.method == "POST":
        calculator = MortgageCalculator(
            loan_amount=form.loan_amount.data,
            interest_rate=form.interest_rate.data,
            down_payment=form.down_payment.data,
            tax_rate=form.tax_rate.data,
            hoa=form.hoa.data,
            home_ins=form.home_ins.data,
            start_date=form.start_date.data,
        )
        schedule = calculator.amortization_table()
        pmi = calculator.monthly_payment()
        property_taxes = calculator.property_taxes()

        return render_template(
            "calculate.html",
            title="Mortgage Calculator",
            form=form,
            pmi=pmi,
            property_taxes="${:,.2f}".format(property_taxes),
            tables=[
                schedule.to_html(
                    classes=".table",
                    index=False,
                    float_format=lambda x: "${:,.2f}".format(x),
                )
            ],
            header="true",
        )
    else:
        return render_template(
            "calculate.html",
            title="Mortgage Calculator",
            pmi=None,
            tables=None,
            property_taxes=None,
            form=form,
        )


if __name__ == "__main__":
    app.run(debug=True)
