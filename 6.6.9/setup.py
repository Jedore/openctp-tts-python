import glob
import os
import pathlib
import shutil
import sys
import sysconfig

import setuptools
from setuptools.command import build_py, build_ext

package_dir = "openctp-ctp"
link_args = []
compile_args = []
libs = []
sources_md = [os.path.join(package_dir, "thostmduserapi.i")]
sources_td = [os.path.join(package_dir, "thosttraderapi.i")]


def custom_compiler():
    # Custom compiler options
    from distutils.unixccompiler import UnixCCompiler

    set_executables = UnixCCompiler.set_executables

    def _set_executables(self, **kwargs):
        set_executables(self, **kwargs)
        if "-pthread" in self.compiler_so:
            self.compiler_so.remove("-pthread")
        if "-g" in self.compiler_so:
            self.compiler_so.remove("-g")
        if "-fwrapv" in self.compiler_so:
            self.compiler_so.remove("-fwrapv")
        if "-O3" in self.compiler_so:
            self.compiler_so.remove("-O3")

        if "-Wall" in self.compiler_so:
            self.compiler_so.remove("-Wall")

        if "-pthread" in self.compiler_cxx:
            self.compiler_cxx.remove("-pthread")

        if "-pthread" in self.linker_so:
            self.linker_so.remove("-pthread")

        # if "-bundle" in self.linker_so:
        #     self.linker_so[self.linker_so.index("-bundle")] = "-dynamiclib"

    UnixCCompiler.set_executables = _set_executables


if sys.platform.startswith("win32"):
    major, minor = sys.version_info[:2]
    if sys.maxsize == 0x7FFFFFFF:
        # 32bit
        base_dir = "win32"

    elif sys.maxsize == 0x7FFFFFFFFFFFFFFF:
        # 64bit
        base_dir = "win64"

    else:
        print("Unsupported windows arch!")
        exit(-1)

    libs = glob.glob(os.path.join(base_dir, "*.dll"))
    libraries = [pathlib.Path(lib).stem for lib in libs]

elif sys.platform.startswith("linux"):
    custom_compiler()
    base_dir = "linux64"
    libs = glob.glob(os.path.join(base_dir, "lib*.so"))
    libraries = [pathlib.Path(lib).stem[3:] for lib in libs]
    compile_args.append("-c")
    compile_args.append("-fPIC")
    link_args.append("-Wl,-shared,-fPIC,--enable-new-dtags,-rpath,.")

elif sys.platform.startswith("darwin"):
    custom_compiler()
    base_dir = "mac64"
    libs = glob.glob(os.path.join(base_dir, "*.a"))
    libraries = [pathlib.Path(lib).stem[3:] for lib in libs]
    compile_args.append("-std=c++11")
    # sources_md = [os.path.join(package_dir, "thostmduserapi_mac.i")]
    # sources_td = [os.path.join(package_dir, "thosttraderapi_mac.i")]

else:
    print("Unsupported platform!")
    exit(-1)

include_dirs = [
    base_dir,
    sysconfig.get_path("include"),
]
swig_include_dir = "-I" + base_dir

library_dirs = [
    base_dir,
    sysconfig.get_path("stdlib"),
]


class BuildExt(build_ext.build_ext):
    def run(self):
        # build paralleled
        self.parallel = 2
        return super().run()

    # def get_ext_filename(self, fullname):
    #     filename = super().get_ext_filename(fullname)
    #     if sys.platform.startswith("darwin"):
    #         filename = filename.replace(".so", ".dylib")
    #     return filename


class BuildPy(build_py.build_py):
    def run(self):
        self.run_command("build_ext")

        if not sys.platform.startswith('linux'):
            for lib in libs:
                shutil.copy(lib, package_dir)

        for lib in glob.glob(os.path.join("build", "lib*", "_*")):
            name = os.path.basename(lib)
            name_split = name.split(os.path.extsep)
            new_name = name_split[0] + os.path.extsep + name_split[2]
            shutil.move(lib, os.path.join(package_dir, new_name))

        return super().run()


def extension(name, sources):
    return setuptools.Extension(
        name,
        sources,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=compile_args,
        extra_link_args=link_args,
        language="c++",
        swig_opts=["-threads", "-c++", swig_include_dir],
    )


with open("README.md", mode="r", encoding="utf8") as fb:
    long_description = fb.read()

setuptools.setup(
    name="openctp-tts",
    version="6.6.9",
    ext_modules=[
        extension("_thostmduserapi", sources_md),
        extension("_thosttraderapi", sources_td),
    ],
    cmdclass={
        "build_py": BuildPy,
        "build_ext": BuildExt,
    },
    description="A package for CTPAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jedore",
    author_email="jedorefight@gmail.com",
    packages=["openctp_tts"],
    package_dir={"openctp_tts": package_dir},
    package_data={
        "openctp_tts": ["*.a", "*.so", "*.dll", "*.pyd", "*.dylib"],
    },
    url="https://github.com/openctp/openctp-ctp-python",
    keywords=["openctp", "ctp", "ctpapi", "trading", "investment"],
    license="BSD-3-Clause",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Natural Language :: Chinese (Simplified)",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)