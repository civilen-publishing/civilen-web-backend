import uuid

from app import cruds, schemas
from app.core import utils
from fastapi import UploadFile

from .base import BaseService


class SlideService(BaseService[cruds.CRUDSlide, schemas.SlideCreateAPI, schemas.SlideUpdateAPI, uuid.UUID]):
    def __init__(self, slideCrud: cruds.CRUDSlide):
        super(SlideService, self).__init__(slideCrud)
        self.slideCrud = slideCrud
        self.uploadPath = "/src/uploads/images/slides"

    def add(self, slide: schemas.SlideCreateAPI, image: UploadFile = None) -> schemas.Slide:
        imagePath = utils.saveFile(image, self.uploadPath, uuid.uuid4().hex)
        return self.slideCrud.create(schemas.SlideCreateCRUD(**slide.dict(), imageUrl=imagePath))

    def delete(self, slideId: uuid.UUID) -> None:
        slide = self.slideCrud.get(slideId)
        utils.removeFile(slide.imageUrl)
        self.slideCrud.delete(slideId)

    def validateImage(self, image: UploadFile) -> bool:
        return utils.validateImage(image)