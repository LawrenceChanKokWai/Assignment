from pathlib import Path
from tempfile import NamedTemporaryFile
import os
import re

# ==== CONSTANTS ====
VC_SUBDIR = Path("develop/global/src")
SCONSTRUCT_FILENAME = "SConstruct"
VERSION_FILENAME = "VERSION"

TMP_FILE_ARGS = {
    "mode": "w", 
    "delete": False,
    "encoding": "utf-8",
    "newline": ""
}

# ==== PATTERNS ====
SCONSTRUCT_PATTERN = re.compile( r"(point\s*=\s*)\d+(\s*,)" )
VERSION_PATTERN = re.compile(r"(ADLMSDK_VERSION_POINT\s*=\s*)\d+")

# ==== EXCEPTIONS ====
class VersionError(Exception):
    pass

class PatternMatchError(VersionError):
    pass

# ==== HELPER FUNCTION (FOR PATH FINDING) ====
def get_src_dir( source_path: Path ) -> Path:
    return source_path / VC_SUBDIR

def get_sconstruct_path(source_path: Path) -> Path:
    return get_src_dir(source_path) / SCONSTRUCT_FILENAME

def get_version_path(source_path: Path) -> Path:
    return get_src_dir(source_path) / VERSION_FILENAME


# ==== FUNCTIONS ====

# Write file function
def write_file(path: Path, content: str) -> None:
    current_file_permission = path.stat().st_mode
    with NamedTemporaryFile(**TMP_FILE_ARGS, dir=str(path.parent)) as tmp:
        tmp_path = Path(tmp.name)
        tmp.write(content)

    os.chmod(tmp_path, current_file_permission)
    os.replace(tmp_path, path)
        
# matching pattern function
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
    
def update_version( source_path: Path, build_num: str ) -> dict[str, bool]:
    sconstruct_path = get_sconstruct_path( source_path )
    version_path = get_version_path( source_path )
    
    updates = [
        ("SConstruct", sconstruct_path, SCONSTRUCT_PATTERN, r"\g<1>" + build_num + r"\g<2>"),
        ("VERSION", version_path, VERSION_PATTERN, r"\g<1>" + build_num),
    ]
    
    return _apply_updates( updates )
    
def _apply_updates( updates: list[tuple[str, Path, re.Pattern, str]] ) -> dict[str, bool]:
    results: dict[str, bool] = {}
        
    for name, path, pattern, replacement in updates:
        results[name] = _update_file_using_regex( path, pattern, replacement )
            
    return results
    
        