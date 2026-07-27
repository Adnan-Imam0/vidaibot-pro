from setuptools import setup, find_packages

setup(
    name="vidaibot-pro",
    version="2.0.0",
    description="Advanced YouTube View Booster with Anti-Detection",
    author="Your Name",
    author_email="your-email@example.com",
    url="https://github.com/yourusername/vidaibot-pro",
    packages=find_packages(),
    install_requires=[
        'selenium==4.15.2',
        'undetected-chromedriver==3.5.4',
        'webdriver-manager==4.0.1',
        'fake-useragent==1.4.0',
        'urllib3==2.1.0',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)