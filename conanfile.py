from nxtools import NxConanFile
from conans import AutoToolsBuildEnvironment,tools
from os import chdir


class SphhinxSearchConan(NxConanFile):
    name = "sphinxsearch"
    version = "2.2.11"
    license = "GPLv2"
    url = "https://github.com/hoxnox/conan-sphinxsearch"
    license = "http://sphinxsearch.com/docs/current.html#license"
    settings = "os", "compiler", "build_type", "arch"
    build_policy = "missing"
    description = "Full-text search engine client"
    options = {"shared":[True, False]}
    default_options = "shared=False"

    def do_source(self):
        self.retrieve("6662039f093314f896950519fa781bc87610f926f64b3d349229002f06ac41a9",
                [
                    "vendor://sphinxsearch/sphinx/sphinx-{v}.tar.gz".format(v=self.version),
                    "http://sphinxsearch.com/files/sphinx-{v}-release.tar.gz".format(v=self.version)
                ],
                "sphinx-{v}.tar.gz".format(v=self.version))

    def do_build(self):
        tools.untargz("sphinx-{v}.tar.gz".format(v=self.version), "{staging_dir}/src".format(staging_dir=self.staging_dir))
        shared_definition = "--enable-static --disable-shared"
        if self.options.shared:
            shared_definition = "--enable-shared --disable-static"
        chdir("{staging_dir}/src/sphinx-{v}-release/api/libsphinxclient".format(staging_dir=self.staging_dir, v=self.version))
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("./configure prefix=\"{staging_dir}\" {shared}".format(
                staging_dir=self.staging_dir, shared=shared_definition))
            self.run("make install")

    def do_package_info(self):
        self.cpp_info.libs = ["sphinxclient"]
