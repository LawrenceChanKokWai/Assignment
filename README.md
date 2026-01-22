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

