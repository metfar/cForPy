#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shellcon.py
#
#  Copyright 2019- W.S. Martinez Bas <metfar@gmail.com>
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

#includes
from __future__ import absolute_import, print_function;
import sys;
import subprocess;
import os;
import tempfile;
import datetime;
import colorama;
import platform;
import hashlib;
import codecs;

#constants
true=TRUE=ON=True;
false=FALSE=OFF=not true;
null=NULL=Nil=NIL=none=None;
DIRES=[];
TIMEOUT=10;
OUTPUT="output";
RETURN="return";
ERROR="error";
MODE,INODE,IWHERE,NLINK="MODE","INODE","IWHERE","NLINK";
UID,GID,SIZE="UID","GID","SIZE";
ACCESS_TIME,MOD_TIME,CHANGE_TIME="ATIME","MTIME","CTIME";
NAN=None;
ESC=chr(27);
BLACK,RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE=range(0,8);
COLORS=[BLACK,BLUE,GREEN,CYAN,RED,MAGENTA,YELLOW,WHITE];
INK=WHITE;
PAPER=BLACK;#ECHO OFF
DEFAULT_METHOD="md5";
SEP=os.sep;
ASC ="º☺☻♥♦♣♠ººººººº♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼ "
ASC+="!\"#$%&'()*+,-./0123456789:;<=>?@"
ASC+="ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"
ASC+="abcdefghijklmnopqrstuvwxyz{|}~⌂Çü"
ASC+="éâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜø£Ø×ƒáíóú"
ASC+="ñÑªº¿®¬½¼¡«»░▒▓│┤ÁÂÀ©╣║╗╝¢¥┐└┴┬├─┼"
ASC+="ãÃ╚╔╩╦╠═╬¤ðÐÊËÈıÍÎÏ┘┌█▄¦Ì▀ÓßÔÒõÕµþ"
ASC+="ÞÚÛÙýÝ¯º0±‗¾¶§÷¸°¨·¹³²■º";
# Start functions on constants
## replace strange characters
for f in range(0,len(ASC)):
	if(ASC[f]=="º"):
		ASC=ASC[:f]+chr(f)+ASC[f+1:];
## set header to batch
if ("x" in platform.os.name):
	HEADER="#!/bin/bash\n";
	FOOT="\n";
	DIR="ls ";
	LX=True;
else:
	HEADER="@echo off\n\r";
	FOOT="\n\r";
	LX=False;
	DIR="dir /b ";

# Functions
def is_void(arg=None)->bool:
	""" is_void		returns if a variable is void or not """
	return(type(arg)==type(None) or str(arg)=='');

def asc(cha:str)->int:
	""" Get the ASCII-limited character position number """
	if(len(cha)>1):
		cha=cha[0];
	return(ASC.index(cha) if(cha in ASC) else 0);

def chr(number:int)->str:
	""" Get an ASCII limited character from its position number """
	try:
		return(ASC[int(number)% len(ASC)]);
	except:
		return(ASC[0]);

def toList(inp):
	"""
	Convert any input to list
	"""
	out=[];
	for f in inp:
		out.append(f);
	return(out);


def ascToIntl(inString:str)->str:
	""" Replace modified characters to intl standard """
	substi='¡¿~_¬\ÀÈÌÒÙẀỲǸÂÊÎÔÛŴŶÁÉÍÓÚẂÝŃÄËÏÖÜẄŸÑÇàèìòùẁỳǹâêîôûŵŷáéíóúẃýńäëïöüẅÿñç';
	substo='!?---/AEIOUWYNAEIOUWYAEIOUWYNAEIOUWYNCaeiouwynaeiouwyaeiouwynaeiouwync';
	out="";
	for f in toList(inString):
		cha=f;
		if f in substi:
			try:
				cha=substo[substi.index(cha)];
			except:
				pass;
		try:
			out+=str(cha);
		except:
			pass;
	return(out);

def aGrossoModo(x,force=False):
	""" aGrossoModo

			Filters codes and spaces of strings to make a rough comparison.
			"""
	out=str(ascToIntl(x)).replace("\\\\","\\").replace("\t","").replace("\r","").replace("\n","").replace('"',"").replace("'","").replace(" ","").replace('\\n',"").replace("/n","");
	if(force):
		out=out.replace('[',"").replace('{',"").replace(']',"").replace('}',"").replace('(',"").replace(')',"").replace(':',"").replace('.',"").replace(',',"");
	return(out);

## crypting
def rot13(inp: str) -> str:
	""" Crypting: Encode/Decode by rot13 """
	return(codecs.encode(inp,"rot13"));

def md5(inp: str) -> str:
	""" Crypting: MD5 from input string """
	return(hashlib.md5(inp.encode()).hexdigest());

def sha1(inp: str) -> str:
	""" Crypting: sha1 from input string """
	return(hashlib.sha1(inp.encode()).hexdigest());

def sha256(inp: str) -> str:
	""" Crypting: sha256 from input string """
	return(hashlib.sha256(inp.encode()).hexdigest());

def sha3(inp: str) -> str:
	""" Crypting: sha3_512 from input string """
	return(hashlib.sha3_512(inp.encode()).hexdigest());

def sha512(inp: str) -> str:
	""" Crypting: sha512 from input string """
	return(hashlib.sha512(inp.encode()).hexdigest());

def plain(inp: str) -> str:
	""" Crypting: Convert a string to international string """
	return(ascToIntl(inp));

def method(Inp:str, Method=DEFAULT_METHOD):
	m=aGrossoModo(Method).lower();
	if 	(m=="rot13"):
		return(rot13(Inp));
	elif(m=="md5"):
		return(md5(Inp));
	elif(m=="sha2"):
		return(sha256(Inp));
	elif(m=="sha3"):
		return(sha3(Inp));
	elif(m=="sha256"):
		return(sha256(Inp));
	elif(m=="sha512"):
		return(sha512(Inp));
	else:
		return(plain(Inp));

def exists(name):
	"""
	File Functions
	--------------

	exists('/tmp')
		returns true if the argument exists
	"""
	return(os.path.exists(name));

def dir_exists(name):
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

def file_exists(name):
	"""
	File Functions
	--------------

	fileExists('/tmp/file.txt')
			returns true if it exists as a file
	"""
	if(os.path.exists(name)):
		return(os.path.isfile(name));
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
		if not(dir_exists(f)):
			try:
				os.makedirs(f,exist_ok=True);
			except:
				try:
					os.makedirs(f);
				except:
					print("Error making "+str(f));
		if(not f in DIRES):
			DIRES.append(f);

def chmod(name,octal):
	""" OS Function: change permissions """
	os.chmod(name,int(str(octal),base=8));

def execute(cmd):
	"""
	OS Function
	-----------

	execute("argument")

		This creates a temporal file to execute with the argument inside.
		Then, it executes the file and destroys it.
	"""
	if (LX):
		fname=tempfile.mktemp("tmp");
	else:
		fname="tmptmp.bat";
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
	output=output.replace("\\r","");
	out={	RETURN:	tmp.returncode,
			OUTPUT:	output.split("\\n"),
			ERROR:	err.split("\\n")};
	return(out);

def scp(source,target):
	"""
		scp(From,To)    uses OS scp command
	"""
	out=execute("scp "+str(source)+" "+str(target)+" 1>/dev/null 2>/dev/null");
	return(out);

def file_get_content(name):
	""" Obtain full content from a file """
	tmp=open(name,"r");
	content=tmp.read();
	return(content);

def file_stats(name):
	""" Obtain file information """
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
	""" convert something to an integer number or NAN """
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
		WIDTH-=1;
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


	color(GREEN,BLACK);
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
	out=execute(DIR)[OUTPUT];
	if(VERSION==2):
		out=out[0].split("\n");
	for f in out:
		print(form2.format(f));

	for f in range(3,(HEIGHT-len(out))//2):
		print("*"," "*(WIDTH-4),"*");
	print("*"*WIDTH);

	return (0);

colorama.init();

WIDTH,HEIGHT=get_terminal_size();
if __name__ == '__main__':
	sys.exit(main(sys.argv));
	print("*"*WIDTH);

#https://raw.githubusercontent.com/metfar/cForPy/master/shellcon.py
# vim: syntax=python ts=4 sw=4 sts=4 sr noet
