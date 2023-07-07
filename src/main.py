from fastapi import FastAPI, Depends

from fastapi_users import FastAPIUsers
from starlette.middleware.cors import CORSMiddleware

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from operations.router import router as router_operation

#from operations.router import router as router_operation

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.staticfiles import StaticFiles

from redis import asyncio as aioredis
from tasks.router import router as router_tasks
from pages.router import router as router_pages
from chat.router import router as router_chat
from config import REDIS_HOST, REDIS_PORT


app = FastAPI(
    title="Trading App"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request:Request, exc: ValidationError):
#     """Вывод ошибки в docs FastAPI"""
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors()}),
#     )
#
#
# fake_users = [
#     {"id":1, "role": "admin", "name": "Bob"},
# ]
#
# fake_users_2 = [
#     {"id":1, "role": "admin", "name": "Bob"},
# ]
#
# class DegreeType(Enum):
#     newbie = "newbie"
#     expert = "expert"
#
#
# class Degree(BaseModel):
#     id: int
#     created_at: datetime
#     type_degree: DegreeType # Используется выбор newbie или expert
#
#
# class User(BaseModel):
#     id: int
#     role: str
#     name: str
#     degree: Optional[List[Degree]] = [] # опциональный параметр
#
# @app.get("/users/{user_id}", response_model=List[User])
# def get_user(user_id: int):
#     return [user for user in fake_users if user.get("id") == user_id]
#
# fake_trades = [
#     {"id":1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
# ]
#
# @app.get("/trades")
# def get_trades(limit:int = 10, offset: int = 0):
#     return fake_trades[offset:][:limit]
#
#
# @app.post("/users/{user_id}")
# def change_user_name(user_id:int, new_name:str):
#     current_user = list(filter(lambda user: user.get('id')== user_id, fake_users_2))[0]
#     current_user["name"] = new_name
#     return {"status": 200, "data": current_user}
#
#
# class Trade(BaseModel):
#     id:int
#     user_id:int
#     currency: str = Field(max_length=5) # кол-во символов
#     side:str
#     price: float = Field(ge=0) # обработка на отрицательное число
#     amount: float
#
#
# @app.post("/trades")
# def add_trades(trades: List[Trade]): # определение сериализатора Trade
#     fake_trades.extend(trades)
#     return {"status": 200, "data":fake_trades}


# fastapi_users = FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    router_operation
)

app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)



@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# current_user = fastapi_users.current_user()
#
# @app.get("/protected-route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.username}"
#
# @app.get("/unprotected-route")
# def unprotected_route():
#     return f"Hello, anonym"