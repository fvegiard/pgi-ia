#!/usr/bin/env python3
"""
Extract PDF plan to image for web display
For PGI-IA Dashboard integration
"""

import os
import sys
from pathlib import Path
from pdf2image import convert_from_path
import pymupdf  # PyMuPDF
from PIL import Image

def extract_pdf_to_image(pdf_path, output_dir, dpi=150, format='PNG'):
    """
    Extract PDF to image format
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save images
        dpi: Resolution for extraction (higher = better quality)
        format: Image format (PNG, JPEG)
    
    Returns:
        List of output image paths
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    
    if not pdf_path.exists():
        print(f"❌ Erreur: Le fichier PDF n'existe pas: {pdf_path}")
        return []
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📄 Extraction du PDF: {pdf_path.name}")
    print(f"📂 Répertoire de sortie: {output_dir}")
    
    output_paths = []
    
    try:
        # Method 1: Using pdf2image (requires poppler)
        print("\n🔧 Méthode 1: Utilisation de pdf2image...")
        try:
            images = convert_from_path(str(pdf_path), dpi=dpi)
            
            for i, image in enumerate(images):
                output_name = f"{pdf_path.stem}_page_{i+1}.{format.lower()}"
                output_path = output_dir / output_name
                
                # Save with optimization
                if format.upper() == 'JPEG':
                    image.save(str(output_path), format, quality=85, optimize=True)
                else:
                    image.save(str(output_path), format, optimize=True)
                
                output_paths.append(output_path)
                print(f"✅ Page {i+1} extraite: {output_name}")
                print(f"   Dimensions: {image.width}x{image.height}")
                
        except Exception as e:
            print(f"⚠️  pdf2image a échoué: {e}")
            print("   Passage à la méthode alternative...")
            
            # Method 2: Using PyMuPDF (fallback)
            print("\n🔧 Méthode 2: Utilisation de PyMuPDF...")
            pdf_document = pymupdf.open(str(pdf_path))
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                
                # Render page to pixmap
                mat = pymupdf.Matrix(dpi/72.0, dpi/72.0)
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_data = pix.tobytes("ppm")
                img = Image.open(pymupdf.io.BytesIO(img_data))
                
                output_name = f"{pdf_path.stem}_page_{page_num+1}.{format.lower()}"
                output_path = output_dir / output_name
                
                # Save with optimization
                if format.upper() == 'JPEG':
                    img.save(str(output_path), format, quality=85, optimize=True)
                else:
                    img.save(str(output_path), format, optimize=True)
                
                output_paths.append(output_path)
                print(f"✅ Page {page_num+1} extraite: {output_name}")
                print(f"   Dimensions: {img.width}x{img.height}")
            
            pdf_document.close()
    
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        return []
    
    print(f"\n✅ Extraction terminée: {len(output_paths)} page(s)")
    return output_paths


def create_web_optimized_version(image_path, output_path, max_width=2000, quality=80):
    """
    Create a web-optimized version of the image
    
    Args:
        image_path: Path to original image
        output_path: Path for optimized image
        max_width: Maximum width for web display
        quality: JPEG quality (1-100)
    """
    img = Image.open(image_path)
    
    # Convert RGBA to RGB if needed (for JPEG)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    
    # Resize if too large
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        print(f"   Redimensionné à: {max_width}x{new_height}")
    
    # Save optimized version
    img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
    print(f"   Version web optimisée créée: {Path(output_path).name}")


if __name__ == "__main__":
    # Configuration
    pdf_path = r"C:\Users\fvegi\OneDrive\Desktop\dataset\Contrats de Projets - En cours\C24-060 - Centre Culturel Kahnawake - Les Entreprises QMD\Plan et devis construction\16 Juin 2025\Electrical\EC-M-RC01-TELECOM-CONDUITS-PATH---GROUND-LEVEL-Rev.1.pdf"
    
    # Convert Windows path to WSL path
    # C:\Users\fvegi\OneDrive\Desktop becomes /mnt/c/Users/fvegi/OneDrive/Desktop
    wsl_path = pdf_path.replace("C:\\", "/mnt/c/").replace("\\", "/")
    
    # Output directory in the frontend assets
    output_dir = Path("/home/fvegi/dev/pgi-ia/frontend/assets/plans")
    
    print("🚀 Extraction du plan PDF pour le dashboard PGI-IA")
    print("=" * 60)
    
    # Extract PDF to images
    extracted_images = extract_pdf_to_image(
        wsl_path,
        output_dir,
        dpi=200,  # High quality for technical drawings
        format='PNG'
    )
    
    # Create web-optimized versions
    if extracted_images:
        print("\n📱 Création des versions optimisées pour le web...")
        for img_path in extracted_images:
            web_path = img_path.parent / f"{img_path.stem}_web.jpg"
            create_web_optimized_version(img_path, web_path)
        
        print("\n✅ Extraction complète!")
        print(f"📂 Images disponibles dans: {output_dir}")
        print("\n📝 Prochaines étapes:")
        print("1. Mettre à jour dashboard.html pour utiliser l'image extraite")
        print("2. Ajuster les positions des marqueurs sur le plan réel")
        print("3. Implémenter le zoom et pan pour naviguer dans le plan")