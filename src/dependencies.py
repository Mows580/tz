from src.views.services.product import ProductService
from src.views.services.review import ReviewService
from src.core.auth import get_current_user
from src.core.database import get_session
from src.views.services.auth import AuthService


def get_review_service() -> ReviewService:
    return ReviewService()

def get_product_service() -> ProductService:
    return ProductService()

def get_auth_service() -> AuthService:
    return AuthService()