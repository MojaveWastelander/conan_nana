from conans import ConanFile, CMake
from conans.tools import unzip, replace_in_file

class NanaConan(ConanFile):
    name = "nana"
    generators = "cmake"
    version = "1.3.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"enable_audio" : [True, False], "enable_png" : [True, False], "enable_jpeg" : [True, False]}
    default_options = "enable_audio=False", "enable_png=False", "enable_jpeg=False"
    license = "Boost"
    url = "https://github.com/MojaveWastelander/conan_nana"
    
    def source(self):
        self.run("git clone https://github.com/cnjinhao/nana.git")
    
    def requirements(self):
        if self.options.enable_jpeg:
            self.requires("libjpeg-turbo/1.4.2@lasote/stable")
        
        if self.options.enable_png:
            self.requires("libpng/1.6.23@lasote/stable")

    def build(self):
        cmake = CMake(self.settings)
        print("Compiler: %s %s" % (self.settings.compiler, self.settings.compiler.version))
        print("Arch: %s" % self.settings.arch)        
        cmake_command_line = cmake.command_line #.replace('-G "MinGW Makefiles"', '-G "Unix Makefiles"')
        lib_opt = "-DCMAKE_DEBUG_POSTFIX:STRING={0} -DCMAKE_RELEASE_POSTFIX:STRING={0}".format("r" if self.settings.build_type == "Release" else "d")

        if self.options.enable_jpeg or self.options.enable_png:
            replace_lines = '''cmake_minimum_required(VERSION 2.8)
    include(../conanbuildinfo.cmake)
    CONAN_BASIC_SETUP()
    '''
            replace_in_file("nana/CMakeLists.txt", "cmake_minimum_required(VERSION 2.8)", replace_lines)
        

        # process options
        if self.options.enable_audio:
            lib_opt += " -DENABLE_AUDIO:BOOL=ON"
        
        if self.options.enable_png:
            lib_opt += " -DENABLE_PNG:BOOL=ON"
        
        if self.options.enable_jpeg:
            lib_opt += " -DENABLE_JPEG:BOOL=ON"
        
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":

                if self.settings.arch == "x86_64":
                    self.run('cmake %s/nana %s -G "Visual Studio %s Win64" %s' % (self.conanfile_directory, cmake.command_line, self.settings.compiler.version, lib_opt))
                else:
                    self.run('cmake %s/nana %s -G "Visual Studio %s" %s' % (self.conanfile_directory, cmake.command_line, self.settings.compiler.version, lib_opt))
            else:
                self.run('cmake %s/nana %s %s' % (self.conanfile_directory, cmake_command_line, lib_opt))
        else:                
                self.run('cmake %s/nana %s %s' % (self.conanfile_directory, cmake_command_line, lib_opt))
        self.run("cmake --build . %s" % cmake.build_config)


    def package(self):
        self.copy("*.*", dst="include", src="nana/include")
        self.copy("*.*", dst="source", src="nana/source")
        self.copy("*.lib", dst="lib", src="Release")
        self.copy("*.lib", dst="lib", src="Debug")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.a", dst="lib", src=".")

    def package_info(self):
        print("Compiler: %s %s" % (self.settings.compiler, self.settings.compiler.version))
        print("Arch: %s" % self.settings.arch)      
        print("Build_type: %s" % self.settings.build_type)     
        if self.settings.compiler == "Visual Studio":
            print("Runtime: %s" % self.settings.compiler.runtime)
        self.cpp_info.libs = ["nana%s" % ("r" if self.settings.build_type == "Release" else "d")]
