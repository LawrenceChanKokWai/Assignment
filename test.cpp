
#include <iostream>

#include "s_reverse.h"

static unsigned test_num = 0;
static unsigned fail_test_case = 0;
static const string test_string = "H0w ARE You...";

static void assert( const string &input, const string &title, const string &expected )
{
    test_num ++;
    string actual = ReverseString( input );
    if( actual != expected )
    {
        fail_test_case++;
        cout    << "Test " << test_num << ": " << title
                << " Failed: expected \"" << expected
                << "\" got \"" << actual
                << "\" (input: \"" << input << "\")"
                << endl;
    }
    else 
    {
        cout    << "Test " << test_num << ": " << title
                << " [Passed]"
                << endl;
    }
}

static void assert_address( const string *actual, const string &title, const string *expected )
{
    if( actual == expected )
    {
        fail_test_case++;
        
        cout    << "Test " << test_num << ": " << title
                << " Failed: expected \"" << expected
                << "\" got \"" << actual
                << "\" (input: \"" << actual << "\")"
                << endl;
    }
    else 
    {
        cout    << "Test " << test_num << ": " << title
                << " [Passed]"
                << endl;
    }
}
    
int main()
{
    assert(test_string, "Happy Path", "w0H ERA uoY...");
    assert("", "Single Empty String", "");
    assert("Ba     nk", "Multiple Empty String In Between", "aB     kn");
    assert(".... :::: '''' ;;;; !!!!", "Punctuation & Spaces / NO SWAPS", ".... :::: '''' ;;;; !!!!");
    assert("chan", "Single Word", "nahc");
    assert("ch-an", "With '-' in between", "hc-na");
    assert("01234", "All digits", "43210");
    assert("chan01234", "Characters With Numbers", "43210nahc");
    assert("Hi! Chan KokWai.", "With Mixed Sentence", "iH! nahC iaWkoK.");

    string b = ReverseString(test_string);
    assert_address(&test_string, "Copied string on reversed", &b);

    cout << "Total FAIL cases: " << fail_test_case << endl;

    return 0;
}

