cmake_minimum_required(VERSION 3.25)
project(neon_ascendancy_native LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(NEON_BUILD_PLUGIN "Build the Windows RED4ext plugin DLL" OFF)
option(NEON_BUILD_TESTS  "Build host native unit tests" ON)

set(NEON_REPO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/..")
set(NEON_SQLITE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/third_party/sqlite")

if(NOT EXISTS "${NEON_SQLITE_DIR}/sqlite3.c" OR NOT EXISTS "${NEON_SQLITE_DIR}/sqlite3.h")
  message(FATAL_ERROR "Missing SQLite amalgamation in ${NEON_SQLITE_DIR}. Run tools/fetch-native-deps.sh first.")
endif()

# 1. Embedded SQLite3 amalgamation (R-Tree enabled, thread-safe, strict SQL).
add_library(neon_sqlite STATIC "${NEON_SQLITE_DIR}/sqlite3.c")
target_include_directories(neon_sqlite PUBLIC "${NEON_SQLITE_DIR}")
target_compile_definitions(neon_sqlite PUBLIC
  SQLITE_ENABLE_RTREE=1
  SQLITE_THREADSAFE=1
  SQLITE_DQS=0
  SQLITE_DEFAULT_FOREIGN_KEYS=1
  SQLITE_OMIT_DEPRECATED=1
  SQLITE_ENABLE_FTS5=0
)
if(MSVC)
  target_compile_options(neon_sqlite PRIVATE /W0)
else()
  target_compile_options(neon_sqlite PRIVATE -w)
  find_package(Threads REQUIRED)
  target_link_libraries(neon_sqlite PUBLIC Threads::Threads ${CMAKE_DL_LIBS})
endif()

# 2. Embedded SQL schemas generated from data/schema/*.sql (single source of truth).
find_package(Python3 REQUIRED COMPONENTS Interpreter)
set(NEON_SCHEMA_HEADER "${CMAKE_CURRENT_BINARY_DIR}/generated/embedded_schemas.hpp")
add_custom_command(
  OUTPUT "${NEON_SCHEMA_HEADER}"
  COMMAND "${Python3_EXECUTABLE}"
    "${CMAKE_CURRENT_SOURCE_DIR}/lib/schema/embed_sql.py"
    "${NEON_REPO_ROOT}/data/schema/world_v1.sql"
    "${NEON_REPO_ROOT}/data/schema/playthrough_v1.sql"
    "${NEON_SCHEMA_HEADER}"
  DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/lib/schema/embed_sql.py"
    "${NEON_REPO_ROOT}/data/schema/world_v1.sql"
    "${NEON_REPO_ROOT}/data/schema/playthrough_v1.sql"
  COMMENT "Embedding data/schema/*.sql into embedded_schemas.hpp"
)
add_custom_target(neon_schema_gen DEPENDS "${NEON_SCHEMA_HEADER}")
add_library(neon_schema INTERFACE)
add_dependencies(neon_schema neon_schema_gen)
target_include_directories(neon_schema INTERFACE "${CMAKE_CURRENT_BINARY_DIR}/generated")

# Strict warning helper for our own code.
function(neon_apply_warnings target)
  if(MSVC)
    target_compile_options(${target} PRIVATE /W4 /WX)
  else()
    target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
  endif()
endfunction()

# 3. Pure C++20 causal simulation engine & era policy (zero Windows.h, SQLite, or RedLib).
add_library(neon_sim STATIC
  lib/sim/era.cpp
  lib/sim/era.hpp
  lib/sim/garrison.cpp
  lib/sim/garrison.hpp
  lib/sim/sim.cpp
  lib/sim/sim.hpp
)
target_include_directories(neon_sim PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/lib/sim")
neon_apply_warnings(neon_sim)

# 4. SQLite store + durable revision-watermark checkpointing.
add_library(neon_store STATIC
  lib/store/store.cpp
  lib/store/store.hpp
)
target_include_directories(neon_store PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/lib/store")
target_link_libraries(neon_store PUBLIC neon_sim neon_schema neon_sqlite)
neon_apply_warnings(neon_store)

# 5. Host offline unit tests (Linux/native).
if(NEON_BUILD_TESTS AND NOT CMAKE_CROSSCOMPILING)
  enable_testing()
  add_executable(neon_tests tests/test_main.cpp)
  target_link_libraries(neon_tests PRIVATE neon_store neon_sim)
  neon_apply_warnings(neon_tests)
  add_test(
    NAME neon_core_tests
    COMMAND neon_tests "${NEON_REPO_ROOT}/dist/world.db"
  )
endif()

# 6. Windows RED4ext + RedLib native plugin DLL.
if(NEON_BUILD_PLUGIN)
  set(RED4EXT_SDK_DIR "${CMAKE_CURRENT_SOURCE_DIR}/third_party/RED4ext.SDK")
  set(REDLIB_DIR "${CMAKE_CURRENT_SOURCE_DIR}/third_party/RedLib")
  if(NOT EXISTS "${RED4EXT_SDK_DIR}/CMakeLists.txt" OR NOT EXISTS "${REDLIB_DIR}/CMakeLists.txt")
    message(FATAL_ERROR "Missing RED4ext.SDK or RedLib in native/third_party/. Run tools/fetch-native-deps.sh first.")
  endif()

  set(RED4EXT_HEADER_ONLY OFF CACHE BOOL "" FORCE)
  set(RED4EXT_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
  set(RED4EXT_INSTALL OFF CACHE BOOL "" FORCE)

  # Linux filesystems are case-sensitive while RED4ext.SDK includes a few
  # headers with Windows-style mixed casing (e.g. RED4ext/rtti/IType.hpp).
  # Feed clang-cl a build-local VFS overlay instead of modifying vendored code.
  if(CMAKE_HOST_UNIX AND CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    set(NEON_VFS_OVERLAY "${CMAKE_CURRENT_BINARY_DIR}/red4ext_vfs.yaml")
    file(WRITE "${NEON_VFS_OVERLAY}"
"version: 0
case-sensitive: false
roots:
  - name: \"${RED4EXT_SDK_DIR}/include/RED4ext/rtti\"
    type: directory
    contents:
      - name: \"ERTTIType.hpp\"
        type: file
        external-contents: \"${RED4EXT_SDK_DIR}/include/RED4ext/RTTI/ERTTIType.hpp\"
      - name: \"IType.hpp\"
        type: file
        external-contents: \"${RED4EXT_SDK_DIR}/include/RED4ext/RTTI/IType.hpp\"
      - name: \"IType-inl.hpp\"
        type: file
        external-contents: \"${RED4EXT_SDK_DIR}/include/RED4ext/RTTI/IType-inl.hpp\"
  - name: \"${RED4EXT_SDK_DIR}/include/RED4ext/Scripting/Natives\"
    type: directory
    contents:
      - name: \"AnimKeyFrames.hpp\"
        type: file
        external-contents: \"${RED4EXT_SDK_DIR}/include/RED4ext/Scripting/Natives/animKeyFrames.hpp\"
")
    set(NEON_VFS_FLAG "-clang:-ivfsoverlay${NEON_VFS_OVERLAY}")
  endif()

  add_subdirectory("${RED4EXT_SDK_DIR}" third_party_red4ext EXCLUDE_FROM_ALL)
  add_subdirectory("${REDLIB_DIR}" third_party_redlib EXCLUDE_FROM_ALL)

  if(DEFINED NEON_VFS_FLAG)
    target_compile_options(RED4ext.SDK PUBLIC "${NEON_VFS_FLAG}")
  endif()

  add_library(NeonAscendancy SHARED plugin/Main.cpp)
  set_target_properties(NeonAscendancy PROPERTIES
    PREFIX ""
    SUFFIX ".dll"
  )
  target_link_libraries(NeonAscendancy PRIVATE
    neon_store
    neon_sim
    RED4ext::SDK
    RedLib
  )
  # Suppress third-party header warnings while keeping strict /W4 /WX on our code.
  target_include_directories(NeonAscendancy SYSTEM PRIVATE
    "${RED4EXT_SDK_DIR}/include"
    "${RED4EXT_SDK_DIR}/vendor/D3D12MemAlloc"
    "${REDLIB_DIR}/include"
    "${REDLIB_DIR}/vendor"
  )
  neon_apply_warnings(NeonAscendancy)
endif()
