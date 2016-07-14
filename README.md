[![Build Status](https://ci.appveyor.com/api/projects/status/github/MojaveWastelander/conan_nana)](https://ci.appveyor.com/project/MojaveWastelander/conan-nana)
[![Build Status](https://travis-ci.org/MojaveWastelander/conan_nana.svg)](https://travis-ci.org/MojaveWastelander/conan_nana)
# conan_nana

[Conan.io](https://conan.io) package for [Nana](https://github.com/cnjinhao/nana) library

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Upload packages to server

    $ conan upload nana/1.3.0@mojavewastelander/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install nana/1.3.0@mojavewastelander/stable

### Package basic test
    $ conan test_package -o nana:enable_png=True -o nana:enable_jpeg=True -o nana:enable_audio=True    
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    nana/1.3.0@mojavewastelander/stable

    [options]
    nana:enable_png=True
    
    [generators]
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
