import logging

from fastapi import FastAPI

from utils.directory import directory
from utils.import_supporter import ImportSupporter

app = FastAPI()
log = logging.getLogger(__name__)

view_image_supporter = ImportSupporter(app)

view_image_supporter.load_modules('routers', directory)
