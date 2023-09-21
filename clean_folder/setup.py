from setuptools import setup, find_namespace_packages

setup(name='main_sort',
      version='1.1.2',
      description='Folder sort',
      author='Aleksandr Gorpynych AG',
      author_email='alejandr000091@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main_sort']})
