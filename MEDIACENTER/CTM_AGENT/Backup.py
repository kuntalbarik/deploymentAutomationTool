import shutil,os,datetime,time
from EnvVariable import EnvVariable
from os import listdir
from os.path import isfile, join
from time import gmtime, strftime
from datetime import datetime
BackupType = EnvVariable["BackupType"]
BackupPath = EnvVariable["BackupPath"]
ArtifactLocation1 = EnvVariable["ArtifactLocation"]
DestinationPath = EnvVariable["DeploymentDestination"]
ReleaseNo = EnvVariable["ReleaseNo"]
ConponentName=EnvVariable["ConponentName"]
StandAloneFolder = "standalone/"
DeploymentDestination = DestinationPath+"/"+StandAloneFolder
retentiondays= EnvVariable["BackupRetentionDays"]
print ("#############$$$$$$$$$$$$$BackupType is" +BackupType)
if os.path.exists(BackupPath):
    print (BackupPath +" is present")
else:
    os.makedirs(BackupPath)
    print (BackupPath +" is created")

def Partial_Backup():
  print("##################Partial_Backup Started############")
  now = datetime.now()
  newDirName = now.strftime("%Y_%m_%d-%H%M")
  print("Creating Backup directory "+newDirName)
  type = "Partial_"
  Component = ConponentName
  os.chdir(BackupPath)
  os.mkdir(type +Component +ReleaseNo +newDirName)
  foldername = type +Component +ReleaseNo + newDirName
  print(foldername)
  BackUpDestination = os.path.join(BackupPath ,foldername)
  print(BackUpDestination)
  path = ArtifactLocation1
  files = []
  for r, d, f in os.walk(path):
    for file in f:
        #print(" files names "+str(os.path.basename(f)))
        files.append(os.path.join(r, file))
  flist=[]
  for f in files:
    filelist=f.split("/")
    flist.append(filelist[-1])
  print ("File names")  
  print(flist)

  filelist=[]
  flist=[]  
  for f in files:
    filelist=f.split("/standalone/")
    flist.append(filelist[-1])
  print ("Print filenames after standalone directory")
  #print(flist)
  Dir_List=[]
  for f in flist:
           TempFile = os.path.join(DeploymentDestination,f)
           Destination=os.path.join(BackUpDestination,f)
           Dir=os.path.dirname(Destination)
           if not os.path.exists(Dir):
            os.makedirs(Dir)
            print(Dir)
           else:
            print (Dir," already exists")
           if os.path.exists(TempFile):
               print("Copying " +TempFile+ " To Backuplocation" " " +Destination)
               shutil.copy(TempFile, Destination)
           else:
               print (TempFile+ " does not exist at deployment directory")
           Destination=""

  print("Partial_Backup completed")

def Full_Backup():
        print("##########Full_Backup Started############")
        now = datetime.now()
        newDirName = now.strftime("%Y_%m_%d-%H%M")
        ComponentName = ConponentName
        print ("ComponentName =>" , ComponentName)
        print ("BackupPath => " , BackupPath)
        os.chdir(BackupPath)
        DeploymentBackupPath = BackupPath + ComponentName + ReleaseNo + newDirName + "/deployments"
        ConfigurtionBackupPath = BackupPath + ComponentName + ReleaseNo + newDirName + "/configuration"
        print ("DeploymentBackupPath =>  ", DeploymentBackupPath)
        print ("ConfigurtionBackupPath => ", ConfigurtionBackupPath)
        CreateDepDirCmd= "mkdir -p " + DeploymentBackupPath
        print ("CreateDepDirCmd =>", CreateDepDirCmd)
        CreateConfDirCmd= "mkdir -p " + ConfigurtionBackupPath
        print ("CretaeConfDirCmd => ", CreateConfDirCmd)
        os.system(CreateDepDirCmd)
        os.system(CreateConfDirCmd)
        DeploymentBackupCmd = "cp -rf " + DeploymentDestination+ "deployments/* " + DeploymentBackupPath + "/"
        ConfigurationBackupCmd ="cp -rf " + DeploymentDestination+ "configuration/* " + ConfigurtionBackupPath + "/"
        print ("DeploymentBackupCmd => ",DeploymentBackupCmd)
        print ("ConfigurationBackupCmd => ", ConfigurationBackupCmd) 
        os.system(DeploymentBackupCmd)
        os.system(ConfigurationBackupCmd)

def delete_oldbackups(BackupPath):
        print("*******************Deleting Old Backup*******************")
        path = BackupPath
        now = time.time()
        old = now - 86400*retentiondays
        print("BackupPath is "+path)
        
        dirlist = os.listdir(BackupPath)
        print("All backup directories")
        for _dir in dirlist:
               print(BackupPath+_dir)
        
        for _dir in dirlist:
            Check_Time = os.path.getmtime(BackupPath+_dir)
            if Check_Time < old:
                shutil.rmtree(BackupPath+_dir) 
#        print("")
                print ("Deleting directory "+BackupPath+_dir+" as its older than retention period")
#                           print (actualpath)
#                            print(_dir)
#                            print("Deleting the  Backup Folders older than retentiondays days")

#        for (root, dirs, files) in os.walk(path, topdown=True):
#                for _dir in root:
#                        actualpath= root+_dir
#                        print("Backup directories marked for deletion are" +actualpath)
#                       print("Backup directories marked for deletion are" +root) 
#                       for _dir in root:
#                           Check_Time = os.path.getmtime(_dir)
#                        print(Check_Time)
 #                       print(old)
#                    if Check_Time < old:
#                           print (actualpath)
#                            print(_dir)
#                            print("Deleting the  Backup Folders older than retentiondays days")
                           # shutil.rmtree(BackupPath+"/"+_dir)
#                       print("Old backups deleted")
        print("#######Deleted Old Backups Directory############")                                

delete_oldbackups(BackupPath)

if BackupType == 'Partial':
                Partial_Backup()
if BackupType == 'Full':
                Full_Backup()
if BackupType == 'No':
                print("###########Backup not Required#############")
