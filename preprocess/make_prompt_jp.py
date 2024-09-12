from lib763.fs import *
import pyperclip

max_answer_len = 200

subseq = pyperclip.paste()
revised = subseq.replace('\\x0a',"\n").replace('\\x09',"\t")


instructions = f"""
## 指示
マルウェアの可能性があるプログラムを解析し、呼び出されたシステムコールの情報を取得しました。
取得したシステムコールのシーケンスの中で、重要な部分シーケンスを抜き出しました。
あなたは、部分シーケンス全体の挙動を{max_answer_len}文字以内で説明してください。

## システムコールの情報の形式
システムコール名,retval=返り値,引数名1=値,引数名2=値,...

## システムコールの情報
{revised}
"""

pyperclip.copy(instructions)
