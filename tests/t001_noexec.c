/* t001_noexec.c */

static int check_val (int v)
{
    if (v == 0)
        return (0);
    else
        return (1);
}

int
main (void)
{
    check_val (0);
    return (0);
}
