#!/usr/bin/env python3
"""
Script pour extraire le texte du fichier EMAILS DEMO.pdf
Utilise PyPDF2 comme dans le directive_agent.py du projet
"""

import PyPDF2
from pathlib import Path
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def extract_pdf_text(file_path: Path) -> str:
    """Extrait le texte d'un fichier PDF"""
    text = ""
    
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            logger.info(f"📄 Nombre de pages dans le PDF: {len(pdf_reader.pages)}")
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    text += f"\n\n{'='*50}\n"
                    text += f"PAGE {page_num + 1}\n"
                    text += f"{'='*50}\n\n"
                    text += page_text
                    
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'extraction: {str(e)}")
        raise
        
    return text

def main():
    # Chemin vers le fichier PDF
    pdf_path = Path("/mnt/c/Users/fvegi/OneDrive/Desktop/EMAILS DEMO.pdf")
    
    logger.info(f"🔍 Extraction du texte de: {pdf_path}")
    
    # Vérifier que le fichier existe
    if not pdf_path.exists():
        logger.error(f"❌ Le fichier n'existe pas: {pdf_path}")
        return
        
    # Extraire le texte
    try:
        text = extract_pdf_text(pdf_path)
        
        # Afficher le texte extrait
        logger.info("\n📋 TEXTE EXTRAIT DU PDF:\n")
        print(text)
        
        # Optionnellement, sauvegarder dans un fichier texte
        output_path = Path("/home/fvegi/dev/pgi-ia/EMAILS_DEMO_extracted.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f"\n💾 Texte sauvegardé dans: {output_path}")
        
    except Exception as e:
        logger.error(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main()