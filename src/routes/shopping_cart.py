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
    CartDetailSchema
)


router = APIRouter()


@router.get(
    "/",
    response_model=CartDetailSchema,
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
) -> CartDetailSchema:
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


@router.delete(
    "/remove/{movie_id}",
    response_model=CartItemDetailSchema,
    summary="Remove a movie from the shopping cart",
    description=(
        "<h3>Removes a specific movie from the user's shopping cart.</h3>"
        "If the movie is not found in the cart, returns an error."
    ),
    responses={
        404: {"description": "Movie or cart not found."},
        401: {"description": "Unauthorized request."}
    }
)
def remove_from_cart(
        movie_id: int,
        db: Annotated[Session, Depends(get_postgresql_db)],
        token: Annotated[str, Depends(get_token)],
        jwt_manager: Annotated[JWTAuthManager, Depends(get_jwt_auth_manager)]
) -> CartItemResponse:
    try:
        payload = jwt_manager.decode_access_token(token)
        user_id = payload.get("user_id")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    cart = get_user_cart(user, db)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = get_cart_item(cart, movie_id, db)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Movie not in cart")

    delete_cart_item(cart_item, db)
    return CartItemResponse(message="Movie removed from cart")