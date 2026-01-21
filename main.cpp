
#include <iostream>
#include <string>

#include "s_reverse.h"

using namespace std;

int main()
{
    string orginal = "This)IS_MYfirstAs_sessment";
    cout    << "\nInput String: " << orginal
                << "\nReversed String: "
                << ReverseString(orginal) << endl;

    return 0;
}
