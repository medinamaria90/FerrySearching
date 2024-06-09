# forms.py
from django import forms

ROUTES = (
    ("ALGECEUT", "Algeciras - Ceuta"),
    ("CEUTALGE", "Ceuta - Algeciras"),
    ("ALGETANM", "Algeciras - Tangier Med"),
    ("TANMALGE", "Tangier Med - Algeciras"),
)


class SearcherForm(forms.Form):
    route = forms.ChoiceField(choices=ROUTES)
    depart_date = forms.DateField(
        required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'}))
