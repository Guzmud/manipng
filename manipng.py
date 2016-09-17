#! /usr/bin/python

import binascii
import zlib
import os.path

pngtags = {"header": "89504e470d0a1a0a",
           "trailer": "49454e44"}

pngchunks = {"IHDR": "image header",
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

infolder = "originaldata"
otfolder = "extractedpng"


def chunkeater(data):
    mdata = []

    k = 0
    while k < len(data):
        tlen = int(''.join([hex(ord(x))[2:].zfill(2) for x in data[k:k+4]]),
                   16)
        k += 4

        ttype = data[k:k+4]
        k += 4

        tdata = ''.join([hex(ord(x))[2:].zfill(2) for x in data[k:k+tlen]])
        k += tlen

        tcrc = int(''.join([hex(ord(x))[2:].zfill(2) for x in data[k:k+4]]),
                   16)
        k += 4

        cdata = ''.join([hex(ord(x))[2:].zfill(2) for x in ttype])+tdata
        ctcrc = int(binascii.crc32(binascii.unhexlify(cdata)) & 0xffffffff)
        mdata += [[ttype, tlen, (ctcrc == tcrc)], ]

    return mdata


def harvester_run(data, tags):
    harvester = {t: [] for t in tags}

    k = 0
    while k < len(data):
        ttype = data[k+4:k+8]

        tlen = int(''.join([hex(ord(x))[2:].zfill(2)
                            for x in data[k:k+4]]),
                   16)
        k += 8

        if ttype in tags:

            tdata = ''.join([hex(ord(x))[2:].zfill(2)
                             for x in data[k:k+tlen]])
            k += tlen

            tcrc = int(''.join([hex(ord(x))[2:].zfill(2)
                                for x in data[k:k+4]]),
                       16)
            k += 4

            cdata = ''.join([hex(ord(x))[2:].zfill(2)
                             for x in ttype])+tdata
            ctcrc = int(binascii.crc32(binascii.unhexlify(cdata)) & 0xffffffff)
            if ctcrc != tcrc:
                print "Bad CRC ! Bad !"
            harvester[ttype].append(tdata)
        else:
            k += tlen+4

    return harvester

filename = "lorempixel.png"  # regular png
# filename = "time2000.png"  # png with timestampe
# filename = "textualdata.png"  # png with tEXt and zTXt data
# filename = "utf8hindi.png"  # png with iTXt data
# filename = "drinkme.txt"  # textualdata.png inside a .txt file
# filename = "sstic2015.png"  #

print "\n\tEXTRACTION"

print "Opening file "+str(os.path.join(infolder, filename))
with open(os.path.join(infolder, filename), "rb") as f:
    data = f.read().encode("hex")
f.close()

tag1 = pngtags["header"]
tag2 = pngtags["trailer"]

print "Original data length in hexadecimal: "+str(len(data))
print "Data size before the png header: "+str(data.find(tag1))
ptrailer = len(data)-(data.find(tag2)+len(tag2)+8)
print "Data size after the png trailer: "+str(ptrailer)

pngdata = data[data.find(tag1):data.find(tag2)+len(tag2)+8]

print "Extracted png data length in hexadecimal: "+str(len(pngdata))

extracted_filename = "extracted_"+filename.rsplit('.', 1)[0]+".png"

print "Writing file "+str(os.path.join(otfolder, extracted_filename))
with open(os.path.join(otfolder, extracted_filename), 'wb') as hf:
    hf.write(binascii.a2b_hex(pngdata))
hf.close()

print "\n\tANALYZE"

print "Analyzing file "+str(os.path.join(otfolder, extracted_filename))
with open(os.path.join(otfolder, extracted_filename), 'rb') as f:
    data = f.read()
f.close()

mdata = []

header = pngtags["header"]
theader = ''.join([hex(ord(k))[2:].zfill(2)
                   for k
                   in data[:len(header)/2]]).lower()

if header != theader:
    print "Something's wrong: "+theader+" vs "+header
else:
    data = data[len(header)/2:]
    mdata = chunkeater(data)

print "PNG chunks (type, len, crc check)"
print mdata
clist = list(set([k[0]
                  for k
                  in mdata]))
ulist = []
for k in clist:
    if k in pngchunks:
        print "\t "+k+": "+pngchunks[k],
    else:
        ulist.append(k)
elist = [x for x in mdata
         if (x[0] == 'IDAT' and x[1] == 0)]
print ""

print "\n\tINVESTIGATION"

if len(elist) > 0:
    print "Empty IDAT chunks found: "+str(elist)

if len(ulist) > 0:
    print "Unknow chunks found: "+str(ulist)

print "Looking for data of interest..."
dftags = ["tEXt", "zTXt", "iTXt", "tIME"]
tags = dftags+ulist
harvester = harvester_run(data, tags)

if len(harvester["tEXt"]) > 0:
    print "\t... tEXt data foud"
    for k in harvester["tEXt"]:
        print "\t "+binascii.unhexlify(k)

if len(harvester["zTXt"]) > 0:
    print "\t... zTXt data found"
    for k in harvester["zTXt"]:
        tharvest = k.split("00", 1)
        print "\t"+binascii.unhexlify(k.split("00", 1)[0]),

        if k.split("00", 1)[1][:2] != "00":
            print "Unknow compression algorithm"
        else:
            tmess = k.split("00", 1)[1][2:]
            print zlib.decompress(binascii.unhexlify(tmess))

if len(harvester["iTXt"]) > 0:
    print "\t... iTXt data found"
    for k in harvester["iTXt"]:
        print "\t"+binascii.unhexlify(k).decode("utf-8")

if len(harvester["tIME"]) > 0:
    print "\t ... tIME data found"
    for k in harvester["tIME"]:
        print "\t Year : "+str(int(k[:4], 16))
        print "\t Month : "+str(int(k[4:6], 16))
        print "\t Day : "+str(int(k[6:8], 16))
        print "\t Hour : "+str(int(k[8:10], 16))
        print "\t Minute : "+str(int(k[10:12], 16))
        print "\t Second : "+str(int(k[12:14], 16))

for k in harvester.keys():
    if k not in dftags and len(harvester[k]) > 0:
        print "\t ... "+str(k)+" data found"
        for e in harvester[k]:
            print "\t hex size : "+str(len(k)),
        print ""

# check against the norm (size of ancillary chunks, scale of values,
# position of ancillary, keywords in tEXt and zTXt, etc.)
