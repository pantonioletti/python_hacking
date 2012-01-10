#include <cstdio>
#include <iostream>
#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/dom/DOM.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/sax/HandlerBase.hpp>
#include <xercesc/util/XMLString.hpp>

using namespace std;
using namespace xercesc;

int main (int argc, char* argv[])
{
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
	return 0;
}