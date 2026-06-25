from django import forms
from .models import DatasetUpload


class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = DatasetUpload
        fields = ["titre", "fichier"]

    def clean_fichier(self):
        fichier = self.cleaned_data.get("fichier")
        if fichier:
            if not fichier.name.endswith(".csv"):
                raise forms.ValidationError("Seuls les fichiers .csv sont acceptes.")
        return fichier
