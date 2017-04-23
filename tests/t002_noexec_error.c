/* t002_noexec_error.c */

static int check_val (int v)
{
    if (v == 0)
        return (0);
    else if (v == 1)
        return (1);
    else if (v == 2)
        return (2);
    else if (v == 3)
        return (3);
    else if (v == 4)
        return (4);
    else if (v == 5)
        return (5);
    else if (v == 6)
        return (6);
    else if (v == 7)
        return (7);
    else if (v == 8)
        return (8);
    else
        return (9);
}

int
main (void)
{
    check_val (0);
    return (0);
}
