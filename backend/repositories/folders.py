from datetime import datetime
from loguru import logger
from models.models import Folder

def create_folder(db, name: str, user_id: int):
    folder = Folder(
        name=name,
        user_id=user_id,
        created_at=datetime.utcnow(),
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)
    logger.info("Created folder: folder_id={}, user_id={}", folder.folder_id, user_id)
    return folder

def get_folders_by_user(db, user_id: int):  
    folders = db.query(Folder).filter(Folder.user_id == user_id).all()
    logger.info("Retrieved {} folders for user_id={}", len(folders), user_id)
    return folders

def get_folder_by_id(db, user_id: int, folder_id: int):
    folder = db.query(Folder).filter(Folder.user_id == user_id, Folder.folder_id == folder_id).first()
    if folder:
        logger.info("Retrieved folder: folder_id={}, user_id={}", folder_id, user_id)
    else:
        logger.warning("Folder not found: folder_id={}, user_id={}", folder_id, user_id)
    return folder