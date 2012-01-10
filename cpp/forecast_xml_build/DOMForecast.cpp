/* 
 * File:   DOMForecast.cpp
 * Author: pantonio
 * 
 * Created on August 27, 2010, 11:16 AM
 */

#include "include/DOMForecast.hpp"
#include <iostream>
#include <fstream>
#include <cstring>

using namespace std;
using namespace wfm;
using namespace xercesc;

DOMForecast::DOMForecast(char* file_name) {
    int grpId = 50;
    int elemId = 50;
    int defId=1;

    ifstream data;
    data.open(file_name);

    char line[1024];
    data.getline(line, 1024);
    //First of all define de Sales element and the default group
    IdCodeName salesEl, defGrp;
    XMLString::transcode("Ventas", salesEl.code, 49);
    XMLString::transcode("Ventas", salesEl.name, 99);
    salesEl.id = 1;
    this->elemCodeMap["Ventas"] = salesEl;


    XMLString::transcode("Default", defGrp.code, 49);
    XMLString::transcode("Default", defGrp.name, 99);
    defGrp.id = 1;
    this->grpCodeMap["Default"] = defGrp;

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
        string def, elem, el_name, group, group_name;
        token = strtok(line,";");
        def = token;
        /*
         * If defininition was not added yet, I add it to the definitions map
         * and increment the definition id variable
         */
        map<string,ElementGroups>::iterator defIt = defMap.find(def);
        ElementGroups *defElGrpMap;
        if (defIt==defMap.end())
        {
            ElementGroups elGrpMap;
            elGrpMap.id = defId++;
            defMap[def] = elGrpMap;
            defElGrpMap = &elGrpMap;
        }
        else
            defElGrpMap = &(defIt->second);

        /*
         * If element has not been added yet to elements map
         * I add it and increment the element id
         */
        token = strtok(NULL,";");
        el_name = token;
        token = strtok(NULL,";");
        elem = token;
        IdCodeName newElem;
        XMLString::transcode(elem.c_str(), newElem.code,49);
        if (elemCodeMap.find(elem)== elemCodeMap.end())
        {
            XMLString::transcode(el_name.c_str(), newElem.name,49);
            newElem.id = elemId++;
            elemCodeMap[elem] = newElem;
        }

        /*
         * If group has not been added yet to groups map
         * I add it and increment the group id
         */
        token = strtok(NULL,";");
        group_name = token;
        token = strtok(NULL,";");
        group = token;
        IdCodeName newGroup;
        XMLString::transcode(group.c_str(), newGroup.code,49);
        if (grpCodeMap.find(group) == grpCodeMap.end())
        {
            XMLString::transcode(group_name.c_str(), newGroup.name,99);
            newGroup.id = grpId++;
            grpCodeMap[group]= newGroup;
        }

        /*
         * If the element has not been associated to the definition yet I
         * create a set of groups and associate the element with the groups
         * set.
         * If the element already exists I just add the group to groups set
         * associated to the element
         */

        // AQUI ESTA EL RPOBLEMA DEBE AGREGAR EN this->defMap
        CodeCodesMap::iterator elGrpsIt = defElGrpMap->elGrps.find(elem);
        if (elGrpsIt == defElGrpMap->elGrps.end()){
            set<string> groups;
            groups.insert(group);
            defElGrpMap->elGrps[elem] = groups;
        }
        else
            elGrpsIt->second.insert(group);
        data.getline(line, 1024);
    }
    data.close();
    XMLString::transcode("definition",defTag,19);
    XMLString::transcode("defElement",defElTag,19);
    XMLString::transcode("linkedElement",lnkElTag,19);
    XMLString::transcode("projection",projTag,19);
    XMLString::transcode("elementGroup",elGrpTag,19);
    XMLString::transcode("element",elementTag,19);
    XMLString::transcode("group",groupTag,19);
    XMLString::transcode("code",codeAttr,19);
    XMLString::transcode("elementID",elIdAttr,19);
    XMLString::transcode("groupID",grpIdAttr,19);
    XMLString::transcode("displayName",dispNameAttr,19);
    XMLString::transcode("id",idAttr,19);
    XMLString::transcode("defaultGroup",defGrpAttr,19);
    XMLString::transcode("defaultFormat",defFmtAttr,19);
    XMLString::transcode("initValueType",initValTypeAttr,19);
    XMLString::transcode("rank",rankAttr,19);

}

DOMDocument* DOMForecast::build_dom()
{
    XMLCh tmp_str[50];
    XMLCh tmp_str2[100];

    /*
     * First step is to create the DOM document with its root
     */
    XMLString::transcode("Range", tmp_str,99);
    DOMImplementation *impl = DOMImplementationRegistry::getDOMImplementation(tmp_str);
    XMLString::transcode("root", tmp_str,99);
    DOMDocument *doc = impl->createDocument(0,tmp_str,0);
    DOMElement *root = doc->getDocumentElement();
    char idStr[10];

    /*I will add definitions to the documents*/
    DOMElement *def;
    definition::iterator defIter = this->defMap.begin();
    while(defIter != this->defMap.end())
    {
        def = doc->createElement(this->defTag);
        sprintf(idStr,"%i",defIter->second.id);
        XMLString::transcode(idStr,tmp_str,49);
        def->setAttribute(this->idAttr, tmp_str);
        XMLString::transcode(defIter->first.c_str(),tmp_str,49);
        def->setAttribute(this->dispNameAttr, tmp_str);
        XMLString::transcode("initDaysPrior",tmp_str,49);
        XMLString::transcode("",tmp_str2,99);
        def->setAttribute(tmp_str, tmp_str2);
        XMLString::transcode("timeIncrement",tmp_str,49);
        XMLString::transcode("",tmp_str2,99);
        def->setAttribute(tmp_str, tmp_str2);
        CodeCodesMap::iterator  defElGrpIter = defIter->second.elGrps.begin();
        DOMElement *defEl;
        int rank = 1;
        while(defElGrpIter != defIter->second.elGrps.end())
        {
            //    <defElement elementID="1" initValueType="&INIT_TYPE_TREND;" rank="1" >
            IdCodeNameMap::iterator elIt = this->elemCodeMap.find(defElGrpIter->first);
            if (elIt != this->elemCodeMap.end())
            {
                defEl = doc->createElement(this->defElTag);
                XMLString::transcode("",tmp_str2,99);
                defEl->setAttribute(this->initValTypeAttr,tmp_str2);
                sprintf(idStr,"%i",elIt->second.id);
                XMLString::transcode(idStr,tmp_str,49);
                defEl->setAttribute(this->elIdAttr,tmp_str);
                sprintf(idStr,"%i",rank++);
                XMLString::transcode(idStr,tmp_str,49);
                defEl->setAttribute(this->rankAttr,tmp_str);
                def->appendChild(defEl);
                CodeSet::iterator grpCodeIt = defElGrpIter->second.begin();
                int grpRank = 1;
                while(grpCodeIt != defElGrpIter->second.end())
                {
                    //<elementGroup groupID="1" rank="1" />
                    IdCodeNameMap::iterator grpIt = this->grpCodeMap.find(*grpCodeIt);
                    if (grpIt == this->grpCodeMap.end())
                        cout << "Error: group " << *grpCodeIt << " not found.\n";
                    else{
                        DOMElement *elGrp = doc->createElement(this->elGrpTag);
                        sprintf(idStr,"%i",grpIt->second.id);
                        XMLString::transcode(idStr,tmp_str,49);
                        elGrp->setAttribute(this->grpIdAttr, tmp_str);
                        sprintf(idStr,"%i",grpRank++);
                        XMLString::transcode(idStr,tmp_str,49);
                        elGrp->setAttribute(this->rankAttr, tmp_str);
                        defEl->appendChild(elGrp);
                    }
                    *grpCodeIt++;
                }
            }
            *defElGrpIter++;
        }
        root->appendChild(def);
        *defIter++;
    }

    /* I add all elements defined in elements map to the document*/
    DOMElement *elem;
    IdCodeNameMap::iterator elemIter= this->elemCodeMap.begin();
    while (elemIter != this->elemCodeMap.end())
    {
        elem = doc->createElement(this->elementTag);
        // Sales element has a different format
        if (strcmp(elemIter->first.data(),"Ventas") == 0)
            XMLString::transcode("$###,###", tmp_str2,99);
        else
            XMLString::transcode("###,###", tmp_str2,99);
        elem->setAttribute(this->defFmtAttr, tmp_str2);
        elem->setAttribute(this->dispNameAttr, elemIter->second.name);
        elem->setAttribute(this->codeAttr, elemIter->second.code);
        sprintf(idStr, "%i", elemIter->second.id);
        XMLString::transcode(idStr, tmp_str2,99);
        elem->setAttribute(this->idAttr, tmp_str2);
        root->appendChild(elem);

        *elemIter++;
    }

    /* I add all groups defined in the groups maps to the documents*/
    DOMElement *grp;
    XMLString::transcode("N", tmp_str,49);
    IdCodeNameMap::iterator grpIter = this->grpCodeMap.begin();
    while (grpIter != this->grpCodeMap.end())
    {
        grp = doc->createElement(this->groupTag);
        if (strcmp(grpIter->first.data(),"Default")== 0)
        {
            XMLString::transcode("Y", tmp_str2,99);
            grp->setAttribute(this->defGrpAttr, tmp_str2);
        }
        else
            grp->setAttribute(this->defGrpAttr, tmp_str);
        grp->setAttribute(this->dispNameAttr, grpIter->second.name);
        grp->setAttribute(this->codeAttr, grpIter->second.code);
        sprintf(idStr, "%i", grpIter->second.id);
        XMLString::transcode(idStr, tmp_str2,99);
        grp->setAttribute(this->idAttr, tmp_str2);
        root->appendChild(grp);
        *grpIter++;
    }
    return doc;
}

void DOMForecast::createXMLFile(DOMDocument *doc)
{
    XMLCh tempStr[100];
    XMLString::transcode("LS", tempStr, 99);
    DOMImplementation *impl = DOMImplementationRegistry::getDOMImplementation(tempStr);
    DOMLSSerializer* theSerializer = ((DOMImplementationLS*)impl)->createLSSerializer();

    XMLFormatTarget* myFormTarget = new StdOutFormatTarget();
    DOMLSOutput* theOutput = ((DOMImplementationLS*)impl)->createLSOutput();
    theOutput->setByteStream(myFormTarget);

    try {
        // do the serialization through DOMLSSerializer::write();
        theSerializer->write(doc, theOutput);
    }
    catch (const XMLException& toCatch) {
        char* message = XMLString::transcode(toCatch.getMessage());
        cout << "Exception message is: \n"
             << message << "\n";
        XMLString::release(&message);
        return;
    }
    catch (const DOMException& toCatch) {
        char* message = XMLString::transcode(toCatch.msg);
        cout << "Exception message is: \n"
             << message << "\n";
        XMLString::release(&message);
        return;
    }
    catch (...) {
        cout << "Unexpected Exception \n" ;
        return;
    }

    theOutput->release();
    theSerializer->release();
    delete myFormTarget;

}

DOMForecast::~DOMForecast()
{
}
