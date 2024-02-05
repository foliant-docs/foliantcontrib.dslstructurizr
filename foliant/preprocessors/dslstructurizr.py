import re
from foliant.preprocessors.base import BasePreprocessor

class DslStructPreprocessor(BasePreprocessor):
    defaults = {
        'tag': 'dsl_struct'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = self.logger.getChild('dsl_struct')
        self.logger.debug(f'DslStructPreprocessor initialized: {self.__dict__}')
        self.run_tests()

    def run_tests(self):
        self.logger.debug('Running tests...')
        self.test_init()
        self.test_process_tags()

    def test_init(self):
        assert self.options['tag'] == 'dsl_struct'

    def test_process_tags(self):
        content = 'This is a {{ dsl_struct }} example.'
        processed_content = self._process_tags(content)
        assert processed_content == 'This is a DSL STRUCTURIZR example.'

    def _process_tags(self, content):
        return re.sub(f'{{\s*{re.escape(self.options["tag"])}\s*}}', 'DSL STRUCTURIZR', content)

    def apply(self):
        self.logger.info('Applying DslStructPreprocessor')
        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                content = markdown_file.read()

            processed_content = self._process_tags(content)

            if processed_content:
                with open(markdown_file_path, 'w') as markdown_file:
                    markdown_file.write(processed_content)
        self.logger.info('DslStructPreprocessor applied')

if __name__ == "__main__":
    # Instantiate the preprocessor, which will run tests as part of initialization
    DslStructPreprocessor()
