#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Import named entities from plain text list
#

from entity_manager.manager import Entity_Manager


class Entity_Importer_List(object):

    # defaults
    verbose = False

    def import_entities(self, filename, types=[], encoding="utf-8"):

        entity_manager = Entity_Manager()
        entity_manager.verbose = self.verbose
        
        # open and read plaintext file line for line
    
        file = open(filename, encoding=encoding)
    
        for line in file:
            
            value = line.strip()
        
            if value:

                if self.verbose:
                    print ("Import entity {}".format(value))
    
                entity_manager.add(id=value, types=types, preferred_label=value, prefLabels=[value])


        file.close()


#
# Read command line arguments and start import
#

# if running (not imported to use its functions), run main function
if __name__ == "__main__":

    #get filenames from command line args

    from optparse import OptionParser

    parser = OptionParser("entity_import_list filename")
    parser.add_option("-t", "--type", dest="types", default=None, help="Type of the entities")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=None, help="Print debug messages")

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("No filename given")

    filename = args[0]

    importer = Entity_Importer_List()
    
    # set options from command line
    if options.verbose == False or options.verbose==True:
        importer.verbose=options.verbose

    types = options.types
    if not types:
        types=[filename]

    # import list of entities
    importer.import_entities(filename=filename, types=types)
