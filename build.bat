
REM cd %1

set ANT_HOME=C:/Ant196
set MW_HOME=C:/Oracle/Middleware/Oracle_Home
set WL_HOME=%MW_HOME%/wlserver
set JAVA_HOME=C:/Java8
set PATH=%ANT_HOME%\bin;%PATH%
set CURRENT_FOLDER=%CD%
REM set weblogic.home=%MW_HOME%/wlserver
set OLD_CLASSPATH=%CLASSPATH%
set CLASSPATH=


IF "%~nx1"=="scaBuild.xml" set CLASSPATH=%MW_HOME%/osb/lib/modules/oracle.servicebus.kernel-wls.jar;%MW_HOME%/osb/lib/modules/oracle.servicebus.kernel-api.jar;%MW_HOME%/wlserver/server/lib/weblogic.jar;%MW_HOME%/Oracle_OSB1/lib/alsb.jar;%MW_HOME%/oep/common/modules/com.bea.common.configfwk_1.3.0.0.jar
IF "%~nx1"=="mdsBuild.xml" set CLASSPATH=%MW_HOME%/osb/lib/modules/oracle.servicebus.kernel-wls.jar;%MW_HOME%/osb/lib/modules/oracle.servicebus.kernel-api.jar;%MW_HOME%/wlserver/server/lib/weblogic.jar;%MW_HOME%/Oracle_OSB1/lib/alsb.jar;%MW_HOME%/oep/common/modules/com.bea.common.configfwk_1.3.0.0.jar
IF "%~nx1"=="osbBuild.xml" set CLASSPATH=%OLD_CLASSPATH%

set OSB_OPTS=-Dweblogic.home=C:/Oracle/Middleware/Oracle_Home/wlserver/server -Dosb.home=C:/Oracle/Middleware/Oracle_Home/osb -Djava.util.logging.config.class=oracle.core.ojdl.logging.LoggingConfiguration -Doracle.core.ojdl.logging.config.file=C:/Oracle/Middleware/Oracle_Home/osb/tools/configjar/logging.xml
set JAVA_OPTS=-Dweblogic.home=C:/Oracle/Middleware/Oracle_Home/wlserver -Dosb.home=C:/Oracle/Middleware/Oracle_Home/osb -Djava.util.logging.config.class=oracle.core.ojdl.logging.LoggingConfiguration -Doracle.core.ojdl.logging.config.file=C:/Oracle/Middleware/Oracle_Home/osb/tools/configjar/logging.xml

call %MW_HOME%/wlserver/server/bin/setWLSEnv.cmd
IF "%~nx1"=="osbBuild.xml" call C:/Oracle/Middleware/Oracle_Home/osb/tools/configjar/setenv.bat
IF "%~nx1"=="wlsBuild.xml" call C:/Oracle/Middleware/Oracle_Home/osb/tools/configjar/setenv.bat

set BLD=%1
shift
set TGT=%1
shift
set TNV=%1
shift
REM the next shift command removes the literal project.list from the input parameters
shift
set PLT="%*"
shift

IF "%TNV%" == "" Echo                                                .
IF "%TNV%" == "" Echo                                                .
IF "%TNV%" == "" Echo Missing parameter for target environment {local, DEV, ST, SIT, UAT}, exiting ...
IF "%TNV%" == "" Echo                                                .
IF "%TNV%" == "" Exit 1

IF NOT "%ant.project.list%" == "" set PLT="%ant.project.list%"
IF NOT "%ant.target.environment%" == "" set TNV="%ant.target.environment%"

echo Running CMD: ant -f %BLD% %TGT% -Dtarget.environment=%TNV% -Dproject.list='%PLT%'
ant -f %BLD% %TGT% -Dtarget.environment="%TNV%" -Dproject.list='%PLT%'

