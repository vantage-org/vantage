from setuptools import setup, find_packages

setup(
    name="vantage",
    version="3.4.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["certifi==2022.12.7", "strictyaml==1.4.4"],
    entry_points="""
        [console_scripts]
        vantage=vantage.entry:vantage
        vg=vantage.entry:vantage
    """,
)
