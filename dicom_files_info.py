#!/usr/bin/env python3

import pydicom
import os
import argparse

parser = argparse.ArgumentParser(description='Show DICOM file informations about study/series hierarchy.')
parser.add_argument('--path', type=str, help='Filesystem directory')
args = parser.parse_args()


class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKRED = '\033[91m'
    ENDC = '\033[0m'

    def get_blue(value):
        return "{}{}{}".format(bcolors.OKBLUE, value, bcolors.ENDC)

    def get_green(value):
        return "{}{}{}".format(bcolors.OKGREEN, value, bcolors.ENDC)

    def get_red(value):
        return "{}{}{}".format(bcolors.OKRED, value, bcolors.ENDC)


all_files = []
for root, dirnames, filenames in os.walk(args.path):
    for filename in filenames:
        all_files.append(os.path.join(root, filename))


print("files: {}".format(len(all_files)))

studies = {}
for item in all_files:
    try:
        dataset = pydicom.dcmread(item, force=True)

        if dataset.StudyInstanceUID not in studies:
            studies[dataset.StudyInstanceUID] = {}

        if dataset.SeriesInstanceUID not in studies[dataset.StudyInstanceUID]:
            studies[dataset.StudyInstanceUID][dataset.SeriesInstanceUID] = {'images': []}

        studies[dataset.StudyInstanceUID][dataset.SeriesInstanceUID]['images'].append({'SOPInstanceUID': dataset.SOPInstanceUID, 'modality': dataset.Modality, 'SOPClassUID': dataset.SOPClassUID})
    except:
        print("{}: [{}]".format(bcolors.get_red('Fail on parse DICOM'), bcolors.get_blue(item)))
        pass


for StudyInstanceUID, series in studies.items():
    print("----")
    print("{}: [{}]".format(bcolors.get_blue('StudyInstanceUID'), bcolors.get_green(StudyInstanceUID)))
    for SeriesInstanceUID, data in series.items():
        print("\t{}: [{}] {}: [{}]".format(bcolors.get_blue('SeriesInstanceUID'), bcolors.get_green(SeriesInstanceUID), bcolors.get_blue('files'), bcolors.get_green(len(data['images']))))
        for item in data['images']:
            print("\t\t{}: [{}] {}: [{}] {}: [{}]".format(  bcolors.get_blue('SOPInstanceUID')
                                                          , bcolors.get_green(item['SOPInstanceUID'])
                                                          , bcolors.get_blue('Modality')
                                                          , bcolors.get_green(item['modality'])
                                                          , bcolors.get_blue('SOPClassUID')
                                                          , bcolors.get_green(item['SOPClassUID'])))
