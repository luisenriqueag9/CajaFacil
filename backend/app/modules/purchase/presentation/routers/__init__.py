from app.modules.purchase.presentation.routers.supplier_router import router

# Wait, the module name is purchase_router! Let's correct it:
from app.modules.purchase.presentation.routers.purchase_router import router

__all__ = [
    "router",
]
