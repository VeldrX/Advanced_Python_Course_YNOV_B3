from django.db import models


class DatasetUpload(models.Model):
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to="uploads/")
    nom_original = models.CharField(max_length=255)
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class ImportReport(models.Model):
    dataset = models.OneToOneField(
        DatasetUpload, on_delete=models.CASCADE, related_name="rapport"
    )
    total_lignes = models.IntegerField()
    lignes_inserees = models.IntegerField()
    lignes_rejetees = models.IntegerField()
    erreurs = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport - {self.dataset.titre}"
