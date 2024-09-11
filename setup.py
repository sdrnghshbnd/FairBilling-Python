from setuptools import setup, find_packages

setup(
    name='fair_billing',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'fair_billing=fair_billing:main',
        ],
    },
)
