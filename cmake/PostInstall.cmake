#message(STATUS "Compiling hierarchical blocks...")
#execute_process(COMMAND "cmake -P ${CMAKE_SOURCE_DIR}/apps/hier/CMakeLists.txt")

#message(STATUS "Compiling applications...")
#add_custom_command(SCRIPT "cmake -P ${CMAKE_SOURCE_DIR}/apps/bin/CMakeLists.txt")
