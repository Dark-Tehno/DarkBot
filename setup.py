import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='DarkBot',  
    version='0.1.3',   
    author='vsp210', 
    author_email='vsp210@gmail.com', 
    description='Клиентская библиотека Python для создания Dark-ботов.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vsp210/DarkBot", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
