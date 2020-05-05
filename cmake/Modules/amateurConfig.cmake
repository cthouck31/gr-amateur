INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_AMATEUR amateur)

FIND_PATH(
    AMATEUR_INCLUDE_DIRS
    NAMES amateur/api.h
    HINTS $ENV{AMATEUR_DIR}/include
        ${PC_AMATEUR_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    AMATEUR_LIBRARIES
    NAMES gnuradio-amateur
    HINTS $ENV{AMATEUR_DIR}/lib
        ${PC_AMATEUR_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(AMATEUR DEFAULT_MSG AMATEUR_LIBRARIES AMATEUR_INCLUDE_DIRS)
MARK_AS_ADVANCED(AMATEUR_LIBRARIES AMATEUR_INCLUDE_DIRS)

