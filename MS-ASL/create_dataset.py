import json
import pytube
import os
import pytube.exceptions
from tqdm import tqdm


TRAIN_JSON = 'MS-ASL/MSASL_train.json'
TEST_JSON = 'MS-ASL/MSASL_test.json'
VAL_JSON = 'MS-ASL/MSASL_val.json'

noOfFiles = 20
FILE_DIR = 'MS-ASL/'
DATA_DIR = 'MS-ASL/data'

def _check_id_(file):
    d = []
    with open(file, 'r') as f:
        x = json.load(f)
        for i, doc in enumerate(x):
            if 'id' not in doc.keys():
                doc['id'] = i
            d.append(doc)

    with open(file, 'w') as f:
        json.dump(d, f, indent = 2)

def _logs_(logs, name):
    if not os.path.isdir(FILE_DIR+'/logs'):
        os.mkdir(FILE_DIR+'/logs')

    with open(os.path.join(FILE_DIR+'/logs',f'{name}_logs.json'), 'w') as f:
        json.dump(logs, f, indent=2)

def download_videos(dataset):
    log = []
    with open(dataset, 'r') as f_read:
        videos = json.load(f_read)[:noOfFiles]

        for i, video in enumerate(tqdm(videos)):
            video['id'] = i
            log.append({video['id']:fetch_video(video['url'])})

    return log

def fetch_video(url:str):
    try:
        yt = pytube.YouTube(url)

        mp4_streams = yt.streams.filter(file_extension='mp4').first()
        mp4_streams.download(output_path = DATA_DIR)
        return 'Success'
    
    except pytube.exceptions.VideoPrivate:
        return 'Private Video'
    
    except pytube.exceptions.VideoUnavailable:
        return 'Unavailable'
    
    except pytube.exceptions.PytubeError:
        return 'Unknown Failure'

def main():
    _check_id_(TRAIN_JSON)
    set_name = 'train'

    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    
    status_log = download_videos(TRAIN_JSON)
    _logs_({set_name:status_log}, set_name)

if __name__ == '__main__':
    main()

