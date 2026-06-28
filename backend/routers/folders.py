from database import get_db
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from repositories import folders as folders_repo

router = APIRouter(
    prefix="/folders",
    tags=["folders"],
)

@router.post("/")
async def create_folder(name: str, user_id: int, db = Depends(get_db)):
    logger.info("Create folder request received: name={}, user_id={}", name, user_id)
    folder = folders_repo.create_folder(db, name, user_id)
    return folder

@router.get("/")
def get_user_folders(user_id: int, db = Depends(get_db)):
    return folders_repo.get_folders_by_user(db, user_id)


@router.get("/{folder_id}")
def get_folder(folder_id: int, user_id: int, db = Depends(get_db)):
    folder = folders_repo.get_folder_by_id(db, user_id, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found.")
    return folder