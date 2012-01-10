/* 
 * File:   main.cpp
 * Author: pantonio
 *
 * Created on August 27, 2010, 10:10 AM
 */

#include <cstdlib>
#include <iostream>
#include <fstream>
#include <set>
#include <map>
#include <iterator>
#include <string>
#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/dom/DOM.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/sax/HandlerBase.hpp>
#include <xercesc/util/XMLString.hpp>
#include "include/DOMForecast.hpp"

using namespace std;
using namespace xercesc;
using namespace wfm;

void read_data(char* file_name) {
    ifstream data;
    data.open(file_name);

    set<string> def_set;
    map<string, string> elem_map;
    map<string, string> group_map;
    char line[1024];
    data.getline(line, 1024);
    while(data)
    {
        /*
         * Line format
         * 0: Definition 15MIN
         * 1: Element Display name Atención de Vta en Piso
         * 2: Element NATE
         * 3: Group display name At.Vta Piso-Acc. Muj.
         * 4: Group D101
         * @param file_name
         */
        char *token;
        char def[20], elem[20], el_name[50], group[20], group_name[50];
        //data.getline(line, 1024);
        token = strtok(line,";");
        memcpy(def, token, strlen(token)+1);
        //cout << "Def token: " << def << "\n";
        def_set.insert(def);
        token = strtok(NULL,";");
        memcpy(el_name, token, strlen(token)+1);
        //cout << "Element name token: " << el_name << "\n";
        token = strtok(NULL,";");
        memcpy(elem, token, strlen(token)+1);
        //cout << "Element token: " << elem << "\n";
        if (elem_map.find(elem) == elem_map.end())
            elem_map[elem] = el_name;
        token = strtok(NULL,";");
        memcpy(group_name, token, strlen(token)+1);
        //cout << "Group name token: " << group_name << "\n";
        token = strtok(NULL,";");
        memcpy(group, token, strlen(token)+1);
        //cout << "Group token: " << group << "\n";
        if (group_map.find(group) == group_map.end())
            group_map[group] = group_name;
        //cout << "Group added: " << elem << "\n";

        data.getline(line, 1024);
        //cout << "Line read length: " << strlen(line) << "\n";
         
    }

    cout << "Def size: " << def_set.size() << "\n";
    map<string, string>::iterator gr_itr;
    gr_itr = group_map.begin();
    //set<string>::iterator def_itr;
    //def_itr = def_set.begin();
    for(; gr_itr != group_map.end();++gr_itr){
        cout << "Group : ";
        cout << gr_itr->first ;
        cout <<  " - ";
        cout << gr_itr->second;
        cout << "\n";
        cout.flush();
    }
    data.close();
}
/*
 * 
 */
int main(int argc, char** argv) {

    try{
        XMLPlatformUtils::Initialize();
    }
    catch(const XMLException& to_catch){
        char* message = XMLString::transcode(to_catch.getMessage());
        cout << "Error during initialization! :\n"
             << message << "\n";
        XMLString::release(&message);
        return -1;
    }

    //cout << "Create object \n";
    DOMForecast *df = new DOMForecast(argv[1]);
    //cout << "Build DOM \n";
    DOMDocument* doc = df->build_dom();
    //cout << "Print XML\n";
    if (doc)
    {
        df->createXMLFile(doc);
        doc->release();
    }
    delete df;
    XMLPlatformUtils::Terminate();
    //cout << "Starting\n";
    //cout << argc << "\n";
    //cout << argv[0] << "\n";
    //cout << argv[1] << "\n";
    //read_data(argv[1]);
    /*
    try{
        XMLPlatformUtils::Initialize();
    }
    catch(const XMLException& to_catch){
        char* message = XMLString::transcode(to_catch.getMessage());
        cout << "Error during initialization! :\n"
             << message << "\n";
        XMLString::release(&message);
        return 1;
    }

    XercesDOMParser *parser = new XercesDOMParser();
    parser->setValidationScheme(XercesDOMParser::Val_Always);
    ErrorHandler *errHandler = (ErrorHandler *) new HandlerBase();
    parser->setErrorHandler(errHandler);

    char xmlFile[]="Forecast.xml";

    try{
            parser->parse(xmlFile);
    }
    catch(const XMLException& to_catch)
    {
        char* message = XMLString::transcode(to_catch.getMessage());
        cout << "Error during parsing! :\n"
             << message << "\n";
        XMLString::release(&message);
        return 1;

    }
    catch(const DOMException& to_catch)
    {
        char* message = XMLString::transcode(to_catch.getMessage());
        cout << "DOM exception :\n"
             << message << "\n";
        XMLString::release(&message);
        return 1;

    }
    catch(const SAXParseException& to_catch)
    {
        char* message = XMLString::transcode(to_catch.getMessage());
        cout << "SAX exception :\n"
             << message << "\n";
        XMLString::release(&message);
        return 1;

    }
    catch (...) {
        cout << "Unexpected Exception \n" ;
        return -1;
    }

	delete parser;
	delete errHandler;

	XMLPlatformUtils::Terminate();
	cout << "Hello world \n";
     */
    return 0;
}

