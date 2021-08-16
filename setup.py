# Copyright 2019 Softwerks LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tournament",
    version="1.0.0",
    author="Softwerks",
    author_email="info@softwerks.com",
    description="Match service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/softwerks/tournament",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["aioredis", "backgammon"],
    extras_require={"dev": ["hupper"], "dev-opt": ["watchdog"]},
    entry_points={"console_scripts": ["tournament=tournament.__main__:main"]},
)
