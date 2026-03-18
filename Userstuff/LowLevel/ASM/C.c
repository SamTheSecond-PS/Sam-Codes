#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int len(char *string)
{
    int lenn = 0;
    int pos = 0;
    while (string[pos] != '\0')
    {
        pos += 1;
        lenn += 1;
    }

    return lenn;
}

char *f(char *sentence, char *insertable)
{
    int ilen = len(insertable);
    char *new_buff = malloc(len(sentence) + ilen - 2 + 1);
    if (*new_buff != NULL)
    {

        int sfsen = 0;

        while (sentence[sfsen] != '{' && sentence[sfsen] != '\0')
        {
            new_buff[sfsen] = sentence[sfsen];
            sfsen++;
        }

        int x = 0;
        while (x < ilen)
        {
            new_buff[sfsen + x] = insertable[x];
            x++;
        }

        int newpos = sfsen + ilen;

        sfsen += 2;

        while (sentence[sfsen] != '\0')
        {
            new_buff[newpos++] = sentence[sfsen++];
        }

        new_buff[newpos] = '\0';

        return new_buff;
    }
    else
    {
        char *failed = "Failed memory allocation";
        return failed;
    }
}

int move_until_char(char *sentence, char word)
{
    int x = 0;
    while (sentence[x] != '\0')
    {
        if (*(sentence + x) == word)
        {
            return x;
        }
        x++;
    }
    return -1;
}

void swap(char *this, char *that)
{
    char temp;

    temp = *this;
    *this = *that;
    *that = temp;
}

void reverse_string(char *string)
{
    int start = 0;
    int end = len(string) - 1;
    while (start < end)
    {
        if (start > end)
        {
            break;
        }
        swap(&string[start], &string[end]);
        start++;
        end--;
    }
}

void mcpy(char *src, char *dest, size_t i)
{
    int x = 0;
    while (x < i)
    {
        *(dest + x) = *(src + x);
        x++;
    }
}

int main()
{
    char s[1028] = "hello";
    reverse_string(s);
    printf("%s", s);
    int x = move_until_char(s, 'l');
    printf("%c", s[x]);
    char *sentence = "hello, {}";
    char *name = "sam";
    char *ss = f(sentence, name);
    printf("%s", ss);
    fflush(stdout);
    return 0;
}
