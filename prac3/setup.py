import setuptools

setuptools.setup(
	name='helloworldpkg',
	version='0.0.1',
	author='me',
	author_email='me@me.me',
	description='dummy pkg',
	packages=setuptools.find_packages(),
	package_data={'': ['hw.json']},
	include_package_files=True
)