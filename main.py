from bs4 import BeautifulSoup
import requests


def filter_by_ext(content, extension):
    for i in content:
        if extension in content.text:
            return str(content.text)
        else:
            continue


def filter_by_time(content, max_time):

    if content is None:
        return False
    else:
        content = content.split('-')
        if int(content[1].strip('h')) <= max_time:
            return True
        else:
            return False


def page_parse(url):

    out_list = []
    response = requests.get(url)
    page = BeautifulSoup(response.text, 'lxml')
    table_main = page.find_all("td", class_="content")
    table_main = table_main[2].find_all("a")
    for i in table_main:
        filtered_str = filter_by_ext(content=i, extension='.grib2')
        if filter_by_time(filtered_str, 30):
            out_list.append(filtered_str)
    return out_list


def file_download(source_url, output_dir, file_name):
    __SUCCESS__ = "Successfully done"
    __FAIL__ = "Downloading failed"

    tries = 0
    try:
        while tries < 10:
            response = requests.get(source_url, stream=True)
            if response.status_code == 200:
                with open((str(output_dir + file_name)), 'wb') as file:
                    file.write(response.content)
                return print(__SUCCESS__)
            else:
                tries += 1
    except:
        return print(__FAIL__)


if __name__ == '__main__':
    source_url = 'https://data.ecmwf.int/forecasts/20230312/00z/0p4-beta/oper/'
    out_dir = './output/'
    files_to_download_list = page_parse(url=source_url)
    for i in range(len(files_to_download_list)):
        file_download(
            source_url=str(source_url + files_to_download_list[i]),
            output_dir=out_dir,
            file_name=files_to_download_list[i]
        )
