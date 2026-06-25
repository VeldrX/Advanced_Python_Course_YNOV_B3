from django.shortcuts import render, redirect, get_object_or_404
from .forms import DatasetUploadForm
from .models import DatasetUpload, ImportReport
from .services.import_service import executer_import
from product_repository import get_all_products


def upload_dataset(request):
    if request.method == "POST":
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.nom_original = request.FILES["fichier"].name
            dataset.save()
            rapport = executer_import(dataset)
            return redirect("import_result", dataset_id=dataset.id)
    else:
        form = DatasetUploadForm()
    return render(request, "imports/upload.html", {"form": form})


def import_result(request, dataset_id):
    dataset = get_object_or_404(DatasetUpload, id=dataset_id)
    rapport = get_object_or_404(ImportReport, dataset=dataset)
    return render(request, "imports/result.html", {"dataset": dataset, "rapport": rapport})


def products_list(request):
    produits = get_all_products()
    return render(request, "imports/products.html", {"produits": produits})
