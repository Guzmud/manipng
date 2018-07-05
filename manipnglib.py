#!/usr/bin/env python3

import binascii
import hashlib
import json
import pathlib
import zlib


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
        ptr = end+1

    return epngs


def epng_extract(data, start, stop):
    return data[start:stop]


def chunk_length(data):
    return int(data, 16)


def chunk_type(data):
    return bytes.fromhex(data).decode("utf-8")


def chunk_data(data):
    return data


def chunk_crc(data):
    return int(data, 16)


def chunk_check(cdata, ccrc):
    tcrc = binascii.crc32(bytes.fromhex(cdata))
    tcrc = tcrc & 0xffffffff
    tcrc = int(tcrc)
    return tcrc == ccrc


def chunk_eating(data):
    k = 0
    while k<len(data):
        clen = 2*chunk_length(data[k:k+8])
        ctype = chunk_type(data[k+8:k+16])
        cdata = chunk_data(data[k+16:k+16+clen])
        ccrc = chunk_crc(data[k+16+clen:k+24+clen])
        check = chunk_check(data[k+8:k+16+clen], ccrc)
        yield {"len": clen,
               "type": ctype,
               "data": cdata,
               "crc": ccrc,
               "check": check}
        k += 24+clen


def get_tIME(data):
    """format: YYYYMMDDHHmmss"""
    return ("{}{}{}{}{}{}".format(int(data[:4], 16),
                                  int(data[4:6], 16),
                                  int(data[6:8], 16),
                                  int(data[8:10], 16),
                                  int(data[10:12], 16),
                                  int(data[12:14], 16),
                                  ))


def get_tEXT(data):
    """Also valid for iTXT, python3 for the win!"""
    return bytes.fromhex(data).decode("utf-8")


def get_zTXt(data):
    return zlib.decompress(bytes.fromhex(data), 0)


def chunk_extract(ctype, cdata):
    if ctype == "tIME":
        return get_tIME(cdata)
    elif ctype == "tEXT":
        return get_tEXT(cdata)
    elif ctype == "iTXt":
        return get_tEXT(cdata)
    elif ctype == "zTXt":
        return get_zTXt(cdata)


def chunk_analysis(data):
    analysis = {'legit_type': data["type"] in chunks,
                'total_len': 24+data["len"],
                'failed_crc': not data["check"],
               }
    return analysis


def chunk_eater(data):
    content = dict()
    analysis = dict()
    metanalysis = {"suspicious_types": list(),
                   "empty_chunks": list(),
                   "extracted_signals": list(),
                   "detected_errors": list(),
                  }
    ptr = 0

    for chunk in chunk_eating(data):
        if chunk["type"] in ["tIME", "tEXT", "iTXt"]:  #wip: zTXt
            chunk["extract"] = chunk_extract(chunk["type"], chunk["data"])
            metanalysis["extracted_signals"].append((ptr,
                                                     chunk["type"],
                                                     chunk["extract"],
                                                     ))

        content[ptr] = chunk
        analysis[ptr] = chunk_analysis(chunk)

        if not analysis[ptr]['legit_type']:
            metanalysis["suspicious_types"].append((ptr,
                                                    chunk["type"],
                                                    analysis[ptr]["total_len"],
                                                    ))
        if chunk["len"] < 1 and not chunk["type"] == "IEND":
            metanalysis["empty_chunks"].append((ptr,
                                                chunk["type"],
                                                ))

        if not chunk["check"]:
            metanalysis["detected_errors"].append((ptr,
                                                  chunk["type"],
                                                  ))

        if chunk["type"] == "IEND" and chunk["len"] > 0:
            metanalysis["IEND_data"] = chunk["data"]

        ptr += 1

    metanalysis["number_of_chunks"] = ptr
    return content, analysis, metanalysis


def png_export(epng_data, export_folder='.'):
    path = pathlib.Path(export_folder)
    epng_data = bytes.fromhex(epng_data)
    png_sha256 = hashlib.sha256(epng_data)
    path = pathlib.Path(path, "{}.png".format(png_sha256.hexdigest()))
    w = path.write_bytes(epng_data)
    return w, path


def json_report(outfolder, wpath, data, data_name):
    fileheader = wpath.name.split('.png', 1)[0]
    filename = "{}-{}.json".format(fileheader, data_name)
    report_path = pathlib.Path(outfolder, filename)

    with report_path.open("w") as f:
        json.dump(data, f, indent=4, sort_keys=True)
