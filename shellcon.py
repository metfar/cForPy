#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shellcon.py
#  
#  Copyright 2019 W.S. Martinez Bas <metfar@gmail.com>
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

from __future__ import print_function;
import sys;
import subprocess;
import os;
import tempfile;
import datetime;


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
	#tmp=subprocess.run([fname],timeout=TIMEOUT,input=None,capture_output=True); tmp.stdout, tmp.stderr
	tmp=subprocess.Popen([fname], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
	output, err = tmp.communicate(b"");
	if(VERSION==3):
		output=str(output)[2:-1];
		err=str(err)[2:-1];
	os.unlink(fname);
	out={	RETURN:	tmp.returncode,
			OUTPUT:	output.split("\\n"),
			ERROR:	err.split("\\n")};
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

MODE,INODE,IWHERE,NLINK="MODE","INODE","IWHERE","NLINK";
UID,GID,SIZE="UID","GID","SIZE";
ACCESS_TIME,MOD_TIME,CHANGE_TIME="ATIME","MTIME","CTIME";
NAN=None;
ESC=chr(27);
BLACK,RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE=range(0,8);
COLORS=[BLACK,BLUE,GREEN,CYAN,RED,MAGENTA,YELLOW,WHITE];

INK=WHITE;
PAPER=BLACK;

def file_stats(name):
	(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(name);
	out={	MODE:			mode, 
			INODE:			ino, 
			IWHERE:			dev, 
			NLINK:			nlink, 
			UID:			uid, 
			GID:			gid, 
			SIZE:			size, 
			ACCESS_TIME:	atime, 
			MOD_TIME:		mtime, 
			CHANGE_TIME:	ctime};
	return(out);

def Int(num=0):
	try:
		out=int(float(str(num)));
	except:
		out=NAN;
	return(out);

def repeat(num=1,character=" "):
	try:
		out=character*Int(num);
	except:
		out=character;
	return(out);

def spc(num=1):
	return(repeat(num," "));


def gotoxy(x,y):
	print(ESC+"["+str(y)+";"+str(x)+"H",end="");

def locate(y,x):
	gotoxy(x,y);

def color(Ink=None,Paper=None):
	global INK,PAPER;
	if(type(Ink)!=type(None)):
		try:
			INK=0+Int(Ink) % len(COLORS);
		except:
			pass;
	if(type(Paper)!=type(None)):
		try:
			PAPER=0+Int(Paper) % len(COLORS);
		except:
			pass;
	print(ESC+"[3"+str(COLORS[INK])+";4"+str(COLORS[PAPER])+"m",end="");

def clrscr():
	color();
	print(ESC+"[2J"+ESC+"[0;0H\n"+ESC+"[1A",end="");

def ink(Ink=None):
	if(type(Ink)==type(None)):
		return(INK);
	try:
		INK=0+Int(Ink) % len(COLORS);
	except:
		pass;
	print(ESC+"[3"+str(COLORS[INK])+"m",end="");

def paper(Paper=None):
	if(type(Paper)==type(None)):
		return(PAPER);
	try:
		PAPER=0+Int(Paper) % len(COLORS);
	except:
		pass;
	print(ESC+"[4"+str(COLORS[PAPER])+"m",end="");


def file_date(name):
	try:
		tm=file_stats(name)[MOD_TIME];
		out=datetime.datetime.fromtimestamp(tm).strftime('%Y-%m-%d %H:%M:%S (%j|%U|%u)');
	except:
		out=None;
	return(out);

def get_terminal_size():
	global WIDTH,HEIGHT,VERSION;
	try:
		WIDTH,HEIGHT=os.get_terminal_size();
		VERSION=3;
	except:
		HEIGHT,WIDTH=os.popen("stty size","r").read().split();
		VERSION=2;
	
	#for f in os.popen("stty size","r").read().split():
	#	print(f);
	#print(WIDTH,"_",HEIGHT);
	#exit(1);
	return Int(WIDTH),Int(HEIGHT);



def main(args):
	vargs=list(args);
	APP=vargs.pop(0);
	
	
	color(7,1);
	clrscr();
	print("*"*WIDTH);
	form1="*{:^"+str(WIDTH-2)+"}*";
	form2="*{:<"+str(WIDTH-2)+"}*";
	for f in range(2):
		print("*"+(" "*(WIDTH-2))+"*");
	print(form1.format(APP+spc(2)+file_date(APP)));
	for f in range(2):
		print("*"+(" "*(WIDTH-2))+"*");
	
	print("*"*(WIDTH));
	out=execute("ls")[OUTPUT];
	if(VERSION==2):
		out=out[0].split("\n");
	for f in out:
		print(form2.format(f));
	
	for f in range(3,(HEIGHT-len(out))//2):
		print("*"," "*(WIDTH-4),"*");
	print("*"*WIDTH);
	
	return (0);


WIDTH,HEIGHT=get_terminal_size();
if __name__ == '__main__':
	sys.exit(main(sys.argv));


#https://raw.githubusercontent.com/metfar/cForPy/master/shellcon.py
# vim: syntax=python ts=4 sw=4 sts=4 sr noet
