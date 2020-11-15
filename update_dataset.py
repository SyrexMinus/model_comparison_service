import requests
import os
import sys



if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python update_dataset.py url file_path info")
        sys.exit(0)
    url = sys.argv[1]
    file_path = sys.argv[2]
    info = sys.argv[3]        

    ds = open(file_path, "rb")
    response = requests.post(url, data={"description": info}, files={"dataset": ds})
    print(response.json())