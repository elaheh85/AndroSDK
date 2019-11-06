import sys
import os
import ntpath
import subprocess



def extract_classpath(apk_path):
	try:
		apk_name = ntpath.basename(apk_path);
		print("extracting class dump for: " + apk_path)
		dir_name = apk_name.split('.apk')[0]
		current_dir = os.getcwd()
		if not os.path.exists(dir_name):
   			os.makedirs(dir_name)		
		os.chdir(dir_name) 
		output = subprocess.getoutput("""dexdump %s | grep 'Class descriptor' | awk -F ":" '{print $2}'""" %apk_path)
			
		classdump = open('classdump.txt', 'w')
		classdump.write(output)	
		os.chdir(current_dir)
		#print(os.getcwd())		

		

	except:
		e = sys.exc_info()
		print(e)

def main():

  if len(sys.argv) == 2:
    extract_classpath(sys.argv[1])
  else:
    print("Please specify dex class/apk path")

if __name__ == '__main__':
  main()
	
	
