#!/usr/bin/env python3

import hashlib
import pathlib


tags = {"header": "89504e470d0a1a0a",
        "trailer": "49454e44"}

chunks = {"IHDR": "image header",
          "PLTE": "color palette",
          "IDAT": "image data",
          "IEND": "image trailer",
          "bKGD": "background color",
          "cHRM": "primary chromaticities",
          "gAMA": "image gamma",
          "hIST": "image histogram",
          "pHYs": "physical pixel dimensions",
          "sBIT": "significant bits",
          "tEXt": "textual data",
          "tIME": "last modification time",
          "tRNS": "transparency",
          "zTXt": "compressed textual data",
          "iTXt": "international textual data"}


def file_import(filepath):
    p = pathlib.Path(filepath)
    data = None
    if p.exists() and p.is_file():
        data = p.read_bytes().hex()
    return data


def epngs_info(data):
    epngs = []
    ptr = 0

    while data.find(tags["header"], ptr) > -1:
        start = data.find(tags["header"])
        end = data.find(tags["trailer"], start+1)  # start or (start+1) ?
        if end != -1:
            end += len(tags["trailer"])
        epngs.append({"start": start, "stop": end})
        print("{} - {}".format(start, end))
        ptr = end+1

    return epngs


def epng_extract(data, start, stop):
    return data[start:stop]


def chunk_eating(data):
    pass


def png_export(epng_data, export_folder='.'):
    path = pathlib.Path(export_folder)
    epng_data = bytes.fromhex(epng_data)
    png_sha256 = hashlib.sha256(epng_data)
    path = pathlib.Path(path, "{}.png".format(png_sha256.hexdigest()))
    w = path.write_bytes(epng_data)
    return w, path
