from conans import ConanFile, CMake, tools
import os


class SobjectizerConan(ConanFile):
    name = "restinio"
    version = "0.4.8.3"

    license = "BSD-3-Clause"
    url = "https://github.com/Stiffstream/restinio-conan"

    description = (
            "RESTinio is a header-only C++14 library that gives you "
            "an embedded HTTP/Websocket server."
    )

    settings = "os", "compiler", "build_type", "arch"

    requires = "http-parser/2.8.1@bincrafters/stable", "asio/1.12.0@bincrafters/stable", "fmt/5.2.1@bincrafters/stable"

    generators = "cmake"

    source_subfolder = "restinio"

    def source(self):
        source_url = "https://bitbucket.org/sobjectizerteam/restinio-0.4/downloads"
        tools.get("{0}/restinio-{1}.zip".format(source_url, self.version))
        extracted_dir = "restinio-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions['RESTINIO_INSTALL'] = True
        cmake.definitions['RESTINIO_TEST'] = False
        cmake.definitions['RESTINIO_SAMPLE'] = False
        cmake.definitions['RESTINIO_INSTALL_SAMPLES'] = False
        cmake.definitions['RESTINIO_BENCH'] = False
        cmake.definitions['RESTINIO_INSTALL_BENCHES'] = False
        cmake.definitions['RESTINIO_FIND_DEPS'] = False
        cmake.configure(source_folder = self.source_subfolder + "/dev")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.hpp", dst="include/restinio", src=self.source_subfolder + "/dev/restinio")
        self.copy("license*", src=self.source_subfolder, dst="licenses",  ignore_case=True, keep_path=False)
