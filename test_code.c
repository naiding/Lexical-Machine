// 1 /* hh *
/* 2 // */
// 3
   /* 4
   5
   // 6
   */

#include <stdio.h>
#include <cmath.h>

long fact(int n);
long rfact (int n);

int main (  void    )
{
int num;

printf("This program calculates factorials.\n");
    printf("Enter a value in the range 0-12 (q to quit):\n");

    while (scanf("%d", &num) == 1)
    {
        if (num < 0)
        {
            printf("No negative numbers, please.\n");
        }
        else if (num > 12)
        {
            printf("Keep input under 13.\n");
        }
        else
        {
            printf("loop: %d factorial = %ld\n", num, fact(num));
            printf("recursion: %d factorial = %ld\n", num, rfact(num));
        }
        printf("Enter a value in the range 0-12 (q to quit):\n");
    }
    printf("Bye.\n");
    return 0;
}

long fact
(int n)
{
    long ans;
    for (ans = 1;n > 1;n--){
        ans *= n;
    }
    ;//这里就是一个空语句
    float a = 1, b = 2, c = 3;
    a = 2; c = 4;; b = 2;
    ;a = 4; b = a;;;c = a + b;;
    return ans;
}

long rfact	(int n)
{
    ;//这里就是一个空语句
    long ans;
    if (n > 0) ans= n * rfact(n-1);
    else ans = 1;

    if (n > 0) {
        ans= n * rfact(n-1);
    } else {
        ans = 1;
    }
    return ans;
}
