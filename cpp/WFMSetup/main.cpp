/* 
 * File:   main.cpp
 * Author: pantonio
 *
 * Created on May 16, 2011, 10:42 AM
 */

#include <cstdlib>
#include <iostream>
#include <string.h>
#include <forecast.h>
#include <zlib.h>

using namespace std;

void test_zip_read()
{
    
}
/*
 * 
 */
int main(int argc, char** argv) {

    if (argc > 1)
    {
        if (strcmp(argv[1],"FORECAST")==0)
        {
            proc_forecast(argv[2]);
            
        }
        else if (strcmp(argv[1],"LOAD_XLSX")==0)
        {
            
        }
        
    }
    
    return 0;
}

