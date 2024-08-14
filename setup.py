from setuptools import setup

setup(
    name="Fenrir",
    version="1.0",
    description="Fenrir Editor Application",
    author="Hasan Bahadır Nural",
    author_email="bahadir.nural@example.com",  
    packages=["fenrir"], 
    install_requires=[
        "tkinter",
        "pyautogui",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "fenrir = fenrir.main:main", 
        ],
    },
)
