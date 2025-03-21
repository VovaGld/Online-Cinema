from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.session import init_db, close_db
from routes import (
    movie_router,
    accounts_router,
    order_router,
    payments_router,
    shopping_cart_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Online Cinema",
    lifespan=lifespan,
)

api_version_prefix = "/api"

app.include_router(accounts_router, prefix=f"{api_version_prefix}/accounts", tags=["accounts"])
app.include_router(movie_router, prefix=f"{api_version_prefix}/movies", tags=["movies"])
app.include_router(payments_router, prefix=f"{api_version_prefix}/payments", tags=["payments"])
app.include_router(shopping_cart_router, prefix=f"{api_version_prefix}/shoppingcart", tags=["shopping cart"])
app.include_router(order_router, prefix=f"{api_version_prefix}/orders", tags=["orders"])
