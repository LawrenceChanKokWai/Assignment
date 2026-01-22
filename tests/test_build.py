import unittest
import os
import stat
import re
from tempfile import TemporaryDirectory
from pathlib import Path

from build_core import write_file, _update_file_using_regex

class TestWriteFile( unittest.TestCase ):
    def test_write_file_and_permissions( self ):
        with TemporaryDirectory() as temp_dir:
            # print(f"Temp directory {temp_dir}")
            file_path = Path( temp_dir ) / "example"
            # input("Press enter to continue")
            
            # Arrange
            file_path.write_text("old text\n", encoding="utf-8")
            os.chmod( file_path, 0o640 )
            old_permission_mode = stat.S_IMODE( file_path.stat().st_mode )
            
            # Act
            write_file( file_path, "NEW TEXT!!!" )
            
            # Assert Equals to the new content after write
            self.assertEqual( file_path.read_text(encoding="utf-8"), "NEW TEXT!!!" )
            
            #Assert Equals on permission (It will be removed immediatly after the test finishes)
            new_mode = stat.S_IMODE( file_path.stat().st_mode )
            self.assertEqual( new_mode, old_permission_mode )
            
class TestUpdateFileWithRegex( unittest.TestCase ):
    def test_update_file_when_one_match( self ):
        with TemporaryDirectory() as temp_dir:
            path = Path( temp_dir ) / "one.txt"
            path.write_text( "point=6,\n", encoding="utf-8" )
            
            pattern = re.compile( r"(point=)\d+(,)" )
            replacement = r"\g<1>123\g<2>"
            
            changed = _update_file_using_regex( path, pattern, replacement )
            
            self.assertTrue( changed )
            self.assertEqual( path.read_text(encoding="utf-8"), "point=123,\n" )
            
if __name__ == "__main__":
    unittest.main