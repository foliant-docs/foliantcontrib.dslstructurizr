'''
Gibberish preprocessor for Foliant documenation authoring tool.
'''

import re

from random import choice
from random import randint
from random import random

from foliant.preprocessors.base import BasePreprocessor


def pick_letter() -> str:
    """
    Pick a random letter.
    Vowels have a higher chance of picking.
    Letters q, w, x and z have the lowest chance of picking.
    """

    rare_letters = 'qwxz'
    vowels = 'aeiouy'
    consonants = 'cdfghjklmnpqrstv'

    pick = random()
    if pick > 0.9:
        return choice(rare_letters)
    elif pick > 0.3:
        return choice(vowels)
    else:
        return choice(consonants)

def gen_word() -> str:
    """Return a word consisting of 2 to 9 letters."""
    word_len = randint(2, 9)
    return ''.join(pick_letter() for _ in range(word_len))


def gen_sentence(num_words: int = 7) -> str:
    """Generate a sentence consisting of `num_words` words."""
    words = (gen_word() for _ in range(num_words))
    return ' '.join(words).capitalize()


def gen_text(num_sentences: int = 10) -> str:
    """
    Generate a paragraph of gibberish consisting of `num_sentences`
    senteces, each consisting of 3 to 12 words.
    """

    sizes = (randint(3, 12) for _ in range(num_sentences))
    sentences = (gen_sentence(size) for size in sizes)
    return '. '.join(sentences) + '.'


class Preprocessor(BasePreprocessor):
    defaults = {
        'default_size': 10
    }
    tags = ('gibberish',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('gibberish')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def _process_tags(self, content):
        def sub_tag(match):
          tag_options = self.get_options(match.group('options'))
          default_size = self.options['default_size']
          size = tag_options.get('size', default_size)
          return gen_text(size)

        return self.pattern.sub(sub_tag, content)

    def apply(self):
        self.logger.info('Applying preprocessor Gibberish')
        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                content = markdown_file.read()

            processed_content = self._process_tags(content)

            if processed_content:
                with open(markdown_file_path, 'w') as markdown_file:
                    markdown_file.write(processed_content)
        self.logger.info('Preprocessor Gibberish applied')