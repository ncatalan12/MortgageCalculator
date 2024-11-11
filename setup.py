from setuptools import setup, find_packages

setup(
    name="mortgage-calculator",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pandas"],
    description="Tools for calculating mortgage payment and income taxes"
)
