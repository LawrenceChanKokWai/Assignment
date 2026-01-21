# Assessment One (Reverse string)

## Understanding the problem

Given a string:
- The word consists of letters or/and digits or/and punctuations or/and spaces or/and symbols
- To reverse each word individually
- remain the word order (unchanged)
- Punctuation, spaces and symbols will remain in their original positions

### Example
```
Original Input: "Hi, How ARE-You, 2O_2!!"
Reversed Output: "iH, woH ERA-uoY, O2_2!!"
```

### Solution
1. Run through the string from left to right
2. When it hits a word that contains chars/digits:
    - Set the first index as the starting point
    - Continue moving forward till the word ends
    - Execuate Reverse only to the part of the string
3. Continue searching for the next word after any punctuation, spaces and symbols
4. Continue until finishing the end of the string

### Pseudo
#### Helper function: `IsCharOrDigit`
- Uses `inline` since function is small and prevents function call overhead.
- `static` being used since function is used in this file only.
- `isalum`[https://en.cppreference.com/w/cpp/string/byte/isalnum], part of the std lib
- `static_cast<unsigned char>`, for value between 0 and 255
```
FUNCTION IsCharOrDigit(character):
    RETURN TRUE if character is a letter or digit
    RETURN FALSE otherwise
END FUNCTION
```

#### Static function: `ReverseActionEvent`
- Uses `size_t` which will be big enough for memory sizes. int with 32bit may overflow and int can be negative which will cause problem.
- Swapping of characters by using `pointers`.  In pointing to positions of characters in a string array. It's fine but however overkilled for short sentences or words.
- no copy is done during the process.
```
FUNCTION ReverseActionEvent(str, firstP, lastP)
    left ← firstP
    right ← lastP - 1

    WHILE left < right
        SWAP str[left] and str[right]
        left ← left + 1
        right ← right - 1
    END WHILE
END FUNCTION
```

#### Static function: `Reverse`
```
FUNCTION Reverse(str)
    i ← 0

    WHILE i < length(str)
        IF str[i] is NOT letter or digit THEN
            i ← i + 1
            CONTINUE
        END IF

        from ← i

        WHILE i < length(str) AND str[i] is letter or digit
            i ← i + 1
        END WHILE

        to ← i

        CALL ReverseActionEvent(str, from, to)
    END WHILE
END FUNCTION
```

#### Static function: `ReverseString`
- `copy` the original input before reversing the string. This keeps the orignal copy `original`.
```
FUNCTION ReverseString(input)
    newString ← copy of input
    CALL Reverse(newString)
    RETURN newString
END FUNCTION
```

### Build by using Makefile
#### `Build everything`
```
make
```

#### `Executing the program`
```
make exec
```

#### `Running the test file`
```
make run_test
```

#### `cleaning off build files`
```
make clean
```





