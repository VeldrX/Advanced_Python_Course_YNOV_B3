def valider_ligne(ligne):
    erreurs = []

    if not ligne.get("nom"):
        erreurs.append("Champ 'nom' manquant")

    if not ligne.get("prix"):
        erreurs.append("Champ 'prix' manquant")
    else:
        try:
            float(ligne["prix"])
        except ValueError:
            erreurs.append("'prix' doit etre un nombre")

    if not ligne.get("stock"):
        erreurs.append("Champ 'stock' manquant")
    else:
        try:
            int(ligne["stock"])
        except ValueError:
            erreurs.append("'stock' doit etre un entier")

    return erreurs
