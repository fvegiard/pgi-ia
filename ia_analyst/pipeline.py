"""
Pipeline d'analyse de données :
- Parcours récursif du répertoire de données
- Extraction de contenu pertinent
- Génération de vecteurs sémantiques
- Analyse des embeddings pour non-conformités et optimisations
- Stockage des résultats (vecteurs et métadonnées)
"""

from utils import list_files_recursive


def run(data_dir: str):
    """
    Exécute la chaîne de traitement complète sur le dossier spécifié.
    """
    files = list(list_files_recursive(data_dir))
    # TODO: implémenter le traitement de fichiers,
    # génération des embeddings et analyse
    print(f"Trouvé {len(files)} fichiers à analyser dans '{data_dir}'")