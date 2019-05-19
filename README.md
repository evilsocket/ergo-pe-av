An artificial neural network and API to detect Windows malware, based on [Ergo](https://github.com/evilsocket/ergo) and [LIEF](https://lief.quarkslab.com/).

## Installation

    sudo pip3 install -r requirements.txt

### Use as an API

    ergo serve . --classes "clean, malware"

From the client:

    curl "http://localhost:8080/?x=/path/to/file.exe"

### Model Statistics

<img src="https://raw.githubusercontent.com/evilsocket/ergo-pe-av/master/history.png"/>

<img src="https://raw.githubusercontent.com/evilsocket/ergo-pe-av/master/training_cm.png"/> <img src="https://raw.githubusercontent.com/evilsocket/ergo-pe-av/master/test_cm.png"/> <img src="https://raw.githubusercontent.com/evilsocket/ergo-pe-av/master/validation_cm.png"/>

### License

Made with ♥  by [the dev team](https://github.com/evilsocket/ergo-pe-av/graphs/contributors) and it is released under the GPL 3 license.

