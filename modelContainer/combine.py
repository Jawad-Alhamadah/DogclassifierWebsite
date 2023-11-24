
import os
import sys
from alive_progress import alive_bar;




KB_CONVERSION_UNIT = 1024
MB_CONVERSION_UNIT = 1024 * 1024
GB_CONVERSION_UNIT = 1024 * 1024 * 1024

#* Colors for CMD messages
fail='\033[91m'
bold = '\033[1m'
cyan = '\033[96m'
warning = '\033[93m'
pink = '\033[95m'
underline = '\033[4m'
green = '\033[92m'
grey = '\033[90m'
end_color='\033[0m'
highlight_grey ='\033[100m'

#* Function to get the value for arg flags
def get_flag_value(flag,args):
     flag_index = args.index(flag) + 1 
     flag_value = args [flag_index]
     return flag_value


#*flags
filename_flag = "--filename"
num_chunks_flag = "--num-chunk-files"
help_flag = "--help"
keep_flag = "--keep-chunks"
delete_chunks_flag = "--force-delete"
extension_flag = "--ext"
chunks_filename_flag = "--chunks-filename"
default_chunk_name = "_temp-chunk.txt"
chunks_filename = default_chunk_name

script_args = [arg.lower() for arg in sys.argv]

#* Help instructions.
intro = f"""{bold}{pink}{underline}Enter the Following values with their respective Flags:{end_color}"""
filename_instruction = f"""{bold}{cyan}chunk combination Filename:  {grey}{ filename_flag }{end_color}"""
num_chunks_instruction =f"""{bold}{warning}Number of chunks:  {grey}{ num_chunks_flag }{end_color}"""
ext_instruction = f"""{bold}{green}File extension : {grey} {extension_flag} {end_color}"""
help_instruction =f"""{bold}{pink}-optional- {bold}{warning}intructions for script:  {grey}{help_flag}{end_color}"""
keep_instruction =f"""{bold}{pink}-optional- {bold}{warning}combine all chunks and keep the original chunks: {grey}{keep_flag}{end_color}"""
no_chunks_instruction =f"""{bold}{pink}-optional- {bold}{warning}Remove Chunks without asking: {grey}{delete_chunks_flag}{end_color}"""
example_instruction = f"""{bold}{highlight_grey}example:{end_color} {end_color}{warning}python {end_color} combine.py {grey}{filename_flag}{end_color} {cyan}myCopy.pt {warning} {grey}{num_chunks_flag}{end_color} {green}11{end_color} """

#* Error messages

NO_FILENAME_FLAG_ERROR = f"{bold}{fail}No file name provided. Use {grey}{filename_flag}{fail} to name your result file. {end_color}"
NUM_CHUNKS_ERROR = f"{bold}{fail}No chunk number provided. Use {grey}{num_chunks_flag}{fail} to indicate the number of chunks to sum. {end_color}"
NO_EXT_ERROR = f"{bold}{fail}No extension included. Use {grey}{extension_flag}{fail} to set the extension. {end_color}"
KEEP_AND_DELETE_ERROR = f"{grey}{keep_flag}{end_color}{warning} and {grey}{delete_chunks_flag}{warning} are contradictory flags. Remove one of them according to your needs. use {grey} --help {warning} to see options{end_color}"


FIRST_FILE_NOT_EXIST = f"""{fail}{bold}ERROR: First chunk file is missing. Its likley that the chunk files don't exit, or inncorrect name provided to {grey}{chunks_filename_flag}{end_color}
{fail}The default chunks name is {cyan}{default_chunk_name}{fail}. make sure the files exist or provide the correct chunks name {end_color}"""

#* Warnings
KEEP_DELETE_WARNING = f"""{bold}{warning}If you continue, data chunks will combine into a file and the chunks will be {fail}DELETED !{bold}{green} (exit and use flag {bold}{cyan}{keep_flag}{green} to combine and keep the chunks)
{bold}{warning}  do you want to continue?{fail} y/n {end_color}"""



#* error checking
if filename_flag not in script_args:
    print(NO_FILENAME_FLAG_ERROR)
    sys.exit()

if num_chunks_flag not in script_args:
    print(NUM_CHUNKS_ERROR)
    sys.exit()

if extension_flag not in script_args:
    print(NO_EXT_ERROR)
    sys.exit()

#* error if contradiction flag keep and delete are both raised
is_delete_and_keep = keep_flag in script_args and delete_chunks_flag in script_args

if is_delete_and_keep:
    print(KEEP_AND_DELETE_ERROR)
    sys.exit()

combined_filename = get_flag_value( filename_flag, script_args )
ext = get_flag_value( extension_flag, script_args )
num_chunks = int( get_flag_value( num_chunks_flag, script_args ) )
if chunks_filename_flag in script_args:
    chunks_filename = get_flag_value( chunks_filename_flag, script_args ) 

copy_ext = combined_filename.split(".")[1]


EXTENSION_MISMATCH_ERROR = f"""{bold}{fail}\nThe copy name extenstion in filename: {cyan}{combined_filename} {fail}doesn't match flag extention {grey}{extension_flag} {cyan}{ext}{end_color} 
{fail}{bold}Both must match to insure you combine the file into the correct extension. \n {end_color}"""
if ext != copy_ext:
     print(EXTENSION_MISMATCH_ERROR)
     sys.exit()


#* flag values.
if "-help" in script_args or help_flag in script_args :
    print( f""" \n{intro}\n
                1. {filename_instruction}
                2. {num_chunks_instruction}
                3. {ext_instruction}
                4. {help_instruction}
                5. {keep_instruction}
                6. {no_chunks_instruction}
    \n{example_instruction}
          {end_color}""")
    sys.exit()


delete_or_keep_user_input="yes"

#* if neither keep or delete is raised, print a warning.
is_neither_delete_or_keep = keep_flag not in script_args and delete_chunks_flag not in script_args
if is_neither_delete_or_keep :
    delete_or_keep_user_input = input(KEEP_DELETE_WARNING)

#* if use answer is no, exist
is_user_answer_no = delete_or_keep_user_input.lower() !="yes" and delete_or_keep_user_input !="y"
if is_user_answer_no:
    sys.exit()

#* if the first file doesn't exist, print an error
first_filename ="1"+chunks_filename
if first_filename not in os.listdir():
     print(FIRST_FILE_NOT_EXIST)
     sys.exit()



#* count the number of chunks to combine
chunk_files_count=0
list_dir= os.listdir()
for i in range( len(list_dir) ):
     if chunks_filename in list_dir[i]:
          chunk_files_count+=1

#* check the count provided against the count detected in the actual file.
CHUNK_COUNT_MISMATCH = f"""{bold}{grey}\nText files with the token name :  {end_color}{chunks_filename} {grey}are higher in number {cyan}({chunk_files_count
} counted) {grey}than the inputted number of chunk files: {cyan}{num_chunks}{grey} This will likely lead to some chunks being combined without reproducing the original file.
\n{warning}do you want to continue regardless? {fail}y/n {green}(correcting the number is highly recommended){end_color}"""
if chunk_files_count > num_chunks:
    delete_or_keep_user_input = input(CHUNK_COUNT_MISMATCH)

#* if answer is no, print an error
is_user_answer_no = delete_or_keep_user_input.lower() !="yes" and delete_or_keep_user_input !="y"
if is_user_answer_no:
    sys.exit()

#* get chunks size
chunk_size = os.path.getsize(str(1) + chunks_filename)
byte_unit = "B"

#* determine the unit for the byte size
if chunk_size>=GB_CONVERSION_UNIT :
    adjusted_chunk_size= chunk_size/GB_CONVERSION_UNIT
    byte_unit= "Gb"

elif chunk_size>=MB_CONVERSION_UNIT :
    adjusted_chunk_size= chunk_size/MB_CONVERSION_UNIT
    byte_unit="Mb"

elif chunk_size>=KB_CONVERSION_UNIT :
    adjusted_chunk_size= chunk_size/KB_CONVERSION_UNIT
    byte_unit="Kb"


#* open file to write
model_copy = open( combined_filename,mode="wb" )
is_chunk_process_successful=True

print("\n")

#* Loop to combine files into one.
with alive_bar(num_chunks,bar="blocks",unit=" File",title="Combine",spinner="radioactive") as bar:
    for i in range(1,num_chunks+1):
        try:
            #* read chunk
            chunk = open(str(i) + chunks_filename, mode="rb")
            data = chunk.read(chunk_size)

            #* write into combined file
            model_copy.write(data)
            bar()
        except FileNotFoundError:
            print(f"""{bold}{fail}Some chunk files may be missing. Can't find file named: {grey}{str(i)+chunks_filename}. {fail}Make sure that the value of {grey}--num-chunks{fail} flag is correct. 
    its possible that the file was combined correctly but you should verify using fc.{end_color}""")
            is_chunk_process_successful=False
            break
        finally:  
            chunk.close()
        
model_copy.close()

are_chunks_deleted= "Yes" if keep_flag not in script_args else "No"

if keep_flag not in script_args and is_chunk_process_successful:
    print(f"{green}\nFile Combined !\n{end_color}")
    with alive_bar(num_chunks,bar="blocks",unit=" File",title="Delete",spinner="arrows_in") as bar:
        for i in range(1,num_chunks+1):
                    os.remove( str(i) + chunks_filename)
                    bar()

if is_chunk_process_successful:
     print(f"""\n{green}{bold}  * Files Combine Successful *{end_color}
        {bold} {grey} File created: {cyan}{combined_filename} {end_color}
        {bold} {grey} Number of chunks combined : {cyan} {num_chunks} Files{end_color}
        {bold} {grey} Were chunks deleted?  : {cyan} {are_chunks_deleted}{end_color}
        {bold} {grey} Byte Size per chunk : {cyan} {adjusted_chunk_size} {byte_unit}  - {chunk_size} Bytes  
            {end_color}""")  

