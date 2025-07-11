#!/usr/bin/env python3
"""
ENTRAÎNEMENT DEEPSEEK LOCAL - PLANS KAHNAWAKE & ALEXIS-NIHON
Traitement de 300+ PDFs techniques avec extraction OCR optimisée
"""

import os
import sys
import json
import logging
import torch
from pathlib import Path
from datetime import datetime
import PyPDF2
import easyocr
import cv2
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import re
from tqdm import tqdm

# Configuration
BASE_DIR = Path("/home/fvegi/dev/pgi-ia")
PLANS_DIR = BASE_DIR / "plans_kahnawake"
ALEXIS_DIR = BASE_DIR / "plans_alexis_nihon" 
OUTPUT_DIR = BASE_DIR / "deepseek_training_complete"
MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"

# Configuration GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deepseek_training_kahnawake.log'),
        logging.StreamHandler()
    ]
)

class KahnawakePlanProcessor:
    """Processeur optimisé pour plans techniques Kahnawake"""
    
    def __init__(self):
        self.reader = easyocr.Reader(['fr', 'en'])
        self.processed_count = 0
        self.failed_count = 0
        
    def extract_text_from_pdf(self, pdf_path):
        """Extraction texte multi-méthodes pour plans techniques"""
        text_content = ""
        
        try:
            # Méthode 1: PyPDF2 pour texte natif
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text_content += page.extract_text() + "\n"
            
            # Si peu de texte extrait, utiliser OCR
            if len(text_content.strip()) < 100:
                text_content += self.extract_with_ocr(pdf_path)
                
        except Exception as e:
            logging.warning(f"Erreur extraction PDF {pdf_path}: {e}")
            text_content = self.extract_with_ocr(pdf_path)
            
        return self.clean_technical_text(text_content)
    
    def extract_with_ocr(self, pdf_path):
        """OCR optimisé pour plans techniques"""
        text_content = ""
        
        try:
            # Conversion PDF en images
            doc = fitz.open(pdf_path)
            
            for page_num in range(min(5, len(doc))):  # Limiter à 5 pages max
                page = doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))  # Haute résolution
                img_data = pix.pil_tobytes(format="PNG")
                
                # OCR avec EasyOCR
                results = self.reader.readtext(img_data)
                page_text = " ".join([result[1] for result in results])
                text_content += f"Page {page_num + 1}: {page_text}\n"
                
            doc.close()
            
        except Exception as e:
            logging.error(f"Erreur OCR {pdf_path}: {e}")
            
        return text_content
    
    def clean_technical_text(self, text):
        """Nettoyage spécialisé pour plans électriques"""
        if not text:
            return ""
            
        # Patterns techniques fréquents
        technical_patterns = {
            r'\b\d+A\b': 'ampères',
            r'\b\d+V\b': 'volts', 
            r'\b\d+W\b': 'watts',
            r'\bMCC\b': 'Motor Control Center',
            r'\bMDP\b': 'Main Distribution Panel',
            r'\bEWC\b': 'Electric/Water Cooler',
            r'\b(E-\d+)\b': r'Plan électrique \1'
        }
        
        cleaned_text = text
        for pattern, replacement in technical_patterns.items():
            cleaned_text = re.sub(pattern, replacement, cleaned_text, flags=re.IGNORECASE)
            
        # Suppression caractères parasites
        cleaned_text = re.sub(r'[^\w\s\-\.,\(\)\/]', ' ', cleaned_text)
        cleaned_text = ' '.join(cleaned_text.split())
        
        return cleaned_text
    
    def extract_plan_metadata(self, text, filename):
        """Extraction métadonnées spécifiques aux plans"""
        metadata = {
            "filename": filename,
            "project": "Kahnawake" if "kahnawake" in filename.lower() else "Alexis-Nihon",
            "plan_type": "electrical",
            "revision": "",
            "date": "",
            "elements": []
        }
        
        # Recherche numéro de plan
        plan_match = re.search(r'(E-\d+)', text, re.IGNORECASE)
        if plan_match:
            metadata["plan_number"] = plan_match.group(1)
            
        # Recherche révision
        rev_match = re.search(r'Rev\.?\s*([A-Z])', text, re.IGNORECASE)
        if rev_match:
            metadata["revision"] = rev_match.group(1)
            
        # Éléments électriques détectés
        elements = []
        element_patterns = [
            r'Panel\s+([A-Z0-9\-]+)',
            r'Circuit\s+(\d+)',
            r'Breaker\s+(\d+A?)',
            r'Transformer\s+([0-9kVA\s]+)',
            r'Motor\s+([0-9HP\s]+)'
        ]
        
        for pattern in element_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            elements.extend(matches)
            
        metadata["elements"] = list(set(elements))
        
        return metadata

class DeepSeekTrainingDatasetGenerator:
    """Générateur de dataset JSONL pour DeepSeek"""
    
    def __init__(self, processor):
        self.processor = processor
        self.training_data = []
        
    def process_plans_directory(self, plans_dir, project_name):
        """Traitement complet d'un répertoire de plans"""
        pdf_files = list(Path(plans_dir).glob("**/*.pdf"))
        
        logging.info(f"Traitement {len(pdf_files)} fichiers PDF pour {project_name}")
        
        for pdf_path in tqdm(pdf_files, desc=f"Processing {project_name}"):
            try:
                # Extraction du contenu
                text_content = self.processor.extract_text_from_pdf(pdf_path)
                metadata = self.processor.extract_plan_metadata(text_content, pdf_path.name)
                
                # Génération d'exemples d'entraînement
                self.generate_training_examples(text_content, metadata, project_name)
                
                self.processor.processed_count += 1
                
            except Exception as e:
                logging.error(f"Erreur traitement {pdf_path}: {e}")
                self.processor.failed_count += 1
                
    def generate_training_examples(self, text_content, metadata, project_name):
        """Génération d'exemples d'entraînement contextuels"""
        
        # Exemple 1: Analyse de plan
        example_1 = {
            "instruction": f"Analysez ce plan électrique du projet {project_name} et identifiez les composants principaux.",
            "input": f"Plan: {metadata.get('plan_number', 'N/A')} Rev {metadata.get('revision', 'A')}\nContenu: {text_content[:1000]}",
            "output": f"Ce plan électrique du projet {project_name} contient les éléments suivants:\n" +
                     f"- Éléments détectés: {', '.join(metadata['elements'][:5])}\n" +
                     f"- Type: {metadata['plan_type']}\n" +
                     f"- Révision: {metadata.get('revision', 'A')}\n" +
                     "Les composants sont organisés selon les standards électriques canadiens."
        }
        
        # Exemple 2: Estimation de coûts
        if metadata['elements']:
            example_2 = {
                "instruction": "Estimez les implications budgétaires pour ce plan électrique.",
                "input": f"Projet {project_name} - Éléments: {', '.join(metadata['elements'][:3])}",
                "output": f"Pour le projet {project_name}, les éléments identifiés suggèrent:\n" +
                         "- Coût estimé: Analyse requise selon devis\n" +
                         "- Impact: Modification électrique standard\n" +
                         "- Recommandation: Révision par ingénieur électrique"
            }
            self.training_data.append(example_2)
        
        # Exemple 3: Classification directive
        example_3 = {
            "instruction": "Classifiez cette information technique selon le système PGI-IA.",
            "input": f"Document: {metadata['filename']}\nProjet: {project_name}\nContenu technique détecté",
            "output": f"Classification PGI-IA:\n" +
                     f"- Catégorie: Plan électrique\n" +
                     f"- Projet: {project_name}\n" +
                     f"- Statut: À réviser\n" +
                     f"- Action: Intégration au système de suivi des directives"
        }
        
        self.training_data.extend([example_1, example_3])
        
    def save_training_dataset(self, output_path):
        """Sauvegarde du dataset au format JSONL"""
        
        # Ajout des exemples existants du PGI-IA
        existing_examples = self.load_existing_pgi_examples()
        combined_data = existing_examples + self.training_data
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in combined_data:
                json.dump(example, f, ensure_ascii=False)
                f.write('\n')
                
        logging.info(f"Dataset sauvegardé: {len(combined_data)} exemples dans {output_path}")
        return len(combined_data)
    
    def load_existing_pgi_examples(self):
        """Charge les exemples PGI-IA existants"""
        existing_path = BASE_DIR / "deepseek_training_dataset.jsonl"
        examples = []
        
        if existing_path.exists():
            try:
                with open(existing_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        examples.append(json.loads(line.strip()))
                logging.info(f"Chargé {len(examples)} exemples PGI-IA existants")
            except Exception as e:
                logging.warning(f"Erreur chargement exemples existants: {e}")
                
        return examples

class DeepSeekLocalTrainer:
    """Entraîneur DeepSeek local optimisé GPU"""
    
    def __init__(self, model_name, output_dir):
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def prepare_model_and_tokenizer(self):
        """Préparation modèle et tokenizer"""
        logging.info(f"Chargement modèle {self.model_name}")
        
        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            padding_side="right"
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        # Modèle avec optimisations mémoire
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        
        logging.info(f"Modèle chargé sur {device}")
        
    def prepare_dataset(self, jsonl_path):
        """Préparation dataset pour entraînement"""
        
        # Chargement des données
        training_texts = []
        
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())
                
                # Format d'entraînement conversationnel
                formatted_text = f"### Instruction:\n{data['instruction']}\n\n### Input:\n{data['input']}\n\n### Response:\n{data['output']}"
                training_texts.append(formatted_text)
        
        # Tokenisation
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding=True,
                max_length=2048,
                return_tensors="pt"
            )
        
        dataset = Dataset.from_dict({"text": training_texts})
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        logging.info(f"Dataset préparé: {len(tokenized_dataset)} exemples")
        return tokenized_dataset
        
    def train_model(self, dataset):
        """Entraînement du modèle"""
        
        # Configuration d'entraînement optimisée
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=1,  # Ajuster selon GPU
            gradient_accumulation_steps=8,
            warmup_steps=100,
            max_steps=1000,
            learning_rate=5e-5,
            fp16=True,  # Précision mixte pour économiser mémoire
            logging_dir=self.output_dir / "logs",
            logging_steps=10,
            save_steps=200,
            save_total_limit=3,
            prediction_loss_only=True,
            remove_unused_columns=False,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator,
        )
        
        logging.info("Début entraînement DeepSeek local")
        
        # Entraînement
        trainer.train()
        
        # Sauvegarde du modèle final
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)
        
        logging.info(f"Modèle entraîné sauvegardé dans {self.output_dir}")

def create_plans_directories():
    """Création des répertoires pour les plans"""
    plans_dir = BASE_DIR / "plans_kahnawake"
    alexis_dir = BASE_DIR / "plans_alexis_nihon"
    
    plans_dir.mkdir(exist_ok=True)
    alexis_dir.mkdir(exist_ok=True)
    
    # Instructions pour l'utilisateur
    instructions = f"""
📁 RÉPERTOIRES CRÉÉS POUR LES PLANS:

1. Plans Kahnawake (300+ PDFs):
   {plans_dir}
   
2. Plans Alexis-Nihon:
   {alexis_dir}

📋 INSTRUCTIONS:
- Déposez vos 300+ PDFs de plans Kahnawake dans le premier répertoire
- Déposez les plans Alexis-Nihon dans le second répertoire
- Les plans seront traités automatiquement avec OCR optimisé
- Le dataset d'entraînement sera généré au format JSONL

🚀 APRÈS DÉPÔT DES FICHIERS:
Relancez ce script pour démarrer l'entraînement DeepSeek local
"""
    
    print(instructions)
    
    with open(BASE_DIR / "INSTRUCTIONS_PLANS.md", 'w') as f:
        f.write(instructions)
        
    return plans_dir, alexis_dir

def main():
    """Fonction principale d'entraînement"""
    print("🧠 ENTRAÎNEMENT DEEPSEEK LOCAL - PLANS TECHNIQUES")
    print("=" * 60)
    
    # Vérification GPU
    if torch.cuda.is_available():
        print(f"✅ GPU disponible: {torch.cuda.get_device_name(0)}")
        print(f"   Mémoire GPU: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        print("⚠️ GPU non disponible - Entraînement CPU (lent)")
    
    # Création répertoires
    plans_dir, alexis_dir = create_plans_directories()
    
    # Vérification présence des plans
    kahnawake_pdfs = list(plans_dir.glob("**/*.pdf"))
    alexis_pdfs = list(alexis_dir.glob("**/*.pdf"))
    
    if not kahnawake_pdfs and not alexis_pdfs:
        print("\n⏳ Aucun plan détecté. Déposez vos PDFs dans les répertoires créés.")
        print("   Relancez ensuite ce script pour démarrer l'entraînement.")
        return
        
    print(f"\n📊 Plans détectés:")
    print(f"   Kahnawake: {len(kahnawake_pdfs)} PDFs")
    print(f"   Alexis-Nihon: {len(alexis_pdfs)} PDFs")
    
    # Traitement et entraînement
    processor = KahnawakePlanProcessor()
    dataset_generator = DeepSeekTrainingDatasetGenerator(processor)
    
    # Traitement des plans
    if kahnawake_pdfs:
        dataset_generator.process_plans_directory(plans_dir, "Kahnawake")
    if alexis_pdfs:
        dataset_generator.process_plans_directory(alexis_dir, "Alexis-Nihon")
    
    # Génération dataset
    dataset_path = OUTPUT_DIR / "training_dataset_complete.jsonl"
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    total_examples = dataset_generator.save_training_dataset(dataset_path)
    
    print(f"\n📈 Statistiques traitement:")
    print(f"   PDFs traités: {processor.processed_count}")
    print(f"   Échecs: {processor.failed_count}")
    print(f"   Exemples d'entraînement: {total_examples}")
    
    # Entraînement DeepSeek local
    if total_examples > 0:
        trainer = DeepSeekLocalTrainer(MODEL_NAME, OUTPUT_DIR)
        
        try:
            trainer.prepare_model_and_tokenizer()
            dataset = trainer.prepare_dataset(dataset_path)
            trainer.train_model(dataset)
            
            print(f"\n🎉 ENTRAÎNEMENT TERMINÉ!")
            print(f"   Modèle sauvegardé: {OUTPUT_DIR}")
            
        except Exception as e:
            logging.error(f"Erreur entraînement: {e}")
            print(f"\n❌ Erreur entraînement: {e}")
    
    print(f"\n📋 Logs complets: deepseek_training_kahnawake.log")

if __name__ == "__main__":
    main()