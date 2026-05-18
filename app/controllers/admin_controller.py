# Rotas acessiveis apenas para administradores
from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import get_admin, hash_senha, verificar_senha, criar_token

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

templates = Jinja2Templates(directory="app/templates/users")

#Exibir usuarios do sistema
@router.get("/", response_class=HTMLResponse)
def listar_usuarios(
    request: Request,
    db: Session = Depends(get_db),
    admin = Depends(get_admin)
):
    usuarios = db.query(Usuario).order_by(Usuario.nome)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request, 
            "admin": admin,
            "usuarios": usuarios
        }
    )

@router.get("/novo", response_class=HTMLResponse)
def tela_criar_usuario(
    request: Request,
    admin = Depends(get_admin)
):
    return templates.TemplateResponse(
        request,
        "criar_usuarios.html",
        {
            "request": request, 
            "admin": admin
        }
    )

@router.post("/novo")
def cadastrar_usuario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    #Verificar se o email já existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario_existente:
        return templates.TemplateResponse(
            request,
            "templates/users/criar_usuarios.html",
            {"request": request, "erro": "E-mail já cadastrado"}
        )
    
    #Criar novo usuário
    senha_hash = hash_senha(senha)
    novo_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
    db.add(novo_usuario)
    db.commit()

    #Redirecionar para a tela de login após cadastro
    return RedirectResponse("/auth/login?cadastro=success", status_code=303)