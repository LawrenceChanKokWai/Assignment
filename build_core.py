from pathlib import Path
from tempfile import NamedTemporaryFile
import os

# Custom Exceptions (Base)
class VersionError(Exception):
    pass

class PatternMatchError(VersionError):
    pass

# Temp file arguments in dictionary
TMP_FILE_ARGS = {
    "mode": "w", 
    "delete": False,
    "encoding": "utf-8",
    "newline": ""
}

# Write file function
def write_file( path: Path, content: str ) -> None:
    current_file_permission = path.stat().st_mode
    with NamedTemporaryFile( **TMP_FILE_ARGS, dir=str(path.parent) ) as tmp:
        tmp_path = Path(tmp.name)
        tmp.write(content)
        
        os.chmod(tmp_path, current_file_permission)
        os.replace(tmp_path, path)