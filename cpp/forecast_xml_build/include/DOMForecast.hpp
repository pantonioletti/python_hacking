/* 
 * File:   DOMForecast.hpp
 * Author: pantonio
 *
 * Created on August 27, 2010, 11:16 AM
 */
#include <xercesc/dom/DOM.hpp>
#include <xercesc/util/XMLString.hpp>
#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/framework/StdOutFormatTarget.hpp>
#include <string>
#include <set>
#include <map>

#ifndef DOMFORECAST_HPP
#define	DOMFORECAST_HPP
using namespace xercesc;
using namespace std;

namespace wfm{

struct stIdCdName {
    XMLCh name[100];
    XMLCh code[50];
    int id;} ;

typedef stIdCdName IdCodeName;
typedef set<IdCodeName> IdCodeNameSet;
typedef set<string> CodeSet;
typedef map<string, CodeSet> CodeCodesMap;
typedef map<string, IdCodeName> IdCodeNameMap;
struct stElGroups{int id;
        string dispName;
        CodeCodesMap elGrps;};
typedef stElGroups ElementGroups;
typedef map<string, ElementGroups> definition;

class DOMForecast {
public:
    DOMForecast(char* file_name);
    virtual ~DOMForecast();
    DOMDocument* build_dom();
    void createXMLFile(DOMDocument *doc);
private:
    IdCodeNameMap grpCodeMap;
    IdCodeNameMap elemCodeMap;
    definition defMap;

    XMLCh defTag[20];
    XMLCh defElTag[20];
    XMLCh elementTag[20];
    XMLCh elGrpTag[20];
    XMLCh groupTag[20];
    XMLCh lnkElTag[20];
    XMLCh projTag[20];

    XMLCh codeAttr[20];
    XMLCh defFmtAttr[20];
    XMLCh defGrpAttr[20];
    XMLCh dispNameAttr[20];
    XMLCh elIdAttr[20];
    XMLCh grpIdAttr[20];
    XMLCh idAttr[20];
    XMLCh initValTypeAttr[20];
    XMLCh rankAttr[20];

};

#endif	/* DOMFORECAST_HPP */

}