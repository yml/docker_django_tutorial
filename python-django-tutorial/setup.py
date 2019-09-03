from setuptools import find_packages, setup

setup(
    name="python_django_tutorial",
    version="1.0",
    packages=find_packages("python_django_tutorial"),
    package_dir={"": "python_django_tutorial"},
    include_package_data=True,
    description="A very simple django project",
    url="http://www.example.com/",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires=[],
    scripts=["python_django_tutorial/manage.py"],
    extras_require={},
)