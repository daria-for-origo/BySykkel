BySykkel
========
Retrieve city bicycle stands information for public API

* User has to provide a path to auto-discovery file in gbfs format.
* By default, Oslo City Information is retrieved and presented
* List of bicycle stations is sorted by the distance from the user
* Dump version allows retrieving of data in customized output format (see --dump_format)
* Demo version allows manual update of the current user position
* Automated version current position is only a place holder for now




## Usage

* python(3) ride/dump.py
* python(3) ride/main.py --help
* python(3) ride/main.py --demo


## API
* BySykkelAPI.py presents <del>an amateur</del> preliminary version of REST-based endpoint for retrieving all or specific station info in json format
#### Usage: 
* BySykkelAPI.request("stations")
* BySykkelAPI.request("stations/id")
* BySykkelAPI.request("stations?top=k&bikes=n&docks=m&gps=[lat,lon]")
* BySykkelAPI.request("stations/id/?gps=[lat,lon]")

#### Examples and Test
* python(3) BySykkelAPI.py query]
* python(3) BySykkelAPI.py --help
* python(3) test/API.py



## Windows Notes 

* Python 3.6 and up


## Ubuntu on Windows 10 Notes

* install XMing on windows

* apt-get install python3
* apt-get install python3-tk (Sic!)
* echo "export DISPLAY:=0" >> ~/.bashrc

## Linux

Presumably, the only requirement for any linux environment is python3. Having said that, I hadn't tried


## macOS

Is a unicorn