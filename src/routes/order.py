from fastapi import APIRouter
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.ext.asyncio import AsyncSession

# from database.session import get_db
# from repositories.order_rep import create_order, get_movie_from_card
# from schemas.order import OrderCreateResponseSchema

router = APIRouter()

# @router.post("/create/")
# async def create(
#     db: AsyncSession = Depends(get_db)
# ) -> OrderCreateResponseSchema:
#     try:
#         order = await create_order(
#             db=db,
#             user_id=1,
#             movies= await get_movie_from_card(
#                 user_id=1,
#                 db=db
#             )
#         )
#     except SQLAlchemyError as e:
#         raise e
#     return OrderCreateResponseSchema(
#         order_id=order.id,
#         total_price=order.total_amount,
#         status=order.status,
#         payment_url="some url",
#     )