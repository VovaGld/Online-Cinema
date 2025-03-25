from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request

from exceptions import TokenExpiredError, InvalidTokenError
from exceptions.cart_item import CartItemNotInCartError, CartItemAlreadyInCartError
from exceptions.shopping_cart import DeleteCartItemError
from security.jwt_auth_manager import JWTAuthManagerInterface
from services.shopping_cart import ShoppingCartService
from dependencies.shopping_cart import get_shopping_cart_service
from security.http import get_token
from dependencies.accounts import get_jwt_auth_manager
from schemas.shopping_cart import (
    CartItemCreateSchema,
    CartItemDetailSchema,
    CartDetailSchema,
    CartItemResponseSchema,
)


router = APIRouter()


@router.get(
    "/",
    response_model=CartDetailSchema,
    status_code=status.HTTP_200_OK,
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
        request: Request = Request,
) -> CartDetailSchema:
    create_order_url = str(request.url_for("create"))
    clear_cart_url = str(request.url_for("clear_cart"))
    response = await cart_service.get_user_cart(
        create_order_url=create_order_url,
        clear_cart_url=clear_cart_url,
    )
    return response


@router.post(
    "/add/{movie_id}",
    status_code=status.HTTP_201_CREATED,
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
        movie_id: int,
        cart_service: Annotated[ShoppingCartService, Depends(get_shopping_cart_service)],
) -> CartItemDetailSchema:
    cart = await cart_service.get_user_cart()

    try:
        response = await cart_service.add_movie_to_cart(cart.id, movie_id)
    except CartItemAlreadyInCartError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie already in cart."
        )
    return response


@router.delete(
    "/remove/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
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
async def remove_from_cart(
        movie_id: int,
        cart_service: Annotated[ShoppingCartService, Depends(get_shopping_cart_service)],
) -> None:
    cart = await cart_service.get_user_cart()

    try:
        await cart_service.remove_movie_from_cart(cart.id, movie_id)
    except CartItemNotInCartError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not in cart")
    except DeleteCartItemError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove movie")


@router.delete(
    "/clear/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove all movies from user's cart",
    description="Clear a cart from all cart items (movies).",
    responses={
        401: {"description": "Token has expired"},
        403: {"description": "Invalid Token"}
    }
)
async def clear_cart(
    cart_service: Annotated[ShoppingCartService, Depends(get_shopping_cart_service)],
):
    try:
        cart = await cart_service.get_user_cart()
    except TokenExpiredError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exception)
        )
    except InvalidTokenError as exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exception)
        )
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cart is already empty.")

    await cart_service.clear_cart(cart.id)
