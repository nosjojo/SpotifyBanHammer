from typing import Union
import json
import pathlib
from banhammer_service import USER_DIR

def dump_response_to_file(data:Union[str, dict], name:str) -> None:
    file = pathlib.Path(USER_DIR)/f"{name}.json"
    with open(file, 'wt') as f:
        json.dump(data, f)
    return
