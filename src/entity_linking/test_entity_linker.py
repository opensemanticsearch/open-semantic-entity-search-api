#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest

from entity_manager.manager import Entity_Manager
from entity_linking.entity_linker import Entity_Linker

# is an entity id with same value in a field in OpenRefine result?
def is_in_resultdata(resultdata, entity_id, fieldname, value):
    result = False
    for queryresult in resultdata:
        for candidate in resultdata[queryresult]['result']:
            if candidate['id'] == entity_id:
                if fieldname in candidate:
                    if candidate[fieldname] == value:
                       result = True
    return result


class Test_entity_linker(unittest.TestCase):

    def test(self):

        # add test entity to entities index
        entity_manager = Entity_Manager()
    
        entity_manager.add( id = "http://entity-unittest.local/entities/1", types=['entity-unittest_type_one','entity-unittest_type_two'], preferred_label = "entity-unittest_preferred_label_part_one entity-unittest_preferred_label_part_two", prefLabels = ["entity-unittest_preferredLabels"], labels = ["entity-unittest_labels_one_part_one entity-unittest_labels_one_part_two", "entity-unittest_labels_two", "entity-unittest_labels_umlaut_äöüß"] )

        # extracts and normalizes/links all known entities/names/labels
        linker = Entity_Linker()

        # check if entity is found by preferred label
        results = linker.entities( text = "I want to extract the id of entity-unittest_preferred_label_part_one entity-unittest_preferred_label_part_two from a full text." )

        self.assertTrue(is_in_resultdata(resultdata=results, entity_id='http://entity-unittest.local/entities/1', fieldname='name', value='entity-unittest_preferred_label_part_one entity-unittest_preferred_label_part_two'))

        # check if is_in_resultdata works ok and does not return true even on not existing id
        self.assertFalse(is_in_resultdata(resultdata=results, entity_id='http://entity-unittest.local/entities/notexistententityid', fieldname='name', value='notexistant entity'))

        # check returned types of returned entity id
        self.assertTrue(is_in_resultdata(resultdata=results, entity_id='http://entity-unittest.local/entities/1', fieldname='type', value=['entity-unittest_type_one','entity-unittest_type_two']))

        # check if entity is found by another preferred label
        results = linker.entities( text = "I want to extract the id of entity-unittest_preferredLabels from a full text." )
        self.assertTrue(is_in_resultdata(resultdata=results, entity_id='http://entity-unittest.local/entities/1', fieldname='name', value='entity-unittest_preferred_label_part_one entity-unittest_preferred_label_part_two'))

        # check if entity is found by (alternate) labels
        results = linker.entities( text = "I want to extract the id of entity-unittest_labels_one_part_one entity-unittest_labels_one_part_two from a full text." )
        self.assertTrue(is_in_resultdata(resultdata=results, entity_id='http://entity-unittest.local/entities/1', fieldname='name', value='entity-unittest_preferred_label_part_one entity-unittest_preferred_label_part_two'))

        results = linker.entities( text = "I want to extract the id of entity-unittest_labels_two from a full text." )
        self.assertTrue(is_in_resultdata(resultdata=results, entity_id='http://entity-unittest.local/entities/1', fieldname='name', value='entity-unittest_preferred_label_part_one entity-unittest_preferred_label_part_two'))

        # check if entity is found by alternate label with special chars
        results = linker.entities( text = "I want to extract the id of entity-unittest_labels_umlaut_äöüß from a full text." )
        self.assertTrue(is_in_resultdata(resultdata=results, entity_id='http://entity-unittest.local/entities/1', fieldname='name', value='entity-unittest_preferred_label_part_one entity-unittest_preferred_label_part_two'))

        # entity should not be linked by only a part of the label
        results = linker.entities( text = "I dont want to extract the id of entity-unittest_labels_one_part_one (missing second part of name) from a full text." )
        self.assertFalse(is_in_resultdata(resultdata=results, entity_id='http://entity-unittest.local/entities/1', fieldname='name', value='entity-unittest_preferred_label_part_one entity-unittest_preferred_label_part_two'))

       
if __name__ == '__main__':
    unittest.main()

