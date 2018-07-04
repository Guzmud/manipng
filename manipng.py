#! /usr/bin/python

import binascii  # legacy
import pathlib
import json
import zlib  # legacy

import manipnglib as mpng


infolder = "originaldata"
filename = "utf8hindi.png"

data = mpng.file_import(pathlib.Path(infolder, filename))
epngs_info = mpng.epngs_info(data)

for epng in epngs_info:
    start = epng["start"]
    stop = epng["stop"]
    print("[info] next epng starting at byte {}".format(start))

    if stop == -1:
        print("[warning] no trailer found for the next epng.")
    else:
        print("[info] next epng stopping at {}".format(stop))
        print("[info] epng length {} bytes".format(stop-start))

    epng_data = mpng.epng_extract(data, start, stop)

    wbytes, wpath = mpng.png_export(epng_data)
    if wbytes < 1:
        print("[warning] could not write down the epng")
    else:
        print("[info] epng extracted and saved on disk {}".format(wpath))

    data = data[16:]  # 16 for the header
    content, analysis, metanalysis = mpng.chunk_eater(data)

    mpng.json_report('.', wpath, content, "content")
    mpng.json_report('.', wpath, analysis, "analysis")
    mpng.json_report('.', wpath, metanalysis, "metanalysis")
    print("[info] reports ready for {}".format(wpath.name))

    raise NotImplementedError


# LEGACY
for k in harvester["zTXt"]:
    tharvest = k.split("00", 1)
    print("zTXt (compressed): {}".format(binascii.unhexlify(k.split("00", 1)[0]),))

    if k.split("00", 1)[1][:2] != "00":
        print("Unknow compression algorithm")
    else:
        tmess = k.split("00", 1)[1][2:]
        print("zTXt: {}".format(zlib.decompress(binascii.unhexlify(tmess))))
