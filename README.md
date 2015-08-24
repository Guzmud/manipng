manipng
=======

MANIPNG, a bad wordplay on PNG manipulation and actually a PNG extractor (in case the PNG is embedded into something else, let's say an executable. Make me think I did not anticipated the case where there is more than one PNG inside the file) and analyzer. Nothing big, mainly a chunk analyzer.

Non-authoritative todo list
===========================
- Manage the case where there is more than one PNG inside the file (produce an adapted test sample)
- Expand the investigation part
- Allows dynamic library import for chunk analysis (in order to easily integrate a reading/decoding function for custom chunk)
- Produce a dump of the data before and after the PNG ?

Thanks to
=========
- lorempixel and PngSuite (Willem van Schaik) for the test samples !