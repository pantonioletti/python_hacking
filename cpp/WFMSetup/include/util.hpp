/* 
 * File:   util.hpp
 * Author: pantonio
 *
 * Created on May 16, 2011, 5:44 PM
 */
#include <string>
#include <vector>
#include <zlib.h>|

/*
#include <xercesc/dom/DOM.hpp>
#include <xercesc/util/XMLString.hpp>
#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/framework/StdOutFormatTarget.hpp>
**/
using namespace std;

#ifndef UTIL_HPP
#define	UTIL_HPP

#ifdef	__cplusplus
extern "C" {
#endif


#if defined(MSDOS) || defined(OS2) || defined(WIN32) || defined(__CYGWIN__)
#  include <fcntl.h>
#  include <io.h>
#  define SET_BINARY_MODE(file) setmode(fileno(file), O_BINARY)
#else
#  define SET_BINARY_MODE(file)
#endif

#define CHUNK 262144
    
    
   

#ifdef	__cplusplus
}
#endif

void get_tokens(string str, string separator, vector<string>* v)
{
    //vector<string> v = new vector<string>();
    
    int cur_sep=0, last_sep = 0;
    
    while ((cur_sep = str.find(separator, last_sep)) != string::npos)
    {
        string s = str.substr(last_sep, cur_sep-last_sep);
        v->push_back(s);
        last_sep=cur_sep+1;
    }
}


/*using namespace xercesc;

struct stIdCdName {
    XMLCh name[100];
    XMLCh code[50];
    int id;} ;

typedef stIdCdName IdCodeName;
*/

#endif	/* UTIL_HPP */

