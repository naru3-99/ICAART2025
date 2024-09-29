# ICAART2025

## get started
install lib763 (custom python library made by naru3)
```
git clone https://github.com/naru-99/lib763.git
cd lib763
chmod +x install.sh
sudo ./install.sh
```

## directory
- malware_preparation/: gather malware from [Malware Bazzar](https://bazaar.abuse.ch/), `unzip` all downloaded payloads, `rm -rf` all 32-bit architecture elf files (because our test environment is 64-bit) and `chmod +x` to all malware samples.

- preprocess/: process captured data (sclda_host/[tcp, udp]/input/**.pickle), and create prompt for ChatGPT

## data samples
- DAData.zip: captured data (sclda_host/[tcp, udp]/input/**.pickle), which is used in preprocess/ directory
> https://drive.google.com/file/d/15-jrNknAEZYA29maozkojC9NnRpiWSNZ/view?usp=drive_link

- Processed DA data: Processed sample data in preprocess/ directory
> https://drive.google.com/drive/folders/1tS1pyxBDLzzUE4fR9LzUqhonQZo8Ulam?usp=sharing

- Key Chat (presented in my paper)
> - https://chatgpt.com/share/66f4fa02-3788-800c-b321-949fd05ac68a
> - https://chatgpt.com/share/66f6390b-a794-800c-a7a8-0a31bd55598f
> - https://chatgpt.com/share/66f7c5f0-2c6c-800c-a073-1d973f5ab37b
> - https://chatgpt.com/share/66f8d9e9-9138-800c-964e-3d71031bd750