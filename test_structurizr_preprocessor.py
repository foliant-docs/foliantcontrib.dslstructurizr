import unittest
from unittest.mock import MagicMock
from pathlib import Path
from foliant.preprocessors import StructurizrPreprocessor


class TestStructurizrPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = StructurizrPreprocessor()
        self.preprocessor._warning = MagicMock()

    def test_init(self):
        self.assertEqual(self.preprocessor.tags, ('structurizr', '_structurizr'))

    def test_get_diagram_format(self):
        options = {
            'format': 'png',
            'params': {
                'tsvg': True,
                'tparam1': 'value1',
                'tparam2': 'value2',
            }
        }

        result = self.preprocessor._get_diagram_format(options)

        self.assertEqual(result, 'svg')

    def test_parse_diagram_source_valid(self):
        source = '!START:\nstructurizr source\n!END'

        result = self.preprocessor._parse_diagram_source(source)

        self.assertEqual(result, '!START:\nstructurizr source\n!END')

    def test_parse_diagram_source_invalid(self):
        source = 'Invalid diagram source'

        result = self.preprocessor._parse_diagram_source(source)

        self.assertIsNone(result)

    # Add more tests as needed

    def tearDown(self):
        del self.preprocessor


if __name__ == '__main__':
    unittest.main()
