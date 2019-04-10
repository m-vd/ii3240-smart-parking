from django import forms
from .models import ParkRecord

class ParkRecordForm(forms.ModelForm):
	class Meta:
		model = ParkRecord