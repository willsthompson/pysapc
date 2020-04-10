from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
from sys import platform
import warnings

compile_args = {
    "macos" : ['-Xpreprocessor', '-fopenmp'],
    "default" : ['-fopenmp']
}

link_args = {
    "macos" : ['-Xpreprocessor', '-fopenmp', '-L/usr/local/opt/libomp/lib'],
    "default" : ['-fopenmp']
}

include_dirs = {
    "macos" : [numpy.get_include(), '/usr/local/opt/libomp/include'],
    "default": [numpy.get_include()]
}

ext = Extension("pysapc.sparseAP_cy", ['pysapc/sparseAP_cy.pyx'])

class build_ext_subclass( build_ext ):
    def build_extensions(self):
        # Apply platform-specific build options

        if platform[:3] == "dar": # NB "Darwin"
            args_key = "macos"
            msg  = "\n\n\nMacOS detected, adding Apple Clang-specific build options.\n"
            msg += "Note: OpenMP must be installed separately, i.e.: brew install libomp\n\n\n"
            warnings.warn(msg)
        else:
            args_key = "default"

        for e in self.extensions:
            if e is ext:
                e.extra_link_args = link_args[args_key]
                e.extra_compile_args = compile_args[args_key]
                e.include_dirs = include_dirs[args_key]

        build_ext.build_extensions(self)

setup(
    name="pysapc",
    version="1.0.0",
    description="Sparse Affinity Propagation Clustering",
    author="Huojun Cao",
    author_email="bioinfocao@gmail.com",
    url="https://github.com/bioinfocao/pysapc",
    license="BSD 3 clause",
    packages=["pysapc","pysapc.tests"],
    #packages = find_packages(), 
    package_data = {
            # If any package contains *.txt or *.rst files, include them:
            '': ['*.txt', '*.rst'],
        },
    include_package_data=True,
    install_requires=["numpy","scipy","pandas","cython"],
    cmdclass = {"build_ext": build_ext_subclass},
    ext_modules = [ext],
)
