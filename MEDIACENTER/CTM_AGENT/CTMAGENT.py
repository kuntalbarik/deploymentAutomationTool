cmd = os.system('sudo apt-get -y  install mysql.connector')
cmd = os.system('sudo apt-get -y install python-requests')

import shutil,os,requests,json,mysql.connector,time
from os import path
from EnvVariable import EnvVariable
from mysql.connector import Error
NumOfCheck = 1

MCIP = EnvVariable["CTMMasterIP"]
WebServicesIp = EnvVariable["WebServices"]
AgentIp = EnvVariable["HostIP"]
#AgentIp = '10.6.0.12'
#MCIP =  '10.6.0.11'
#WebServicesIp = '10.6.0.3'

def ChangeAgentState():
	headers = {'TenantId': '9001' ,'UserId': '1234' , 'Token': 'fsfsfdf' ,'Host': ''+WebServicesIp+':1005' , 'Content-Type':'application/json'}
	body = {"mcManagerIP": MCIP , "agentIP": AgentIp , "attributeName": "isActive" , "attributeValue":"0","attributeValue":"1"}
	url = "http://"+WebServicesIp+":1005/PFT.Clear.Configuration/Configuration.svc/webHttp/Json/UpdateAgent"
	print("Making the request to url "+url)
	r = requests.post(url, headers=headers, data=json.dumps(body))
	print("Request Completed, Response  "+str(r.status_code))
def GetAllAgent():
	headers = {'TenantId': '9001' ,'UserId': '1234' , 'Token': 'fsfsfdf' ,'Host': ''+WebServicesIp+':1005' , 'Content-Type':'application/json'}
	body = {"mcManagerIP": MCIP}
	url = "http://"+WebServicesIp+":1005/PFT.Clear.Configuration/Configuration.svc/webHttp/Json/GetAllAgents"
	print("Making the request to url "+url)
	r = requests.post(url, headers=headers, data=json.dumps(body))
	print("Request Completed, Response  "+str(r.status_code))
#def ManagerClearCache():
#	headers = {'TenantId': '9001' ,'UserId': '1234' , 'Token': 'fsfsfdf' ,'Host': ''+MCIP+':8080' , 'Content-Type':'application/json'}
#	url = "http://"+MCIP+":8080/PFT.CTMService-0.0.1/CTMService/ClearAgentConfig"
#	print("Making the request to url "+url)
#	r = requests.get(url, headers=headers)
#	print("Request Completed, Response  "+str(r.status_code))
file = "MCESBComponent-ear-1.0-SNAPSHOT.ear"
DeploymentDirectory = "/standalone/deployments/"
src = EnvVariable["ArtifactLocation"]+DeploymentDirectory
dest = EnvVariable["DeploymentDestination"]+DeploymentDirectory
MCSEBFileLocation = EnvVariable["ArtifactLocation"]+DeploymentDirectory+"/"+file
print("Checking if File " +file+ " Is Present in deployment artifacts package"+MCSEBFileLocation)
if (path.exists(MCSEBFileLocation)):
	print("File " +file+ " Is Present In deployment artifacts package"+MCSEBFileLocation)
	ChangeAgentState()
	GetAllAgent()
#	ManagerClearCache()
	try:
		connection = mysql.connector.connect(host= MCIP,database='quartz',user='root',password='root')
		def IsInprogresJobExist():
			NumOfCheck = 1
			if connection.is_connected():
				print("Successfully connected to host :: " + str(MCIP))
				cursor = connection.cursor()
				while(NumOfCheck < 11):
					print("Checking for in-progress jobs for "+str(NumOfCheck)+" time \n\n\n")
					cursor.execute("select agent_ip,wf_status,job_id,job_name from quartz.WF_JOB_DETAILS where agent_ip='"+AgentIp+"' +'and'+ wf_status='1'")
					records = cursor.fetchall()
					print(records)
					inprogressRows = cursor.rowcount
					if(inprogressRows>0):
						print("Number of jobs in inprogress :: " + str(inprogressRows))
						for i in range(0,10):
							print("Waiting for "+str(i+1)+" seconds \n")
							i = i+1
							time.sleep(1)
#                                                       break
					else:
						break
					NumOfCheck = NumOfCheck+1
			else:
				print("Unable to connect to host :: " + str(MCIP))

	except Error as e:
		print("Error while connecting to MySQL", e)
	finally:
		IsInprogresJobExist()
		if (connection.is_connected()):
			connection.close()
			ChangeAgentState()
			print("Undeploying Files")
			cmd = "sudo rm -rf MCESBComponent-ear-1.0-SNAPSHOT.ear.deployed"
			os.system(cmd)
			print("Killing Java")
			cmd = "sudo pkill java"
			os.system(cmd)
                        #os.system('sudo sh /e/clear/clearjboss.sh')
			print("Java Killed")
			for filename in os.listdir(src):
				if filename.endswith('.war') or ('.ear'):
					print("Copying File " +filename+ " From ArtifactLocation " +src+ " To DeploymentLocation" " " +dest)
					shutil.copy( src + filename, dest)
					print(" File Copied " +filename+ " From ArtifactLocation " +src+ " To DeploymentLocation" " " +dest)
					print("##########Starting the JBOSS Service")
					myCmdl=os.system('nohup sudo sh /e/clear/jboss-eap-6.2/bin/standalone.sh -b 0.0.0.0 -c standalone-full.xml -P="/e/clear/jboss-eap-6.2/standalone/configuration/clear/configless.properties" > /dev/null 2>&1 &')
                                        #os.system('sudo sh /e/clear/jboss-eap-6.2/bin/standalone.sh -b 0.0.0.0 -c standalone-full.xml -P="/e/clear/jboss-eap-6.2/standalone/configuration/clear/configless.properties" &')
					print("###########Jboss started#########")
else:
        print("File " +file+ " Is Not Present In deployment artifacts package"+MCSEBFileLocation)
        for filename in os.listdir(src):
                if filename.endswith('.war') or ('ear'):
                        print("Copying File " +filename+ " From ArtifactLocation " +src+ " To DeploymentLocation" " " +dest)
                        shutil.copy( src + filename, dest)
                        print("Copied File " +filename+ " From ArtifactLocation " +src+ " To DeploymentLocation" " " +dest)
