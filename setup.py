from setuptools import setup, find_packages

setup(
    name="vantage",
    version="3.0.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "sh", "pyyaml", "certifi"],
    entry_points="""
        [console_scripts]
        vantage=vantage.entry:vantage
        vg=vantage.entry:vantage
    """,
)
