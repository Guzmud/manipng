manipng
=======

_manipng_, wordplay about PNG manipulation, actually a PNG analyser. Analysis is made using a simple chunk parser, although _manipng_ can incenditally be used as a _PNG_ extractor (e.g. from an executable). Made following a friendly request regarding one specific step from a SSTIC challenge (hence the sstic file in the test samples).


Todo list
---------

- **Move to python3** ('bout time)
- Splitting the test samples folder and the source folder notion
- Removing extractedpng and providing an optional location to the user
- Handle more than one _PNG_ embedded in the original data
- Produce a test sample file with three _PNG_ files embedded
- Use a configuration file in json for various tweaks and features
- Offer the user configuration regarding data dump
- Add a traditional argparser-based cli
- Expand the investigation part
- Allows custom chunk analysers
- Results provided as a _.json_ string or document
- Option for automated _.md_ writeup document from the analysis _.json_
- Wrap all that in a shiny package


Credits
---------

- [RFC 2083](https://tools.ietf.org/html/rfc2083)
- [lorempixel](http://lorempixel.com/)
- [PngSuite](http://www.schaik.com/pngsuite/)
