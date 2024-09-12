from openai import OpenAI
from lib763.fs import (
    load_str_from_file,
    get_all_file_path_in,
    get_file_name,
    save_str_to_file,
    ensure_path_exists,
    save_object_to_file,
    load_object_from_file
)
from make_prompt_eng import make_prompt_eng
from CONST import TARGET_DATA_PATH, API_KEY_PATH, CHATGPT_MODEL, CHATGPT_RES_DIR

client = OpenAI(api_key=load_str_from_file(API_KEY_PATH).replace("\n", ""))


def throw_prompt(prompt):
    res = client.chat.completions.create(
        model=CHATGPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in the Linux kernel and system calls.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.1,
    )
    return res.choices[0].message.content


def throw_all_dadata():
    ensure_path_exists(CHATGPT_RES_DIR)
    for path in get_all_file_path_in(TARGET_DATA_PATH):
        if not get_file_name(path) == "subsequence.txt":
            continue
        current_malname = path.split("/")[-2]
        for i, subseq in enumerate(load_str_from_file(path).split("\n\n")):
            save_path = f"{CHATGPT_RES_DIR}{current_malname}_{i}.txt"
            prompt = make_prompt_eng(subseq)
            res = throw_prompt(prompt)
            save_str = f"{prompt}\n\n{res}"
            save_str_to_file(save_str, save_path)


if __name__ == "__main__":
    throw_all_dadata()
