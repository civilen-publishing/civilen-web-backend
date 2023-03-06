from fastapi import APIRouter

from .routers import (admin, bulk, errata, order, payment, product,
                      recommended, slide)

apiRouter = APIRouter()

apiRouter.include_router(admin.router, prefix="/admin", tags=["admin"])
apiRouter.include_router(bulk.router, prefix="/bulk", tags=["bulk"])
apiRouter.include_router(product.router, prefix="/product", tags=["product"])
apiRouter.include_router(order.router, prefix="/order", tags=["order"])
apiRouter.include_router(errata.router, prefix="/errata", tags=["errata"])
apiRouter.include_router(recommended.router, prefix="/recommended", tags=["recommended"])
apiRouter.include_router(slide.router, prefix="/slide", tags=["slide"])
apiRouter.include_router(payment.router, prefix="/payment", tags=["payment"])