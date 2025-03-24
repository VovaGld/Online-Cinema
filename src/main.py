from fastapi import FastAPI

from routes import (
    movie_router,
    genre_router,
    star_router,
    certification_router,
    director_router,
    accounts_router,
    order_router,
    payments_router,
    shopping_cart_router,
)

app = FastAPI(
    title="Online Cinema",
)

api_version_prefix = "/api"

app.include_router(accounts_router, prefix=f"{api_version_prefix}/accounts", tags=["accounts"])
app.include_router(movie_router, prefix=f"{api_version_prefix}/movies", tags=["movies"])
app.include_router(genre_router, prefix=f"{api_version_prefix}/genres", tags=["genres"])
app.include_router(star_router, prefix=f"{api_version_prefix}/stars", tags=["stars"])
app.include_router(director_router, prefix=f"{api_version_prefix}/directors", tags=["directors"])
app.include_router(certification_router, prefix=f"{api_version_prefix}/certifications", tags=["certifications"])
app.include_router(payments_router, prefix=f"{api_version_prefix}/payments", tags=["payments"])
app.include_router(shopping_cart_router, prefix=f"{api_version_prefix}/shoppingcart", tags=["shopping cart"])
app.include_router(order_router, prefix=f"{api_version_prefix}/orders", tags=["orders"])
