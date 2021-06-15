from setuptools import setup, find_packages

setup(
    name='shiny_dollop',
    version='1.0',
    packages=find_packages(),
    url='',
    license='',
    author='Matthew Wells',
    author_email='matthew.wells@canada.ca',
    description='Script for reorganizing Results data',
    zip_safe=False,
    install_requires=["pandas>=1.2.3", "openpyxl>=3.0.7", "setuptools>=49.6.0", "epiweeks>=2.1.2", "numpy>=1.20.2"],
    entry_points={'console_scripts': ['shiny_dollop=shiny_dollop.vcfparser_tables:main'],
                  }
)
#"build/lib/shiny_dollop/vcfparser_tables.py"