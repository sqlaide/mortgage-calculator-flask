from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class MortgageForm(FlaskForm):
  loan_amount = FloatField('Loan Amount', validators=[DataRequired()])
  interest_rate = FloatField('Annual Interest Rate', validators=[DataRequired()])
  down_payment = FloatField('Down Payment', validators=[DataRequired()])
  property_taxes = FloatField('Property Taxes', validators=[DataRequired()])
  hoa = FloatField('HOA', validators=[DataRequired()])
  submit = SubmitField("Calculate")
