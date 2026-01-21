
#include "s_reverse.h"

static inline bool IsCharOrDigit( char character )
{
    return isalnum( static_cast<unsigned char>(character) ) != 0;
}

static void ReverseActionEvent( string &str, size_t firstP, size_t lastP )
{
    char* input = &str[0];
    char* pLeft = input + firstP;
    char* pRight = input + lastP -1;

    while( pLeft < pRight )
    {
        char tempHolder = *pLeft;
        *pLeft = *pRight;
        *pRight = tempHolder;
        pLeft ++;
        pRight --;
    }
}

static void Reverse( string &str )
{
    size_t i = 0;
    while( i < str.size() )
    {
        if( !IsCharOrDigit(str[i]) )
        {
            i ++;
            continue;
        }

        size_t from = i;
        while( i < str.size() && IsCharOrDigit(str[i]) )
        {
            i ++;
        }

        size_t to = i;
        
        ReverseActionEvent( str, from, to );
    }
}

string ReverseString( const string &str )
{
    string newString = str;
    Reverse( newString );
    return newString;
}
