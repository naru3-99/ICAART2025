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
- get_data/: gather malware from [Malware Bazzar](https://bazaar.abuse.ch/), `unzip` all downloaded payloads, `rm -rf` all 32-bit architecture elf files (because our test environment is 64-bit) and `chmod +x` to all malware samples.

- preprocess/: process captured data (sclda_host/[tcp, udp]/input/**.pickle), and create prompt for ChatGPT

## data samples
- DAData.zip: captured data (sclda_host/[tcp, udp]/input/**.pickle), which is used in preprocess/ directory
> https://drive.google.com/file/d/15-jrNknAEZYA29maozkojC9NnRpiWSNZ/view?usp=drive_link

- Processed DA data: Processed sample data in preprocess/ directory
> https://drive.google.com/drive/folders/1tS1pyxBDLzzUE4fR9LzUqhonQZo8Ulam?usp=sharing