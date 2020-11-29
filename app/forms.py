from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import DateField, DecimalField


class MortgageForm(FlaskForm):
    loan_amount = FloatField("Loan Amount", validators=[DataRequired()])
    interest_rate = FloatField("Annual Interest Rate", validators=[DataRequired()])
    down_payment = FloatField("Down Payment", validators=[Optional()])
    tax_rate = FloatField("Tax Rate", validators=[Optional()])
    hoa = FloatField("HOA", validators=[Optional()])
    home_ins = FloatField("Home Insurance", validators=[Optional()])
    start_date = DateField("Start Date", format="%Y-%m-%d", validators=[Optional()])
    submit = SubmitField("Calculate")
