import datetime
import os
import re
from time import sleep

import datetime
import os
from re import X
import re
import shutil
import ntpath
from time import sleep

from models.settings import *

def createDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def create_folder_in_directory(parent_path, folder_name):
    # todo later check for /
    if not parent_path.endswith('/'):
        path = parent_path + '/' + folder_name
    else:
        path = parent_path + folder_name
    if not os.path.exists(path):
        os.makedirs(path)

# finsih plot lifetime

def my_file_copy_to_directory(source_path, destination_directory, destination_filename_additional_naming='',append_filename_additional_part = False):
    file_basename = ntpath.basename(source_path)
    if destination_filename_additional_naming == '':
        destination_path = f'{destination_directory}/{file_basename}'
    else:
        if not append_filename_additional_part:
            destination_path = f'{destination_directory}/{destination_filename_additional_naming}_{file_basename}'
        else:
             destination_path = f'{destination_directory}/{file_basename}_{destination_filename_additional_naming}'

    # https://www.geeksforgeeks.org/python-shutil-copyfile-method/
    shutil.copyfile(source_path, destination_path)

def copy_file_new_name(source_path, destination_directory, new_name):
    destination_path = f'{destination_directory}/{new_name}'
    shutil.copy(source_path, destination_path)

def my_data_write_to_directory(data, destination_directory, file_basename, filename_prefix='', ext='.txt'):
    destination_path = f'{destination_directory}/'
    if filename_prefix != '':
        destination_path = destination_path + f'{filename_prefix}_'
    destination_path = destination_path + f'{file_basename}{ext}'

    my_data_write(data, destination_path)

def my_data_write(data, filepath):
    python_file = open(filepath, "w")
    python_file.write(data)
    python_file.close()


def my_data_append(data, filepath):
    python_file = open(filepath, "a")
    python_file.write('\n'+str(data))
    python_file.close()

def my_print(s, always_print_to_console = False):
    if settings.silent_console:
        if always_print_to_console:
            print(s)
        my_data_append(data=s,filepath=settings.temp_log_file_path)
    else:
        print(s)
        my_data_append(data=s,filepath=settings.temp_log_file_path)
        pass

class FilesHelper:  # keep it reusable, flexible, and generic. Helpfull to know what methods we have while developing. todo move other things to here and rename

    def build_filename_append(variables_dictionery, template_bracket_based):
      # variables_dictionery = {
      #   'apple_price': 50,
      #   'orange_price': 40,
      # }
      return substitute_vars_in_template_brackets_based(variables_dictionery, template_bracket_based)

    def get_l1_directory_path(parent_directory=None, l1_folder_name=None):
        dir = parent_directory
        if not dir:
            dir = '.'
        if l1_folder_name:
            dir = dir + f'/{l1_folder_name}'
        return dir

    def create_output_directory(parent_directory=None, l1_folder_name=None, l2_folder_name=None):
        output_directory=""
        # if user_specifies_parent_directory:
        #     output_directory = input("Please enter prefered output PARENT DIRECTORY PATH:\n").rstrip(
        #         '/')  # remove any ending slash
        #     print(f'You entered directory: {output_directory}')
        #     input("Press any key to continue, or stop to correct folder name.\n")

        l1_folder_path= FilesHelper.get_l1_directory_path(parent_directory, l1_folder_name)
        if l2_folder_name:
            output_directory = l1_folder_path + f'/{l2_folder_name}'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        return output_directory
def readable_current_datetime():
    sleep(2) # as datetime is used in filenames, make sure filenames will be different. can check if %f is enouph later.
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d-%H-%M-%S-%f")

def substitute_vars_in_template_brackets_based(variables_dictionery, template):
    # text = "Apple costs $ [apple_price] and Orange costs $ [orange_price] $ [does_not_exist]"
    return re.sub(
            r"[\[](.*?)[\)\]]",
            lambda m: str(variables_dictionery.get(m.group(1), m.group(0))),
            template,)

def clean_file_name(sourcestring,  removestring =" %:/,.\\[]<>*?"):
  # copied from https://www.programcreek.com/python/?CodeExample=clean+filename
    """Clean a string by removing selected characters.

    Creates a legal and 'clean' source string from a string by removing some 
    clutter and  characters not allowed in filenames.
    A default set is given but the user can override the default string.

    Args:
        | sourcestring (string): the string to be cleaned.
        | removestring (string): remove all these characters from the string (optional).

    Returns:
        | (string): A cleaned-up string.

    Raises:
        | No exception is raised.
    """
    #remove the undesireable characters
    try:
        name = ''.join([c for c in sourcestring if c not in removestring])
    except Exception as e:
        my_print(e)
        #raise e
    return name    #todo remove white space
    
def test_substitute_vars_in_template_brackets_based():
    variables_dictionery = {
    'apple_price': 50,
    'orange_price': 40,
    }
    #print(substitute_vars_in_template_brackets_based( variables_dictionery, "Apple costs $ [apple_price] and Orange costs $ [orange_price] $ [does_not_exist]"))


if __name__ == '__main__':
    test_substitute_vars_in_template_brackets_based()