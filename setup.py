from pathlib import Path
from setuptools import setup
from kista import __name__, version
long_description=(Path(__file__).parent / "README.md").read_text()
entry_points=dict(console_scripts=[f'{__name__}={__name__}.cli:main'])
import os.path
setup(name=__name__,
      version=version,
      description='miscellaneous stuff, old norse for bag',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/circleclick-labs/'+__name__,
      author='Joel Ward',
      author_email='jmward+python@gmail.com',
      license='MIT',
      packages=[__name__],
      entry_points=entry_points,
      scripts=(lambda d='scripts':
               [d+'/'+x for x in os.listdir(d)])(),
      install_requires=['web3', 'docopt'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=True)
