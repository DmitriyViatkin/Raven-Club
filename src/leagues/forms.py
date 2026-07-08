from django import forms
from src.results.models import Prediction

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['home_ft', 'away_ft', 'home_scored', 'away_scored',
                  'home_clean_sheet', 'away_clean_sheet',
                  'home_clean_sheet', 'away_clean_sheet'
                  ]