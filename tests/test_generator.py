import unittest
import json
import yaml
from os.path import abspath
from agenerate.template.generator import Generator
from troposphere.template_generator import TemplateGenerator

class TestGenerator(unittest.TestCase):

    def test_template_is_same_as_sample(self):
        work_sample_name_path = abspath("tests/worksample.cfn.template")
        g = Generator()
        generated = g.to_dict()
        json_sample = json.loads(self.__open_and_read_file(work_sample_name_path))
        actual = TemplateGenerator(json_sample).to_dict()
        self.assertDictEqual(generated, actual)

    def __open_and_read_file(self, filename):
        with open(filename, 'r') as fin:
            return fin.read()

    def test_is_valid_json(self):
        g = Generator()
        json_sample = g.to_json()
        self.assertTrue(json.loads(json_sample))

    def test_is_valid_yaml(self):
        g = Generator()
        yaml_sample = g.to_yaml()
        self.assertTrue(yaml.load(yaml_sample))


    if __name__ == '__main__':
        unittest.main()
