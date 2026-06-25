import csv
import io
import requests
from .cleaners import nettoyer_ligne
from .validators import valider_ligne
from ..models import ImportReport

API_URL = "http://127.0.0.1:5000/products"


def executer_import(dataset):
    total = 0
    inserees = 0
    rejetees = 0
    erreurs_list = []

    fichier = dataset.fichier.read()
    decoded = fichier.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded), delimiter=";")

    for ligne in reader:
        total += 1
        ligne_propre = nettoyer_ligne(ligne)
        errs = valider_ligne(ligne_propre)

        if errs:
            rejetees += 1
            erreurs_list.append(
                f"Ligne {total}: {', '.join(errs)} (donnees: {ligne_propre})"
            )
        else:
            try:
                resp = requests.post(
                    API_URL,
                    json={
                        "nom": ligne_propre["nom"],
                        "prix": float(ligne_propre["prix"]),
                        "stock": int(ligne_propre["stock"]),
                    },
                    timeout=5,
                )
                if resp.status_code == 201:
                    inserees += 1
                else:
                    rejetees += 1
                    erreurs_list.append(
                        f"Ligne {total}: API a retourne {resp.status_code} - {resp.text}"
                    )
            except requests.ConnectionError:
                rejetees += 1
                erreurs_list.append(
                    f"Ligne {total}: API Flask inaccessible - verifie que app.py tourne sur le port 5000"
                )
                break
            except Exception as e:
                rejetees += 1
                erreurs_list.append(f"Ligne {total}: Erreur - {e}")
                break

    ImportReport.objects.create(
        dataset=dataset,
        total_lignes=total,
        lignes_inserees=inserees,
        lignes_rejetees=rejetees,
        erreurs="\n".join(erreurs_list),
    )

    return {
        "total": total,
        "inserees": inserees,
        "rejetees": rejetees,
        "erreurs": erreurs_list,
    }
