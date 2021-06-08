from setuptools import setup

setup(
    name='shiny_dollop',
    version='1.0',
    packages=['shiny_dollop'],
    url='',
    license='',
    author='Matthew Wells',
    author_email='matthew.wells@canada.ca',
    description='Script for reorganizing Results data',
    zip_safe=False,
    install_requires=["pandas>=1.2.3", "openpyxl>=3.0.7", "setuptools>=49.6.0"],
    entry_points={'console_scripts':
                      ['bergen=List_mutations.build.lib.shiny_dollop.vcfparser_tables.main', ], }
)
