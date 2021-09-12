from setuptools import setup, find_packages
import pathlib

# I have no idea what this file does
# or how it works 
# or if it works
# Use at own risk

here = pathlib.Path(__file__).parent.resolve()

setup(name="SolarSystemMaker",
      version="1.0.3",
      description="Minimalistic, educational 2D solar system simulation software",
      author="George Lawrence",
      author_email="georgeblawrence@hotmail.co.uk",
      url="https://github.com/gblawrence03/solar-system-maker",
      packages=find_packages(),
      install_requires=[
          "pygame",
          "cx_Oracle"])