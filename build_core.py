from pathlib import Path
from tempfile import NamedTemporaryFile
import os
import re

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
        
def _update_file_using_regex( path: Path, pattern: re.Pattern, replacement: str ) -> bool:
    if not path.exists():
        raise FileNotFoundError( f"File does not exist: {path}" )
    read_content = path.read_text( encoding="utf-8" )
    read_matches = list( pattern.finditer(read_content) )
        
    if len( read_matches ) != 1:
        raise PatternMatchError( f"{path}: expected exactly 1 match but found {len(read_matches)}" )
    
    updated_content = pattern.sub( replacement, read_content )
    if( updated_content == read_content ):
        return False
    write_file( path, updated_content )
    return True
    
    
        