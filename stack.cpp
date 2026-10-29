#include <iostream>
#include <stack>
using namespace std;

bool isBalanced(string s)
{
    stack<char> st;

    for (char ch : s)
    {
        // Opening brackets
        if (ch == '(' || ch == '{' || ch == '[')
        {
            st.push(ch);
        }

        // Closing brackets
        else if (ch == ')' || ch == '}' || ch == ']')
        {
            if (st.empty())
                return false;

            char top = st.top();
            st.pop();

            if ((ch == ')' && top != '(') ||
                (ch == '}' && top != '{') ||
                (ch == ']' && top != '['))
            {
                return false;
            }
        }
    }

    return st.empty();
}

int main()
{
    string s;

    cout << "Enter string: ";
    getline(cin, s);

    if (isBalanced(s))
        cout << "Balanced";
    else
        cout << "Not balanced";

    return 0;
}