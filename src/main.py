from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from routes import (
    accounts_router,
    certification_router,
    director_router,
    genre_router,
    movie_router,
    order_router,
    payments_router,
    profiles_router,
    shopping_cart_router,
    star_router,
)

app = FastAPI(
    title="Online Cinema",
)

api_version_prefix = "/api"


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI application",
        version="1.0.0",
        description="JWT Authentication and Authorization",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.include_router(
    accounts_router, prefix=f"{api_version_prefix}/accounts", tags=["accounts"]
)
app.include_router(
    profiles_router, prefix=f"{api_version_prefix}/profiles", tags=["profiles"]
)
app.include_router(movie_router, prefix=f"{api_version_prefix}/movies", tags=["movies"])
app.include_router(genre_router, prefix=f"{api_version_prefix}/genres", tags=["genres"])
app.include_router(star_router, prefix=f"{api_version_prefix}/stars", tags=["stars"])
app.include_router(
    director_router, prefix=f"{api_version_prefix}/directors", tags=["directors"]
)
app.include_router(
    certification_router,
    prefix=f"{api_version_prefix}/certifications",
    tags=["certifications"],
)
app.include_router(
    payments_router, prefix=f"{api_version_prefix}/payments", tags=["payments"]
)
app.include_router(
    shopping_cart_router,
    prefix=f"{api_version_prefix}/shoppingcart",
    tags=["shopping cart"],
)
app.include_router(order_router, prefix=f"{api_version_prefix}/orders", tags=["orders"])

app.openapi = custom_openapi
