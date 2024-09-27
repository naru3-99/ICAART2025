import pyperclip

MAX_WORDS = 100

def make_prompt_eng(da_data):
    instructions = f"""## Instructions
We analyzed a suspicious program and obtained information about the system call invocation.
We extracted an important subsequence of these system calls.
Your task is to explain the overall behavior of the subsequence in less than {MAX_WORDS} words.
Specifically, mention whether the behavior can be considered malicious or if it can be classified as anti-debugging or anti-VM behavior.

## Format of the system call information
System Call Name,retval=Return Value,Arg1 Name=Value1,Arg2 Name=Value1,...
Note that the return values and argument values are represented as internal numbers (e.g., int or long types) and are not shown as readable names such as -EFAULT or -EINVAL.

## System Call Information
{da_data}
"""
    return instructions

if __name__ == '__main__':
    subseq = pyperclip.paste()
    revised = subseq.replace("\\x0a", "\n").replace("\\x09", "\t")
    pyperclip.copy(make_prompt_eng(revised))