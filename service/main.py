from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.config import DEBUG, PROJECT_NAME
from app.utils.exeption_handlers import add_all_handlers
from app.views.api_routes.about_us_routes.about_us_routes import about_us_router
from app.views.api_routes.announcements_routes.announcements_routes import (
    announcements_router,
)
from app.views.api_routes.coinquotes_routes.coinquotes_routes import coinquotes_router
from app.views.api_routes.faq_routes.faq_routes import faq_router
from app.views.api_routes.transparency_routes.transparency_routes import (
    transparency_router,
)
from app.views.api_routes.whitepaper_routes.whitepaper_routes import whitepaper_router


app = FastAPI(title=PROJECT_NAME, debug=DEBUG)

add_all_handlers(app)

app.include_router(faq_router, prefix="/faq")
app.include_router(coinquotes_router, prefix="/coin_quotes")
app.include_router(about_us_router, prefix="/about_us")
app.include_router(whitepaper_router, prefix="/whitepaper")
app.include_router(transparency_router, prefix="/transparency")
app.include_router(announcements_router, prefix="/announcements")

add_pagination(app)
