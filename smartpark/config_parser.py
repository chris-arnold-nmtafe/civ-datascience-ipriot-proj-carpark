"""A class or function to parse the config file and return the values as a dictionary.

The config file itself can be any of the following formats:

- ryo: means 'roll your own' and is a simple text file with key-value pairs separated by an equals sign. For example:
```
location = "Moondalup City Square Parking"
number_of_spaces = 192
```
**you** read the file and parse it into a dictionary.
- json: a json file with key-value pairs. For example:
```json
{location: "Moondalup City Square Parking", number_of_spaces: 192}
```
json is built in to python, so you can use the json module to parse it into a dictionary.
- toml: a toml file with key-value pairs. For example:
```toml
[location]
name = "Moondalup City Square Parking"
spaces = 192
```
toml is part of the standard library in python 3.11, otherwise you need to install tomli to parse it into a dictionary.
```bash
python -m pip install tomli
```
see [realpython.com](https://realpython.com/python-toml/) for more info.

Finally, you can use `yaml` if you prefer.



"""
# smartpark/config_parser.py
import tomli  # Python 3.11未満では tomli が必要（pip install tomli）

def parse_config(filepath: str) -> dict:
    """TOMLファイルを読み込んで辞書として返す"""
    with open(filepath, "rb") as file:
        config = tomli.load(file)

    # 必要な値を取得（[parking_lot] セクション前提）
    if "parking_lot" in config:
        parking = config["parking_lot"]
        return {
            "name": "raf-park",  # 名前は固定でもOK
            "location": parking["location"],
            "total-spaces": parking["total_spaces"],
            "total-cars": 0,
            "broker": parking["broker_host"],
            "port": parking["broker_port"],
            "topic-root": "lot",
            "topic-qualifier": "entry"
        }
    else:
        raise ValueError("Missing [parking_lot] section in config.")
