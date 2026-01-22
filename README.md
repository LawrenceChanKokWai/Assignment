# Assessment Two (Script on Versioning)

## Understanding the current provided code
### WHAT we understand with the original.py
- This script `updates` the build version number between `two` files as part of the build process as below stated.
    - `SConstruct`
        - The root path of the sourece tree
    - `VERSION`
        - Where the new build number to be written into the files.

- What it does:
    - The version number is taken from the `environment` variable: `BuildNum`
    - then `rewrites` them with the `updated version number.`

- `Purpose` of this script:
    - Ensures the same build is synchronised in both files.

### Inputs of requirements 
- Script depends on two environment variables.
``` bash
export SourcePath="the path to the project"
export BuildNum="the build number"
```
### Directory Structure
``` 
develop
└── global
    └── src
        ├── SConstruct
        └── VERSION
```

### Format of the file
- `SConstruct` expects a line similar to: `point=6` and `replaces` the number with the `BuildNum`
- an example content:
```
config.version = Version(
    major=15,
    minor=0,
    point=6,
    patch=0
)
```
- The VERSION script expects a line similar to  in replacing the number with the value of `BuildNum`
```
ADLMSDK_VERSION_POINT=6
```

### How to run this script
``` bash
export SourcePath="/path to the project"
export BuildNum="number"

python3 original.py
```

### Steps on what the script does
1. `Changes` file permissions to 755
2. `Opens` the original file for `reading`
3. Creates a temp file(SConstruct/VERSION) for `writing`
4. Uses a regular expression in replacing the version number
5. Write lines into the temp file
6. Close both the file
7. delete the original file
8. Renames the temp file to the original filename

### Output from provided script
- Script does not print anything on the console while it's a success.
- check the output result using `cat`

### Inital syntax that was changed before refactoring
- changed from 0755 to 0o755 (as accordance to python3 which i'm using)
```python
os.chmod(os.path.join(os.environ["SourcePath"],"develop","global","src","SConstruct"), 0o755)
```
- cleared off warnings by adding `r` as raw strings in front of the string resolving syntax warning
```python
line=re.sub(r"point\=[\d]+","point="+os.environ["BuildNum"],line)
line=re.sub(r"ADLMSDK_VERSION_POINT=[\d]+","ADLMSDK_VERSION_POINT="+os.environ["BuildNum"],line)
```

## Constrints on current implementation
- No `error handling`
- environment variables must always exists
- files must always exists
- it overwrites the file permissions
- Uses non-atomic file replacements to delete and rename. (which to say, inconsistency)
- No verification on any replacement which has happened

## Refactoring goals
- shall make file updates atomic and safe
- shall add validations
- improve the maintaince and testability

### Refactoring tree structure of the project
```python
assessmentTwo
├── README.md
├── build.py                        #the main entrypoint
├── build_core.py             #implentations
├── develop
│   └── global
│       └── src
│           ├── SConstruct
│           └── VERSION
├── original.py                     #the orignal provided code
└── test
    └── test_build.py           #test file
```

---
### Constraints
This refactor code enforces **exact matching** to avoid corruption.
- Both target file must exsist
- The regex pattern must match **exactly one time** in the file. Which means:
    - IF **0 matches**, "FAIL"
    - IF **Greater than 1 matches**, TRUE
- IF the replacement produces the same content, the file content shall not be rewritten. 

### Benifits
- Writes will be performed using a temporary file by using NamedTemporaryFile, and replaced using `os.replace(...)` performing the update.
- Original file permissions are preserved.

### Pseudocode
- High Level algorithm:
```python
READ SourcePath from the enviroment
READ BuildNum from the environment
IF SourcePath or BuildNum are not set:
    PRINT the error
EXIT with a non-zero code

SET SourcePath/develop/global/src to base_dir
DEFINE updaterules:
    RULE1: 
        base_dir/SConstruct as file
        (point\s*=\s*)\d+(\s*,) as the pattern
        group1 + BuildNum + group2 as replacement
    RULE2:
        base_dir/VERSION as file
        (ADLMSDK_VERSION_POINT\s*=\s*)\d+ as pattern
        group1 + BuildNum as replacement
FOR each of the rule in update:
    IF file does not exist:
        RAISE FileNotFoundError Exception
    READ the file content
        FIND matches using regex
    IF number of matches is not 1
        RAISE PatternMatchError Exception
APPLY replacement
    IF updated content is the same as the original content:
        MARK result as "NO CHANGE"
    ELSE:
        WRITE with the updated content
        MARK the result as "UPDATED"
PRINT the result
EXIT with success
```

## Running the program
- From the project root: export the details and run the program.
```bash
export SourcePath="$(pwd)
export BuildNum="**the build number**"

python3 build.py
```

## Testing 
- Run all unit tests:
```
python3 -m unittest -v  

OR

python3 -m unittest discover -s tests -p "test_*.py" -v
```

## References used
- Make your Python Code More Readable with Custom Exceptions https://www.youtube.com/watch?v=hLLaw9BI-EE
-  Modular Docs / NamedTemporaryFile https://docs.modular.com/mojo/std/tempfile/tempfile/NamedTemporaryFile/
- Modular Doc / stat https://docs.modular.com/mojo/std/stat/stat/
- Modular Docs / TemporaryDirectory https://docs.modular.com/mojo/std/tempfile/tempfile/TemporaryDirectory
- Modular Docs / testing https://docs.modular.com/mojo/std/testing/testing/
- Modular Docs / Dictionary https://docs.modular.com/mojo/std/collections/dict/Dict/
- re — Regular expression operations https://docs.python.org/3/library/re.html