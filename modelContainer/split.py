import sys
import os
import math
from alive_progress import alive_bar;
filename_flag ="--filename"
bytes_flag ="--size-in-bytes"
help_flag ="--help"
KB_CONVERSION_UNIT=1024
MB_CONVERSION_UNIT=1024000





class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREY = '\033[90m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    HIGHLIGHT_GREY='\033[100m'
    UNDERLINE = '\033[4m'

fail=bcolors.FAIL
bold = bcolors.BOLD
cyan = bcolors.OKCYAN
warning = bcolors.WARNING
pink = bcolors.HEADER
underline = bcolors.UNDERLINE
green = bcolors.OKGREEN
grey = bcolors.OKGREY
end_color=bcolors.ENDC
highlight_grey =bcolors.HIGHLIGHT_GREY


if help_flag in sys.argv:
    print( f"""{end_color} {bold}{pink}Enter the following in order : {end_color}
                1. {bold}{cyan}Filename to split: {grey}{ filename_flag }{end_color}{end_color}
                2. {bold}{green}segment size in bytes: {grey}{ bytes_flag }{end_color}{end_color}
                3. {bold}{pink}-optional- {bold}{warning}intructions for script:  {grey}{help_flag}{end_color}
                          
        {bold}example:{end_color} python split.py {cyan}fileToSplit.pt {green}50000000 
          {end_color}""")
    sys.exit()


file_to_split_index = sys.argv.index(filename_flag) + 1 
file_to_split = sys.argv[file_to_split_index]

chunk_size_index = sys.argv.index(bytes_flag) + 1 
chunk_size = int( sys.argv[chunk_size_index] )


if not os.path.isfile(file_to_split):
    print(f"{bold}{fail} ERROR: File named: {grey}{file_to_split} {fail}does not exist. {end_color}")
    exit()
#file_to_split = sys.argv[1]
#chunk_size = int(sys.argv[2]) #50000000 #50 Mb
#ext = file_to_split.split(".")[1]

model_file = open(file_to_split,mode="rb")
#data = model_file.read(chunk_size)
files_list=[]
file_name_counter=1
file_common_name="-temp-chunk.txt"

file_size = os.stat(file_to_split).st_size
file_split_count = math.ceil(file_size/chunk_size)

# import time
# with alive_bar(5000,bar="smooth") as bar:
#     for i in range(5000):
#         time.sleep(.001)
#         bar()
with alive_bar(file_split_count,bar="blocks",unit=" File",title="Split") as bar:
    for i in range(1,file_split_count+1) :
        data = model_file.read(chunk_size)
        file_name=str(file_name_counter)+file_common_name
        file = open(file_name,mode="wb")
        file.write(data)
        file.close()
        #files_list.append(file_name)
        file_name_counter+=1
        bar()


unit= "Kb" if chunk_size>=KB_CONVERSION_UNIT else "B"

if chunk_size>=MB_CONVERSION_UNIT:
    unit= "Mb"

chunk_in_MB = 0

if chunk_size>=KB_CONVERSION_UNIT and chunk_size< MB_CONVERSION_UNIT :
    chunk_in_MB= chunk_size/KB_CONVERSION_UNIT

if chunk_size>=MB_CONVERSION_UNIT :
    chunk_in_MB= chunk_size/MB_CONVERSION_UNIT



print(f"""{green}{bold} \n  * File Split Successful *
      {grey}    Number of chunks created : {cyan} {file_name_counter-1}
      {grey}    Byte Size per chunk : {cyan} {chunk_in_MB} {unit}  - {chunk_size} Bytes  
         {end_color}""")  
model_file.close()

