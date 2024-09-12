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