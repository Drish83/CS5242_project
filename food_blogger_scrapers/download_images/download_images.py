import requests
from os import listdir, path
from os.path import isfile, join
import pandas as pd

def download_images():
    folder = "image_links"
    image_links = [f for f in listdir(folder) if isfile(join(folder, f))]

    search_results_df = pd.DataFrame(columns=['category', 'filepath'])
    for f in image_links:
        if ".csv" in f:
            keyword = f.replace(".csv", "")
            index = 1
            filepath = join(folder, f)
            df = pd.read_csv(filepath)
            data = []
            for i in range(len(df)):
                img_url = df['img_url'][i]
                image_name = "images/%s_%s.jpg" % (keyword, index)
                response = requests.get(img_url, timeout=10)
                if response.status_code:
                    fp = open(image_name, 'wb')
                    fp.write(response.content)
                    fp.close()
                    data.append([keyword, image_name])
                    index += 1

def write_to_csv():
    folder = "images"
    files = [f for f in listdir(folder) if isfile(join(folder, f))]
    data = []
    def get_category(str):
        vals = str.split("_")
        return vals[0]
    for f in files:
        filepath = join(folder, f)
        keyword = get_category(f)
        data.append([keyword, filepath])

    search_results_df = pd.DataFrame(data, columns=['category', 'filepath'])
    search_results_df.to_csv("final.csv")


write_to_csv()