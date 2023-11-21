from setuptools import setup, find_packages

setup(
    name="lyzr",
<<<<<<< HEAD
    version="0.1.16",
=======
    version="0.1.15",
>>>>>>> 9103ec3f6948c2eab40a99ff8f281f5c53ce0131
    author="lyzr",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.1, <3.12",
    install_requires=[
        "transformers",
        "accelerate",
        "datasets[audio]",
        "pydub",
        "streamlit",
        "audio-recorder-streamlit",
        "ffmpeg",
        "asyncio",
        "nest_asyncio",
        "openai==1.3.4",
        "litellm==1.2.0",
        "llama-index==0.9.4",
        "langchain==0.0.339",
        "python-dotenv>=1.0.0",
        "lancedb==0.3.3",
        "beautifulsoup4==4.12.2",
        "pandas==2.0.2",
    ],
)
