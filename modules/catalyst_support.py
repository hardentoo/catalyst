import sys,string,os

config_file_values=["storedir","sharedir","distdir","portdir"]

class CatalystError(Exception):
	def __init__(self, message):
		if message:
			print "catalyst: "+message
def die(msg=None):
	warn(msg)
	sys.exit(1)

def warn(msg):
	print "catalyst: "+msg

def ismount(path):
	"enhanced to handle bind mounts"
	if os.path.ismount(path):
		return 1
	a=open("/proc/mounts","r")
	mylines=a.readlines()
	a.close()
	for line in mylines:
		mysplit=line.split()
		if path == mysplit[1]:
			return 1
	return 0

def arg_parse(mydict,remaining={}):
	global config_file_values
	for x in sys.argv[1:]:
		foo=string.split(x,"=")
		if len(foo)!=2:
			raise CatalystError, "Invalid arg syntax: "+x
		remaining[foo[0]]=foo[1]
	if not remaining.has_key("target"):
		raise CatalystError, "Required value \"target\" not specified."
	mydict["target"]=remaining["target"]
	for x in config_file_values:
		if not mydict.has_key(x):
			raise CatalystError, "Required config file value \""+x+"\" not found."

		
def addl_arg_parse(myspec,addlargs,requiredspec,validspec):
	"helper function to help targets parse additional arguments"
	global config_file_values
	for x in addlargs.keys():
		if x not in validspec and x not in config_file_values:
			raise CatalystError, "Argument \""+x+"\" not recognized."
		else:
			myspec[x]=addlargs[x]
	for x in requiredspec:
		if not myspec.has_key(x):
			raise CatalystError, "Required argument \""+x+"\" not specified."
	
def spec_dump(myspec):
	for x in myspec.keys():
		print x+": "+repr(myspec[x])


