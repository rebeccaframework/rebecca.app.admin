from setuptools import setup, find_packages


requires = [
    "pyramid",
    "setuptools>=0.7",
    "deform>=2.0dev",
    "pyramid-deform",
    "pyramid-layout",
    "sqlalchemy",
    "zope.sqlalchemy",
]

tests_require = [
    "testfixtures",
]

setup(name="rebecca.app.admin",
      namespace_packages=['rebecca', 'rebecca.app'],
      install_requires=requires,
      packages=find_packages(),
      tests_require=tests_require,
      extras_require={
          "testing": requires+tests_require,
      },
)

