import sys
import os
import math
from alive_progress import alive_bar;

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



#* one of these flags must exist. But only 1. if the size is bigger than 1, we throw an error
size_flags_counter=0

#* Flags
FILENAME_FLAG = "--filename"
BYTES_FLAG = "--size-bytes"
KBYTES_FLAG = "--size-kilobytes"
MBYTES_FLAG = "--size-megabytes"
GBYTES_FLAG = "--size-gigabytes"
EXT_FLAG = "--extention"
HELP_FLAG ="--help"
OUTPUT_FILENAME_FLAG ="--chunks-filename"

KB_CONVERSION_UNIT=1024
MB_CONVERSION_UNIT=1024 * 1024
GB_CONVERSION_UNIT= 1024 * 1024 * 1024

script_args = [arg.lower() for arg in sys.argv]
def get_chunk_size(flag,conversion ):
    chunk_size_index = script_args.index(flag) + 1 
    chunk_byte_size = int( script_args[chunk_size_index] )
    return chunk_byte_size * conversion


if BYTES_FLAG in script_args:
    # bytes_chosen_flag = BYTES_FLAG
    # chunk_size_index = script_args.index(BYTES_FLAG) + 1 
    chunk_byte_size = get_chunk_size(BYTES_FLAG,1)
    size_flags_counter+=1

if KBYTES_FLAG in script_args:
    chunk_byte_size = get_chunk_size(KBYTES_FLAG,KB_CONVERSION_UNIT)
    size_flags_counter+=1

if MBYTES_FLAG in script_args:
    chunk_byte_size = get_chunk_size(MBYTES_FLAG,MB_CONVERSION_UNIT)
    size_flags_counter+=1

if GBYTES_FLAG in script_args:
    chunk_byte_size = get_chunk_size(GBYTES_FLAG,GB_CONVERSION_UNIT)
    size_flags_counter+=1

if OUTPUT_FILENAME_FLAG in script_args:
    output_filename_index = script_args.index(OUTPUT_FILENAME_FLAG) + 1
    chunks_filename = script_args[output_filename_index]


filename_flag_instruction = f"""{bold}{cyan}Filename to split: {grey}{ FILENAME_FLAG }{end_color}{end_color}"""
bytes_flag_instructions = f"""{bold}{green}segment size in bytes, KiloBytes, MegaBytes or GigaBytes: {grey}{BYTES_FLAG} {cyan}- {grey}{KBYTES_FLAG} {cyan}- {grey}{MBYTES_FLAG} {cyan}- {grey}{GBYTES_FLAG} {end_color}  """
help_flag_instructions = f"""{bold}{pink}-optional- {bold}{warning}intructions for script:  {grey}{HELP_FLAG}{end_color}"""
example_instruction = f""" {bold}{highlight_grey}example:{end_color} {warning}python {end_color}split.py {grey}{FILENAME_FLAG} {cyan}fileToSplit.pt {grey}{BYTES_FLAG} {green}50000000 """
output_filename_instruction = f"""{bold}{pink}-optional- {warning} choose a name for output chunk files: {grey}{OUTPUT_FILENAME_FLAG}{end_color} """

#* text to display for when the help flag is raised
HELP_INSTRUCTIONS =f"""\n{end_color}{underline}{bold}{pink}Enter the Following values with their respective Flags:\n {end_color}
                1. {filename_flag_instruction}
                2. {bytes_flag_instructions}
                3. {output_filename_instruction}
                4. {help_flag_instructions}
                
                          
{example_instruction}
          {end_color}"""


#* display text when the file is not found

NO_FILENAME_FLAG_ERROR = f"{bold}{fail}No file name provided. Use {grey}{FILENAME_FLAG}{fail} to pick the file to split {end_color}"

NO_SIZE_ERROR = f"{bold}{fail}No size provided. Use {grey}--help {fail}to see avilable size flags{end_color}"

MULTI_SIZE_ERROR= f"{bold}{fail}You can only have one {grey} --size {fail} flag at once. use {grey}--help{fail} for options{end_color}"

file_name_counter=1

#* default chunks name
chunks_filename="_temp-chunk.txt" 


#* error checking
if HELP_FLAG in script_args:
    print(HELP_INSTRUCTIONS)
    sys.exit()

if FILENAME_FLAG not in script_args:
    print(NO_FILENAME_FLAG_ERROR)
    sys.exit()

    
#* if size_flags_counter is 0, it means no chunks size was provided
if size_flags_counter ==0:
    print(NO_SIZE_ERROR)
    sys.exit()

if size_flags_counter >1:
    print(MULTI_SIZE_ERROR)
    sys.exit()




file_to_split_index = script_args.index(FILENAME_FLAG) + 1 
filename = script_args[file_to_split_index]

#* check the size of the file to split. Then, calculate the number of resulting chunks
file_size = os.stat(filename).st_size
chunks_count = math.ceil(file_size/chunk_byte_size)


#* use has the flag for a different name, change the default name

FILE_NOT_FOUND_ERROR = f"{bold}{fail} ERROR: File named: {grey}{filename} {fail}does not exist. {end_color}"
if not os.path.isfile(filename):
    print(FILE_NOT_FOUND_ERROR)
    exit()

#* read the file
model_file = open(filename,mode="rb")



with alive_bar(chunks_count,bar="blocks",unit=" File",title="Split") as bar:
    for i in range(1,chunks_count+1) :
        data = model_file.read(chunk_byte_size)
        file_name=str(file_name_counter)+chunks_filename
        file = open(file_name,mode="wb")
        file.write(data)
        file.close()
        file_name_counter+=1
        bar()


byte_unit = 'B'
adjusted_chunk_size = chunk_byte_size


#* convert to bytes to kb,mb,gb
if chunk_byte_size >= GB_CONVERSION_UNIT :
    adjusted_chunk_size = chunk_byte_size/GB_CONVERSION_UNIT
    byte_unit = "Gb"

elif chunk_byte_size >= MB_CONVERSION_UNIT :
    adjusted_chunk_size = chunk_byte_size/MB_CONVERSION_UNIT
    byte_unit = "Mb"

elif chunk_byte_size >= KB_CONVERSION_UNIT :
    adjusted_chunk_size = chunk_byte_size/KB_CONVERSION_UNIT
    byte_unit = "Kb"


split_complete_message =f"""{green}{bold} \n  * File Split Successful *
      {grey}    Number of chunks created : {cyan} {file_name_counter-1}
      {grey}    Byte Size per chunk : {cyan} {adjusted_chunk_size} {byte_unit}  - {chunk_byte_size} Bytes  
         {end_color}"""

#
print(split_complete_message)  
model_file.close()

