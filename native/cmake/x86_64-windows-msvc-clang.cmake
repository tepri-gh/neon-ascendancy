# Cross-compile Cyberpunk 2077 native RED4ext plugins from Linux targeting the
# MSVC x64 C++ ABI (clang-cl + lld-link + xwin).
# Requires an xwin splat; pass -DXWIN_ROOT=... or set $XWIN_ROOT.

set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

set(CMAKE_C_COMPILER   clang-cl)
set(CMAKE_CXX_COMPILER clang-cl)
set(CMAKE_LINKER       lld-link)
set(CMAKE_AR           llvm-lib)
set(CMAKE_RC_COMPILER  llvm-rc)
set(CMAKE_MT           llvm-mt)

set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

if(NOT XWIN_ROOT)
  if(DEFINED ENV{XWIN_ROOT})
    set(XWIN_ROOT "$ENV{XWIN_ROOT}")
  else()
    set(XWIN_ROOT "$ENV{HOME}/.cache/neon-ascendancy/xwin")
  endif()
endif()

foreach(_dir
    "${XWIN_ROOT}/crt/include"
    "${XWIN_ROOT}/sdk/include/ucrt"
    "${XWIN_ROOT}/sdk/include/um"
    "${XWIN_ROOT}/sdk/include/shared"
    "${XWIN_ROOT}/sdk/include/winrt")
  if(NOT EXISTS "${_dir}")
    message(FATAL_ERROR "xwin splat incomplete, missing: ${_dir} (run tools/fetch-native-deps.sh --xwin)")
  endif()
endforeach()

set(_incs
  "/imsvc${XWIN_ROOT}/crt/include /imsvc${XWIN_ROOT}/sdk/include/ucrt /imsvc${XWIN_ROOT}/sdk/include/um /imsvc${XWIN_ROOT}/sdk/include/shared /imsvc${XWIN_ROOT}/sdk/include/winrt")

set(CMAKE_C_FLAGS_INIT
  "--target=x86_64-pc-windows-msvc ${_incs} /DWIN32 /D_WINDOWS /D_CRT_SECURE_NO_WARNINGS /DUNICODE /D_UNICODE /utf-8")
set(CMAKE_CXX_FLAGS_INIT
  "--target=x86_64-pc-windows-msvc ${_incs} /DWIN32 /D_WINDOWS /D_CRT_SECURE_NO_WARNINGS /DUNICODE /D_UNICODE /utf-8 /std:c++20 /EHsc /permissive- /Zc:__cplusplus /GR- /D_HAS_EXCEPTIONS=1 /DNOMINMAX /DWIN32_LEAN_AND_MEAN")

set(CMAKE_SHARED_LINKER_FLAGS_INIT
  "/INCREMENTAL:NO /DEBUG:FULL /Brepro /LIBPATH:${XWIN_ROOT}/crt/lib/x86_64 /LIBPATH:${XWIN_ROOT}/sdk/lib/um/x86_64 /LIBPATH:${XWIN_ROOT}/sdk/lib/ucrt/x86_64")

# Static CRT (/MT): Proton 11's builtin msvcp140.dll exports zero __std_*
# symbols required by RedLib's std::format helpers.
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded")

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
