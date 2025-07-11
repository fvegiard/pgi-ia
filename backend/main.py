"""
PGI-IA Backend API
Plateforme de Gestion Intégrée avec Intelligence Artificielle
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from pathlib import Path
import os
from datetime import datetime

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Créer les dossiers nécessaires
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    logger.info("🚀 Démarrage PGI-IA Backend...")
    yield
    logger.info("🛑 Arrêt PGI-IA Backend...")

# Initialisation FastAPI
app = FastAPI(
    title="PGI-IA API",
    description="API pour la Plateforme de Gestion Intégrée avec Intelligence Artificielle",
    version="0.1.0",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes de base
@app.get("/")
async def root():
    """Route racine - Vérification que l'API fonctionne"""
    return {
        "message": "PGI-IA API est opérationnelle! 🚀",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {
        "status": "healthy",
        "service": "pgi-ia-backend",
        "timestamp": datetime.now().isoformat()
    }

# Upload de fichiers
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload d'un fichier pour traitement par l'orchestrateur
    
    Types supportés:
    - PDF (plans, directives)
    - Images (photos chantier)
    - Emails (.eml, .msg)
    """
    try:
        # Validation du type de fichier
        allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.eml', '.msg', '.docx'}
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Type de fichier non supporté: {file_extension}"
            )
        
        # Sauvegarde du fichier
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = UPLOAD_DIR / safe_filename
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"📁 Fichier reçu: {file.filename} ({len(content)} bytes)")
        
        # TODO: Appeler l'orchestrateur ici
        # orchestrator.process_file(file_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "size": len(content),
            "path": str(file_path),
            "message": "Fichier uploadé avec succès. Traitement en cours..."
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de l'upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Routes projets
@app.get("/api/projects")
async def get_projects():
    """Récupérer la liste des projets"""
    # TODO: Récupérer depuis la base de données
    return [
        {
            "id": "kahnawake",
            "name": "S-1086 - Musée Kahnawake",
            "status": "estimation",
            "progress": 25
        },
        {
            "id": "alexis_nihon",
            "name": "C-24-048 - Place Alexis-Nihon",
            "status": "construction",
            "progress": 60
        }
    ]

@app.get("/api/projects/{project_id}/directives")
async def get_project_directives(project_id: str):
    """Récupérer les directives d'un projet"""
    # TODO: Récupérer depuis la base de données
    
    # Pour l'instant, retourner des données de test
    if project_id == "kahnawake":
        return [
            {
                "id": "CO-ME-039",
                "date": "2025-06-16",
                "description": "Repositionnement des luminaires sur rail",
                "status": "À préparer",
                "price": 0
            }
        ]
    
    return []

@app.get("/api/projects/{project_id}/timeline")
async def get_project_timeline(project_id: str):
    """Récupérer la chronologie d'un projet"""
    # TODO: Récupérer depuis la base de données
    
    return [
        {
            "id": "evt-001",
            "timestamp": "2025-07-09T08:15:00",
            "type": "file_upload",
            "title": "Plan E-101 Rev A reçu",
            "description": "Fichier PDF du plan électrique principal déposé.",
            "icon": "file-pdf"
        }
    ]

# WebSocket pour temps réel (à implémenter)
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     # Logique WebSocket ici

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )