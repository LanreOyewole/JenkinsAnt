#===================================================================================
#TITLE           :AWWLSAdminstration.py
#DESCRIPTION     :This WebLogic script is built to administer WebLogic server 
#				  activities such as:
#					- SOA Deployments
#					- Service Bus Deployments
#					- BAM Deployments
#					- Managing Data Sources
#					- Managing JMS Resources
#					- Managing Security Realm
#AUTHOR		     : Jawad Hafeez
#DATE            :03/06/2016
#VERSION         :0.1
#USAGE		     :./AWWLSAdminstration.sh
#NOTES           :
#===================================================================================
# 			-----------C H A N G E - H I S T O R Y-----------
#===================================================================================
# DATE				UPDATED BY				COMMENTS						VERSION
#===================================================================================
# 03/06/2016		HAFEEZJ					Initial Build						0.1
#===================================================================================
import sys
from java.util import Properties
from java.io import FileInputStream
from java.io import File
from java.io import FileOutputStream
from java import io
from java.lang import Exception
from java.lang import Throwable
from java.util import Collections
import datetime
import time
import os
import commands
import wlstModule
import traceback
from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
from java.io import FileInputStream
#from com.bea.wli.sb.util import Refs
#from com.bea.wli.config import Ref
#from com.bea.wli.config.customization import Customization
#from com.bea.wli.sb.management.importexport import ALSBImportOperation
#from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
import re
import fileinput
#from oracle.fabric.blocks.folder import Folder
#from oracle.fabric.management.folder import FolderManager
from javax.management import MBeanException 
from java.lang.reflect import InvocationTargetException
#import getpass
#import msvcrt
import tempfile
from weblogic.descriptor import BeanAlreadyExistsException
#***************************************************
# Declaration Section
#***************************************************
# CONTANT FOR PROPERTIES FILE NAME
ConfigFileName = 'config.properties'


# CONSTANTS FOR COLOR CODES
PROMPT_COLOR_CODE = '\033[1;35m' #PURPLE
OPTION_COLOR_CODE = '\033[1;36m' #CYAN
STATUS_PASS_COLOR_CODE = '\033[1;32m' #GREEN
STATUS_FAIL_COLOR_CODE = '\033[1;31m' #RED    
INFORMATION_COLOR_CODE = '\033[1;33m' #YELLOW  
END_COLOR_CODE = '\033[1;m'

#***************************************************
# Clearing terminal
#*************************************************** 
os.system('clear')

#***************************************************
# Getting the environment for deployment
#***************************************************
HostNameOut=os.environ['HOSTNAME']
MachineName=HostNameOut[0:HostNameOut.find(".")]

#***************************************************
# Temp file for WLST output
#***************************************************
wlstOut = tempfile.mktemp(suffix="_wlst.txt")


#***************************************************
# Start Transactions
#***************************************************
def startTransaction():
	edit()
	startEdit()
	
#***************************************************
# End Transactions
#***************************************************
def endTransaction():
	save()
	activate(block="true")
	
#***************************************************
# Progress bar.  
#***************************************************
def progressBar(starttype,endcolor,endtype,time):
	print INFORMATION_COLOR_CODE+starttype+' [          ]'+END_COLOR_CODE,
	print '\b'*12,
	steps = 300/10
	for i in range(300):
		#time.sleep(10)
		Thread.sleep(time)
		if i%steps == 0:
			print '\b.',
	print '\b'+INFORMATION_COLOR_CODE+']'+endcolor+' '+endtype+'.'+END_COLOR_CODE	

#***************************************************
# Create JMS Module
#***************************************************
def createJMSModule(moduleName):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating JMS Module: '+moduleName+END_COLOR_CODE
	cd('/')
	cmo.createJMSSystemResource(moduleName)
	cd('/JMSSystemResources/'+moduleName)
	progressBar('Creating',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)	

#***************************************************
# Target JMS Module
#***************************************************
def targetJMSModule(moduleName, targetName):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Targeting JMS File Store to: '+targetName+END_COLOR_CODE
	#startRedirect()
	set('Targets',jarray.array([ObjectName('com.bea:Name='+targetName+',Type=Server')], ObjectName))	
	#stopRedirect()
	progressBar('Trageting',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)	
	
print '======================================================================'
print INFORMATION_COLOR_CODE+'   WELCOME TO THE WEBLOGIC ADMINISTRATION SCRIPT 	 '+END_COLOR_CODE
print '======================================================================'
ConfigFilePath = '/WorkArea/JenkinsAnt'
WLSPassword = 'welcome1'
ConfigProperties = Properties()
ConfigSeg={}
#Lanre
print '===============Config File: ' + ConfigFilePath+'/'+ConfigFileName + ' ... ' + MachineName.upper() + '============='
ConfigProperties.load(FileInputStream(File(ConfigFilePath+'/'+ConfigFileName)))
WLSUsername=ConfigProperties.getProperty(MachineName.upper()+'.ADMIN.USER_NAME')
#Lanre
print '===============WebLogic Username: ' + WLSUsername + '============='
WLSHost=ConfigProperties.getProperty(MachineName.upper()+'.ADMIN.HOST')
WLSPort=ConfigProperties.getProperty(MachineName.upper()+'.ADMIN.PORT')
WLSUrl='t3://' + WLSHost + ':' + WLSPort
connect(WLSUsername, WLSPassword, WLSUrl)

#! Connect to WebLogic Server
#connectWLS(WLSUsername, WLSPassword, WLSUrl)

startTransaction()
if (UserOperation_.upper() == 'CREATEJMSMODULE'):
	createJMSModule(moduleName_)
elif (UserOperation_.upper() == 'TARGETJMSMODULE'):
	targetJMSModule(moduleName_, targetName_)

endTransaction()

