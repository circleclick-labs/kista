from setuptools import setup
setup(name='kista',
      version='1.1.0',
      description='miscellaneous stuff, old norse for bag',
      url='https://github.com/circleclick-labs/kista.git',
      author='Joel Ward',
      author_email='jmward+python@gmail.com',
      license='MIT',
      packages=['kista'],
      install_requires=["web3","docopt"],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=True)
