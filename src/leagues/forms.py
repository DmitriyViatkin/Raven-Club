from django import forms
from src.results.models import Prediction

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['home_ft', 'away_ft',

                  ]