from setuptools import setup, find_packages


requires = [
    "pyramid",
    "setuptools>=0.7",
]

setup(name="rebecca.app.admin",
      namespace_packages=['rebecca', 'rebecca.app'],
      install_requires=requires,
      packages=find_packages(),
)

