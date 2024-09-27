import pyperclip

MAX_WORDS = 200


def make_prompt_jp(da_data):
    instructions = f"""## 指示
マルウェアの可能性があるプログラムを解析し、呼び出されたシステムコールの情報を取得しました。
取得したシステムコールのシーケンスの中で、重要な部分シーケンスを抜き出しました。
あなたは、部分シーケンス全体の挙動を{MAX_WORDS}文字以内で説明してください。

## システムコールの情報の形式
システムコール名,retval=返り値,引数名1=値,引数名2=値,...

## システムコールの情報
{da_data}
"""
    return instructions


if __name__ == "__main__":
    subseq = pyperclip.paste()
    revised = subseq.replace("\\x0a", "\n").replace("\\x09", "\t")
    pyperclip.copy(make_prompt_jp(revised))
