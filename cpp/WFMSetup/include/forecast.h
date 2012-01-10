/* 
 * File:   forecast.h
 * Author: pantonio
 *
 * Created on May 16, 2011, 11:07 AM
 */

#include <cstdlib>
#include <iostream>
#include <fstream>
#include <set>
#include <map>
#include <string>
//#include <xercesc/util/PlatformUtils.hpp>

#include <util.hpp>

#ifndef FORECAST_H
#define	FORECAST_H
using namespace std;

struct node{
    string code;
    string name;
};

struct forecast_group{
    node group;
    map<string, node> sub_groups;
};

struct forecast_element{
    node element;
    map<string, forecast_group> groups;
};
struct forecast_def{
    string code;
    int increment;
    map<string,forecast_element> elements;
};

struct forecast_conf{
        set<string> def_set;
        map<string, node> elem_map;
        map<string, node> group_map;
        map<string, forecast_def> defs;
};

forecast_conf* read_data(char* file_name) 
{
    ifstream data;
    forecast_conf* fc=new forecast_conf;
    node* my_node;

    //cout << "Starting reading data" << endl;
    try{
        data.open(file_name);

        char line[1024];
        data.getline(line, 1024);
        while(!(data.fail() || data.eof()))
        {
            /*
             * Line format
             * 0: Definition 15MIN
             * 1: Element NATE
             * 2: Element Display name
             * 3: Group
             * 4: Group display name
             * 5: Sub-Group
             * 6: Sub-Group display name
             * @param file_name
             */
            
            //string* tokens = get_tokens(line, ';');
            cout << "Current line: " << line << endl;
            vector<string> v;
            get_tokens(line, ";", &v);
            //cout << "Got tokens" << endl;

            if (v.size() < 5)
                cout << "Current line has not enough data variables: " << endl << line << endl;
            else{
                if (fc->defs.find(v[0]) == fc->defs.end())
                {
                    forecast_def* fd = new forecast_def;
                    fd->code = v[0];
                    fd->increment=15;
                    fc->defs[fd->code] = *fd;
                    fc->def_set.insert(fd->code);
                }
                
                if(fc->defs[v[0]].elements.find(v[1]) == fc->defs[v[0]].elements.end())
                {
                    if (fc->elem_map.find(v[1]) == fc->elem_map.end())
                    {
                        my_node = new node;
                        my_node->code = v[1];
                        my_node->name = v[2];
                        fc->elem_map[v[1]] = *my_node;
                    }
                    else
                        my_node = &(fc->elem_map[v[1]]);
                        
                    fc->elem_map[my_node->code] = *my_node;
                    forecast_element* fe = new forecast_element;
                    fe->element = *my_node;
                    fc->defs[v[0]].elements[v[1]] = *fe;
                }
                
                if(fc->defs[v[0]].elements[v[1]].groups.find(v[3]) == fc->defs[v[0]].elements[v[1]].groups.end())
                {
                    if (fc->group_map.find(v[3]) == fc->group_map.end())
                    {
                        my_node = new node;
                        my_node->code = v[3];
                        my_node->name = v[4];
                        fc->group_map[v[3]] = *my_node;
                    }
                    else
                        my_node = &(fc->group_map[v[3]]);
                    
                    fc->group_map[my_node->code] = *my_node;
                    forecast_group* fg = new forecast_group;
                    fg->group = *my_node;
                    fc->defs[v[0]].elements[v[1]].groups[v[3]] = *fg; 
                }
                
                if (v.size() > 5)
                {
                    if(fc->defs[v[0]].elements[v[1]].groups[v[3]].sub_groups.find(v[5]) == fc->defs[v[0]].elements[v[1]].groups[v[3]].sub_groups.end())
                    {
                        if (fc->group_map.find(v[3]) == fc->group_map.end())
                        {
                            my_node = new node;
                            my_node->code = v[5];
                            my_node->name = v[6];
                            fc->group_map[v[5]] = *my_node;
                        }
                        else
                            my_node = &(fc->group_map[v[5]]);
                        fc->group_map[my_node->code] = *my_node;
                        fc->defs[v[0]].elements[v[1]].groups[v[3]].sub_groups[my_node->code] = *my_node;
                    }
                }
            }
           
            data.getline(line, 1024);

        }
        cout << "Def size: " << fc->def_set.size() << endl;
        data.close();
    }
    catch(ifstream::failure e)
    {
        cout << "Exception while opening/reading file:"<< endl << "\t" << file_name;
        delete fc;
        fc = NULL;
    }
    return fc;
}

void proc_forecast(char * file_name){
    forecast_conf* fc = read_data(file_name);
}


//using namespace xercesc;


#endif	/* FORECAST_H */

