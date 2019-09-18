#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cforpy.py - cForPy project: https://github.com/metfar/cForPy
#  
#  File: https://raw.githubusercontent.com/metfar/cForPy/master/cforpy.py
#
#  This library is a combination of a lot of previous jobs.
#  I started it when I began to study C language, with a gw/qbas!c baggage.
#  So, this is based on my BASIC.h(1988), bib.h(1989), bibc.py (c/cpp compat),
#  func.py (basic functions), php.py (php compat).
#  Historical previous approximations:
#  https://sourceforge.net/projects/pythonconsoleproje/ 
#  https://github.com/metfar/pyInfo
#
#  Sister project:  https://github.com/metfar/javaprintf
#
#  This has no warranties.
#
#  Copyright 2013- William Sebastian Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys,os,io;
from pprint import pprint;

TRUE=true=(1==1);
FALSE=false=(1!=1);
DBG=false;


if sys.version < '3':
	integer_types = (int, long,);
else:
	integer_types = (int,);

if (DBG):
	devnull = open(os.devnull, 'w');
	sys.stderr = devnull;

def array(*args, **kwargs):
	n=0;
	res=list();
	for a in args:
		res.append(a);
	return(res);



def is_imported(x):
	""" 
	is_imported("module")
						returns true if "module" was imported previously.
	"""
	return(x in sys.modules);
    
def rnd(x=1):
	""" 
	rnd([n])
				returns a number in [0,n)
	"""
	if(not is_imported(x)):
		import random;
	return (random.random() * x);

def print_r(*args, **kwargs):
	"""
		print_r("Something",(1,2))
				
				prints out mixed type data.
	"""
	for a in args:
		pprint(a);
		
	
"""
File Functions
--------------

Example:
========
fp = fopen('date.txt', 'w')
fprintf(fp,"%04d-%02d-%02d",2002,6,11);
fclose(fp);

"""

def fopen(File,Mode):
	""" 
	File Functions
	==== =========
	
	fopen (Filename,Mode)
					 returns pointer to file
	
	Filename 	Path and filename
	
	MODE
	-----
	r - Read 
	a - Append 
	w - Write 
	x - Create - returns error if the file exist
	t - Text
	b - Binary

		
	Example:
	========
	fp = fopen('date.txt', 'wt')

	"""
	return(open(File, Mode));

def fclose(handle):
	""" 
	File Functions
	==== =========
	
	fclose (FilePointer) 
	
	Example:
	========
	
	fclose(fp);

	"""
	handle.close();

def fprintf(*vargs):
	""" 
	File Functions
	--------------
	
	fprintf (FilePointer, FORMAT [,arg1,arg2,...])
	
	FilePointer
	
	FORMAT
	%d	integer with sign
	%i	integer with sign
	%u	unsigned int
	%o	octal
	%x	hexadecimal lowercase
	%X	hexadecimal uppercase
	%f	floating point
	%lf	double float
	%e 	scientific notation lowercase
	%E 	scientific notation upppercase
	%c 	character
	%s 	string
	
	
	Example:
	========

	fprintf C-Style function 
	
	
	
	"""
	args=list(vargs);
	try:
		Arch=args.pop(0);
		assert(isinstance(Arch, io.TextIOBase) or isinstance(Arch, io.BufferedIOBase)), "Wrong file handler";  
		Format=args.pop(0);
		print(Format % tuple(args), file=Arch);
	except:
		raise Exception("Error on fprintf");


def sprintf(*vargs):
	out="";
	args=list(vargs);
	try:
		Format=args.pop(0);
		out=(Format % tuple(args));
	except:
		raise Exception("Error on sprintf");
	return(out);


def printf(*vargs):
	out="";
	args=list(vargs);
	try:
		Format=args.pop(0);
		out=(Format % tuple(args));
	except:
		raise Exception("Error on sprintf");
	print(out,end='');

def fread(fp,length=1):
	return(fp.read(length));



def ascii ():
	""" Prints to screen ASCII from 32 to 255 
		 (omission range [133,160] because printing errors)
		 """
	for f in range(32,132):
		printf("%2x %c\t",f,f);
		if(f%8 == 7):
			printf("\n");
	for f in range(161,256):
		printf("%2x %c\t",f,f);
		if((f)%8 == 4):
			printf("\n");

def cls():
	""" CLear text mode Screen """
	print(chr(27)+'[2j',end='');
	print('\033c',end='');
	print('\x1bc',end='');

clc=cls;

def file_exists(name):
	return(os.path.exists(name));

echo=print;
