#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile, tools, CMake
import os

class LibCrossGuidConan(ConanFile):

    name = "crossguid"
    version = "0.2.2"
    url = "http://github.com/fbergmann/conan-crossguid"
    homepage = "https://github.com/copasi/copasi-dependencies/tree/master/src/crossguid"
    author = "Frank Bergmann"
    license = "MIT"

    description = ("CrossGuid is a minimal, cross platform, C++ GUID library. It uses the best native GUID/UUID generator on the given platform and has a generic class for parsing, stringifying, and comparing IDs. ")

    settings = "os", "arch", "compiler", "build_type"

    options = {
        "fPIC": [True, False]
    }

    default_options = (
        "fPIC=True"
    )

    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

        if self.settings.os == "Linux":
            del self.options.fPIC
            self.requires("libuuid/1.0.3@bincrafters/stable")
            self.options['libuuid'].shared = False


    def source(self):
        tools.get('https://github.com/copasi/copasi-dependencies/releases/download/v4.26.213/crossguid-0.2.2-Source.zip')
        os.rename("crossguid-0.2.2-Source", "src") 
        tools.replace_in_file('src/CMakeLists.txt', "project(CrossGuid)", '''project(CrossGuid)

include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure(self, cmake):
        args = ['-DCROSSGUID_TESTS=OFF']
        if self.settings.compiler == 'Visual Studio' and 'MT' in self.settings.compiler.runtime:
            args.append('-DWITH_STATIC_RUNTIME=ON')

        cmake.configure(build_folder="build", args=args, source_folder="src")

    def build(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.install()
        self.copy("*.lib", dst="lib", keep_path=False)
        if self.settings.os == "Windows":
            self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):

        libfile = "crossguid"

        if not self.settings.os == "Windows":
            libfile += "lib" + libfile + ".a"
        else:
            libfile += ".lib"

        self.cpp_info.libs = [libfile]
