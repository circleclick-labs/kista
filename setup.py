import os, kista, setuptools
setuptools.setup(name='kista',
                 version=kista.version,
                 description='miscellaneous stuff, old norse for bag',
                 long_description=open(f"{__file__[:-8]}README.md").read(),
                 long_description_content_type='text/markdown',
                 url='https://github.com/circleclick-labs/kista',
                 author='Joel Ward',
                 author_email='jmward+python@gmail.com',
                 license='MIT',
                 packages=['kista'],
                 entry_points=dict(console_scripts=[f'kista=kista.cli:main']),
                 scripts=(lambda d:[d+x for x in os.listdir(d)])('scripts/'),
                 install_requires=[x.strip() for x in
                                   open("requirements.txt").readlines()],
                 zip_safe=True,
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ])
