# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src

# Include any dependencies generated for this target.
include CMakeFiles/testsolis.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/testsolis.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/testsolis.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/testsolis.dir/flags.make

CMakeFiles/testsolis.dir/testsolis.cc.o: CMakeFiles/testsolis.dir/flags.make
CMakeFiles/testsolis.dir/testsolis.cc.o: testsolis.cc
CMakeFiles/testsolis.dir/testsolis.cc.o: CMakeFiles/testsolis.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sergio/GitProjects/PracticaFinalMetaheuristicas/src/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/testsolis.dir/testsolis.cc.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/testsolis.dir/testsolis.cc.o -MF CMakeFiles/testsolis.dir/testsolis.cc.o.d -o CMakeFiles/testsolis.dir/testsolis.cc.o -c /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src/testsolis.cc

CMakeFiles/testsolis.dir/testsolis.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/testsolis.dir/testsolis.cc.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src/testsolis.cc > CMakeFiles/testsolis.dir/testsolis.cc.i

CMakeFiles/testsolis.dir/testsolis.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/testsolis.dir/testsolis.cc.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src/testsolis.cc -o CMakeFiles/testsolis.dir/testsolis.cc.s

# Object files for target testsolis
testsolis_OBJECTS = \
"CMakeFiles/testsolis.dir/testsolis.cc.o"

# External object files for target testsolis
testsolis_EXTERNAL_OBJECTS =

testsolis: CMakeFiles/testsolis.dir/testsolis.cc.o
testsolis: CMakeFiles/testsolis.dir/build.make
testsolis: libcec17_test_func.so
testsolis: CMakeFiles/testsolis.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sergio/GitProjects/PracticaFinalMetaheuristicas/src/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable testsolis"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/testsolis.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/testsolis.dir/build: testsolis
.PHONY : CMakeFiles/testsolis.dir/build

CMakeFiles/testsolis.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/testsolis.dir/cmake_clean.cmake
.PHONY : CMakeFiles/testsolis.dir/clean

CMakeFiles/testsolis.dir/depend:
	cd /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src /home/sergio/GitProjects/PracticaFinalMetaheuristicas/src/CMakeFiles/testsolis.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/testsolis.dir/depend

