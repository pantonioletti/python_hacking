#include <boost/python/module.hpp>
#include <boost/python/def.hpp>

#include <cstdio>
#include <fstream>

using std;

void filter(char* file_name, char* white_lis[])
{
	ifstream in_file;
	in_file.open(file_name);
	
	char[1024] line;
	in_file.getline(line, 1024);
	
	while(in_file){
		
	}
}

BOOST_PYTHON_MODULE(pmas_ext)
{
    using namespace boost::python;
    def("filter", filter);
}