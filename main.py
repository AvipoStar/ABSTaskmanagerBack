from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.AuthReg import router as authReg_router
from routers.team import router as team_router
from routers.project import router as project_router
from routers.worker import router as worker_router

app = FastAPI()

# Добавляем middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Здесь можно указать список допустимых источников запросов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(
    router=authReg_router,
    prefix='/authReg'
)

app.include_router(
    router=team_router,
    prefix='/team'
)
app.include_router(
    router=project_router,
    prefix='/project'
)
app.include_router(
    router=worker_router,
    prefix='/worker'
)
