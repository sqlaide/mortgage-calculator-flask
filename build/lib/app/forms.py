from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class MortgageForm(FlaskForm):
    loan_amount = FloatField("Loan Amount", validators=[DataRequired()])
    interest_rate = FloatField("Annual Interest Rate", validators=[DataRequired()])
    down_payment = FloatField("Down Payment", validators=[DataRequired()])
    property_taxes = FloatField("Property Taxes", validators=[DataRequired()])
    hoa = FloatField("HOA", validators=[DataRequired()])
    start_date = DateField("Start Date", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Calculate")
