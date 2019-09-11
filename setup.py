from setuptools import setup, find_packages

setup(
    name='Your Application',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==1.1.1', 
        'flask-sqlalchemy==2.4.0', 
        'psycopg2==2.8.3',
        'flask-migrate',
        'Flask-API',
        'flask-script',
        'pytest'
    ]
)