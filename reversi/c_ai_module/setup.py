from distutils.core import setup, Extension

setup(name='c_ai_module', version='1.0', description='C Reversi AI Module',
      ext_modules=[Extension('c_ai_module', ['ai_core.c', 'c_ai_module.c'])],
      )
