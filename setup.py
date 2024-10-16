from setuptools import setup, find_packages
 
classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License"
]

__version__ = "0.1.2"
__author__ = 'programminglaboratorys'
__description__ = 'create nin0chat bots with python!'
_long_description_ = open('README.md').read() + "\n\n" + open("CHANGELOG.txt").read()
if __name__ == '__main__':
	setup(
	  name='nin0lib',
	  version=__version__,
	  description=__description__,
	  long_description=_long_description_,
	  long_description_content_type='text/markdown',
	  url='',  
	  author=__author__,
	  author_email='programming.laboratorys@gmail.com',
	  license='MIT', 
	  classifiers=classifiers,
	  keywords='chat,nin0,bot,commands', 
	  packages=find_packages(),
	  install_requires=[]
	)
