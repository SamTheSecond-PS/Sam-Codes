#include <stdio.h>
#include <stdlib.h>

#define MAX_DIMENSION 100

typedef struct
{
    int width;
    int height;
} Rectangle;

int area(Rectangle *r)
{
    return r->width * r->height;
}

int main()
{
    const int MIN_DIMENSION = 1;
    int wid, hei;

    Rectangle r;

    do
    {
        printf("Enter width (%d-%d): ", MIN_DIMENSION, MAX_DIMENSION);
        scanf("%d", &wid);
    } while (wid < MIN_DIMENSION || wid > MAX_DIMENSION);

    do
    {
        printf("Enter height (%d-%d): ", MIN_DIMENSION, MAX_DIMENSION);
        scanf("%d", &hei);
    } while (hei < MIN_DIMENSION || hei > MAX_DIMENSION);

    r.width = wid;
    r.height = hei;

    int ans = area(&r);
    printf("Area: %d\n", ans);

    return 0;
}