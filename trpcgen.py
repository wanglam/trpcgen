#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ptsd.loader import Loader
from Cheetah.Template import Template
from os import path, mkdir
import os
import argparse

import base

parser = argparse.ArgumentParser(description='Code generation tool for trpc')
parser.add_argument('action', metavar='action', type=str,
                   help='generation action: struct|service|both', choices=["struct", "service", "both"])
parser.add_argument('thrift_file_path', metavar='thrift_file_path', type=str,
                   help='input thrift file path')
parser.add_argument('-l', '--lang', metavar='lang', type=str, choices=["java","javascript"],
                   help='language to be generated: java')
parser.add_argument('output_folder_path', metavar='output_folder_path', type=str,
                   help='out folder path')

args = parser.parse_args()

def write_file(fname, content):
	dir = path.dirname(fname)
	if not path.exists(dir):
		os.makedirs(dir)

	with open(fname, "w") as f:
		f.write(content)

lang_ext = {
	"java": ".java",
	"javascript":".js"
}

def handle_struct(module, loader):
	for obj in module.structs:
		tpl_path = os.path.join('tpl', args.lang, "struct.%s_tpl" % args.lang)

		tpl = open(tpl_path, 'r').read().decode("utf8")
		t = Template(tpl, searchList=[{"loader": loader, "obj": obj}])
		code = str(t)
		out_path = os.path.join(args.output_folder_path, "gen_" + obj.name.value + lang_ext[args.lang])
		write_file(out_path, code)

def handle_service(module, loader):
	for obj in module.services:
		tpl_path = os.path.join('tpl', args.lang, "service.%s_tpl" % args.lang)

		tpl = open(tpl_path, 'r').read().decode("utf8")
		print obj.functions[0]
		t = Template(tpl, searchList=[{"loader": loader, "obj": obj}])
		code = str(t)
		out_path = os.path.join(args.output_folder_path, "gen_service_" + obj.name.value + lang_ext[args.lang])
		write_file(out_path, code)

def main(thrift_idl):
	loader = base.load_thrift(thrift_idl)

	if args.lang == None:
		args.lang = "java"

	for module in loader.modules.values():
		if args.action == "struct":
			handle_struct(module, loader)
		elif args.action == "service":
			handle_service(module, loader)
		else:
			handle_struct(module, loader)
			handle_service(module, loader)

main(args.thrift_file_path)
