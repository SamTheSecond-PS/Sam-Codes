#include <iostream>
#include <fstream>
#include <cstdio>

using namespace std;

class FileSystem
{
private:
    fstream file;

public:
    void wrtF(string filename, string sentence)
    {
        file.open(filename, ios::out | ios::app);

        file << sentence << endl;

        file.close();
    }

    string rdF(string filename)
    {

        file.open(filename, ios::in);

        string line, result;

        while (getline(file, line))
        {
            result += line + "\n";
        }

        file.close();

        return result;
    }

    int delF(string filename)
    {
        if (remove(filename.c_str()) == 0)
        {
            return 0;
        }
        else
        {
            return -1;
        }
    }
};