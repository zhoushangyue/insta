cmake_minimum_required(VERSION 3.7)
project(promdns_service)

set(CMAKE_C_STANDARD 99)

set(SOURCE_FILES main.c cmake-build-debug/mDNS.h cmake-build-debug/mDNS.c cmake-build-debug/mDNS_socket.h cmake-build-debug/mDNS_socket.c)
add_executable(promdns_service ${SOURCE_FILES})