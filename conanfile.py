from conans import ConanFile, CMake

class NanaConan(ConanFile):
    name = "nana"
    generators = "cmake"
    version = "1.3.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"enable_audio" : [True, False], "enable_png" : [True, False], "enable_jpeg" : [True, False]}
    default_options = "enable_audio=False", "enable_png=False", "enable_jpeg=False"
    license = "Boost"
    url = ""
    
    def source(self):
        self.run("git clone https://github.com/cnjinhao/nana.git")

    def build(self):
        cmake = CMake(self.settings)
        print("Compiler: %s %s" % (self.settings.compiler, self.settings.compiler.version))
        print("Arch: %s" % self.settings.arch)        
        cmake_command_line = cmake.command_line #.replace('-G "MinGW Makefiles"', '-G "Unix Makefiles"')
        lib_opt = "-DCMAKE_DEBUG_POSTFIX:STRING={0} -DCMAKE_RELEASE_POSTFIX:STRING={0}".format("r" if self.settings.build_type == "Release" else "d")
        
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
        self.copy("*.a", dst="lib", src=".")

    def package_info(self):
        print("Compiler: %s %s" % (self.settings.compiler, self.settings.compiler.version))
        print("Arch: %s" % self.settings.arch)      
        print("Build_type: %s" % self.settings.build_type)      
        print("Runtime: %s" % self.settings.compiler.runtime)
        self.cpp_info.libs = ["nana%s" % ("r" if self.settings.build_type == "Release" else "d")]
