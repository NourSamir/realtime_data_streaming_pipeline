import setuptools
from setuptools import find_packages

_name = "data_streaming_pipeline"
_repo_name = "realtime_data_streaming_pipeline"
_license = 'Proprietary: Internal use only'
_description = "Realtime Data pipeline and Web application"
_github_username = "NourSamir"

setuptools.setup(
    name=_name,
    version='1.0.0',
    description=_description,
    license=_license,
    url=f'https://github.com/{_github_username}/{_repo_name}.git',
    author='Nour Samir',
    author_email='Noursamir96@gmail.com',
    python_requires='>=3.7',

    classifiers=[
        'Development Status :: Alpha',
        'Environment :: cli',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],

    packages=find_packages(exclude=['tests']),

    install_requires=[
        "Flask",
        "Flask-Cors",
        "python-dotenv",
        "kafka-python",
        "redis",
    ],

    test_suite='unittest.TestCase',
    include_package_data=True,

    entry_points={
        'console_scripts': [
            "run_app_service = app_service.main:main",
            "run_metrics_calculation_flow = metrics_calculation_flow.main:main",
            "run_data_transformation_flow = data_transformation_flow.main:main",
            "run_producer_app = producer_app.main:main",
        ],
    },
)