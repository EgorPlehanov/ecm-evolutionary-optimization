from setuptools import find_packages, setup

setup(
    name="ecm-evolutionary-optimization",
    version="0.1.0",
    packages=find_packages(include=["ecm_optimizer", "ecm_optimizer.*"]),
    install_requires=["click>=8.1", "numpy>=1.24", "scipy>=1.10"],
    entry_points={"console_scripts": ["ecm-optimizer=ecm_optimizer.cli.main:main"]},
)
