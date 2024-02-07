import uvicorn
from src.core.configs import settings


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=settings.app_settings.PORT,
        host=settings.app_settings.HOST,
        reload=settings.app_settings.RELOAD,
    )
