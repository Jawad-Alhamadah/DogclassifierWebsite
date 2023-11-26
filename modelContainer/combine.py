
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

def byte_to_Kilo_mega_giga(bytes):
    if bytes>=GB_CONVERSION_UNIT :
        return {'bytes':bytes/GB_CONVERSION_UNIT , "unit":"Gb"}
        
    if bytes>=MB_CONVERSION_UNIT :
        return {'bytes':bytes/MB_CONVERSION_UNIT , "unit":"Mb"}

    if bytes>=KB_CONVERSION_UNIT :
        return {'bytes':bytes/KB_CONVERSION_UNIT , "unit":"Kb"}
    
    return {'bytes':bytes , "unit":"Bytes"}

def check_flag_error(flag, error_message,args):
    #* some errors are thrown when the flag doesn't exist.
          if flag not in args:
            print(error_message)
            sys.exit()
     
#*flags
#4
merged_filename_flag = "--filename"
num_chunks_flag = "--num-files"
help_flag = "--help"
#keep_flag = "--keep"
force_delete_flag = "--force-delete"
extension_flag = "--ext"
chunks_filename_flag = "--filename-chunks"
default_chunk_name = "_temp-chunk.txt"
chunks_filename = 'None'

script_args = [arg.lower() for arg in sys.argv]

#* Help instructions.
intro = f"""{bold}{pink}{underline}Enter the Following values with their respective Flags:{end_color}"""
merged_filename_instruction = f"""{bold}{cyan}Merged Filename:  {grey}{ merged_filename_flag }{end_color}"""
num_chunks_instruction =f"""{bold}{warning}Number of chunks:  {grey}{ num_chunks_flag }{end_color}"""
ext_instruction = f"""{bold}{green}File extension : {grey} {extension_flag} {end_color}"""
filename_chunk_instruction =f"""{bold}{pink}-optional- {green}Token file name of Chunks: {grey} {chunks_filename_flag} {end_color}"""
help_instruction =f"""{bold}{pink}-optional- {bold}{warning}intructions for script:  {grey}{help_flag}{end_color}"""
keep_instruction =f"""{bold}{pink}-optional- {bold}{warning} keep or delete the original chunks after merging: {grey}{force_delete_flag}{end_color}"""
#no_chunks_instruction =f"""{bold}{pink}-optional- {bold}{warning}Remove Chunks without asking: {grey}{delete_chunks_flag}{end_color}"""
example_instruction = f"""{bold}{highlight_grey}example:{end_color} {end_color}{warning}python {end_color} combine.py {grey}{merged_filename_flag}{end_color} {cyan}myCopy.pt {warning} {grey}{num_chunks_flag}{end_color} {green}11{end_color} """

#* Error messages

NO_FILENAME_FLAG_ERROR = f"{bold}{fail}No file name provided. Use {grey}{merged_filename_flag}{fail} to name your result file. {end_color}"
NO_NUM_CHUNKS_ERROR = f"{bold}{fail}No chunk number provided. Use {grey}{num_chunks_flag}{fail} to indicate the number of chunks to sum. {end_color}"
NO_EXT_ERROR = f"{bold}{fail}No extension included. Use {grey}{extension_flag}{fail} to set the extension. {end_color}"
#KEEP_AND_DELETE_ERROR = f"{grey}{keep_flag}{end_color}{warning} and {grey}{delete_chunks_flag}{warning} are contradictory flags. Remove one of them according to your needs. use {grey} --help {warning} to see options{end_color}"


#* Warnings
KEEP_DELETE_WARNING = f"""{bold}{warning}data chunks will combine into a file and the chunks will be {fail}DELETED !{bold}{green} (exit and use flag {bold}{cyan}{force_delete_flag} {end_color}no{green} to combine and keep the chunks)
{bold}{warning}  do you want to continue?{fail} y/n {end_color}"""
HELP_INSTRUCTIONS =f""" \n{intro}\n
                1. {merged_filename_instruction}
                2. {num_chunks_instruction}
                3. {ext_instruction}
                4. {filename_chunk_instruction}
                5. {help_instruction}
                6. {keep_instruction}
                7. {warning}{bold}Default token chunk name: {cyan}{default_chunk_name}{end_color}
                
    \n{example_instruction}
          {end_color}"""

if "-help" in script_args or help_flag in script_args :
    print(HELP_INSTRUCTIONS)
    sys.exit()

#* error checking
check_flag_error(merged_filename_flag, NO_FILENAME_FLAG_ERROR , script_args)
check_flag_error(num_chunks_flag, NO_NUM_CHUNKS_ERROR , script_args)
check_flag_error(extension_flag, NO_EXT_ERROR , script_args)

#*get values
merged_filename = get_flag_value( merged_filename_flag, script_args )
ext = get_flag_value( extension_flag, script_args )
num_chunks = int( get_flag_value( num_chunks_flag, script_args ) )



#* special considerations for getting values
if chunks_filename_flag in script_args:
    chunks_filename = get_flag_value( chunks_filename_flag, script_args )
else:
     chunks_filename = default_chunk_name 

copy_ext = merged_filename.split(".")[1]


#* if --force-delete flag isn't raised, throw a warning
user_input_continue="yes"
delete_chunks = 'no'

if force_delete_flag not in script_args :
    user_input_continue = input(KEEP_DELETE_WARNING)
    is_user_answer_no = user_input_continue.lower() !="yes" and user_input_continue.lower() !="y"
    delete_chunks='yes'
    if is_user_answer_no:
        sys.exit()
else:
     delete_chunks = get_flag_value(force_delete_flag,script_args)
     
EXTENSION_MISMATCH_ERROR = f"""{bold}{fail}\nThe copy name extenstion in filename: {cyan}{merged_filename} {fail}doesn't match flag extention {grey}{extension_flag} {cyan}{ext}{end_color} 
{fail}{bold}Both must match to insure you combine the file into the correct extension. \n {end_color}"""
if ext != copy_ext:
     print(EXTENSION_MISMATCH_ERROR)
     sys.exit()


FIRST_FILE_NOT_EXIST = f"""{fail}{bold}ERROR: First chunk file is missing. Its likley that the chunk files don't exit, or inncorrect name provided to {grey}{chunks_filename_flag}{end_color}

 {warning}Default chunk name:  {cyan}{default_chunk_name} 
 
 {fail}make sure the chunks have the default name or provide the correct common name with {grey}{chunks_filename_flag} {end_color}"""

current_folder_files= os.listdir()

first_filename ="1"+chunks_filename
if first_filename not in current_folder_files:
     print(FIRST_FILE_NOT_EXIST)
     sys.exit()

#* count the number of chunks to combine
chunk_files_count=0
for file in current_folder_files:
     if chunks_filename in file:
          chunk_files_count+=1

#* check the count provided against the count detected in the actual file.
CHUNK_COUNT_MISMATCH = f"""{bold}{grey}\nText files with the token name :  {end_color}{chunks_filename} {grey} Don't match provided number{end_color} 

{chunks_filename} {grey}token files counted : {cyan}{chunk_files_count}

{grey}number of files to combine provided by {num_chunks_flag}: {cyan}{num_chunks}{grey}

The Program will either partially combine the files or will go over the available chunks and cause an error.
\n{warning}do you want to continue regardless? {fail}y/n {green}(correcting the number is highly recommended){end_color}"""
if chunk_files_count != num_chunks:
    continue_user_input = input(CHUNK_COUNT_MISMATCH)
    is_user_answer_no = continue_user_input.lower() !="yes" and continue_user_input.lower() !="y"
    if is_user_answer_no:
        sys.exit()


#* get chunks size
chunk_size = os.path.getsize(str(1) + chunks_filename)

#* determine the unit for the byte size

byte_and_unit = byte_to_Kilo_mega_giga(chunk_size)
adjusted_chunk_size = byte_and_unit["bytes"]
byte_unit = byte_and_unit["unit"]


#* open file to write
model_copy = open( merged_filename,mode="wb" )
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

is_keep_chunks = delete_chunks.lower() =="yes" or delete_chunks.lower() =="y"
if is_keep_chunks!=False and is_chunk_process_successful:
    print(f"{green}\nFile Combined !\n{end_color}")
    with alive_bar(num_chunks,bar="blocks",unit=" File",title="Delete",spinner="arrows_in") as bar:
        for i in range(1,num_chunks+1):
                    os.remove( str(i) + chunks_filename)
                    bar()


new_file_size = os.path.getsize(merged_filename)

unit = "B"

#* determine the unit for the byte size

byte_and_unit = byte_to_Kilo_mega_giga(new_file_size)
new_file_size = byte_and_unit["bytes"]
unit = byte_and_unit["unit"]

if is_chunk_process_successful:
     print(f"""\n{green}┌────────────────────────────────────────────────────────────────────────┐{end_color}""")
     print(f"""\n{green}{bold}  * File Merge Successful *{end_color}
        {bold} {grey} File created: {cyan}{merged_filename} {end_color}
        {bold} {grey} Number of chunks combined : {cyan} {num_chunks} Files{end_color}
        {bold} {grey} Were chunks deleted?  : {cyan} {is_keep_chunks}{end_color}
        {bold} {grey} Byte Size per chunk : {cyan} {adjusted_chunk_size} {byte_unit}  - {chunk_size} Bytes
        {bold} {grey} Merged File Size : {cyan} {round(new_file_size,2)} {unit}
            {end_color}""")  
     print(f"""{green}└────────────────────────────────────────────────────────────────────────┘{end_color}""")

