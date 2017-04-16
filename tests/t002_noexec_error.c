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
    else
        return (9);
}

int
main (void)
{
    check_val (0);
    return (0);
}
