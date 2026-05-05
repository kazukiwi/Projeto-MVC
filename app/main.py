from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="Sistema estoque")

#Configurar o Fastapi para servir os arquivos estáticos (CSS, JV, IMGS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")