from setuptools import setup, find_packages

setup(
    name="vantage",
    version="3.2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["sh==1.14.2", "ruamel.yaml==0.17.10", "certifi==2021.5.30"],
    entry_points="""
        [console_scripts]
        vantage=vantage.entry:vantage
        vg=vantage.entry:vantage
    """,
)
