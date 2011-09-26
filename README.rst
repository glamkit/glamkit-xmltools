``xmltools`` is a set of tools for handling XML files with unwieldy or undefined schemas, specifically large XML files or large collections of XML files.

Analysis
========

``analyse_xml`` is a command-line tool that takes a path (or ./) and returns a csv file containing an analysis of every element in every xml file in the path.

Usage examples::

    ./analyse_xml --help               # show help
    ./analyse_xml -l                   # list all xml files to be analysed
    ./analyse_xml                      # analyse all xml files in the current path
    ./analyse_xml > analysis.csv       # analyse all xml files in the current path and write the results to a csv file.
    ./analyse_xml -d path/to/xml       # analyse all xml files in the current path
    ./analyse_xml -d path/to/xml -r    # traverse the current path recursively

The analysis csv contains these fields:

=================   ==============================================================
Column              Description
=================   ==============================================================
``path``            A dot-separated path to each XML tag.
``min_valency``     The minimum number of these elements that each of its parents has
``max_valency``     The maximum number of these elements that each of its parents has
``sample_values``   Non-repeating sample values of the text within the XML tag.
``attributes``      A list of all the attributes found for each tag.
=================   ==============================================================


Interpreting the analysis
-------------------------

path
~~~~
A path that ``looks.like.this`` represents the <this> tag of a file structured like this::

   <looks>
      <like>
         <this></this>
      </like>
   </looks>

sample_values
~~~~~~~~~~~~~

``sample_values`` is a particularly useful field. Apart from seeing the values to discern their likely data type, you can see the variety of values produced.

If you asked for 5 sample values, but only got 1 value, that means the value is constant. If you get 2 values, that means there are only 2 values in the entire collection, which means that the value is boolean. If you got 0 values, that means the tag is always empty, or only ever contains children (see the next row of the csv file to see if an element has any children).

The number of sample values can be set with the ``-n`` option to ``analyse_xml``, but you should keep it more than 3 for easily discerning the range of values.

min/max_valency
~~~~~~~~~~~~~~~

``min_valency`` and ``max_valency`` will tell you the minimum and maximum number of these elements you'll have to deal with each time you encounter them. If a min_valency is 0, it means the element is optional. If a max_valency is 1 it means that it's a singleton value. If max_valency is more than 1, it means that the element is repeated to make up a list.

attributes
~~~~~~~~~~

This field lists out all the attributes found for the tag, and a sample of their values.

Harvesting
==========

``xmltools`` comes with tools to process large amounts of XML, e.g. to save it to a database quickly, and without taking up more memory than necessary to process a single record.

The principle is to define a ``BaseHandler`` handler that ``__call__``s one of several BaseProcessor subclasses, with the XML to process.

Handlers
~~~~~~~~
Which chunks are sent to which Saver is defined by CSS selectors in the handler, like this:

    from xmltools.handler import node, BaseHandler
    from xml_savers import OrganisationAndPersonSaver, SeriesWorkSaver, TitleWorkSaver, UniformTitleSaver
    from models import *

    class MyHandler(BaseHandler):
        namespaces = { 'mv': "http://example.com/uri"}

        handle_nodes = (
            node('mv|record > mv|Organisation', OrganisationAndPersonSaver(model=Organisation)),
            node('mv|record > mv|Person', OrganisationAndPersonSaver(model=Person)),
            node('mv|record > mv|SeriesWork', SeriesWorkSaver(model=SeriesWork)),
            node('mv|record > mv|TitleWork', TitleWorkSaver(model=TitleWork)),
        )

        def pre_process(self):
            # this is called before any xml is processed
            pass

        def post_process(self):
            # this is called after all the xml is processed
            pass

Then initialise the handler and call it with a list of paths to XML files to process.

    from xmltools.lib.getfiles import getfiles
    paths = getfiles(path=folder_or_file, regex=r"\.xml$", recursive=True)
    harvester = MyHandler()
    harvester.process(paths)

Processors
~~~~~~~~~~

XMLTools comes with a BaseProcessor class, and two subclasses, DjangoSaver and MongoSaver. Subclass these classes to define your own saver. For example:

    from xmltools.processors.django import DjangoSaver
    from xmltools.lib.xml2dict import xml2dict

class PersonSaver(DjangoSaver):
    """
    Person has:
    firstnames = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255, blank=True)
    date_of_birth = models.CharField(max_length=255, blank=True)
    date_of_death = models.CharField(max_length=255, blank=True)

    The incoming tag also has a list of work ids by this person, which were saved earlier.
    """

    def make_params(self, tag):
        d = xml2dict(tag)
        r = {}

        r['id'] = int(d['id'][0]['_value'])
        r['firstnames'] = d['firstnames'][0]['_value']
        r['lastname'] = d['lastname'][0]['_value']
        r['date_of_birth'] = d['pe_sym_dob_year'][0]['_value']
        r['date_of_death'] = d['pe_sym_dod_year'][0]['_value']

        def postsave(person):
            for work in d['works']
                work, created = Work.objects.get_or_create(id=work[0]['_value'])
                person.works.add(work)

        return {'id': r['id']}, r, postsave

The items in the returned result should be:

1) The query dictionary for a get() lookup to find an existing model instance to update
2) A dictionary of {field: value, ...} of fields to update for the model instance
3) A function to be called once the item has been saved, for post-processing.

NB MongoSaver works a bit differently at the moment. See the code.

Or you can subclass BaseProcessor directly to process an XML tag in another way.