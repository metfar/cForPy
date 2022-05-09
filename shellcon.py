#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shellcon.py
#  
#  Copyright 2019 William Martinez Bas <metfar@gmail.com>
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

import sys;
import subprocess;
import os;
import tempfile;

DIRES=[];
TIMEOUT=10;
OUTPUT="output";
RETURN="return";
ERROR="error";
def exists(name):
	"""
	File Functions
	--------------
	
	exists('/tmp')
		returns true if the argument exists
	"""
	return(os.path.exists(name));
	
def dirExists(name):
	"""
	File Functions
	--------------

	dirExists('/tmp')
			returns true if it exists and it is a directory
	"""
	if(os.path.exists(name)):
		return(os.path.isdir(name));
	else:
		return(False);

def mkdires(arr_dirs=["Temp"]):
	"""
	File Functions
	--------------
	
	mkdires()
		create default Temp directory
	
	mkdires(["This","Another"])
		create desired directories
	
	"""
	global DIRES;
	if(type(arr_dirs)==type("casa")):
		arr_dirs=[arr_dirs];
	for f in arr_dirs:
		if not(dirExists(f)): 
			os.makedirs(f,exist_ok=True);
		if(not f in DIRES):
			DIRES.append(f);
			
def chmod(name,octal):
	os.chmod(name,int(str(octal),base=8));
	
def execute(cmd):
	"""
	OS Function
	-----------
	
	execute("argument")
	
		This creates a temporal file to execute with the argument inside.
		Then, it executes the file and destroys it.
	"""
	HEADER="#!/bin/bash\n";
	FOOT="\n";
	fname=tempfile.mktemp("tmp");
	f=open(fname,"w");
	f.write(HEADER+cmd+FOOT);
	f.close();
	chmod(fname,777);
	tmp=subprocess.run([fname],timeout=TIMEOUT,input=None,capture_output=True);
	os.unlink(fname);
	out={	RETURN:	tmp.returncode,
			OUTPUT:	str(tmp.stdout)[2:-1].split("\\n"),
			ERROR:	str(tmp.stderr)[2:-1].split("\\n")};
	return(out);
	
def scp(source,target):
	"""
		scp(From,To)
	"""
	out=execute("scp "+str(source)+" "+str(target)+" 1>/dev/null 2>/dev/null");
	return(out);

def file_get_content(name):
	tmp=open(name,"r");
	content=tmp.read();
	return(content);

def main(args):
	global WIDTH,HEIGHT;
	vargs=list(args);
	APP=vargs.pop(0);
	WIDTH,HEIGHT=os.get_terminal_size();
	print("*"*WIDTH);
	form="{:^"+str(WIDTH-4)+"}";
	for f in range(3,HEIGHT//2-1):
		print("*"," "*(WIDTH-4),"*");
	print("*",form.format(APP),"*");
	for f in range(3,HEIGHT//2-1):
		print("*"," "*(WIDTH-4),"*");
	print("*"*WIDTH);
	print(execute("ls")[OUTPUT]);
	print("*"*WIDTH);
	
	print();
	return (0);

if __name__ == '__main__':
	sys.exit(main(sys.argv));

	
#from https://raw.githubusercontent.com/metfar/cForPy/master/shellcon.py
