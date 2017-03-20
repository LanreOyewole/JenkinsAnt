
#cd $1

export ANT_HOME=/usr/bin/ant
export MW_HOME=/home/lanre/Oracle/Middleware/OracleHome
export WL_HOME=SMW_HOME/wlserver
export JAVA_HOME=/java
export PATH=$ANT_HOME\bin;$PATH
export CURRENT_FOLDER=`pwd`
#export weblogic.home=$MW_HOME/wlserver
export OLD_CLASSPATH=$CLASSPATH
export CLASSPATH=


[ "$1"=="scaBuild.xml" ] && export CLASSPATH=$MW_HOME/osb/lib/modules/oracle.servicebus.kernel-wls.jar;$MW_HOME/osb/lib/modules/oracle.servicebus.kernel-api.jar;$MW_HOME/wlserver/server/lib/weblogic.jar;$MW_HOME/Oracle_OSB1/lib/alsb.jar;$MW_HOME/oep/common/modules/com.bea.common.configfwk_1.3.0.0.jar
[ "$1"=="mdsBuild.xml" ] && export CLASSPATH=$MW_HOME/osb/lib/modules/oracle.servicebus.kernel-wls.jar;$MW_HOME/osb/lib/modules/oracle.servicebus.kernel-api.jar;$MW_HOME/wlserver/server/lib/weblogic.jar;$MW_HOME/Oracle_OSB1/lib/alsb.jar;$MW_HOME/oep/common/modules/com.bea.common.configfwk_1.3.0.0.jar
[ "$1"=="osbBuild.xml" ] && export CLASSPATH=$OLD_CLASSPATH$

export OSB_OPTS=-Dweblogic.home=/Oracle/Middleware/Oracle_Home/wlserver/server -Dosb.home=/Oracle/Middleware/Oracle_Home/osb -Djava.util.logging.config.class=oracle.core.ojdl.logging.LoggingConfiguration -Doracle.core.ojdl.logging.config.file=/Oracle/Middleware/Oracle_Home/osb/tools/configjar/logging.xml
export JAVA_OPTS=-Dweblogic.home=/Oracle/Middleware/Oracle_Home/wlserver -Dosb.home=/Oracle/Middleware/Oracle_Home/osb -Djava.util.logging.config.class=oracle.core.ojdl.logging.LoggingConfiguration -Doracle.core.ojdl.logging.config.file=/Oracle/Middleware/Oracle_Home/osb/tools/configjar/logging.xml

$MW_HOME/wlserver/server/bin/setWLSEnv.sh
[ "$1"=="osbBuild.xml" ] && /Oracle/Middleware/Oracle_Home/osb/tools/configjar/setenv.sh
[ "$1"=="wlsBuild.xml" ] && /Oracle/Middleware/Oracle_Home/osb/tools/configjar/setenv.sh

export BLD=$1
shift
export TGT=$1
shift
export TNV=$1
shift
## The next shift command removes the literal project.list from the input parameters
shift
export PLT="$*"
shift

IF "$TNV$" == "" Echo                                                .
IF "$TNV$" == "" Echo                                                .
IF "$TNV$" == "" Echo Missing parameter for target environment {local, DEV, ST, SIT, UAT}, exiting ...
IF "$TNV$" == "" Echo                                                .
IF "$TNV$" == "" Exit 1

IF NOT "$ant.project.list$" == "" export PLT="$ant.project.list$"
IF NOT "$ant.target.environment$" == "" export TNV="$ant.target.environment$"

echo Running CMD: ant -f $BLD$ $TGT$ -Dtarget.environment=$TNV$ -Dproject.list='$PLT$'
ant -f $BLD$ $TGT$ -Dtarget.environment="$TNV$" -Dproject.list='$PLT$'

