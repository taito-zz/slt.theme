from setuptools import find_packages
from setuptools import setup


setup(
    name='slt.theme',
    version='0.17',
    description="Turns plone them into SLT shopping theme.",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@abita.fi',
    url='https://github.com/taito/slt.theme',
    license='None-free',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['slt'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'five.grok',
        'five.pt',
        'setuptools',
        'sll.basetheme',
        'sll.carousel',
        'slt.content',
        'slt.portlet',
        'z3c.jbot'],
    extras_require={'test': ['hexagonit.testing']},
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
