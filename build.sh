#!/bin/bash

echo -n "Please enter the build number: "
read BUILD_NUM

export SourcePath="$(pwd)"
export BuildNum="$BUILD_NUM"

while true
 do
    echo ""
    echo "What would you want to do?"
    echo "1) Run build"
    echo "2) Run tests"
    echo "3) Exit"
    echo -n "Choice: "
    read CHOICE

    case "$CHOICE" in
        1) 
            echo "[INFO] RUNNING BUILD..."
            python3 build.py
            ;;
        2)
            echo "[INFO] RUNNING TESTS..."
            if [ -d "tests" ]; then
                python3 -m unittest discover -s tests -p "test_*.py" -v
            else 
                python3 -m unittest discover -s test -p "test_*.py" -v
             fi
            ;;
        3)
            echo "[INFO] EXIT"
            exit 0
             ;;
        *)
            echo "[WARNING] Invalid option selected. Please enter 1, 2 OR 3"
            ;;
    esac
done
