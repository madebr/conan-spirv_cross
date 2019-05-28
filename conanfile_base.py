# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os
import re
import shutil


class ConanfileBase(ConanFile):
    _base_name = "spirv_cross"
    name = "spirv_cross"
    version = "2019-05-20"
    description = "SPIRV-Cross is a practical tool and library for performing reflection on SPIR-V and disassembling SPIR-V back to high level languages."
    topics = ("conan", "spirv", "assembly", "tool", )
    url = "https://github.com/bincrafters/conan-spirv_cross"
    homepage = "https://github.com/KhronosGroup/SPIRV-Cross"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md", ]
    exports_sources = ["CMakeLists.txt", ]
    no_copy_source = True
    generators = "cmake",

    _source_subfolder = "source_subfolder"

    def source(self):
        source_url = "https://github.com/KhronosGroup/SPIRV-Cross/archive/{}.tar.gz".format(self.version)
        sha256 = "bc01afeacd77ff786a10755117a7aeb219c8d50e3db3931e59bf8f50f4cad55d"
        tools.get(source_url, sha256=sha256)
        os.rename("SPIRV-Cross-{}".format(self.version), self._source_subfolder)

        cmakelists_path = os.path.join(self._source_subfolder, "CMakeLists.txt")
        tools.replace_in_file(cmakelists_path,
                              'message(FATAL_ERROR "Must build static libraries if building CLI.")',
                              '')
        tools.replace_in_file(cmakelists_path,
                              "if (SPIRV_CROSS_STATIC)",
                              "if (TRUE)")

        cmake_src = open(cmakelists_path, "r").read()
        newtxt, _ = re.subn(r"(spirv_cross_add_library\([a-zA-Z _\-]+)STATIC",
                            r"\1",
                            cmake_src)
        open(cmakelists_path, "w").write(newtxt)

    @property
    def _build_shared(self):
        return "shared" in self.options and self.options.shared,

    def build(self):
        cmake = CMake(self)
        cmake_defines = {
            "SPIRV_CROSS_SHARED": self._build_shared,
            "SPIRV_CROSS_STATIC": not self._build_shared,
        }
        cmake.configure(defs=cmake_defines)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install(build_dir=self.build_folder)

        self.copy("*.h", src=os.path.join(self._source_subfolder, "include"), dst=os.path.join("include"))
        self.copy("*.hpp", src=os.path.join(self._source_subfolder, "include"), dst=os.path.join("include"))
        self.copy(pattern="LICENSE", src=self._source_subfolder, dst="licenses")

        if self._build_shared:
            shutil.rmtree(os.path.join(self.package_folder, "share", "pkgconfig"))
