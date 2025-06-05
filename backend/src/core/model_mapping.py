from ..models.user import USER
from ..models.file import FILE
from ..models.chat import CHAT
from ..models.folder import FOLDER
mongoModels = {
    'coll_users'    : USER,
    'coll_files'    : FILE,
    'coll_chat'     : CHAT,
    'coll_folders'  : FOLDER,
}