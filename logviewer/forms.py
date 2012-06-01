from django import forms

class RecordSearchForm(forms.Form):
    start_date = forms.DateField()
    end_date   = forms.DateField()
    incoming   = forms.BooleanField()
    outgoing   = forms.BooleanField()
