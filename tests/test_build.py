import unittest
import os
import stat
import re
from tempfile import TemporaryDirectory
from pathlib import Path

from build_core import write_file, _update_file_using_regex, PatternMatchError

class TestWriteFile( unittest.TestCase ):
    def test_write_file_and_permissions( self ):
        with TemporaryDirectory() as temp_dir:
            # print(f"Temp directory {temp_dir}")
            file_path = Path( temp_dir ) / "example"
            # input("Press enter to continue")
            
            file_path.write_text("old text\n", encoding="utf-8")
            os.chmod( file_path, 0o640 )
            old_permission_mode = stat.S_IMODE( file_path.stat().st_mode )
            
            write_file( file_path, "NEW TEXT!!!" )
            
            self.assertEqual( file_path.read_text(encoding="utf-8"), "NEW TEXT!!!" )
            
            new_mode = stat.S_IMODE( file_path.stat().st_mode )
            self.assertEqual( new_mode, old_permission_mode )
            
class TestUpdateFileWithRegex( unittest.TestCase ):
    def test_update_file_when_one_match( self ):
        with TemporaryDirectory() as temp_dir:
            path = Path( temp_dir ) / "one"
            path.write_text( "point=6,\n", encoding="utf-8" )
            
            pattern = re.compile( r"(point=)\d+(,)" )
            replacement = r"\g<1>123\g<2>"
            
            changed = _update_file_using_regex( path, pattern, replacement )
            
            self.assertTrue( changed )
            self.assertEqual( path.read_text(encoding="utf-8"), "point=123,\n" )
            
    def test_preserves_permissions(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "permissions"
            path.write_text("point=6,\n", encoding="utf-8")
            
            os.chmod(path, 0o640)
            old_mode = stat.S_IMODE(path.stat().st_mode)

            pattern = re.compile(r"(point=)\d+(,)")
            replacement = r"\g<1>777\g<2>"

            changed = _update_file_using_regex(path, pattern, replacement)

            self.assertTrue(changed)
            self.assertEqual(path.read_text(encoding="utf-8"), "point=777,\n")
            new_mode = stat.S_IMODE(path.stat().st_mode)
            self.assertEqual(new_mode, old_mode)
            
    def test_raises_pattern_match_error_when_there_is_no_match(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nomatch.txt"
            path.write_text("hello world\n", encoding="utf-8")

            pattern = re.compile(r"(point=)\d+(,)")
            replacement = r"\g<1>123\g<2>"

            with self.assertRaises(PatternMatchError):
                _update_file_using_regex(path, pattern, replacement)
                
    def test_raises_pattern_match_error_when_there_is_no_match(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nomatch.txt"
            path.write_text("hello world\n", encoding="utf-8")

            pattern = re.compile(r"(point=)\d+(,)")
            replacement = r"\g<1>123\g<2>"

            with self.assertRaises(PatternMatchError):
                _update_file_using_regex(path, pattern, replacement)
                
    def test_raises_file_not_found_error(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "missing.txt"

            pattern = re.compile(r"(point=)\d+(,)")
            replacement = r"\g<1>123\g<2>"

            with self.assertRaises(FileNotFoundError):
                _update_file_using_regex(path, pattern, replacement)
                
    def test_returns_false_when_already_updated(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "same.txt"
            path.write_text("point=123,\n", encoding="utf-8")

            pattern = re.compile(r"(point=)\d+(,)")
            replacement = r"\g<1>123\g<2>"

            changed = _update_file_using_regex(path, pattern, replacement)

            self.assertFalse(changed)
            self.assertEqual(path.read_text(encoding="utf-8"), "point=123,\n")
            
if __name__ == "__main__":
    unittest.main