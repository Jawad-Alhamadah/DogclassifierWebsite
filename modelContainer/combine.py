
import os
import sys

filename_flag ="--filename"
#bytes_flag ="--size-in-bytes"
num_chunks_flag ="--num-chunk-files"
help_flag ="--help"
keep_flag ="--keep-chunks"
delete_chunks_flag ="--force-delete-chunks"


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

bold = bcolors.BOLD
cyan = bcolors.OKCYAN
warning = bcolors.WARNING
pink = bcolors.HEADER
underline = bcolors.UNDERLINE
green = bcolors.OKGREEN
grey = bcolors.OKGREY
end_color=bcolors.ENDC
highlight_grey =bcolors.HIGHLIGHT_GREY
fail=bcolors.FAIL



if "-help" in sys.argv or help_flag in sys.argv :
    print( f""" {bold}{pink}{underline}Enter the Following values with their respective Flags: {end_color}
                1. {bold}{cyan}chunk combination Filename:  {grey}{ filename_flag }{end_color}
                2. {bold}{warning}Number of chunks:  {grey}{ num_chunks_flag }{end_color}
                3. {bold}{pink}-optional- {bold}{warning}intructions for script:  {grey}{help_flag}{end_color}
                4. {bold}{pink}-optional- {bold}{warning}combine all chunks and keep the original chunks: {grey}{keep_flag}{end_color}
                5. {bold}{pink}-optional- {bold}{warning}Remove Chunks without asking: {grey}{delete_chunks_flag}{end_color}
    {bold}{highlight_grey}example:{end_color} python combine.py {cyan}{grey}{filename_flag}{end_color} myCopy.pt {warning} {grey}{num_chunks_flag}{end_color} 11
          {end_color}""")
    sys.exit()

if keep_flag in sys.argv and delete_chunks_flag in sys.argv:
    print(f"{grey}{keep_flag}{end_color}{warning} and {grey}{delete_chunks_flag}{warning} are contradictory flags. Remove one of them according to your needs. use {grey} --help {warning} to see options{end_color}")
    sys.exit()

#2. {bold}{green}chunk size in bytes:  {grey}{ bytes_flag }{end_color}


user_cont_or_stop="yes"
if keep_flag not in sys.argv:
    user_cont_or_stop = input(f"""{bold}{bcolors.WARNING}If you continue, data chunks will combine into a file and the chunks will be {bcolors.FAIL}DELETED !{bcolors.BOLD}{bcolors.OKGREEN} (exit and use flag {bcolors.BOLD}{bcolors.OKCYAN}--keep{bcolors.OKGREEN} to combine and keep the chunks)
{bold}{bcolors.WARNING}  do you want to continue?{fail} y/n {bcolors.ENDC}""")


if user_cont_or_stop.lower() !="yes" and user_cont_or_stop !="y":
    sys.exit()


index =1


file_copy_name_index = sys.argv.index(filename_flag) + 1 
file_copy_name = sys.argv[file_copy_name_index]

#chunk_size_index = sys.argv.index(bytes_flag) + 1 
#chunk_size = int( sys.argv[chunk_size_index] )

num_segments_index = sys.argv.index(num_chunks_flag) + 1 
num_segments = int( sys.argv[num_segments_index] )


file_common_name="-temp-chunk.txt"

if "1"+file_common_name not in os.listdir():
     print(f"{fail}{bold}ERROR: First chunk file is missing. Its likley that the chunk files don't exit.{end_color}")
     sys.exit()

count=0
list_dir= os.listdir()
for i in range( len(list_dir) ):
     if file_common_name in list_dir[i]:
          count+=1

if count > num_segments:
    user_cont_or_stop = input(f"""{bold}{grey}\nText files with the token name :  {end_color}{file_common_name} {grey}are higher in number {cyan}({count} counted) {grey}than the inputted number of chunk files: {cyan}{num_segments}{grey} This will likely lead to some chunks being combined without reproducing the original file.
\n{warning}do you want to continue regardless? {fail}y/n {green}(correcting the number is highly recommended){end_color}""")

if user_cont_or_stop.lower() !="yes" and user_cont_or_stop !="y":
    sys.exit()

chunk_size = os.path.getsize(str(1) + file_common_name)


model_copy = open( file_copy_name,mode="wb" )
is_chunk_process_successful=True

for i in range(1,num_segments+1):
    try:
        
        chunk = open(str(i) + file_common_name, mode="rb")
        data = chunk.read(chunk_size)
        model_copy.write(data)
    except FileNotFoundError:
        print(f"""{bold}{fail}Some chunk files may be missing. Can't find file named: {grey}{str(i)+file_common_name}. {fail}Make sure that the value of {grey}--num-chunks{fail} flag is correct. 
its possible that the file was combined correctly but you should verify using fc.{end_color}""")
        is_chunk_process_successful=False
        break
    finally:
        chunk.close()
        
model_copy.close()

yes_or_no = "Yes" if keep_flag not in sys.argv else "No"

if keep_flag not in sys.argv and is_chunk_process_successful:
    for i in range(1,num_segments+1):
                os.remove( str(i) + file_common_name)

if is_chunk_process_successful:
     print(f"""{green}{bold}  * Combined successfully *{end_color}
        {bold} {grey} File created: {cyan}{file_copy_name} {end_color}
        {bold} {grey} Number of chunks combined : {cyan} {num_segments}{end_color}
        {bold} {grey} Were chunks deleted?  : {cyan} {yes_or_no}{end_color}
            {end_color}""")  


    


