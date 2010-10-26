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

Documentation to come...