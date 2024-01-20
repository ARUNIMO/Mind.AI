from pathlib import Path
from typing import Any, Dict, List
import json
from urllib.request import urlretrieve


def download_file(url: str) -> Path:
    example_dirpath = Path(__file__).parent
    data_dirpath = example_dirpath / "data"
    data_dirpath.mkdir(exist_ok=True)
    filepath = data_dirpath / Path(url).name

    urlretrieve(url, filepath)
    return filepath


def print_emotions(emotions: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
    sorted_emotions = sorted(emotions, key=lambda x: x["score"], reverse=True)
    top_emotions = sorted_emotions[:top_n]
    
    print(top_emotions)

    json_data = json.dumps(top_emotions)
    file_path = 'data.json'
    with open(file_path, 'w') as json_file:
        json_file.write(json_data)

    return top_emotions

# Example usage:
# emotions_data = [...]  # Replace with your actual emotions data
# print_emotions(emotions_data, top_n=10)
