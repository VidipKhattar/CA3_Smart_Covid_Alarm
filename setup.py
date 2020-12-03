import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="CA3_project-pkg-vkhattar", # Replace with your own username
    version="0.0.1",
    author="Vidip Khattar",
    author_email="vk284@exeter.ac.uk",
    description="A Covid smart alarm for daily use designed for this period of Covid for CA3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VidipKhattar/CA3_Smart_Alarm.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)