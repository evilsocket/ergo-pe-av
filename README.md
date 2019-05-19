An artificial neural network and API to detect Windows malware, based on [Ergo](https://github.com/evilsocket/ergo) and [LIEF](https://lief.quarkslab.com/).

## Installation

    sudo pip3 install -r requirements.txt

### Use as an API

    ergo serve . --classes "clean, malware"

From the client:

    curl "http://localhost:8080/?x=/path/to/file.exe"

### Model Statistics

The dataset is made of ~200000 samples divided in two subfolders:

- `classes/pe-malicious` with 100000 malware samples from VirusTotal
- `classes/pe-clean` with 100000 clean samples

The `dataset.csv` training file has been generated with:

    ergo encode ergo-pe-av /media/evilsocket/4TB/datapath-pe/classes --filter "*.exe"

<img src="https://raw.githubusercontent.com/evilsocket/ergo-pe-av/master/history.png"/>

| Training | Validation | Testing |
|----------|------------|---------|
![](https://raw.githubusercontent.com/evilsocket/ergo-pe-av/master/training_cm.png) | ![](https://raw.githubusercontent.com/evilsocket/ergo-pe-av/master/validation_cm.png) | ![](https://raw.githubusercontent.com/evilsocket/ergo-pe-av/master/test_cm.png) |

### License

Made with ♥  by [the dev team](https://github.com/evilsocket/ergo-pe-av/graphs/contributors) and it is released under the GPL 3 license.

