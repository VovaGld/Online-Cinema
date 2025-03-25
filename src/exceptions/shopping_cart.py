class ShoppingCartException(Exception):
    pass


class CreateShoppingCartError(ShoppingCartException):
    pass


class AddCartItemError(ShoppingCartException):
    pass


class DeleteCartItemError(ShoppingCartException):
    pass


class ShoppingCartNotFoundError(ShoppingCartException):
    pass
