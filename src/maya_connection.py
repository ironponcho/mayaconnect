import socket
from contextlib import contextmanager
import re
from itertools import islice

import config

MAYA_PYTHON_PORT = (config.maya_connection['host'], config.maya_connection['python_port'])
MAYA_MEL_PORT = (config.maya_connection['host'], config.maya_connection['mel_port'])
BATCH_SIZE = config.maya_connection['command_send_batch_size']
IS_DEBUG = config.maya_connection['is_debug']
BUFFER_LENGTH = config.maya_connection['buffer_length']


@contextmanager
def tcp_connection_to(*args, **kwargs):
    s = socket.create_connection(*args, **kwargs)
    yield s
    s.close()


def send_cmd(conn, cmd_batch):
    if len(cmd_batch) > BUFFER_LENGTH:
        raise Exception(
            f"The amount of the characters of the command exceed the specified buffer length of {BUFFER_LENGTH}. "
            f"Increase the buffer length or reduce the command chunk size.")
    conn.send(cmd_batch.encode())
    # print(cmd_batch)
    result = conn.recv(BUFFER_LENGTH).decode("UTF-8")
    result = re.sub('\W+', '', result)
    return result


def chunker(seq, size):
    it = iter(seq)
    return iter(lambda: tuple(islice(it, size)), ())


def send_python_commands(cmd_df):
    cmd_df = cmd_df.sort_values(by=["Command Type Order", "Command Order"])
    total_command_count = len(cmd_df.index)
    batches_needed = int(round(total_command_count / BATCH_SIZE, 0)) + 1
    print(f"{total_command_count} python commands were generated. Import will be chunked into {batches_needed} batches.")
    with tcp_connection_to(MAYA_PYTHON_PORT) as python_conn:
        if IS_DEBUG:
            # save results for the debug report
            cmd_df["Response"] = cmd_df.apply(lambda it: send_cmd(python_conn, it['Command']))
        else:
            batches_send = 0
            for batch in chunker(cmd_df['Command'], BATCH_SIZE):
                command_batch_str = ""
                for cmd in batch:
                    command_batch_str = command_batch_str + cmd + ";"
                send_cmd(python_conn, command_batch_str)
                batches_send += 1
                print(f"Maya command import progress: {round(batches_send / batches_needed, 2) * 100} %")
            print(f"Maya command import completed")
            return cmd_df


def purge_workspace():
    with tcp_connection_to(MAYA_MEL_PORT) as conn:
        send_cmd(conn, "file -f -new;")
