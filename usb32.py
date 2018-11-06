#!/bin/python
##################################################################################
## convert all usb31 to usb32 for src folder#depo = "//dwh/usb31_iip/dev/usb32/..."
#################################################################################
import os
import sys
import logging
import shutil 
import re
import io
import subprocess
import os.path

def p4_cmd(cmd):
	logger.info("Running the cmd " + cmd)
	os.system(cmd)

def run_bash(cmd):
	cmd_proc = subprocess.Popen(cmd , shell=True ,stdout=subprocess.PIPE , stderr=subprocess.STDOUT)
	cmd_lines = cmd_proc.communicate()[0].splitlines()
	cmd_lines = [i.decode() for i in cmd_lines]
	return(cmd_lines)

########################################################################################
def replaceFile_src ( file_usb31 , file_usb32 ):
	#regex = r"(`include \S+)"
	regex = r"(`include \S+)"
	regex_eval = r"\{\[eval_param @DWC_USB3_GENERATION] == 31\}"
	enc = "utf-8"
	logger.info("copying : " + file_usb31 + " with :" + file_usb32)
	#with io.open(file_usb31,"r",encoding = "ISO-8859-1") as file:   
	with open(file_usb31,"r") as file:
		contents = file.read()
	replace_content = contents.replace('DWC_usb31','DWC_usb32')
	replace_content1 = replace_content.replace('DWC_USB31','DWC_USB32')
	replace_content1 = replace_content1.replace('usb31','usb32')
	replace_content1 = replace_content1.replace('DWC-USB31','DWC-USB32')
	replace_content1 = replace_content1.replace('USB31','USB32')
	replace_content1 = replace_content1.replace('define DWC_USB3_GENERATION 31','define DWC_USB3_GENERATION 32') 
	replace_content1 = replace_content1.replace('MAC31','MAC32') 
	replace_content1 = replace_content1.replace("//dwh/usb32_iip/usb32_br_usb32/DWC_usb32/","//dwh/usb32_iip/dev/usb32/DWC_usb32/")
	logger.info(file_usb31)
	if "`include " in replace_content1:
		result = re.findall(regex,replace_content1)
		for line in result:
			module_result = (line.split('"')[1])
			#if "params.v" in module_result or "param.v" in module_result or "hparams" in module_result:
			if module_result:
				logger.info("Replacing " + module_result + " with .svh")
				module_final = module_result.split(".")[0] + ".svh"
				logger.info(module_final)
				replace_content1 = replace_content1.replace(module_result , module_final)
	dir_name =(os.path.dirname(file_usb32))
	logger.info(dir_name)
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	text_file = open(file_usb32,"w")
	text_file.write(replace_content1)
	text_file.close()
	print("Wrote " + file_usb32)
### Replace the contents only ... 

def replaceFile ( file_usb31 , file_usb32 ):
	logger.info("Running replaceFile for " + file_usb31 +" " + file_usb32)
	#regex = r"(`include \S+)"
	regex = r"(`include \S+)"
	enc = "utf-8"
	#logger.info("replacing : " + file_usb31 + " with :" + file_usb32)
	#with io.open(file_usb31,"r",encoding = "ISO-8859-1") as file:   
	with open(file_usb31,"r",encoding="ISO-8859-1") as file:
		contents = file.read()
	replace_content = contents.replace('DWC_usb31','DWC_usb32')
	replace_content1 = replace_content.replace('DWC_USB31','DWC_USB32')
	replace_content1 = replace_content1.replace('usb31','usb32')
	replace_content1 = replace_content1.replace('DWC-USB31','DWC-USB32')
	replace_content1 = replace_content1.replace('USB31','USB32')
	replace_content1 = replace_content1.replace('define DWC_USB3_GENERATION 31','define DWC_USB3_GENERATION 32') 
	replace_content1 = replace_content1.replace('MAC31','MAC32') 
	replace_content1 = replace_content1.replace("@DWC_USB3_GENERATION == 31","@DWC_USB3_GENERATION == 32")
	replace_content1 = replace_content1.replace("//dwh/usb32_iip/usb32_br_usb32/DWC_usb32/","//dwh/usb32_iip/dev/usb32/DWC_usb32/")
	logger.info(file_usb31)
	if "{[eval_param @DWC_USB3_GENERATION] == 31}" in replace_content1:
		if value[0]:
			logger.info("value is " + value[0])
			replace_content1 = replace_content1.replace("{[eval_param @DWC_USB3_GENERATION] == 31}","{[eval_param @DWC_USB3_GENERATION] == 32}")
	if "`include " in replace_content1:
		result = re.findall(regex,replace_content1)
		for line in result:
			module_result = (line.split('"')[1])
			if "params.v" in module_result:
				logger.info("Replacing " + module_result + " with .svh")
				module_final = module_result.split(".")[0] + ".svh"
				logger.info(module_final)
				replace_content1 = replace_content1.replace(module_result , module_final)
			else:
				logger.info("Replacing " + module_result + " with .sv")
				module_final = module_result.split(".")[0] + ".sv"
				logger.info(module_final)
				replace_content1 = replace_content1.replace(module_result , module_final)
	dir_name =(os.path.dirname(file_usb32))
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	text_file = open(file_usb32,"w")
	text_file.write(replace_content1)
	text_file.close()
	logger.info("Wrote " + file_usb32)

#####################################################################################

def processDiff(files_usb31):
	files_changed = {}
	dict_int = {}
	files_usb32 = []
	tmp_list = []
	## replace the usb31 files here with usb32 
	for file_usb31 in files_usb31:
		logger.info(file_usb31)
		#print(file_usb31)
		file_usb32 = file_usb31.replace("usb31_br_usb32/DWC_usb31","dev/usb32/DWC_usb32")
		file_usb32 = file_usb32.replace("DWC_usb31","DWC_usb32")
		file_usb32 = file_usb32.replace("usb31","usb32")
		file_usb32 = file_usb32.replace("utb", "pve")
		files_usb32.append(file_usb32)
		## replace function will try to get usb31 with all content replaced to usb32 and save as usb32.tmp
		replaceFile(file_usb31,file_usb32+ ".tmp")
		#print(file_usb32 + " for " + file_usb31)
		logger.info(file_usb32)
		files_usb32.append(file_usb32)
		dict_int[file_usb32] = file_usb31
	return(files_usb32,dict_int)	


def processBridge(dest):
	cm_details = ""
	files_usb31 = []
	bridge_dict_desc = {} 
	bridge_dict_cm = {} 
	regex_changelist = r"Change (\d+)"
	regex_crm = r"(CRM_\d+)"
	os.chdir(dest)
	for root,dirs,files in os.walk( dest,followlinks=True):
		for name in files:
			file_usb31 = root + "/" + name 
			file_output = os.popen("p4 changes -m 1 -l " + root + "/" + name).read()
			if "Change " in file_output:
				#logger.info("file_output" + file_output)
				change_list = re.findall(regex_changelist ,file_output)[0]
				cmd = "p4 describe -s " + change_list
				cmd_output = os.popen(cmd).read()
				fileName = os.popen("p4 have " + root + "/" + name).read().split("-")[0]
				file_desc = (fileName.split("usb31_usb32/"))[-1]
				desc = (file_output.split('\t'))[-1]
				if "CRM_" in cmd_output:
					crm_number = re.findall(regex_crm,cmd_output)[0]
					cm_details = (crm_number + "::" + change_list)
					bridge_dict_cm[file_usb31] = cm_details
			
				file_details = (fileName + "::" + desc).strip()
				#logger.info("cmd "  + cm_details + "\t" +file_details)
				bridge_dict_desc[file_usb31] = cm_details + "\t" + file_details 
						
			else:
				logger.info("No Change for file " + root + "/" +name)
	       			
			if ".pdf" not in name:
				files_usb31.append(root + '/' + name)
	#print(files_usb31)
	return(files_usb31,bridge_dict_desc)

########################################################################################
## process the usb32 files
#######################################################################################

def translatePkgFiles(pkg_files):
	for pkg_file in pkg_files:
		print(pkg_file)

def readlst_file(dict_int):
	logger.info("Inside readlst")
	result = ''
	dict_final = {}
	lst_file = "/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32/dev/usb32/DWC_usb32/src/DWC_usb32.lst"
	p = open("/tmp/list" ,"w")
	print(dict_int)
	p.write(str(dict_int))
	p = open(lst_file,"r")
	file_lst = p.readlines()
	for key in dict_int:
		if key.endswith(".v") or key.endswith(".sv") or key.endswith(".svh"):
			main_key = key.split("/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32/dev/usb32/DWC_usb32/src/")[1].split(".")[0]
			print(key.split("/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32/dev/usb32/DWC_usb32/src/")[1])
			dict_final[main_key] = key.split("/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32/dev/usb32/DWC_usb32/src/")[1]
	for line in file_lst:
		wanted = (line.strip().split(".")[0])
		if wanted in dict_final:
			logger.info("wanted from lst_file " + wanted)
			logger.info("From the dict " + dict_final[wanted])
			result = result + dict_final[wanted] + "\n"
		else:
			print(wanted + " is not in dict_final")
	cmd = "p4 edit " + lst_file
	p4_cmd(cmd)
	y = open(lst_file,"w")
	y.write(result)
	y.close()
	logger.info("Updated the " + lst_file)

def readlst_file1(dict_int,bridge_dict):
	dict_final = {}
	result = ''
	for key in dict_int:
		main_key = key.split("/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32/dev/usb32/DWC_usb32/src/")[1]
		main_value = dict_int[key].split("/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32/usb31_br_usb32/DWC_usb31/src/")[1].split(".")[0]
		dict_final[main_value] = main_key
	lst_file = "/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32/usb31_br_usb32/DWC_usb31/src/DWC_usb31.lst"
	cmd = "p4 edit " + lst_file
	p4_cmd(cmd)
	logger.info(dict_final)
	p = open(lst_file,"r")
	for line in p.readlines():
		wanted = line.strip().split(".")[0]
		logger.info("line from lst_file" + wanted) 
		if wanted in dict_final:
			result = result + dict_final[wanted] + "\n"
			logger.info(wanted + " is present in dic_final")
		else:
			logger.info(wanted + " is not present in dict_final")

	logger.info("result " + result)
	file1 = "/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32/dev/usb32/DWC_usb32/src/DWC_usb32.lst"
	cmd = "p4 edit " + file1
	p4_cmd(cmd)
	q = open(file1,"w")
	q.write(result)
	logger.info("wrote " + file1)
	logger.info("Checkin submit is " + (bridge_dict[lst_file]))
	cmd = "p4 revert " + lst_file
	p4_cmd(cmd)

def find_header(file_usb31,file_usb32):
	result = ''
	define_flag = False
	module_flag = False
	interface_flag = False
	function_flag = False

	f = open(file_usb31,"r")
	for line in f.readlines():
		line = line.lstrip()
		if line.startswith("module ") and not line.startswith("//") and "module" in line:
			module_flag = True
			break
	if module_flag:
		file_usb32 = file_usb32.replace(".v",".sv")
	else:
		file_usb32 = file_usb32.replace(".v",".svh")
	f.close()
	return(file_usb32)

def checkFile(file_usb32,add_files):
	cmd = "ls " + file_usb32.split(".")[0] +".sv*"
	result = run_bash(cmd)
	if "ls: cannot access" in result[0]:
		add_files.append(file_usb32)
		return (file_usb32,add_files)
	else:
		return(result[0],add_files)

def getusb32_src(files_usb31):
	dict_int = {}
	delete_files_usb32 = []
	add_files_usb32 = []
	files_changed = {}
	files_usb32 = []
	tmp_list = []

	for file_usb31 in files_usb31:
		symlink = False
		logger.info('File_usb31 : ' + file_usb31)
		if os.path.islink(file_usb31):
			logger.info(file_usb31 + " is a link ")
			logger.info(" os path realpath : " + os.path.realpath(file_usb31))
			symlink = True

		if "DWC_usb31.lst" in file_usb31:
			continue
		if ".v-2porthub" in file_usb31:
			continue
		file_usb32 = file_usb31.replace("usb31_br_usb32/DWC_usb31","dev/usb32/DWC_usb32")
		file_usb32 = file_usb32.replace("DWC_usb31","DWC_usb32")
		file_usb32 = file_usb32.replace("usb31","usb32")
		file_usb32 = file_usb32.replace("utb", "pve")
		## if the file ends with .v
		file_usb32_old = file_usb32
		file_usb32,add_files_usb32 = checkFile(file_usb32,add_files_usb32)
		logger.info("File_usb31 is " + file_usb31 + " from checkFile")
		logger.info("File_usb32 is " + file_usb32 + " from checkFile")
		if file_usb32:
			if file_usb32.endswith(".v") or file_usb32.endswith(".sv") or file_usb32.endswith(".svh"):
				file_usb32 = find_header(file_usb31,file_usb32)
		dict_int[file_usb32] = file_usb31
		logger.info(file_usb32 + " for " + file_usb31)
		print("File_usb32 is " + file_usb32)

		if symlink:
			inv_map = {v : k for k ,v in dict_int.items()}
			source = os.path.realpath(file_usb31)
			## we need to cd to put the symlink 
			dir_old = os.getcwd()
			os.chdir(os.path.dirname(inv_map[file_usb31]))
			### we get source dir and destionation dir
			src_dir = os.path.dirname(inv_map[source])
			dest_dir = os.path.dirname(inv_map[file_usb31])
			head,tail = os.path.split(inv_map[source])
			## now we need to comute the ../../ as per dire
			count_needed = dest_dir.split(src_dir)[1].count("/")
			cmd = "p4 have " + file_usb32
			result = run_bash(cmd)

			if "not on client" in result[0]:
				cmd = "ln -s " + '../'*count_needed + tail + " ."
				logger.info("Running cmd - { " + cmd)
				p4_cmd(cmd)
				cmd = "p4 add -t symlink " + file_usb32 
				logger.info("Running cmd - { " + cmd)
				p4_cmd(cmd)
				os.chdir(dir_old)
				cmd = "p4 delete " + file_usb32_old
				logger.info("Running cmd - { " + cmd)
				p4_cmd(cmd)
			else:
				cmd = "p4 delete " + file_usb32_old
				logger.info("Running cmd - { " + cmd)
				p4_cmd(cmd)
		else:
			delete_files_usb32.append(file_usb32_old + ":" + file_usb32)
			files_usb32.append(file_usb32)
			replaceFile_src(file_usb31,file_usb32+ ".tmp")
			## checking for the presence of file_usb32 if not p4 rename ... 
			cmd = "p4 have " + file_usb32
			result = run_bash(cmd)
			cmd1 = "p4 have " + file_usb32_old
			result1 = run_bash(cmd1)

			if "not on client" in result[0]:
				if not "not on client" in result1[0]:
					cmd = "p4 edit " + file_usb32_old
					logger.info("Running cmd - { " + cmd)
					p4_cmd(cmd)
					cmd = "p4 rename " + file_usb32_old + " " + file_usb32
					logger.info("Running cmd - { " + cmd)
					p4_cmd(cmd)	
			else:
				if file_usb32_old.endswith(".v"):
					cmd = "p4 delete " + file_usb32_old
					logger.info("Running cmd - { " +cmd)
					p4_cmd(cmd)
	print(dict_int)
	return(files_usb32,add_files_usb32,delete_files_usb32,dict_int)	

#############################################################################

def perforce_cmds(file_usb32,bridge_dict,dict_int):
	edit_flag = False
	add_flag = False
	final_cmd = ""
	logger.info("os.path.isfile(file_usb32) is " + str(os.path.isfile(file_usb32)))
	if os.path.isfile(file_usb32):
		## this is the diff command to check the difference with usb32.tmp and usb32 files to submit the changes to the bridge branch... 
		cmd = "diff " + file_usb32 + " " + file_usb32 + ".tmp" + " | grep -v '\$Date:\|\$Revision:\|\$Id:\' | grep -v '\---' | grep -v '^[0-9]'"
		#cmd = "diff " + file_usb32 + " " + file_usb32 + ".tmp" + " | grep -v 'Date\|Revision\|Change\|ID\|\$Id\|Author' | grep -v '\---' | grep -v '^[0-9]'"
		#cmd = "diff " + file_usb32 + " " + file_usb32 + ".tmp" + " | grep -v '\---' | grep -v '^[0-9]' | grep -v '//  '"
		logger.info("Running the cmd - { " + cmd)
		cmd_output = os.popen(cmd).read()
		logger.info('cmd_output ' + cmd_output)
		### if there is some difference we try to edit the file and move forward for the perforce submit ...
		if (cmd_output):
			print("Difference in this file : " + file_usb32)
			cmd = "p4 edit " + file_usb32 + ";"
			print ("Running the command " + cmd )
			p4_cmd(cmd)
			edit_flag = True
			### now replace with copy contents from tmp file to usb32 main file:
			#os.rename(file_usb32 + ".tmp" , file_usb32)
			cmd = "cp " + file_usb32 + ".tmp " + file_usb32
			print ("Running the command " + cmd )
			p4_cmd(cmd)
			#replaceFile(file_usb32 +".tmp" , file_usb32)
			### the bridge dictionary has the contents of the bridge branch and its description attributes ... 
			print(bridge_dict)
			print(dict_int)
			print(file_usb32)
			if file_usb32 in dict_int:
				###print("file_usb32 " + file_usb32)
				print(file_usb32)
				print(bridge_dict[dict_int[file_usb32]])
				cmd = "p4 submit  -d \"" + bridge_dict[dict_int[file_usb32]] + "\" "  + file_usb32
				final_cmd = final_cmd + " " + cmd
				logger.info("Running the cmd - { " + cmd)
				cmd_output = os.popen(cmd).read()
				### gets the submitted changelist for the CRM number to be added for src only! 
				if "src" in file_usb32:
					regex_changelist = r"Submitting change (\d+).*"
					logger.info("cmd_output : " + cmd_output)
					if (cmd_output):
						logger.info("cmd_output = " + cmd_output)
						changelist = re.findall(regex_changelist,cmd_output)[0]
						logger.info("changelist = " + changelist)
						## CRM number from the dict which is from usb31 bridge branch
						crm_number = bridge_dict[dict_int[file_usb32]].split("::")[0]
						logger.info("bridge_dict = " + crm_number)
						## to add the crm number to the changelist ... 
						cmd = "p4 fix -c " + changelist + " " + crm_number
						logger.info("Running the cmd - { " + cmd)
						p4_cmd(cmd)
						cmd = "p4 submit -c " + changelist 
						logger.info("Running the cmd - { " + cmd)
						##### To fix the CRM and submit the file to perforce src with the CRM number
						p4_cmd(cmd)
					else:
						logger.info("Submit src without CRM ; check the cmd" + cmd)  
	else :
		logger.info(file_usb32 + " is a new file so p4 add ")
		cmd = "p4 add " + file_usb32 + ";"
		logger.info(cmd)
		add_flag = True
		p4_cmd(cmd)
		#replaceFile(file_usb32+".tmp" , file_usb32)
		cmd = "mv " + file_usb32 + ".tmp " + file_usb32
		logger.info("Running the cmd - { " + cmd)
		p4_cmd(cmd)
		cmd = "p4 submit  -d \"" + bridge_dict[dict_int[file_usb32]] + "\" "  + file_usb32
		logger.info("Running the cmd - { " + cmd)
		cmd_output = os.popen(cmd).read()
		### gets the submitted changelist for the CRM number to be added for src only! 
		if "src" in file_usb32:
			regex_changelist = r"Submitting change (\d+).*"
			logger.info("cmd_output : " + cmd_output)
			if (cmd_output):
				logger.info("cmd_output = " + cmd_output)
				logger.info(re.findall("p4 submit -c (\d+)",cmd_output))
				changelist = (re.findall("p4 submit -c (\d+)",cmd_output))[0]
				logger.info("changelist = " + changelist)
				## CRM number from the dict which is from usb31 bridge branch
				crm_number = bridge_dict[dict_int[file_usb32]].split("::")[0]
				logger.info("bridge_dict = " + crm_number)
				## to add the crm number to the changelist ... 
				cmd = "p4 fix -c " + changelist + " " + crm_number
				logger.info("Running the cmd - { " + cmd)
				p4_cmd(cmd)
				cmd = "p4 submit -c " + changelist 
				logger.info("Running the cmd - { " + cmd)
				##### To fix the CRM and submit the file to perforce src with the CRM numb
	logger.info("Done with " + file_usb32)

	return(add_flag,edit_flag)

def perforce_src(file_usb32,bridge_dict,bridge_int):
	edit_flag = False
	add_flag = False
	final_cmd = ""
	## get the symlink ...
	logger.info("os.path.isfile(file_usb32) is " + str(os.path.isfile(file_usb32)))
	if os.path.isfile(file_usb32):
		## this is the diff command to check the difference with usb32.tmp and usb32 files to submit the changes to the bridge branch... 
		cmd = "diff " + file_usb32 + " " + file_usb32 + ".tmp" + " | grep -v '\$Date:\|\$Revision:\|\$Id:\' | grep -v '\---' | grep -v '^[0-9]'"
		logger.info("Running the cmd - { " + cmd)
		print("Running the cmd - { " + cmd)
		cmd_output = os.popen(cmd).read()
		#logger.info('cmd_output ' + cmd_output)
		### if there is some difference we try to edit the file and move forward for the perforce submit ...
		if (cmd_output):
			print("Difference in this file : " + file_usb32)
			cmd = "p4 edit " + file_usb32 + ";"
			#print ("Running the command " + cmd )
			p4_cmd(cmd)
			edit_flag = True
			### now replace with copy contents from tmp file to usb32 main file:
			cmd = "mv -f " + file_usb32 + ".tmp " + file_usb32
			logger.info("Running the cmd - { " + cmd)
			result = run_bash(cmd)
			### the bridge dictionary has the contents of the bridge branch and its description attributes ... 
			if file_usb32 in bridge_int:
				logger.info("File for file usb32 = " + file_usb32)
				###print("file_usb32 " + file_usb32)
				cmd = "p4 submit  -d \"" + bridge_dict[bridge_int[file_usb32]] + "\" "  + file_usb32
				final_cmd = final_cmd + " " + cmd
				logger.info("Running the cmd - { " + cmd)
				cmd_output = os.popen(cmd).read()
				### gets the submitted changelist for the CRM number to be added for src only! 
				if "src" in file_usb32:
					regex_changelist = r"Submitting change (\d+).*"
					logger.info("cmd_output : " + cmd_output)
					if (cmd_output):
						logger.info("cmd_output = " + cmd_output)
						changelist = re.findall(regex_changelist,cmd_output)[0]
						logger.info("changelist = " + changelist)
						## CRM number from the dict which is from usb31 bridge branch
						crm_number = bridge_dict[bridge_int[file_usb32]].split("::")[0]
						logger.info("bridge_dict = " + crm_number)
						## to add the crm number to the changelist ... 
						cmd = "p4 fix -c " + changelist + " " + crm_number
						logger.info("Running the cmd - { " + cmd)
						p4_cmd(cmd)
						cmd = "p4 submit -c " + changelist 
						logger.info("Running the cmd - { " + cmd)
						##### To fix the CRM and submit the file to perforce src with the CRM number
						p4_cmd(cmd)
					else:
						logger.info("Submit src without CRM ; check the cmd" + cmd) 
	else :
		logger.info(file_usb32 + " is a new file so p4 add ")
		cmd = "p4 add " + file_usb32
		logger.info("Running the cmd - { " + cmd)
		p4_cmd(cmd)
		add_flag = True
		cmd = "mv -f " + file_usb32 + ".tmp " + file_usb32
		logger.info("Running the cmd - { " + cmd)
		result = run_bash(cmd)
		#replaceFile(file_usb32+".tmp" , file_usb32)
		if file_usb32 in bridge_int:
			cmd = "p4 submit  -d \"" + bridge_dict[bridge_int[file_usb32]] + "\" "  + file_usb32
		else:
			cmd = "p4 submit  -d \"" + bridge_dict[bridge_int[file_usb32]] + "\" "  + file_usb32
		logger.info("Running the cmd - { " + cmd)
		p4_cmd(cmd)
		cmd_output = os.popen(cmd).read()
		### gets the submitted changelist for the CRM number to be added for src only! 
		if "src" in file_usb32:
			regex_changelist = r"Submitting change (\d+).*"
			logger.info("cmd_output : " + cmd_output)
			if (cmd_output):
				logger.info("cmd_output = " + cmd_output)
				logger.info(re.findall("p4 submit -c (\d+)",cmd_output))
				changelist = (re.findall("p4 submit -c (\d+)",cmd_output))[0]
				logger.info("changelist = " + changelist)
				## CRM number from the dict which is from usb31 bridge branch
				crm_number = bridge_dict[bridge_int[file_usb32]].split("::")[0]
				logger.info("bridge_dict = " + crm_number)
				## to add the crm number to the changelist ... 
				cmd = "p4 fix -c " + changelist + " " + crm_number
				logger.info("Running the cmd - { " + cmd)
				p4_cmd(cmd)
				cmd = "p4 submit -c " + changelist 
				logger.info("Running the cmd - { " + cmd)
				##### To fix the CRM and submit the file to perforce src with the CRM number
				p4_cmd(cmd) 
	return(add_flag,edit_flag)

def deletefile(file_usb32,bridge_dict,bridge_int):
	old_file = file_usb32.split(":")[0]
	new_file = file_usb32.split(":")[1]
	logger.info("File to be deleted is " + old_file)
	cmd = "p4 delete " + old_file + ";"
	logger.info(cmd)
	delete_flag = True
	p4_cmd(cmd)
	cmd = "p4 submit  -d \"" + bridge_dict[bridge_int[new_file]] + "\" "  + new_file
	logger.info("Running the cmd - { " + cmd)
	'''p4_cmd(cmd)
	cmd_output = os.popen(cmd).read()
	### gets the submitted changelist for the CRM number to be added for src only! 
	if "src" in file_usb32:
		regex_changelist = r"Submitting change (\d+).*"
		logger.info("cmd_output : " + cmd_output)
		if (cmd_output):
			logger.info("cmd_output = " + cmd_output)
			logger.info(re.findall("p4 submit -c (\d+)",cmd_output))
			changelist = (re.findall("p4 submit -c (\d+)",cmd_output))[0]
			logger.info("changelist = " + changelist)
			## CRM number from the dict which is from usb31 bridge branch
			crm_number = bridge_dict[file_usb32].split("::")[0]
			logger.info("bridge_dict = " + crm_number)
			## to add the crm number to the changelist ... 
			cmd = "p4 fix -c " + changelist + " " + crm_number
			logger.info("Running the cmd - { " + cmd)
			p4_cmd(cmd)
			cmd = "p4 submit -c " + changelist 
			logger.info("Running the cmd - { " + cmd)
			##### To fix the CRM and submit the file to perforce src with the CRM number
			p4_cmd(cmd) '''

def deleteTmpfiles(tmp_list):
	for file in tmp_list:
		logger.info(file)

def src_main(usb31b_src):
	(files_usb31,bridge_dict) = processBridge(usb31b_src)
	usb32_files,add_usb32,delete_usb32,bridge_int = getusb32_src(files_usb31)
	readlst_file1(bridge_int,bridge_dict)
	#readlst_file(bridge_int) 
	for file_usb32 in usb32_files:
		logger.info("File_usb32 " + file_usb32)
		add,edit = perforce_src(file_usb32,bridge_dict,bridge_int)
	#logger.info("deleting the .v files and adding .sv and .svh based on the content")
	#for file_usb32 in delete_usb32:
		#deletefile(file_usb32,bridge_dict,bridge_int)

def pkg_main(usb31b_pkg,pkg):
	CRV_USB3_BASE_DIR = "/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32"
	os.chdir(usb31b_pkg)
	logger.info(pkg)
	(files_usb31,bridge_dict) = processBridge(usb31b_pkg)
	usb32_files,dict_int = processDiff(pkg)
	for file_usb32 in usb32_files:
		logger.info(file_usb32)
		add,edit = perforce_cmds(file_usb32,bridge_dict,dict_int)

def other_main(usb31b_other):
	(files_usb31,bridge_dict) = processBridge(usb31b_other)
	usb32_files,dict_int = processDiff(files_usb31)
	for file_usb32 in usb32_files:
		logger.info(file_usb32)
		add,edit = perforce_cmds(file_usb32,bridge_dict,dict_int)

def perforce_setup():
	P4CONFIG = "/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32/.p4config"
	CRV_USB3_BASE_DIR = "/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32"
	os.chdir(CRV_USB3_BASE_DIR)
	### setup the p4config 
	cmd = "export P4CONFIG="+ CRV_USB3_BASE_DIR + "/.p4config;"
	p4_cmd(cmd)

	## deleting the symlinks ... 
	cmd = "find . -type l -exec rm {} \;" 
	logger.info(cmd)
	p4_cmd(cmd)
	### delete tmp files ... 
	cmd = "find . -name '*tmp'| xargs rm"
	logger.info(cmd)
	p4_cmd(cmd)

def main(flag):
	CRV_USB3_BASE_DIR = "/slowfs/us01dwt2p226/usb3_rgsn_clients/harini/usb32"
	usb32_dir = CRV_USB3_BASE_DIR + "/dev/DWC_usb32/"
	usb31b_dir = CRV_USB3_BASE_DIR + "/usb31_br_usb32/DWC_usb31/"
	pkg_files = ['pkg/pkg_script/assemblyintent.tcl','pkg/pkg_script/DWC_usb31.tcl','pkg/pkg_script/DWC_usb31_backdoor.tcl','pkg/pkg_script/memoryMap.tcl','pkg/pkg_script/DWC_usb31.elab.tcl']
	perforce_setup()
	if flag == "pkg":
		pkg = []
		for line in pkg_files:
			cmd = "p4 sync -f " + CRV_USB3_BASE_DIR + "/usb31_br_usb32/DWC_usb31/" + line
			p4_cmd(cmd)
			pkg.append(CRV_USB3_BASE_DIR + "/usb31_br_usb32/DWC_usb31/" + line)
		pkg_main(usb31b_dir + "pkg",pkg)
	if flag == "src":
		cmd = "cd " + usb31b_dir + "src; " + " p4 sync -q -f ...;"
		logger.info("Running .. " + cmd)
		#p4_cmd(cmd)
		src_main(usb31b_dir+"src")
	if flag == "other":
		cmd = "cd " + usb31b_dir + "iipregr" 
		logger.info(cmd)
		other_main(usb31b_dir + "iipregr")
	
############MAIN STARTS HERE ....  
if __name__ == "__main__":
	'''logging.basicConfig(format = '%(asctime)s %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p',filename='logfile',
                    level=logging.INFO) '''
	logger = logging.getLogger('root')
	fmt="%(funcName)s():%(lineno)i: %(message)s %(levelname)s"
	logging.basicConfig(level=logging.INFO, format=fmt,filename="logfile")
	logger.info("hello")
	if sys.argv[1]:
		main(sys.argv[1])
	else:
		sys.exit("Specify the pkg or src to be translated ..")
