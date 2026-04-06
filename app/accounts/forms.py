from django import forms
from .models import Garment


class GarmentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Garment
        fields = [
            "rfid_garment",
            "item",
            "buyer",
            "style",
            "wo",
            "color",
            "size",
        ]
        widgets = {
            "rfid_garment": forms.TextInput(attrs={"class": "form-control"}),
            "item": forms.TextInput(attrs={"class": "form-control"}),
            "buyer": forms.TextInput(attrs={"class": "form-control"}),
            "style": forms.TextInput(attrs={"class": "form-control"}),
            "wo": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
            "size": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_rfid_garment(self):
        rfid = self.cleaned_data["rfid_garment"].strip()

        if Garment.objects.filter(rfid_garment=rfid).exists():
            raise forms.ValidationError("RFID card is already registered.")

        return rfid