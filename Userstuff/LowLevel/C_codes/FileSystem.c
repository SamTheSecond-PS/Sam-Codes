#include <stdio.h>
#include <stdlib.h>
#include <io.h>
#include <string.h>
#include <stdarg.h>

int writeToFile(char *filename, char *mode, char *string, char *specifications, ...)
{
    FILE *f = fopen(filename, mode);
    if (!f)
        return -1;

    va_list args;
    va_start(args, specifications);

    vfprintf(f, specifications, args);

    va_end(args);

    fclose(f);
    return 0;
}