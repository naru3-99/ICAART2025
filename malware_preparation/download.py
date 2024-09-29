import requests
import os

# API URL
api_url = "https://mb-api.abuse.ch/api/v1/"

# 保存するディレクトリ
output_dir = "malware_samples"
os.makedirs(output_dir, exist_ok=True)

# APIに送信するデータ（ELFファイル取得）
payload = {
    'query': 'get_file_type',
    'file_type': 'elf',
    'limit': 500  # 取得するサンプル数
}

# APIにリクエストを送信
response = requests.post(api_url, data=payload)

if response.status_code == 200:
    result = response.json()

    if result['query_status'] == 'ok':
        for sample in result['data']:
            sha256_hash = sample['sha256_hash']
            # ファイル名をsha256.elfに設定
            file_name = f"{sha256_hash}.zip"
            download_payload = {
                'query': 'get_file',
                'sha256_hash': sha256_hash
            }

            # ファイルをダウンロード
            file_response = requests.post(api_url, data=download_payload)
            if file_response.status_code == 200:
                file_content = file_response.content
                file_path = os.path.join(output_dir, file_name)

                # ファイルを保存
                with open(file_path, 'wb') as f:
                    f.write(file_content)
                print(f"Downloaded and saved as {file_name}")
            else:
                print(f"Failed to download {sha256_hash}")
    else:
        print("No ELF samples found or query failed.")
else:
    print(f"Error: {response.status_code}")
