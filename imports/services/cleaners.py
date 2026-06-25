def nettoyer_valeur(valeur):
    if valeur is None:
        return ""
    return str(valeur).strip()


def nettoyer_ligne(ligne):
    return {key: nettoyer_valeur(val) for key, val in ligne.items()}
