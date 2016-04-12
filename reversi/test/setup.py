from distutils.core import setup, Extension

setup(name='helloworld', version='1.0', description='Just a test', ext_modules=[Extension('helloworld', ['hello.c'])])
