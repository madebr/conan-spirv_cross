# -*- coding: utf-8 -*-

from conans import CMake, ConanFile, tools
import os


class TestPackageConan(ConanFile):

    exports_sources = ["multiply.comp", "multiply.comp.spv", ]
    settings = "os", "arch", "compiler", "build_type",

    def test(self):
        spv_in = os.path.join(self.source_folder, "multiply.comp.spv")
        cpp_out = os.path.join(self.build_folder, "multiply.comp.cpp")
        try:
            os.unlink(cpp_out)
        except FileNotFoundError:
            pass
        if not tools.cross_building(self.settings):
            self.run('spirv-cross --help')
            self.run('spirv-cross --cpp --output "{}" "{}"'.format(cpp_out, spv_in))
            assert os.path.exists(cpp_out)
