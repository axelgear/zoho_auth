from setuptools import setup, find_packages

setup(
    name="zoho_auth",
    version="0.1.0",
    description="Zoho OAuth2 login for Frappe",
    author="AxelGear",
    author_email="rejithr1995@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["frappe"],
)
