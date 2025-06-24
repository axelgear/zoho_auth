from setuptools import setup, find_packages

setup(
    name='zoho_auth',
    version='0.0.1',
    description='Zoho OAuth app for Frappe',
    author='AxelGear',
    author_email='rejithr1995@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['frappe'],
)
