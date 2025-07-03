from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.controllers.document_controller import router as document_router
from app.controllers.user_controller import router as user_router
from config.database import Base, engine
from config.config import Config
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from app.controllers.similarity_controller import router as similarity_router
from app.controllers.github_controller import GitHubController
from fastapi import Form, Query
from sqlalchemy.orm import Session
from config.database import get_db


# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configuración de evento Lifespan para evitar la deprecación de on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicialización
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    yield
    # Código de limpieza si fuera necesario
app = FastAPI(
    title="Doc2Markdown API",
    description="API para convertir documentos a Markdown",
    version="1.0.0",
    lifespan=lifespan  # Usamos lifespan en lugar de on_event
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar rutas de API
app.include_router(document_router, prefix="/api/documents", tags=["documents"])
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(similarity_router, prefix="/api/similarity", tags=["similarity"])

# Montar archivos estáticos (CSS, JS, imágenes, documentos)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory=Config.UPLOAD_FOLDER), name="uploads")

# Configurar plantillas Jinja2
templates = Jinja2Templates(directory="app/templates")

# Rutas Frontend
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/document_conversion", response_class=HTMLResponse)
async def document_conversion_page(request: Request):
    return templates.TemplateResponse("document_conversion.html", {"request": request})

# Ruta alternativa en caso de que alguien consulte /api root
@app.get("/api", response_class=HTMLResponse)
async def api_home(request: Request):
    return RedirectResponse(url="/")

@app.get("/version_history", response_class=HTMLResponse)
async def version_history_page(request: Request):
    return templates.TemplateResponse("version_history.html", {"request": request})

@app.get("/improved_document/{document_id}", response_class=HTMLResponse)
async def improved_document_page(request: Request, document_id: int):
    return templates.TemplateResponse("improved_document.html", {"request": request, "document_id": document_id})

# Rutas de GitHub
@app.get("/github/login")
async def github_login(
    request: Request,
    document_id: str = Query(None),
    document_ids: str = Query(None),
    publish_type: str = Query("readme"),
    add_home: str = Query(None),
    organization: str = Query(None),
    project_title: str = Query(None),
    context: str = Query(None),
    members: str = Query(None)
):
    return GitHubController.login(
        request, document_id, document_ids, publish_type,
        add_home, organization, project_title, context, members
    )

@app.get("/github/callback")
async def github_callback(
    request: Request, 
    code: str = Query(None), 
    state: str = Query(None)
):
    return await GitHubController.callback(request, code, state)

@app.post("/github/upload-readme")
async def github_upload_readme(
    document_id: str = Form(...),
    repo_name: str = Form(...),
    access_token: str = Form(...),
    github_user: str = Form(...),
    db: Session = Depends(get_db)
):
    return await GitHubController.upload_readme(document_id, repo_name, access_token, github_user, db)

@app.post("/github/upload-wiki")
async def github_upload_wiki(
    document_id: str = Form(...),
    repo_name: str = Form(...),
    access_token: str = Form(...),
    github_user: str = Form(...),
    db: Session = Depends(get_db)
):
    return await GitHubController.upload_wiki(document_id, repo_name, access_token, github_user, db)

# Agregar esta ruta junto con las otras rutas de GitHub
@app.post("/github/upload-wiki-multiple")
async def upload_wiki_multiple(
    document_ids: str = Form(...),
    repo_name: str = Form(...),
    access_token: str = Form(...),
    github_user: str = Form(...),
    home_page_data: str = Form(None),
    db: Session = Depends(get_db)
):
    return await GitHubController.upload_wiki_multiple(
        document_ids, repo_name, access_token, github_user, home_page_data, db
    )