#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Environment
MKDIR=mkdir
CP=cp
GREP=grep
NM=nm
CCADMIN=CCadmin
RANLIB=ranlib
CC=gcc.exe
CCC=g++.exe
CXX=g++.exe
FC=
AS=as.exe

# Macros
CND_PLATFORM=Cygwin_4.x-Windows
CND_CONF=Debug
CND_DISTDIR=dist

# Include project Makefile
include Makefile

# Object Directory
OBJECTDIR=build/${CND_CONF}/${CND_PLATFORM}

# Object Files
OBJECTFILES= \
	${OBJECTDIR}/line_filter.o


# C Compiler Flags
CFLAGS=

# CC Compiler Flags
CCFLAGS=
CXXFLAGS=

# Fortran Compiler Flags
FFLAGS=

# Assembler Flags
ASFLAGS=

# Link Libraries and Options
LDLIBSOPTIONS=

# Build Targets
.build-conf: ${BUILD_SUBPROJECTS}
	"${MAKE}"  -f nbproject/Makefile-Debug.mk dist/Debug/Cygwin_4.x-Windows/libPythonExt.dll

dist/Debug/Cygwin_4.x-Windows/libPythonExt.dll: ${OBJECTFILES}
	${MKDIR} -p dist/Debug/Cygwin_4.x-Windows
	${LINK.cc} -shared -o ${CND_DISTDIR}/${CND_CONF}/${CND_PLATFORM}/libPythonExt.dll ${OBJECTFILES} ${LDLIBSOPTIONS} 

${OBJECTDIR}/line_filter.o: line_filter.cpp 
	${MKDIR} -p ${OBJECTDIR}
	${RM} $@.d
	$(COMPILE.cc) -g -I/cygdrive/C/dev/tools/cygwin/usr/local/include  -MMD -MP -MF $@.d -o ${OBJECTDIR}/line_filter.o line_filter.cpp

# Subprojects
.build-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r build/Debug
	${RM} dist/Debug/Cygwin_4.x-Windows/libPythonExt.dll

# Subprojects
.clean-subprojects:

# Enable dependency checking
.dep.inc: .depcheck-impl

include .dep.inc
