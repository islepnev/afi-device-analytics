# QA Data Analysis

## Input Data

### Device Registry

Data is manually entered.
Storage: Google sheets

Exported CSV:
```
DNS Name,Serial Number,MAC Address,Box,Ecal Half Sector,
mpd-ecal-hs1-adc-1,0e74-f022,02:A6:B8:74:f0:22,1,1,
mpd-ecal-hs1-adc-2,0d11-985f,02:A6:B8:11:98:5f,1,1,поменять местами с нижней
mpd-ecal-hs1-adc-3,0d6b-92e6,02:A6:B8:6b:92:e6,1,1,поменять местами с верхней
mpd-ecal-hs1-adc-4,0e76-18e3,02:A6:B8:76:18:e3,1,1,
mpd-ecal-hs1-adc-5,0cd1-0fe2,02:A6:B8:d1:0f:e2,2,1,
mpd-ecal-hs1-adc-6,0cd0-a142,02:A6:B8:d0:a1:42,2,1,
mpd-ecal-hs1-adc-7,0cd1-7eef,02:A6:B8:d1:7e:ef,2,1,
mpd-ecal-hs1-adc-8,0cd0-bb91,02:A6:B8:d0:bb:91,2,1,
mpd-ecal-hs1-adc-9,0d6c-209d,02:A6:B8:6c:20:9d,3,1,
mpd-ecal-hs1-adc-10,0cd0-a13b,02:A6:B8:d0:a1:3b,3,1,
mpd-ecal-hs1-adc-11,0980-ae27,02:A6:B8:80:ae:27,3,1,
mpd-ecal-hs1-adc-12,0d6c-3307,02:A6:B8:6c:33:07,3,1,
mpd-ecal-hs2-adc-1,,02:A6:B8:10:EB:51,4,2,
mpd-ecal-hs2-adc-2,,02:A6:B8:AD:F2:93,4,2,
mpd-ecal-hs2-adc-3,,02:A6:B8:A0:CC:B5,4,2,
mpd-ecal-hs2-adc-4,,02:A6:B8:6B:92:6B,4,2,
mpd-ecal-hs2-adc-5,,02:A6:B8:75:B7:0A,5,2,
mpd-ecal-hs2-adc-6,,02:A6:B8:7F:BB:DF,5,2,
mpd-ecal-hs2-adc-7,,02:A6:B8:75:B6:F7,5,2,
mpd-ecal-hs2-adc-8,,02:A6:B8:D1:31:94,5,2,
mpd-ecal-hs2-adc-9,,02:A6:B8:7F:D7:7C,6,2,
mpd-ecal-hs2-adc-10,,02:A6:B8:7F:A5:54,6,2,
mpd-ecal-hs2-adc-11,,02:A6:B8:7F:65:E6,6,2,
mpd-ecal-hs2-adc-12,,02:A6:B8:7F:A5:60,6,2,
```

### Firmware Data

Storage: MySQL DB

Schema:
```csv
CREATE TABLE hw_firmware (
  id int(11) unsigned NOT NULL AUTO_INCREMENT,
  datetime timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  revision int(11) DEFAULT NULL,
  fw_maj int(11) DEFAULT NULL,
  fw_min int(11) DEFAULT NULL,
  git_hash varchar(40) DEFAULT NULL,
  base_name varchar(40) NOT NULL,
  pcb_name varchar(20) DEFAULT NULL,
  path text NOT NULL,
  fromHost text NOT NULL,
  goldImg tinyint(1) NOT NULL,
  serial int(11) NOT NULL,
  serialHex tinytext NOT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM AUTO_INCREMENT=15557 DEFAULT CHARSET=utf8;
```

Data sample:
```
"id","datetime","revision","fw_maj","fw_min","git_hash","base_name","pcb_name","path","fromHost","goldImg","serial","serialHex"
"15552","2024-12-09 13:50:53","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","215057809","0CD1-8591"
"15553","2024-12-09 13:50:53","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","242544689","0E74-F031"
"15554","2024-12-09 13:50:53","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","242593915","0E75-B07B"
"15555","2024-12-09 13:50:53","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","225198099","0D6C-4013"
"15556","2024-12-09 13:50:53","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","215028712","0CD1-13E8"
"15551","2024-12-09 13:50:52","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","225199094","0D6C-43F6"
"15549","2024-12-09 13:50:51","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","225198160","0D6C-4050"
"15550","2024-12-09 13:50:51","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","242545096","0E74-F1C8"
"15547","2024-12-09 13:50:50","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","225189921","0D6C-2021"
"15548","2024-12-09 13:50:50","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","242621554","0E76-1C72"
"15545","2024-12-09 13:50:48","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","242544259","0E74-EE83"
"15546","2024-12-09 13:50:48","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","1","242573277","0E75-5FDD"
"15544","2024-12-09 13:48:06","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","242593915","0E75-B07B"
"15542","2024-12-09 13:48:05","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","225198099","0D6C-4013"
"15543","2024-12-09 13:48:05","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","215057809","0CD1-8591"
"15541","2024-12-09 13:48:04","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","242544689","0E74-F031"
"15540","2024-12-09 13:48:03","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","215028712","0CD1-13E8"
"15536","2024-12-09 13:48:02","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","225199094","0D6C-43F6"
"15537","2024-12-09 13:48:02","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","225189921","0D6C-2021"
"15538","2024-12-09 13:48:02","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","225198160","0D6C-4050"
"15539","2024-12-09 13:48:02","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","242573277","0E75-5FDD"
"15534","2024-12-09 13:48:01","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","242621554","0E76-1C72"
"15535","2024-12-09 13:48:01","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","242545096","0E74-F1C8"
"15533","2024-12-09 13:48:00","0","1","8","196bb6a","adc64ecal_felink-1.8-0-g196bb6a.bit",NULL,"/net/afi-nas/vol/firmware/fpga/auto/adc64ecal_felink/adc64ecal_felink-1.8-0-g196bb6a.bit","st42-ecal.example.com","0","242544259","0E74-EE83"
"15532","2024-12-09 12:10:43","0","1","7","bdc1392","ttvxs-1.7-0-gbdc1392.bit",NULL,"/net/afi-nas/vol/firmware/fpga/release/ttvxs/ttvxs-1.7-0-gbdc1392.bit","tof-stand-1.example.com","0","178248011","0A9F-D94B"
```

#### Post-Processing

Ignore id
Reconstruct version: `f"{fw_maj}.{fw_min}.{revision}"`
Split `{base_name: "adc64ecal_felink-1.8-0-g196bb6a.bit"}` to `{firmware: "adc64ecal_felink", version: "1.8-0", git_hash: "g196bb6a"}`. Ignore git_hash (duplicates git_hash column).
Rename fields: `serialHex` -> `serial_number`

## Task: Write python script

Fecth from `Firmware Data`
Read `Device Registry` CSV from stdin or from file specified by argument
Normalize column name for internal data structures: 'lower_case'
Serial numbers: ignore case

Group entries by serial, goldImg. Select latest by datetime.

Join `Firmware Data` and `Device Registry` by serial_number.

Output joined data as CSV table (specified as second positional argument or to STDOUT)

## Data Integrity

Duplicate Serial Numbers in Device Registry: log warning, use first.
Missing Data in Device Registry: keep row, leave empty cells.
Priority: group by both columns (serial_number, goldImg), then output latest by datetime.

## Coding preferences

Python, VSCode, Git.
Securely store credentials in .env
Use venv: `python -m venv .venv`
Create file requirements.txt
Create file .gitignore
Read csv filename as first positional argument, or read from STDIN.
Use argparse module, add '-d', '--debug' options.
Use logging module, log to console.

Modular app for easy support and extensions.

## Task analysis

Analyse requirements for consistency before implementation.
Ask me for decision when requirements is obscure or unclear.

## Answer Preferences

Output script source code as code block
