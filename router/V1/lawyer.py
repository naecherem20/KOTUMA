
from database.connection import get_session
from schema.lawyer_schemas import LawyerCreate, LawyerRead, LawyerBase
from services.lawyer_service import create_lawyer
from models.lawyer_models import Lawyer

router = APIRouter(prefix="/api/v1/lawyers", tags=["Lawyers"])



@router.get("/{full_name}", response_model=LawyerBase)
def find_lawyers(full_name: str, session: Session = Depends(get_session)):
    existing_lawyer = session.exec(
        select(Lawyer).where(func.upper(Lawyer.full_name) == full_name.upper())
    ).first()
    if not existing_lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found!!")
    return existing_lawyer

