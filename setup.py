"""The setup and build script for the SysFS GPIO project."""
from distutils.core import setup

setup(
  name = 'pysysfs-gpio',
  packages = ['pysysfs'],
  version = '0.1',
  license='MIT',
  description = 'Linux SysFS GPIO Access',
  author = 'Yuval Aboulafia',
  author_email = 'yuval.abou@gmail.com',
  url = 'https://github.com/yuvalabou/pysysfs-gpio',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=['Twisted'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
