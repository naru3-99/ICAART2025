# パケットを解釈するための制御文字
# splitting syscall data by this delimiter
SCLDA_DELIMITER = 7
# msg must start with this
SCLDA_MSG_START = 18
# msg must end with this
SCLDA_MSG_END = 20

# decode format
DECODE = "ASCII"

# port number
PORT_NUMBER = 16

# directory setting
RAW_DATA_PATH = "./DAData/"
ANALYZED_DIRNAME = "output/"
PACKET_DIRNAME = "input/"
PACKET_PID_DIRNAME = "PID/"
TARGET_DATA_PATH = "./target/"
SYSCALL_INFO_PATH = "./syscall_info.csv"
