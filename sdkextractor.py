import sys
import os
import ntpath
import classdump
import re
import logging
import datetime


global_class_name_freq = {}
logger = logging.getLogger('sdk_extactor')

def update_global_map(class_map):
    for class_name in class_map:
        if class_name not in global_class_name_freq:
           global_class_name_freq[class_name] = 1
        else:
           global_class_name_freq[class_name] = global_class_name_freq[class_name] + 1

def extract_classdump(dir_name):
    if not os.path.exists(dir_name):
       logger.error("Error! %s is not a directory of APKs!" %dir_name)
       exit()
    os.chdir(dir_name)
    if not os.path.exists('sdk_extractor_out'):
       os.makedirs('sdk_extractor_out')
       os.chdir('sdk_extractor_out')
    for subdir, dirs, files in os.walk(dir_name):
        for file in files:
            if file.endswith(".apk"):
                apk_path = os.path.join(subdir, file)
                classdump.extract_classpath(apk_path)
    return os.path.join(dir_name, 'sdk_extractor_out')


def extract_sdk_list(dir_name):
    for subdir, dirs, files in os.walk(dir_name):
        for file in files:
            if (file == "classdump.txt"):
               classdump_path = os.path.join(subdir, file)
               logger.info("processing class dump: %s" % classdump_path)
               with open(classdump_path, 'r') as classdump:
                    class_map = []
                    for line in classdump:
                        try:
                            packagename = re.search('[a-z0-9\/]+\/', line).group(0)
                            if not packagename in class_map:
                               class_map.append(packagename)
                        except Exception:
                            logger.warning('Warning! skipping class name %s ' %line)
                            pass
                    update_global_map(class_map)
    print(global_class_name_freq)
    print(len(global_class_name_freq))
    with open('class_map' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") , 'w') as map:
         for item in global_class_name_freq:
             map.write(item + "[%d]" %global_class_name_freq[item] + '\n')

                       

def main():
  if len(sys.argv) == 3:
    if(sys.argv[1] == '--apk_dir'):
        classdump_dir = extract_classdump(sys.argv[2])
        extract_sdk_list(classdump_dir)
    elif(sys.argv[1] == '--classdump_dir'):
        extract_sdk_list(sys.argv[2])
    else: 
        print('please specify a correct argument! {--apklist|--dumplist}')
  else:
    print("Please specify a valid option {--apklist|--dumplist} and dircetory of apks/classdump files.")

if __name__ == '__main__':
  main()
	
	
