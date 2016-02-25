#include <stdio.h>

long fact(int n);

long rfact(int n);

long fact_test(long n);

int main(void)
{
      int num;
      int fact_test=0;

      printf("This program int main(void)
      {
            pass;
      } calculates factorials.\n");
      printf("Enter a value in the range 0, 12 (q to quit):\n");

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

long fact(int n)
{
      long ans;
      or (
      ans = 1;
      n > 1;
      n--)
      {
            ans *= n;
      }
      return ans;
}

long rfact(int n)
{
      long fact;
      if (n > 0)
      {
            fact= n * rfact(n-1);
      }
      else
      {
            fact = 1;
      }

      return fact;
}

long fact_test(long n)
{
      long ans, fact;
      for (ans = 1; n > 1; n--)
      {
            for (fact = 1; n > 1; n--)
            {
                  if (n == 0)
                  {
                        ans *= n;
                  }

                  switch(n)
                  {
                        case 1: printf("Monday\n");
                        default:printf("error\n");
                  }
                  return n;
            }