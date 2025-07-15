"""
Fonctions utilitaires pour l'analyse des fichiers.
"""

import os


def list_files_recursive(base_dir: str, extensions=None):
    """
    Génère les chemins de fichiers sous base_dir.
    Si extensions est fourni, ne filtre que sur ces extensions (liste de '.txt', '.py', etc.).
    """
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if extensions is None or os.path.splitext(f)[1].lower() in extensions:
                yield os.path.join(root, f)