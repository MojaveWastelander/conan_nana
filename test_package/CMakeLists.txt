project(nana_test)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_definitions(-DNANA_IGNORE_CONF)

if (CONAN_LIBPNG_ROOT)
   add_definitions(-DNANA_ENABLE_PNG)
endif(CONAN_LIBPNG_ROOT)

if (CONAN_LIBJPEG-TURBO_ROOT)
   add_definitions(-DNANA_ENABLE_JPEG)
endif(CONAN_LIBJPEG-TURBO_ROOT)

add_executable(nana_test nana_test.cpp)
target_link_libraries(nana_test ${CONAN_LIBS})

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" OR "${CMAKE_CXX_COMPILER_ID}" STREQUAL "CLANG")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
  target_link_libraries(nana_test X11 Xft pthread)					
endif()