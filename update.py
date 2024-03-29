#!/usr/bin/env python
import requests
import os
import platform
import json
import datetime
import zipfile


def download(url, filename):
	r = requests.get(url)
	with open(filename, 'wb') as f:
		f.write(r.content)

def is_os_64bit():
	return platform.machine().endswith('64')

# 64bit
if is_os_64bit():
	flavourId = 6

# 32bit
else:
	flavourId = 1

# Get version information
print("(1) OpenRCT2 최신 업데이트 정보")
json_to_fetch = "https://openrct2.org/altapi/?command=get-latest-download&flavourId=" + str(flavourId) + "&gitBranch=develop"
download(json_to_fetch, "./temp.json")

with open("./temp.json") as json_file:
	json_data = json.load(json_file)

print("  - 최신 개발 버전: " + str(json_data['downloadId']))

updateTime = datetime.datetime.strptime(json_data['addedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
updateTimeTuple = updateTime.timetuple()
print("  - 업데이트된 시각: " + str(updateTimeTuple.tm_year) + "." + str(updateTimeTuple.tm_mon).zfill(2) + "." + str(updateTimeTuple.tm_mday).zfill(2) + " " + str(updateTimeTuple.tm_hour).zfill(2) + ":" + str(updateTimeTuple.tm_min).zfill(2) + ":" + str(updateTimeTuple.tm_sec).zfill(2))


# Download
print("(2) 다운로드")
print("  - 다운로드 중 ...")
basename = os.path.basename(json_data['url'])
download(json_data['url'], basename)
print("  - 다운로드 완료")

# Unzip
print("(3) 압축 해제")
binary_zip = zipfile.ZipFile(basename)
binary_zip.extractall("./")
binary_zip.close()

# Remove remnant files
print("(4) 임시 파일 제거")
os.remove("./temp.json")
os.remove(basename)

# Write current version
f = open('version.txt', mode='wt', encoding='utf-8')
f.write(str(json_data['downloadId']))
f.close()

print("")

print("업데이트가 완료되었습니다!")
os.system("pause")
