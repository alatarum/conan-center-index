from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, apply_conandata_patches, export_conandata_patches
import os

class FrugenConan(ConanFile):
    name = "frugen"
    description = "IPMI FRU Information generator / editor tool and library"
    license = ("Apache-2.0", "GPL-2.0-or-later")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://codeberg.org/IPMITool/frugen"
    topics = ("hardware", "ipmi", "fru")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_json": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_json": False
    }
    implements = ["auto_shared_fpic"]

    exports_sources = "CMakeLists.txt", "*.c", "*.h"

    def export_sources(self):
        export_conandata_patches(self)

    def configure(self):
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        if self.options.with_json:
            self.requires("json-c/0.18")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIB"] = self.options.shared
        tc.variables["ENABLE_JSON"] = self.options.with_json
        tc.variables["BINARY_STATIC"] = not self.options.shared
        tc.variables["BINARY_32BIT"] = False
        tc.variables["JSON_STATIC"] = False
        tc.variables["DEBUG_OUTPUT"] = False
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        if self.options.shared:
            self.cpp_info.components["fru-shared"].libs = ["fru"]
        else:
            self.cpp_info.components["fru-static"].libs = ["fru"]
