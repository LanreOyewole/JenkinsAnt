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
# Main Screen
#***************************************************
def mainScreen():
	#***************************************************
	# Get User Operation
	#***************************************************
	print '======================================================================'
	print PROMPT_COLOR_CODE+'1: What do you want to do?:'+END_COLOR_CODE
	print '======================================================================'
	print OPTION_COLOR_CODE+'A -> Manage WebLogic Configurations'+END_COLOR_CODE
	#print OPTION_COLOR_CODE+'B -> Manage Deployments'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'X -> Exit'+END_COLOR_CODE
	print '======================================================================'
	mainScreenInput = raw_input(':')
	return mainScreenInput

#***************************************************
# WebLogic Configuration Operations
#***************************************************
def wlsOperation():	
	#***************************************************
	# Get User Operation
	#***************************************************
	print '======================================================================'
	print PROMPT_COLOR_CODE+'2: What do you want to do now?:'+END_COLOR_CODE
	print '======================================================================'
	print OPTION_COLOR_CODE+'A -> Manage JMS Resource'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'B -> Manage DataSource Resource'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'C -> Generate Thread Dump Report'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'X -> Exit'+END_COLOR_CODE
	print '======================================================================'
	wlsScreenInput = raw_input(':')
	return wlsScreenInput

'''
def jmsOperation():	
	#***************************************************
	# Get User Operation
	#***************************************************
	print '======================================================================'
	print PROMPT_COLOR_CODE+'3: Please choose your option:'+END_COLOR_CODE
	print '======================================================================'
	print OPTION_COLOR_CODE+'A -> Create JMS File Store'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'B -> Create JMS Server'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'C -> Create JMS Module`'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'D -> Create JMS Connection Factory'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'E -> Create JMS Queue'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'F -> Create JMS UDQ'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'G -> Create JMS Foreign Server'+END_COLOR_CODE
	print OPTION_COLOR_CODE+'X -> Exit'+END_COLOR_CODE
	print '======================================================================'
	wlsScreenInput = raw_input(':')
	return wlsScreenInput
'''	
#***************************************************
# Get absolute path for the properties file
#***************************************************
def getAbsPath():
	#***************************************************
	# Getting the configuration.property file path
	#***************************************************	
	print PROMPT_COLOR_CODE+'1: Please enter the absolute path of properties file (without the file name):'+END_COLOR_CODE
	print '======================================================================'
	#Lanre
	##result = raw_input (':') or "/WorkArea/JenkinsAnt/"
	result = "/WorkArea/JenkinsAnt"
	print '======================================================================'
	return result	
	
#***************************************************
# Get WebLogic password
#***************************************************
#def getWLSPassword(prompt=':', stream=None):
def getWLSPassword():
	print PROMPT_COLOR_CODE+'2: Please enter WebLogic Server password:'+END_COLOR_CODE
	print '======================================================================'
	#for c in prompt:
    #    msvcrt.putch(c)
	#pw = ""
	#while 1:
	#	c = msvcrt.getch()
	#	if c == '\r' or c == '\n':
	#		break
	#	if c == '\003':
	#		raise KeyboardInterrupt
	#	if c == '\b':
	#		pw = pw[:-1]
    #       msvcrt.putch('\b')
	#	else:
	#		pw = pw + c
    #       msvcrt.putch("*")
    #msvcrt.putch('\r')
    #msvcrt.putch('\n')
    #return pw
	#os.system("stty -echo")	
	#Lanre
	##result = raw_input (':')#getpass.getpass(':')	
	result = 'welcome1'	
	#os.system("stty echo")
	#print "\n"
	return result

#***************************************************
# Connect to WebLogic Server
#***************************************************
def connectWLS(WLSusername, WLSpassword, WLSurl):
	try:
		connect(WLSusername, WLSpassword, WLSurl)
		print STATUS_PASS_COLOR_CODE+'[STATUS]: Server Connection Status: Successful'+END_COLOR_CODE		
	except:
		print STATUS_FAIL_COLOR_CODE+'[STATUS]: Unable to connect to the WebLogic server'+END_COLOR_CODE
		apply(traceback.print_exception, sys.exc_info())	
		exit()

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
# Exit from the script
#***************************************************
def scriptExit():
	print PROMPT_COLOR_CODE+'Thanks for using the script.'+END_COLOR_CODE
	exit()	
	
#***************************************************
# Create JMS File Store
#***************************************************
def createJMSFileStore(storeName):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating JMS File Store: '+storeName+END_COLOR_CODE
	cd('/')
	cmo.createFileStore(storeName)
	progressBar('Creating',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)	

#***************************************************
# Target JMS File Store
#***************************************************
def targetJMSFileStore(storeName, targetName):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Targeting JMS File Store to: '+targetName+END_COLOR_CODE
	cd('/FileStores/'+storeName)
	cmo.setDirectory(storeName)
	set('Targets',jarray.array([ObjectName('com.bea:Name='+targetName+',Type=Server')], ObjectName))
	progressBar('Trageting',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)		

#***************************************************
# Create JMS Server
#***************************************************
def createJMSServer(serverName, persistentStore):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating JMS Server: '+serverName+END_COLOR_CODE
	cd('/')
	cmo.createJMSServer(serverName)
	cd('/JMSServers/'+serverName)
	if(persistentStore != None):
		print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting the Persistent Store: '+persistentStore+END_COLOR_CODE
		cmo.setPersistentStore(getMBean('/FileStores/'+persistentStore))
	else:
		cmo.setPersistentStore(None)
	cmo.setTemporaryTemplateResource(None)
	cmo.setTemporaryTemplateName(None)
	progressBar('Creating',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)		
	
#***************************************************
# Target JMS Server
#***************************************************
def targetJMSServer(serverName, targetName):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Targeting JMS Server to: '+targetName+END_COLOR_CODE
	set('Targets',jarray.array([ObjectName('com.bea:Name='+targetName+',Type=Server')], ObjectName))
	progressBar('Trageting',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)
	
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
	
#***************************************************
# Add Sub Deployment to a JMS Module
#***************************************************
def creatJMSSubDeployment(moduleName, subDeplyment, serverName):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating JMS Sub Deployment: '+subDeplyment+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName)
	cmo.createSubDeployment(subDeplyment)
	progressBar('Creating',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)		
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Trageting Sub Deployment to: '+serverName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/SubDeployments/'+subDeplyment)
	set('Targets',jarray.array([ObjectName('com.bea:Name='+serverName+',Type=JMSServer')], ObjectName))		

#***************************************************
# Create JMS Connection Factory
#***************************************************
def creatJMSConnFactory(moduleName, connFactoryName, subDeplyment, serverName):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating JMS Connection Factory: '+connFactoryName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName)
	cmo.createConnectionFactory(connFactoryName)
	progressBar('Creating',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)		
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting JNDI to: '+'jms/cf/'+connFactoryName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ConnectionFactories/'+connFactoryName)
	cmo.setJNDIName('jms/'+connFactoryName+'/cf')
	
	#print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting JNDI to: '+'jms/cf/'+connFactoryName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ConnectionFactories/'+connFactoryName+'/SecurityParams/'+connFactoryName)
	cmo.setAttachJMSXUserId(false)
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ConnectionFactories/'+connFactoryName+'/ClientParams/'+connFactoryName)
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting Client Policy to: Restrcited'+END_COLOR_CODE
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting Subscription Sharing Policy to: Exclusive'+END_COLOR_CODE
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting Maximum Messages to: 10'+END_COLOR_CODE	
	cmo.setClientIdPolicy('Restricted')
	cmo.setSubscriptionSharingPolicy('Exclusive')
	cmo.setMessagesMaximum(10)		
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ConnectionFactories/'+connFactoryName+'/TransactionParams/'+connFactoryName)
	cmo.setXAConnectionFactoryEnabled(true)
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting the traget to: '+serverName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/SubDeployments/'+subDeplyment)
	set('Targets',jarray.array([ObjectName('com.bea:Name='+serverName+',Type=JMSServer')], ObjectName))
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Attaching Sub Deployment: '+subDeplyment+serverName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ConnectionFactories/'+connFactoryName)
	cmo.setSubDeploymentName(subDeplyment)		
	
#***************************************************
# Create JMS Queue
#***************************************************
def createJMSQueue(moduleName, queueName, subDeplyment, serverName):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating JMS Queue: '+queueName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName)
	cmo.createQueue(queueName)
	progressBar('Creating',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)	
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting JNDI to: '+'jms/'+queueName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/Queues/'+queueName)
	cmo.setJNDIName('jms/'+queueName+'/queue')
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting Sub Deployment to: '+subDeplyment+END_COLOR_CODE
	cmo.setSubDeploymentName(subDeplyment)	

#***************************************************
# Create JMS Uniform Distributed Queue
#***************************************************
def createJMSUDQueue(moduleName, queueName, subDeplyment, serverName):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating Uniform Distributed Queue: '+queueName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName)
	cmo.createUniformDistributedQueue(queueName)
	progressBar('Creating',STATUS_PASS_COLOR_CODE,'Completed',25)
	Thread.sleep(5)	
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting JNDI to: '+'jms/'+queueName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/UniformDistributedQueues/'+queueName)
	cmo.setJNDIName('jms/'+queueName+'/queue')
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting Sub Deployment to: '+subDeplyment+END_COLOR_CODE
	cmo.setSubDeploymentName(subDeplyment)	
	
#***************************************************
# Primary Target JMS Queue
#***************************************************
def TargetJMSQueue(moduleName, subDeplyment, serverName):	
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Setting Target to: '+serverName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/SubDeployments/'+subDeplyment)
	set('Targets',jarray.array([ObjectName('com.bea:Name='+serverName+',Type=JMSServer')], ObjectName))
	
#***************************************************
# Seconday Target JMS Queue
#***************************************************
def secondaryTargetJMSQueue(moduleName, targetName):	
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Also targeting JMS Queue to: '+targetName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName)
	set('Targets',jarray.array([ObjectName('com.bea:Name='+targetName+',Type=Server')], ObjectName))

#***************************************************
# JMS Uniform Distributed Queue
#***************************************************
#def uniformDistributedJMSQueue(moduleName, queueName, subDeplyment, serverName):
#	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName)
#	try:
#		cmo.createUniformDistributedQueue(queueName)
#		cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/UniformDistributedQueues/'+queueName)
#		cmo.setJNDIName('jms/udq/'+queueName)
#
#		cd('/JMSSystemResources/'+moduleName+'/SubDeployments/'+subDeplyment)
#		set('Targets',jarray.array([ObjectName('com.bea:Name='+serverName+',Type=JMSServer')], ObjectName))
#
#		cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/UniformDistributedQueues/'+queueName)
#		cmo.setSubDeploymentName(subDeplyment)			
#	except BeanAlreadyExistsException:
#		print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS UDQ already exists'+END_COLOR_CODE	

#***************************************************
# Create JMS Foreign Server
#***************************************************
def createJMSForeignServer(foreignServerName, moduleName, serverName, subDeplyment):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating JMS Foreign Server: '+foreignServerName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName)
	cmo.createForeignServer(foreignServerName)
	cd('/JMSSystemResources/'+moduleName+'/SubDeployments/'+subDeplyment)
	set('Targets',jarray.array([ObjectName('com.bea:Name='+serverName+',Type=JMSServer')], ObjectName))
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ForeignServers/'+foreignServerName)
	cmo.setSubDeploymentName(subDeplyment)	

#***************************************************
# Create JMS Foreign Destinations
#***************************************************	
def createJMSForeignServerDestination(foreignDest, moduleName, foreignServerName, localjndi, remotejndi):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating Foreign Destination: '+foreignDest+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ForeignServers/'+foreignServerName)
	cmo.createForeignDestination(foreignDest)
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ForeignServers/'+foreignServerName+'/ForeignDestinations/'+foreignDest)
	cmo.setLocalJNDIName(localjndi)
	cmo.setRemoteJNDIName(remotejndi)	
		
def createJMSForeignConnectionFactory(moduleName, foreignServerName, connFactoryName, localjndi, remotejndi):
	print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating Connection Factory for Foreign Destinations: '+connFactoryName+END_COLOR_CODE
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ForeignServers/'+foreignServerName)
	cmo.createForeignConnectionFactory(connFactoryName)
	cd('/JMSSystemResources/'+moduleName+'/JMSResource/'+moduleName+'/ForeignServers/'+foreignServerName+'/ForeignConnectionFactories/'+connFactoryName)
	cmo.setLocalJNDIName(localjndi)
	cmo.setRemoteJNDIName(remotejndi)		

#***************************************************
# Utility function to print the list of operations
#***************************************************
def printOpMap(map):
    set = map.entrySet()
    for entry in set:
        op = entry.getValue()
        print op.getOperation(),
        ref = entry.getKey()
        print ref
    print

#***************************************************
# Utility function to print the diagnostics
#***************************************************
def printDiagMap(map):
    set = map.entrySet()
    for entry in set:
        diag = entry.getValue().toString()
        print diag
    print
	
#***************************************************
# Create DataSource
#***************************************************
def createDataSource(dataSourceName, dataSourceJNDIName, dataSourceJDBCUrl, dataSourceDriverClassName, dataSourceTestQuery, dataSourceUserName, dataSourceDBName, dataSourceGlobalTransactionProtocol, dataSourceMaxCapacity, dataSourceCapacityIncrement, dataSourceStmtCacheType, dataSourceStmtCacheSize, dataSourceInitialCapacity, dataSourceWaiters, dataSourceShrinkFreq, dataSourceConnectionReverseTimeout, dataSourceInactiveConnectionReverseTimeout, dataSourceStmtTimeout, dataSourceConnectionRetryFreq, dataSourceTimeToTrustIdlePool, dataSourceTestFreq, dataSourceTestTableName, dataSourceLoginDelaySeconds, dataSourceTragets):
	edit()
	startEdit()
	cd('/JDBCSystemResources/')
	listDS=cmo.getJDBCSystemResources()
	for j in listDS:
		if (dataSourceName == j.getName()):
			print STATUS_FAIL_COLOR_CODE+'[STATUS]: DataSource '+dataSourceName+' Creation: '+'Failed'+END_COLOR_CODE
			print INFORMATION_COLOR_CODE+'FAILURE: Reason: DataSource specified already exist. You can not create duplicate DataSource. Please use a different name.'+END_COLOR_CODE 
			DSDuplicate = -1
		else:
			DSDuplicate = 1
	if (DSDuplicate == 1):
		try:
			cd('/')
			print '======================================================================'
			print PROMPT_COLOR_CODE+'6: Please enter JDBC password for '+'\''+dataSourceName+'\''+' DataSource'+END_COLOR_CODE
			print '======================================================================'
			dataSourceJDBCPassword=raw_input(':')
			print '======================================================================'
			print INFORMATION_COLOR_CODE+'[INFORMATION]: Creating DataSource: '+dataSourceName+END_COLOR_CODE	
			#***************************************************
			# Setting DataSource Name
			#***************************************************					
			cmo.createJDBCSystemResource(dataSourceName)
			cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName)
			cmo.setName(dataSourceName)
			#***************************************************
			# Setting DataSource JNDI Name
			#***************************************************
			cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDataSourceParams/' + dataSourceName )
			set('JNDINames',jarray.array([String(dataSourceJNDIName)], String))
			cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDriverParams/' + dataSourceName )			
			#***************************************************
			# Setting DataSource JDBC URL
			#***************************************************					
			cmo.setUrl(dataSourceJDBCUrl)
			print INFORMATION_COLOR_CODE+'JDBC URL is:'+dataSourceJDBCUrl+END_COLOR_CODE
			#scriptExit()		
			#***************************************************
			# Setting DataSource Driver Class Name
			#***************************************************					
			cmo.setDriverName(dataSourceDriverClassName)			
			#***************************************************
			# Setting DataSource Password
			#***************************************************					
			cmo.setPassword(dataSourceJDBCPassword)
			#***************************************************
			# Setting DataSource Test Query
			#***************************************************
			cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCConnectionPoolParams/' + dataSourceName )
			cmo.setTestTableName(dataSourceTestQuery)
			#***************************************************
			# Setting DataSource Username
			#***************************************************					
			cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDriverParams/' + dataSourceName + '/Properties/' + dataSourceName )
			cmo.createProperty('user')
			cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDriverParams/' + dataSourceName + '/Properties/' + dataSourceName + '/Properties/user')
			cmo.setValue(dataSourceUserName)
			#***************************************************
			# Setting DataSource Database Name
			#***************************************************
			cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDriverParams/' + dataSourceName + '/Properties/' + dataSourceName )
			cmo.createProperty('databaseName')
			cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDriverParams/' + dataSourceName + '/Properties/' + dataSourceName + '/Properties/databaseName')
			cmo.setValue(dataSourceDBName)
			cd('/JDBCSystemResources/' + dataSourceName + '/JDBCResource/' + dataSourceName + '/JDBCDataSourceParams/' + dataSourceName )
			cmo.setGlobalTransactionsProtocol(dataSourceGlobalTransactionProtocol)
			cd('/JDBCSystemResources/'+dataSourceName+'/JDBCResource/'+dataSourceName+'/JDBCConnectionPoolParams/'+dataSourceName)
			cmo.setMaxCapacity(int(dataSourceMaxCapacity))
			cmo.setCapacityIncrement(int(dataSourceCapacityIncrement))
			cmo.setStatementCacheType(dataSourceStmtCacheType)
			cmo.setStatementCacheSize(int(dataSourceStmtCacheSize))
			cmo.setInitialCapacity(int(dataSourceInitialCapacity))
			cmo.setHighestNumWaiters(int(dataSourceWaiters))
			#cmo.setWrapTypes(DSWraps)
			cmo.setShrinkFrequencySeconds(int(dataSourceShrinkFreq))
			#cmo.setIgnoreInUseConnectionsEnabled(DSIgnoreConnectionsEnabled)
			cmo.setConnectionReserveTimeoutSeconds(int(dataSourceConnectionReverseTimeout))
			cmo.setInactiveConnectionTimeoutSeconds(int(dataSourceInactiveConnectionReverseTimeout))
			#cmo.setPinnedToThread(DSPinnedToThread)
			cmo.setStatementTimeout(int(dataSourceStmtTimeout))
			#cmo.setRemoveInfectedConnections(DSRemoveInfectedStmts)
			cmo.setConnectionCreationRetryFrequencySeconds(int(dataSourceConnectionRetryFreq))
			cmo.setSecondsToTrustAnIdlePoolConnection(int(dataSourceTimeToTrustIdlePool))
			#cmo.setTestConnectionsOnReserve(DSTestConnectionsReserve)
			cmo.setTestFrequencySeconds(int(dataSourceTestFreq))
			cmo.setTestTableName(dataSourceTestTableName)
			cmo.setLoginDelaySeconds(int(dataSourceLoginDelaySeconds))
			#***************************************************
			# Setting DataSource Target
			#***************************************************			
			#cd('/SystemResources/' + dataSourceName )
			cd('/JDBCSystemResources/' + dataSourceName )
			listLen = int(len(dataSourceTragets)) - 1
			startIterate = 1
			#while  (startIterate <= listLen):
			prepareTargets = None
			for aTarget in dataSourceTragets:
			#	if(int(len(dataSourceTragets)) > 1):
					#prepareTargets = prepareTargets + ',' +
				print INFORMATION_COLOR_CODE+'Number of targets :'+str(len(dataSourceTragets))+END_COLOR_CODE
				print INFORMATION_COLOR_CODE+'Target :'+aTarget+END_COLOR_CODE
				
				#startIterate = startIterate + 1
				#	conStr = 'ObjectName'
				#SystemResources.addTarget(getMBean(aTarget))
				#cmo.addTarget(getTarget('/Servers/'+aTarget))
				set('Targets',jarray.array([ObjectName('com.bea:Name=' + aTarget+ ',Type=Server')], ObjectName))
			#set('Targets',jarray.array(dataSourceTragets,ObjectName))
			#***************************************************
			# Progress Bar
			#***************************************************					
			progressBar('Creating',STATUS_PASS_COLOR_CODE,'Completed',25)
			Thread.sleep(5)					
			print STATUS_PASS_COLOR_CODE+'[STATUS]: DataSource '+dataSourceName+' Creation: '+'Successful'+END_COLOR_CODE 
		except:	
			apply(traceback.print_exception, sys.exc_info())
			print STATUS_FAIL_COLOR_CODE+'[STATUS]: DataSource '+dataSourceName+' Creation: '+'Failed'+END_COLOR_CODE
			print INFORMATION_COLOR_CODE+'FAILURE REASON(S):'+END_COLOR_CODE 
			print INFORMATION_COLOR_CODE+'                  -> Please check the values supplied in your .properties file.'+END_COLOR_CODE
	save()
	activate()
#***************************************************
# Generate Thread-dump report
#***************************************************
def generateThreadDumpReport():
	ECODE='\n \033[0m' # ending of color code
	serverRuntime()	
	cd('/ThreadPoolRuntime/ThreadPoolRuntime/')
	compReq = cmo.getCompletedRequestCount()
	status = cmo.getHealthState()
	hoggingThreads = cmo.getHoggingThreadCount()
	totalThreads = cmo.getExecuteThreadTotalCount()
	idleThrds = cmo.getExecuteThreadIdleCount()
	pending = cmo.getPendingUserRequestCount()
	qLen = cmo.getQueueLength()
	thruput = cmo.getThroughput()
	if idleThrds == 0:
		pstr='\033[1;47;31m'    # RED color
	else:
		pstr='\033[1;40;32m'    # GREEN color
	print(pstr+'Status of the Server: ' + str(status)  +ECODE+pstr+'The completed Requests: ' + str(compReq) +ECODE+pstr+'Total the threads no s: ' +str(totalThreads)+ECODE+pstr+'The Idle threads: ' + str(idleThrds)+ECODE+pstr+'Hogging threads : ' + str(hoggingThreads)+ECODE+pstr+'Pending : ' + str(pending)+ECODE+pstr+'ThreadPool QueueLength: ' + str(qLen)+ECODE+pstr+'Server (Throughput): ' +str(thruput)+ECODE)
	
print '======================================================================'
print INFORMATION_COLOR_CODE+'   WELCOME TO THE WEBLOGIC ADMINISTRATION SCRIPT 	 '+END_COLOR_CODE
print '======================================================================'
ConfigFilePath = getAbsPath()
WLSPassword = getWLSPassword()
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

#! Connect to WebLogic Server
connectWLS(WLSUsername, WLSPassword, WLSUrl)

#! Call main screen function
UserOperation = mainScreen()
if (UserOperation.upper() == 'X'):
	scriptExit()
#! If option is Manage WebLogic Configurations	
elif (UserOperation.upper() == 'A'):
	SubOperation = wlsOperation()
	if (SubOperation.upper() == 'X'):
		scriptExit()
	#! If option is for JMS Resource Configuration		
	elif (SubOperation.upper() == 'A'):
		startTransaction()
		#! Call Create File Store
		jmsFileStoreName=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FILE_STORE_NAME')
		jmsFileStoreTraget=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FILE_STORE_TARGET')
		if (jmsFileStoreName.upper() != 'NA' or jmsFileStoreName != None or jmsFileStoreName.upper() != 'NO'):
			try:
				createJMSFileStore(jmsFileStoreName)
			except BeanAlreadyExistsException:
				print INFORMATION_COLOR_CODE+'[INFORMATION]: This File Store already exists'+END_COLOR_CODE
				ifJMSFSExist = 'Y'
			if (ifJMSFSExist != 'Y'):
				targetJMSFileStore(jmsFileStoreName,jmsFileStoreTraget)
		else:
			print INFORMATION_COLOR_CODE+'[INFORMATION]: No File Store was configured'+END_COLOR_CODE
		
		#! Call Create Server
		jmsServerName=ConfigProperties.getProperty(MachineName.upper()+'.JMS.SERVER_NAME')
		jmsServerTarget=ConfigProperties.getProperty(MachineName.upper()+'.JMS.SERVER_TARGETS')	
		if (jmsServerName.upper() != 'NA' or jmsServerName != None or jmsServerName.upper() != 'NO'):
			try:
				createJMSServer(jmsServerName,jmsFileStoreName)
			except BeanAlreadyExistsException:
				print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS Server already exists'+END_COLOR_CODE
				ifJMSServerExist = 'Y'
			if (ifJMSServerExist != 'Y'):
				targetJMSServer(jmsServerName,jmsServerTarget)
		else:
			print INFORMATION_COLOR_CODE+'[INFORMATION]: No JMS Server was configured'+END_COLOR_CODE	
		
		#! Call Create Module
		jmsModuleName=ConfigProperties.getProperty(MachineName.upper()+'.JMS.MODULE_NAME')
		jmsModuleTargets=ConfigProperties.getProperty(MachineName.upper()+'.JMS.MODULE_TARGETS')
		jmsSubDeployment=ConfigProperties.getProperty(MachineName.upper()+'.JMS.SUBDEPLOYMENT')
		if (jmsModuleName.upper() != 'NA' or jmsModuleName != None or jmsModuleName.upper() != 'NO'):
			try:
				createJMSModule(jmsModuleName)
			except BeanAlreadyExistsException:
				print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS Module already exists'+END_COLOR_CODE	
				ifJMSModuleExist = 'Y'
			if (ifJMSModuleExist != 'Y'):
				splitModuleTragets=jmsModuleTargets.split(",")
				for moduleTarget in splitModuleTragets:
					targetJMSModule(jmsModuleName,moduleTarget)
		else:
			print INFORMATION_COLOR_CODE+'[INFORMATION]: No JMS Module was configured'+END_COLOR_CODE
			
		if (jmsSubDeployment.upper() !='NA' or jmsSubDeployment != None or jmsSubDeployment.upper() !='na'):
			try:
				creatJMSSubDeployment(jmsModuleName,jmsSubDeployment,jmsServerName)
			except BeanAlreadyExistsException:
				print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS Sub Deployment already exists'+END_COLOR_CODE
		else:
			print INFORMATION_COLOR_CODE+'[INFORMATION]: No Sub Deployment was specified'+END_COLOR_CODE
		
		jmdQueueCount=ConfigProperties.getProperty(MachineName.upper()+'.JMS.QUEUE_COUNT')
		k=1
		while (k <= int(jmdQueueCount)):
			jmsConnectionFactoryName=ConfigProperties.getProperty(MachineName.upper()+'.JMS.CONNECTION_FACTORY_NAME.'+str(k))
			jmsQueueName=ConfigProperties.getProperty(MachineName.upper()+'.JMS.QUEUE_NAME.'+str(k))
			jmsQueueType=ConfigProperties.getProperty(MachineName.upper()+'.JMS.QUEUE_TYPE.'+str(k))
			
			#! Call Create Connection Factory
			if (jmsConnectionFactoryName.upper() !='NA' or jmsConnectionFactoryName != None or jmsConnectionFactoryName.upper() !='na'):
				try:
					creatJMSConnFactory(jmsModuleName,jmsConnectionFactoryName,jmsSubDeployment,jmsServerName)
				except BeanAlreadyExistsException:
					print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS Connection Factory already exists'+END_COLOR_CODE					
					ifJMSConnFactExist = 'Y'
			else:
				print INFORMATION_COLOR_CODE+'[INFORMATION]: No Connection Factory was created'+END_COLOR_CODE
				
			#! Call Create Queue	
			if(jmsQueueName.upper() !='NA' or jmsQueueName != None or jmsQueueName !='na'):
				if(jmsQueueType.upper() == 'UDQ'):
					try:
						createJMSUDQueue(jmsModuleName,jmsQueueName,jmsSubDeployment,jmsServerName)
						k = k + 1
					except BeanAlreadyExistsException:
						print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS Queue already exists'+END_COLOR_CODE							
						ifJMSQueueExist = 'Y'
					ifJMSQueueExist = 'N'
					if (ifJMSQueueExist != 'Y'):
						TargetJMSQueue(jmsModuleName, jmsSubDeployment, jmsServerName)
						splitQueueTragets=jmsModuleTargets.split(",")
						for queueTarget in splitQueueTragets:
							secondaryTargetJMSQueue(jmsModuleName, queueTarget)
				elif (jmsQueueType.upper() == 'QUEUE'):		
					#! Call Create Queue
					try:
						createJMSQueue(jmsModuleName,jmsQueueName,jmsSubDeployment,jmsServerName)
						k = k + 1
					except BeanAlreadyExistsException:
						print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS Queue already exists'+END_COLOR_CODE							
						ifJMSQueueExist = 'Y'
					ifJMSQueueExist = 'N'
					if (ifJMSQueueExist != 'Y'):
						TargetJMSQueue(jmsModuleName, jmsSubDeployment, jmsServerName)
						splitQueueTragets=jmsModuleTargets.split(",")
						for queueTarget in splitQueueTragets:
							secondaryTargetJMSQueue(jmsModuleName, queueTarget)			
			else:
				print INFORMATION_COLOR_CODE+'[INFORMATION]: No Queue was created'+END_COLOR_CODE

			#! Call Create Foreign Server
		jmsForeignServerName=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_SERVER.NAME')
		if (jmsForeignServerName.upper() !='NA' or jmsForeignServerName !=None or jmsForeignServerName.upper() !='na'):
			try:
				createJMSForeignServer(str(jmsForeignServerName),str(jmsModuleName),str(jmsServerName),str(jmsSubDeployment))
			except BeanAlreadyExistsException:
				print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS Foreign Server already exists'+END_COLOR_CODE			
			jmsForeignServerConnectionURL=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_SERVER.CONNECTION_URL')
			jmsForeignDestinationCount=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_DESTINATION.COUNT')
			i=1
			while (i <= int(jmsForeignDestinationCount)):
				jmsForeignDestinationName=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_DESTINATION.NAME.'+str(i))
				jmsForeignDestinationLocaljndi=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_DESTINATION.LOCAL_JNDI.'+str(i))
				jmsForeignDestinationRemotejndi=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_DESTINATION.REMOTE_JNDI.'+str(i))	
				#! Call Create Foreign Server Destination
				try:
					createJMSForeignServerDestination(str(jmsForeignDestinationName),str(jmsModuleName),str(jmsForeignServerName),str(jmsForeignDestinationLocaljndi),str(jmsForeignDestinationRemotejndi))
					i = i + 1
				except BeanAlreadyExistsException:
					print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS Foreign Server Destination already exists'+END_COLOR_CODE	
					i = i + 1
					
			jmsForeignConnFactCount=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_CONNFACTORY.COUNT')
			j=1
			while (j <= int(jmsForeignConnFactCount)):
				jmsForeignConnectionFactoryName=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_CONNFACTORY.NAME.'+str(j))
				jmsForeignConnectionFactoryLocaljndi=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_CONNFACTORY.LOCAL_JNDI.'+str(j))
				jmsForeignConnectionFactoryRemotejndi=ConfigProperties.getProperty(MachineName.upper()+'.JMS.FOREIGN_CONNFACTORY.REMOTE_JNDI.'+str(j))		
				
				#! Call Create Foreign Server Connection Factory
				try:
					createJMSForeignConnectionFactory(str(jmsModuleName),str(jmsForeignServerName),str(jmsForeignConnectionFactoryName),str(jmsForeignConnectionFactoryLocaljndi),str(jmsForeignConnectionFactoryRemotejndi))
					j = j + 1
				except BeanAlreadyExistsException:
					print INFORMATION_COLOR_CODE+'[INFORMATION]: This JMS Foreign Server Connection Factory already exists'+END_COLOR_CODE				
					j = j + 1				
		else:
			print INFORMATION_COLOR_CODE+'[INFORMATION]: No Foreign Server was created'+END_COLOR_CODE
		

				
		endTransaction()
	
	#! If option is for DataSource Configuration	
	elif (SubOperation.upper() == 'B'):
		#edit()
		#startEdit()
		print INFORMATION_COLOR_CODE+'INSIDE: :-)'+END_COLOR_CODE
		dsCount=ConfigProperties.getProperty(MachineName.upper()+'.DS.COUNT')
		dsOperationType=ConfigProperties.getProperty(MachineName.upper()+'.DS.OPERATION_NAME')
		dsTargetsList = ()
		i=1
		while (i <= int(dsCount)):
			print INFORMATION_COLOR_CODE+'INSIDE WHILE: :-)'+END_COLOR_CODE
			dsName=ConfigProperties.getProperty(MachineName.upper()+'.DS.NAME.'+str(i))
			dsDBName=ConfigProperties.getProperty(MachineName.upper()+'.DS.DATABASE.NAME.'+str(i))
			dsTargets=ConfigProperties.getProperty(MachineName.upper()+'.DS.TARGET.'+str(i))
			dsFileName=ConfigProperties.getProperty(MachineName.upper()+'.DS.FILE_NAME.'+str(i))
			dsJNDIName=ConfigProperties.getProperty(MachineName.upper()+'.DS.JNDI_NAME.'+str(i))
			dsDriverClassName=ConfigProperties.getProperty(MachineName.upper()+'.DS.DRIVER_CLASS_NAME.'+str(i))
			dsJDBCUrl=ConfigProperties.getProperty(MachineName.upper()+'.DS.JDBC.URL.'+str(i))
			dsJDBCUserName=ConfigProperties.getProperty(MachineName.upper()+'.DS.JDBC.USER_NAME.'+str(i))
			dsTestQuery=ConfigProperties.getProperty(MachineName.upper()+'.DS.TEST.QUERY.'+str(i))
			dsGlobalTrasactionProtocol=ConfigProperties.getProperty(MachineName.upper()+'.DS.GLOBAL_TRANSACTION_PROTOCOL.'+str(i))
			dsMaxCapacity=ConfigProperties.getProperty(MachineName.upper()+'.DS.MAX_CAPACITY.'+str(i))
			dsCapacityIncrement=ConfigProperties.getProperty(MachineName.upper()+'.DS.CAPACITY_INCREMENT.'+str(i))
			dsStmtCacheType=ConfigProperties.getProperty(MachineName.upper()+'.DS.STATEMENT.CACHE.TYPE.'+str(i))
			dsStmtCacheSize=ConfigProperties.getProperty(MachineName.upper()+'.DS.STATEMENT.CACHE.SIZE.'+str(i))
			dsInitialCapacity=ConfigProperties.getProperty(MachineName.upper()+'.DS.INITIAL_CAPACITY.'+str(i))
			dsWaiters=ConfigProperties.getProperty(MachineName.upper()+'.DS.HEIGHEST_NUM_WAITERS.'+str(i))
			dsWraps=ConfigProperties.getProperty(MachineName.upper()+'.DS.WRAP_TYPES.'+str(i))
			dsShrinkFreq=ConfigProperties.getProperty(MachineName.upper()+'.DS.SHRINK_FREQUENCY_SECONDS.'+str(i))
			dsIgnoreConnectionsEnabled=ConfigProperties.getProperty(MachineName.upper()+'.DS.IGNORE_IN_USE_CONNECTION_ENABLED.'+str(i))
			dsConnectionReverseTimeout=ConfigProperties.getProperty(MachineName.upper()+'.DS.CONNECTION_REVERSE_TIMEOUT_SECONDS.'+str(i))
			dsInactiveConnectionReverseTimeout=ConfigProperties.getProperty(MachineName.upper()+'.DS.INACTIVE_CONNECTION_REVERSE_TIMEOUT_SECONDS.'+str(i))
			dsPinnedToThread=ConfigProperties.getProperty(MachineName.upper()+'.DS.PINNED_TO_THREAD.'+str(i))
			dsStmtTimeout=ConfigProperties.getProperty(MachineName.upper()+'.DS.STATEMENT_TIME_OUT.'+str(i))
			dsRemoveInfectedstmts=ConfigProperties.getProperty(MachineName.upper()+'.DS.REMOVE_INFECTED_CONNECTIONS.'+str(i))
			dsConnectionRetryFreq=ConfigProperties.getProperty(MachineName.upper()+'.DS.CONNECTION_CREATION_RETRY_FREQUENCY_SECONDS.'+str(i))
			dsTimeToTrustIdlePool=ConfigProperties.getProperty(MachineName.upper()+'.DS.SECONDS_TO_TRUST_AN_IDLE_POOL_CONNECTION.'+str(i))
			dsTestConnectionsReserve=ConfigProperties.getProperty(MachineName.upper()+'.DS.TEST.CONNECTIONS_ON_RESERVE.'+str(i))
			dsTestFreq=ConfigProperties.getProperty(MachineName.upper()+'.DS.TEST.FREQUENCY_SECONDS.'+str(i))
			dsTestTableName=ConfigProperties.getProperty(MachineName.upper()+'.DS.TEST.TABLE_NAME.'+str(i))
			dsLoginDelaySeconds=ConfigProperties.getProperty(MachineName.upper()+'.DS.LOGIN_DELAY_SECONDS.'+str(i))
			dsAttributesCountToUpdate=ConfigProperties.getProperty(MachineName.upper()+'.DS.NUMBER_OF_ATTRIBUTES_TO_UPDATE.'+str(i))
			if (dsOperationType.upper() == 'CREATE'):
				#dsTargetList=[item for item in dsTargets.split(',') if item.strip()]
				dsTargetsList=dsTargets.split(",")
				#dsTargetsList=dsTargetsList.append(ObjectName('com.bea:Name=' + dsTargets.split(",")+ ',Type=Server'))
				#! Call Create DataSource 
				createDataSource(dsName, dsJNDIName, dsJDBCUrl, dsDriverClassName, dsTestQuery, dsJDBCUserName, dsDBName, dsGlobalTrasactionProtocol, dsMaxCapacity, dsCapacityIncrement, dsStmtCacheType, dsStmtCacheSize, dsInitialCapacity, dsWaiters, dsShrinkFreq, dsConnectionReverseTimeout, dsInactiveConnectionReverseTimeout, dsStmtTimeout, dsConnectionRetryFreq, dsTimeToTrustIdlePool, dsTestFreq, dsTestTableName, dsLoginDelaySeconds, dsTargetsList)
			i = i + 1	
	#! If option is to generate thread dump report
	elif (SubOperation.upper() == 'C'):
		generateThreadDumpReport()	
#scriptExit()		
wlsOperation()
