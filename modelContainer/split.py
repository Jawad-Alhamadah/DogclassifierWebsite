import sys
import os
import math
import time
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


def byte_to_Kilo_mega_giga(bytes):
    if bytes>=GB_CONVERSION_UNIT :
        return {'bytes':bytes/GB_CONVERSION_UNIT , "unit":"Gb"}
        
    if bytes>=MB_CONVERSION_UNIT :
        return {'bytes':bytes/MB_CONVERSION_UNIT , "unit":"Mb"}

    if bytes>=KB_CONVERSION_UNIT :
        return {'bytes':bytes/KB_CONVERSION_UNIT , "unit":"Kb"}
    
    return {'bytes':bytes , "unit":"Bytes"}


#* one of these flags must exist. But only 1. if the size is bigger than 1, we throw an error
size_flags_counter=0

#* Flags
FILENAME_FLAG = "--filename"
BYTES_FLAG = "--size-bytes"
KBYTES_FLAG = "--size-kilobytes"
MBYTES_FLAG = "--size-megabytes"
GBYTES_FLAG = "--size-gigabytes"
HELP_FLAG ="--help"
OUTPUT_FILENAME_FLAG ="--filename-chunks"

#* default chunks name
chunks_filename="_temp-chunk.txt" 


KB_CONVERSION_UNIT=1024
MB_CONVERSION_UNIT=1024 * 1024
GB_CONVERSION_UNIT= 1024 * 1024 * 1024


script_args = [arg.lower() for arg in sys.argv]

def get_chunk_size(flag,conversion ):
    chunk_size_index = script_args.index(flag) + 1 
    chunk_byte_size = int( script_args[chunk_size_index] )
    return chunk_byte_size * conversion

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
if HELP_FLAG in script_args:
    print(HELP_INSTRUCTIONS)
    sys.exit()

#* all flags need a value. This checks if the script args are even. If not, throw an error
#*
flags_count = sum("--" in arg for arg in script_args)
if (len(script_args)-1) -flags_count != flags_count:
    print(f"{fail} Some flags don't have a value. {end_color}")
    sys.exit()

if BYTES_FLAG in script_args:
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

file_to_split_index = script_args.index(FILENAME_FLAG) + 1 
filename = script_args[file_to_split_index]


#* display text when the file is not found

NO_FILENAME_FLAG_ERROR = f"{bold}{fail}No file name provided. Use {grey}{FILENAME_FLAG}{fail} to pick the file to split {end_color}"

NO_SIZE_ERROR = f"{bold}{fail}No size provided. Use {grey}--help {fail}to see avilable size flags{end_color}"

MULTI_SIZE_ERROR= f"{bold}{fail}You can only have one {grey} --size {fail} flag at once. use {grey}--help{fail} for options{end_color}"


#* error checking
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

#* use has the flag for a different name, change the default name
FILE_NOT_FOUND_ERROR = f"{bold}{fail} ERROR: File named: {grey}{filename} {fail}does not exist. {end_color}"
if not os.path.isfile(filename):
    print(FILE_NOT_FOUND_ERROR)
    sys.exit()



#* check the size of the file to split. Then, calculate the number of resulting chunks
file_size = os.stat(filename).st_size
chunks_count = math.ceil(file_size/chunk_byte_size)

# ToDo check if the chunks already exist. If so, delete them first.

KEEP_DELETE_WARNING = f"""{bold}{warning} chunk files named {cyan}{chunks_filename} {warning}already exist. Do you want to overwrite them? y/n {end_color}"""

delete_or_keep_user_input =''
first_filename ="1"+chunks_filename
if first_filename in os.listdir():
     delete_or_keep_user_input = input(KEEP_DELETE_WARNING)
     is_user_answer_no = delete_or_keep_user_input.lower() !="yes" and delete_or_keep_user_input.lower() !="y"
     if is_user_answer_no:
      sys.exit()  


#* if answer is no, print an error

#* read the file
model_file = open(filename,mode="rb")

is_success = True
i=1
with alive_bar(chunks_count,bar="blocks",unit=" File",title="Split") as bar:
    while i<=chunks_count :
        try:
            data = model_file.read(chunk_byte_size)
            file_name=str(i)+chunks_filename
            file = open(file_name,mode="wb")
            file.write(data)
            bar()
            i=i+1
            
        except OSError as e:
            print(f""" {fail}Failed to create file, retrying{end_color}""")
            
        finally:
            file.close()
        

adjusted_chunk_size = chunk_byte_size


#* convert to bytes to kb,mb,gb
byte_and_unit = byte_to_Kilo_mega_giga(adjusted_chunk_size)
adjusted_chunk_size = byte_and_unit["bytes"]
byte_unit = byte_and_unit["unit"]


split_complete_message =f"""\n{green}{bold} * File Split Successful *                                                                            
      {grey}    Number of chunks created : {cyan} {chunks_count}                                        
      {grey}    Size per chunk : {cyan} {adjusted_chunk_size} {byte_unit}  - {chunk_byte_size} Bytes               
         {end_color}"""

print(f"""\n{green}┌────────────────────────────────────────────────────────────────────────┐{end_color}""")
print(split_complete_message)  
print(f"""{green}└────────────────────────────────────────────────────────────────────────┘{end_color}""")
model_file.close()

