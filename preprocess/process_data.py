import time

from lib763.fs import (
    get_all_file_path_in,
    get_all_dir_names_in,
    get_file_name_without_ext,
    load_str_from_file,
    ensure_path_exists,
    save_str_to_file,
    is_exists,
)
from lib763.multp import start_process, is_process_alive

from Analyzer.pid import process_pid
from Analyzer.syscall import process_sc

from CONST import (
    RAW_DATA_PATH,
    TARGET_DATA_PATH,
    ANALYZED_DIRNAME,
    PACKET_DIRNAME,
    PACKET_PID_DIRNAME,
)

FS_SYSCALL_LS = [
    "0-read",
    "1-write",
    "2-open",
    "3-close",
    "17-pread64",
    "18-pwrite64",
    "19-readv",
    "20-writev",
    "32-dup",
    "33-dup2",
    "79-getcwd",
    "80-chdir",
    "81-fchdir",
    "82-rename",
    "83-mkdir",
    "84-rmdir",
    "85-creat",
    "86-link",
    "87-unlink",
    "88-symlink",
    "89-readlink",
    "90-chmod",
    "91-fchmod",
    "92-chown",
    "93-fchown",
    "94-lchown",
    "257-openat",
    "263-unlinkat",
    "264-renameat",
    "267-readlinkat",
    "292-dup3",
    "316-renameat2",
]

SOCKET_SYSCALL_LS = [
    "40-sendfile",
    "41-socket",
    "42-connect",
    "43-accept",
    "44-sendto",
    "45-recvfrom",
    "46-sendmsg",
    "47-recvmsg",
    "49-bind",
    "50-listen",
    "51-getsockname",
    "52-getpeername",
    "53-socketpair",
    "54-setsockopt",
    "55-getsockopt",
]

OTHER_SYSCALL_LS = [
    "21-access",
    "59-execve",
    "62-kill",
    "101-ptrace",
    "200-tkill",
    "231-exit_group",
    "234-tgkill",
    "322-execveat",
]


SYSCALL_LIST = FS_SYSCALL_LS + SOCKET_SYSCALL_LS + OTHER_SYSCALL_LS

SYSCALL_INFO_PATH = "./syscall_info.csv"

# (str)syscall id -> (str)syscall nameの辞書を段取り
id_data_dict = {}
for row in load_str_from_file(SYSCALL_INFO_PATH).split("\n"):
    splited_row = row.split(",")
    if len(splited_row) == 0:
        continue
    id_data_dict[f"{splited_row[1]}-{splited_row[0]}"] = [
        x for x in splited_row[2:] if (len(x) != 0)
    ]


def packet_to_csv(target_dir):
    # target_dir = "./DAData/NOT_{hash}"
    input_dir = f"{target_dir}{PACKET_DIRNAME}"
    output_dir = f"{target_dir}{ANALYZED_DIRNAME}"
    if not is_exists(input_dir):
        print(f"no such directry:{input_dir}")
        return
    ensure_path_exists(output_dir)

    # process pid first
    pid_input_dir = f"{input_dir}{PACKET_PID_DIRNAME}"
    dir_len = len(get_all_file_path_in(pid_input_dir))
    process_pid(
        [f"{pid_input_dir}{p}.pickle" for p in range(dir_len)], f"{output_dir}pid.csv"
    )

    # process syscall
    process_ls = []
    for d in get_all_dir_names_in(input_dir):
        if "PID" in d:
            continue
        dir_len = len(get_all_file_path_in(f"{input_dir}{d}/"))
        arg_list = [f"{input_dir}{d}/{i}.pickle" for i in range(dir_len)]
        p = start_process(process_sc, arg_list, int(d), output_dir)
        process_ls.append(p)

    while any(is_process_alive(p) for p in process_ls):
        time.sleep(1)


def __get_descendant_pids(pid_ppid_ls, target_pid):
    # PIDとその子プロセスのリストを保持するための辞書を作成
    ppid_to_children = {}
    for pid, ppid in pid_ppid_ls:
        if ppid not in ppid_to_children:
            ppid_to_children[ppid] = []
        ppid_to_children[ppid].append(pid)

    # 子プロセスを再帰的に取得する関数
    def collect_descendants(pid, result):
        result.append(pid)  # 現在のPIDを結果に追加
        if pid in ppid_to_children:  # このPIDに対応する子がいる場合
            for child_pid in ppid_to_children[pid]:
                collect_descendants(child_pid, result)  # 子プロセスを再帰的に収集

    # 結果を格納するリスト
    result = []
    # 与えられたPIDの子孫を収集
    collect_descendants(target_pid, result)

    return result


def extract_target_piddata(dirname: str):
    target_name = dirname.split("_")[1]
    current_dir = f"{RAW_DATA_PATH}{dirname}/output/"
    pid_csv = ""
    num_csv_ls = []
    for p in get_all_file_path_in(current_dir):
        if get_file_name_without_ext(p) == "pid":
            pid_csv = p
        else:
            if not get_file_name_without_ext(p).isdigit():
                continue
            num_csv_ls.append(p)

    if len(pid_csv) == 0:
        print(f"err: no pid.csv, {dirname}")
        return

    pid_ppid_ls = []
    for row in load_str_from_file(pid_csv).split("\n"):
        splited = row.split("\t")
        if not (len(splited) == 3):
            print(f"len must be 3: {splited}")
            continue
        if not (splited[0].isdigit() and splited[1].isdigit()):
            print(f"pid must be digit: {splited}")
            continue
        pid_ppid_ls.append([int(splited[0]), int(splited[1])])

    started_pid = 0
    for num_csv in num_csv_ls:
        for row in load_str_from_file(num_csv).split("\n"):
            scdata_ls = row.split("\t")
            if len(scdata_ls) < 5:
                continue
            if not (scdata_ls[1] == "59-execve" or scdata_ls[1] == "322-execveat"):
                continue
            if not (target_name in scdata_ls[3]):
                continue
            started_pid = int(get_file_name_without_ext(num_csv))
            break

    target_pid_ls = __get_descendant_pids(pid_ppid_ls, started_pid)

    ensure_path_exists(f"{TARGET_DATA_PATH}{dirname}/")
    for pid in target_pid_ls:
        save_str_to_file(
            load_str_from_file(f"{current_dir}{pid}.csv"),
            f"{TARGET_DATA_PATH}{dirname}/{pid}.csv",
        )
    return


def filter_data(dn):
    current_dir = f"{TARGET_DATA_PATH}{dn}/"
    for path in get_all_file_path_in(current_dir):
        data_ls = []
        for row in load_str_from_file(path).split("\n"):
            splited_row = row.split("\t")
            if splited_row[1] in SYSCALL_LIST:
                data_ls.append("\t".join(splited_row))
        save_str_to_file("\n".join(data_ls), path)


def __reformat_data(path):
    revised_ls = []
    for row in load_str_from_file(path).split("\n"):
        splited = [x for x in row.split("\t") if (len(x) != 0)][1:]
        if len(splited) == 0:
            continue
        temp_data = []
        data = id_data_dict[splited[0]]
        temp_data.append(splited[0].split("-")[1])
        for x in range(min(len(data), len(splited[1:]))):
            temp_data.append(f"{data[x]}={splited[x+1]}")
        if len(data) < len(splited[1:]):
            temp_data.append("".join(splited[len(data) + 1 :]))
        revised_ls.append(",".join(temp_data))
    if len(revised_ls) == 0:
        return
    save_str_to_file("\n".join(revised_ls), path)


def reformat_data():
    for dn in get_all_dir_names_in(TARGET_DATA_PATH):
        curdir = f"{TARGET_DATA_PATH}{dn}/"
        for path in get_all_file_path_in(curdir):
            __reformat_data(path)


if __name__ == "__main__":
    for dn in get_all_dir_names_in(RAW_DATA_PATH):
        print(dn)
        packet_to_csv(f"{RAW_DATA_PATH}{dn}/")

    ensure_path_exists(TARGET_DATA_PATH)
    for dn in get_all_dir_names_in(RAW_DATA_PATH):
        extract_target_piddata(dn)

    for dn in get_all_dir_names_in(TARGET_DATA_PATH):
        filter_data(dn)

    reformat_data()
