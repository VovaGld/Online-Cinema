class CartItemException(Exception):
    pass


class CartItemNotInCartError(CartItemException):
    pass


class CartItemAlreadyInCartError(CartItemException):
    pass


class AddCartItemError(CartItemException):
    pass


class DeleteCartItemError(CartItemException):
    pass
