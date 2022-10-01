import config
import sys
from src import maya_connection
from service.file_processor import process_file
visualization_is_enabled = config.visualization['is_enabled']
BUFFER_LENGTH = config.maya_connection['buffer_length']

if __name__ == "__main__":

    if visualization_is_enabled:
        try:
            maya_connection.purge_workspace()
        except WindowsError:
            print("Could not connect to maya.")
            print("Make sure you opened the maya python & mel port: \n\n")
            print("----------------------------------------------\n")
            print("import maya.cmds as cmds")
            print(f"cmds.commandPort(name=\":{config.maya_connection['python_port']}\", noreturn=False, bufferSize={BUFFER_LENGTH}, sourceType=\"python\")")
            print(f"cmds.commandPort(name=\":{config.maya_connection['mel_port']}\", noreturn=False, bufferSize={BUFFER_LENGTH}, sourceType=\"mel\")")
            print("\n----------------------------------------------\n\n")
            sys.exit(1)

    process_file()
