
#cd $1
echo "Parameters*1:= $*"

export ANT_HOME=/usr/share/ant
export MW_HOME=/home/lanre/Oracle/Middleware/OracleHome
export WL_HOME=SMW_HOME/wlserver
export JAVA_HOME=/java
export PATH=$ANT_HOME/bin:$PATH
export CURRENT_FOLDER=`pwd`
#export weblogic.home=$MW_HOME/wlserver
export OLD_CLASSPATH=$CLASSPATH
export CLASSPATH=

export BLD=$1
shift
[ -z "$BLD" ] && { echo "Ant build file must be specified"; exit 1; }

export TGT=$1
shift
[ -z "$TGT" ] && { echo "Ant target must be specified"; exit 1; }

export TNV=$1
shift
[ -z "$TNV" ] && { echo "Target environment {local, DEV, ST, SIT, UAT} must be specified"; exit 1; }

export PLT="$*"
echo "Parameters*2:= $*"

#echo TNV=${TNV}
#echo PLT=${PLT}
#echo aTNV is $ant.target.environment
#echo aPLT is $ant.project.list

#[ "$ant.project.list" != "" ] && export PLT="$ant.project.list"
#[ "$ant.target.environment" != "" ] && export TNV="$ant.target.environment"

[ "$BLD" = "*/scaBuild.xml" ] && export CLASSPATH=$MW_HOME/osb/lib/modules/oracle.servicebus.kernel-wls.jar:$MW_HOME/osb/lib/modules/oracle.servicebus.kernel-api.jar:$MW_HOME/wlserver/server/lib/weblogic.jar:$MW_HOME/Oracle_OSB1/lib/alsb.jar:$MW_HOME/oep/common/modules/com.bea.common.configfwk_1.3.0.0.jar
[ "$BLD" = "*/mdsBuild.xml" ] && export CLASSPATH=$MW_HOME/osb/lib/modules/oracle.servicebus.kernel-wls.jar:$MW_HOME/osb/lib/modules/oracle.servicebus.kernel-api.jar:$MW_HOME/wlserver/server/lib/weblogic.jar:$MW_HOME/Oracle_OSB1/lib/alsb.jar:$MW_HOME/oep/common/modules/com.bea.common.configfwk_1.3.0.0.jar
[ "$BLD" = "*/osbBuild.xml" ] && export CLASSPATH=$OLD_CLASSPATH$

export OSB_OPTS="-Dweblogic.home=/home/lanre/Oracle/Middleware/OracleHome/wlserver/server -Dosb.home=/home/lanre/Oracle/Middleware/OracleHome/osb -Djava.util.logging.config.class=oracle.core.ojdl.logging.LoggingConfiguration -Doracle.core.ojdl.logging.config.file=/home/lanre/Oracle/Middleware/OracleHome/osb/tools/configjar/logging.xml"
export JAVA_OPTS="-Dweblogic.home=/home/lanre/Oracle/Middleware/OracleHome/wlserver -Dosb.home=/home/lanre/Oracle/Middleware/OracleHome/osb -Djava.util.logging.config.class=oracle.core.ojdl.logging.LoggingConfiguration -Doracle.core.ojdl.logging.config.file=/home/lanre/Oracle/Middleware/OracleHome/osb/tools/configjar/logging.xml"

$MW_HOME/wlserver/server/bin/setWLSEnv.sh

[ "$BLD" = "*osbBuild.xml" ] && /home/lanre/Oracle/Middleware/OracleHome/osb/tools/configjar/setenv.sh
[ "$BLD" = "*wlsBuild.xml" ] && /home/lanre/Oracle/Middleware/OracleHome/osb/tools/configjar/setenv.sh

echo Running CMD: ant -f $BLD $TGT -Dtarget.environment=$TNV -Dproject.list=$PLT
ant -f $BLD $TGT -Dtarget.environment="$TNV" -Dproject.list=$PLT

