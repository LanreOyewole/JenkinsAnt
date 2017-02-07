import wlstModule
from java.util import Collections
from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
from java.io import FileInputStream

from com.bea.wli.sb.util import Refs
from com.bea.wli.config.customization import Customization
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.sb.management.importexport import ALSBImportOperation
from com.bea.wli.config import Ref

import sys

#=======================================================================================
# Entry function to undeploy a project from an ALSB domain
#=======================================================================================
def undeployProject():
    SessionMBean = None
    
    print 'Attempting to undeploy', project, ' from ALSB Admin Server listening on ', adminUrl
    
    # domainRuntime()      
    sessionName  = "TransientWLSTSession_" + str(System.currentTimeMillis()) 
    sessMgmtMBean = findService(SessionManagementMBean.NAME, SessionManagementMBean.TYPE)
    sessMgmtMBean.createSession(sessionName)

    print 'Created session [', sessionName, '] ... ', ALSBConfigurationMBean.NAME , "." + sessionName, ALSBConfigurationMBean.TYPE

    alsbConfigMBean = findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
    
    projectRefs = alsbConfigMBean.getRefs(Ref.DOMAIN)
    projectRef = Ref(Ref.PROJECT_REF, Ref.DOMAIN, project)

    if alsbConfigMBean.exists(projectRef):
        print "#### removing OSB project: " + projectRef.getProjectName()
        if projectRef.getProjectName() == "System":
            print "Omitting System project, it must not be deleted ..."
        else:
            alsbConfigMBean.delete(Collections.singleton(projectRef))
        print
    else:
        failed = "OSB project <" + projectRef.getProjectName() + "> does not exist"
        print failed
    print
    
    print "Activating session ... "
    sessMgmtMBean.activateSession(sessionName, "Complete project removal with customization using wlst")
    print "Session activated."
    cleanupSession(sessMgmtMBean, sessionName)
    print "done!"

#=======================================================================================
# Entry function to undeploy all projects from an ALSB domain
#=======================================================================================
def undeployProjects():
    SessionMBean = None
    
    print 'Attempting to undeploy from ALSB Admin Server listening on ', adminUrl
    
    # domainRuntime()      
    sessionName  = "TransientWLSTSession_" + str(System.currentTimeMillis()) 
    sessMgmtMBean = findService(SessionManagementMBean.NAME, SessionManagementMBean.TYPE)
    sessMgmtMBean.createSession(sessionName)

    print 'Created session [', sessionName, ']'

    alsbConfigMBean = findService(ALSBConfigurationMBean.NAME + "." + sessionName, ALSBConfigurationMBean.TYPE)
    
    projectRefs = alsbConfigMBean.getRefs(Ref.DOMAIN)

    projectList = projectRefs.iterator()

    while projectList.hasNext():  
        projectRef = projectList.next()
        
        if projectRef.getTypeId() == Ref.PROJECT_REF:             
            print "Project name : " + (projectRef.getProjectName())
            
            if alsbConfigMBean.exists(projectRef):
                print "#### removing OSB project: " + projectRef.getProjectName()
                if projectRef.getProjectName() == "System":
                    print "Omitting System project ..."
                else:
                    alsbConfigMBean.delete(Collections.singleton(projectRef))
                print
            else:
                failed = "OSB project <" + projectRef.getProjectName() + "> does not exist"
                print failed
            print
    
    print "Activating session ... "
    sessMgmtMBean.activateSession(sessionName, "Complete project removal with customization using wlst")
    print "Session activated."

    cleanupSession(sessMgmtMBean, sessionName)

    print "done!"

#=======================================================================================
def cleanupSession(sessMgmtMBean, sessionName):
    try:
        print "Closing session ..."
        if (sessMgmtMBean.sessionExists(sessionName)):
            sessMgmtMBean.discardSession(sessionName)
            sessMgmtMBean.closeSession(sessionName)

    except:
        print "Unexpected error: ", sys.exc_info()[0]
        dumpStack()
        #SessionMBean.discardSession(sessionName)
        raise


# IMPORT script init
try:
    # import the service bus projects and customisation file
    if project == "None":
        undeployProjects()
    else:
        undeployProject()
    print

except:
    print "Unexpected error: ", sys.exc_info()[0]
    dumpStack()
    raise