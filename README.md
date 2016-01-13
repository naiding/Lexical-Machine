BUGS:

使用test_code.c文件，运行test.py文件
（注意要修改文件路径）

1. 如果在配置文件里面允许左边括号另起一行，那么只会给源文件里面有这样的形式的另起一行，其他的并不会改变；
   也就是说，只能对已有的进行改变，无法统一全部的。
2. 如果允许左边括号留白右边不允许，那么两边都留了，无法使一边可以另一边不可以。
3. 大括号的匹配有重大bug，如下
    原始代码：
    long rfact	(int n)
    {
        long ans;
        if (n > 0) ans= n * rfact(n-1);
        else ans = 1;
        return ans;
    }

    匹配之后：
    long rfact(int n)
    {
        long ans;
        if (n > 0) ans= n * rfact(n-1);
        {
            else ans = 1;
            {
                return ans;
            }
        }
    }

4. 多条语句的自动换行实现了，但是如果前面加了关键字int等，就失效了。
5. 大括号括号对齐换行有问题。