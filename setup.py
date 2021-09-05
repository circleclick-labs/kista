from setuptools import setup
from kista import __doc__, __name__, version
def requirements(fn='requirements.txt'):
    return [x.strip() for x in open(fn).readlines() if x!='\n']
setup(name=__name__,
      version=version,
      description='miscellaneous stuff, old norse for bag',
      long_description=__doc__,
      url='https://github.com/circleclick-labs/'+__name__,
      author='Joel Ward',
      author_email='jmward+python@gmail.com',
      license='MIT',
      packages=[__name__],
      entry_points = dict(console_scripts=[f'{__name__}={__name__}.__main__']),
      install_requires=requirements(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=True)
