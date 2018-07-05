manipng
=======

_manipng_, wordplay about PNG manipulation, actually a PNG analyser. Analysis is made using a simple chunk parser, although _manipng_ can incenditally be used as a _PNG_ extractor (e.g. from an executable). Made following a friendly request regarding one specific step from a SSTIC challenge (hence the sstic file in the test samples).


Requirements
------------
- python3


Features
--------
- script and library available
- manage 1+ PNG data in the same file
- extract each .png
- analyse each chunk
- produce a metanalysis
- reports dumped in json


Todo
----
- rework the zTXt extraction
- proper test suite
- produce a test sample file with three _PNG_ files embedded
- argparse based CLI
- configuration for folders, json prettifying, data extraction, etc.
- check ancillary chunks positions and sizes
- check scale of value for color-related data
- check/harvest specific keywords in textual data
- allows custom chunk analysers
- automated _.md_ writeup document from the analysis _.json_
- wrap all that in a shiny package
- packaging a library-only version
- packaginf a hug-api version


Credits
---------

- [RFC 2083](https://tools.ietf.org/html/rfc2083)
- [lorempixel](http://lorempixel.com/)
- [PngSuite](http://www.schaik.com/pngsuite/)
