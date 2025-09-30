from app.crud.base import CRUDBase
from app.models.models import Town
from app.schemas.town import TownCreate, TownUpdate

class CRUDTown(CRUDBase[Town, TownCreate, TownUpdate]):
    pass

town = CRUDTown(Town)