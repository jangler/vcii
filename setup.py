from distutils.core import setup

setup(
    name='vcii',
    version='0.0.0',
    author='Brandon Mulcahy',
    author_email='brandon@jangler.info',
    url='https://github.com/jangler/vcii',
    description='A TUI spreadsheet application.',
    long_description=open('README.md').read(),
    packages=['vcii', 'vcii.test'],
    scripts=['bin/vcii'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
)
