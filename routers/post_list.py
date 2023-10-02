from fastapi import APIRouter

router = APIRouter()


@router.get("/posts/")
async def list_of_posts():
    return [{"username": "Rick"}, {"username": "Morty"}]


def setup(app):
    app.include_router(router)
