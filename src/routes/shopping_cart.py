from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from security.jwt_auth_manager import JWTAuthManagerInterface
from services.shopping_cart import ShoppingCartService
from dependencies.shopping_cart import get_shopping_cart_service
from security.http import get_token
from dependencies.accounts import get_jwt_auth_manager
from schemas.shopping_cart import (
    CartItemCreateSchema,
    CartItemDetailSchema,
    CartResponseSchema
)


router = APIRouter()


@router.get(
    "/",
    response_model=CartResponseSchema,
    summary="Retrieve user's shopping cart",
    description=(
        "<h3>Fetch the user's shopping cart.</h3>"
        "Returns a list of movies currently in the user's shopping cart."
    ),
    responses={
        404: {"description": "User not found."},
        401: {"description": "Unauthorized request."}
    }
)
async def get_cart(
        cart_service: Annotated[ShoppingCartService, Depends(get_shopping_cart_service)],
        token: Annotated[str, Depends(get_token)],
        jwt_manager: Annotated[JWTAuthManagerInterface, Depends(get_jwt_auth_manager)],
) -> CartResponseSchema:
    response = await cart_service.get_user_cart(token, jwt_manager)
    return response


@router.post(
    "/add",
    response_model=CartItemDetailSchema,
    summary="Add a movie to the shopping cart",
    description=(
        "<h3>Add a movie to the user's shopping cart.</h3>"
        "Validates availability and ensures the movie is not already in the cart."
    ),
    responses={
        404: {"description": "User or movie not found."},
        400: {"description": "Movie already in cart."},
        401: {"description": "Unauthorized request."}
    }
)
async def add_to_cart(
        item_data: CartItemCreateSchema,
        cart_service: Annotated[ShoppingCartService, Depends(get_shopping_cart_service)],
        token: Annotated[str, Depends(get_token)],
        jwt_manager: Annotated[JWTAuthManagerInterface, Depends(get_jwt_auth_manager)],
) -> CartItemDetailSchema:
    movie_id = item_data.movie_id
    cart = await cart_service.get_user_cart(token, jwt_manager)

    response = await cart_service.add_movie_to_cart(cart.id, movie_id)

    return response
