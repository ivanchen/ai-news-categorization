from setuptools import setup, find_packages

setup(
    name="ai-news-categorization",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'requests>=2.25.1',
        'transformers>=4.5.1',
        # 'torch>=1.8.1',
        'pyyaml>=5.4.1',
        'numpy>=1.19.5',
        'pandas>=1.2.4',
        'nltk>=3.6.0',
    ],
)
