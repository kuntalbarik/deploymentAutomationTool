import os,time,shutil,os.path,subprocess
#import os.path
from EnvVariable import EnvVariable
dep = "/standalone/deployments/"
src = EnvVariable["ArtifactLocation"]+dep
print(src)
dest= EnvVariable["DeploymentDestination"]+dep
print(dest)
myCmd = 'ps -eaf | grep java'
os.system(myCmd)
print("Checking if the JBOSS is running or not")
jboss_process = subprocess.check_output("ps -eaf | grep jboss | grep -v grep | wc -l", shell=True);
x = int(jboss_process)
print("########## NO. of JBOSS process are Running")
print(x)
##Declaring a function to Copy Binaries##
def copy(src, dest):
	for filename in os.listdir(src):
		if filename.endswith('.ear') or ('.war'):
			shutil.copyfile( src + filename, dest + filename)
			print(filename)

if(x>0):
	print("######Checking if the MCESB or DCESB file is exist in the Artifact location######")
	file_exist = os.path.isfile(src+'/MCESBComponent-ear-1.0-SNAPSHOT.ear' or dest+'/DCRequestESBComponent-ear-1.0-SNAPSHOT.ear')
	if(file_exist==True):
		print("#####MCESB or DCESB files is/are exist#####")
		print("Deleting the MCESB and DCESB .deployed files")
		os.remove(dest+'/MCESBComponent-ear-1.0-SNAPSHOT.ear.deployed')
		os.remove(dest+'/DCRequestESBComponent-ear-1.0-SNAPSHOT.ear.deployed')
		print("Deleted  the MCESB and DCESB .deployed files ")
		print("Checking if the .deployed file exist in CTMM deployment folder")
		time_to_wait = 100
		time_counter = 0
		while not os.path.exists(dest+'/MCESBComponent-ear-1.0-SNAPSHOT.ear.undeployed' and dest+'/DCRequestESBComponent-ear-1.0-SNAPSHOT.ear.undeployed'):
			time.sleep(5)
			print("MCESB or/and DCESB .undeployed files do not exist")
			time_counter += 10
			if time_counter > time_to_wait:
				print("Binaries Deployment failes since .undeployed file is not generating")
				break


		if os.path.isfile(dest+'/MCESBComponent-ear-1.0-SNAPSHOT.ear.undeployed' and dest+'/DCRequestESBComponent-ear-1.0-SNAPSHOT.ear.undeployed'):
			print("MCESB and DCESB .undeployed files exist")
			print("Killing the JBOSS Process")
			mycmd1 = 'sudo pkill -9 java'
			os.system(mycmd1)
			print("Coping the Binaries")
			copy(src,dest)
			print("#####Copying of Binaries completed#####")
			print("##########Starting the JBOSS Service")
			myCmdl=os.system('nohup sudo sh /e/clear/jboss-eap-6.2/bin/standalone.sh -b 0.0.0.0 -c standalone-full.xml -P="/e/clear/jboss-eap-6.2/standalone/configuration/clear/configless.properties" > /dev/null 2>&1 &')
#			myCmd1 = ' sudo sh /e/clear/jboss-eap-6.2/bin/standalone.sh -b 0.0.0.0 -c standalone-full.xml -P="/e/clear/jboss-eap-6.2/standalone/configuration/clear/configless.properties" &'
#			os.system(myCmd1)
			print("###########Jboss started#########")

	else:
		print("Copying the Binaries as MCESB or DCESB files are not present in the Artifact")
		copy(src,dest)
		print("Copying of binaries is  completed")

else:
	print("Copying Binaries as JBOSS is not UP")
	copy(src,dest)
	print("Copying of Binary  is completed")

