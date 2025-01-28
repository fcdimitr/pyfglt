project(
  'flgt',
  'c', 'cpp',
  # https://stackoverflow.com/questions/59201214/can-the-meson-project-version-be-assigned-dynamically
  version: '2.0', # FIXME: git hash (see URL above).
  license: 'GPLv3',
  meson_version: '>= 1.1.0',
  default_options: ['cpp_std=c++20'],
)

py3_mod = import('python')
# py3 = py3_mod.find_installation('/opt/homebrew/anaconda3/envs/zettelkasten/bin/python', required: true)
py3 = py3_mod.find_installation(required: true)

py3_dep = py3.dependency()
pybind11_inc = run_command(py3, '-c',
  # prefix must be stripped to allow venv inside of this repo, which is useful for debug
  'from pybind11 import get_include; from pathlib import Path;  print(get_include().removeprefix(Path().absolute().as_posix() + "/"))',
  check: true).stdout().strip()
pybind11_dep = declare_dependency(
  include_directories : pybind11_inc)

# mesonPythonPybind11Example_inc = include_directories('include/')
# sources of c++ library which is build separately
fglt_sp = subproject('fglt')
fglt_dep = fglt_sp.get_variable('fgltlib_dep')
# sources of python extension wich is build as a shared library and is linked with previous library from external/
subdir('pyfglt')