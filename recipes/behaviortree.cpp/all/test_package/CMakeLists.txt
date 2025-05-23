cmake_minimum_required(VERSION 3.15)
project(test_package LANGUAGES CXX)

add_executable(${PROJECT_NAME} test_package.cpp)

find_package(BehaviorTreeV3 CONFIG)
if(TARGET BT::behaviortree_cpp_v3)
    target_link_libraries(${PROJECT_NAME} PRIVATE BT::behaviortree_cpp_v3)
    target_compile_definitions(${PROJECT_NAME} PRIVATE -DBEHAVIORTREE_CPP_VERSION=3)
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14)
else()
    find_package(BehaviorTree REQUIRED CONFIG)
    target_link_libraries(${PROJECT_NAME} PRIVATE BT::behaviortree_cpp)
    target_compile_definitions(${PROJECT_NAME} PRIVATE -DBEHAVIORTREE_CPP_VERSION=4)
    target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_17)
endif()
