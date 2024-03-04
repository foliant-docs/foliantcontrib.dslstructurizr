'''
Structurizr diagrams preprocessor for Foliant documentation authoring tool.
'''

import re
from collections import namedtuple
from hashlib import md5
from pathlib import Path
from pathlib import PosixPath
from typing import Optional
from typing import Union

from foliant.contrib.combined_options import CombinedOptions
from foliant.contrib.combined_options import Options
from foliant.preprocessors.utils.preprocessor_ext import BasePreprocessorExt
from foliant.preprocessors.utils.preprocessor_ext import allow_fail

BUFFER_TAG = '_structurizr'
PIPE_DELIMITER = '_~_diagram_sep_~_'


OptionValue = Union[int, float, bool, str]
QueueElement = namedtuple('QueueElement', 'args sources filenames')


def parse_diagram_source(source: str) -> Optional[str]:
    """
    Parse source string and get a diagram out of it.
    All text before the first !START: and after the first !END is cut out.
    All spaces before !START: and !END are also removed.

    :param source: diagram source string as stated by the user.

    :returns: parsed diagram source or None if parsing failed.
    """

    pattern = re.compile(r'(!START:.*?\n)\s*(!END)', flags=re.DOTALL)
    match = pattern.search(source)
    if match:
        return match.group(1) + match.group(2)
    else:
        return None


def generate_buffer_tag(diagram_content: str, options: Options) -> str:
    '''
    Generate a buffer tag that should be put in place of a Structurizr diagram in Markdown source.

    After processing the queue, these tags should be replaced by Markdown image tags or inline
    diagram code.

    :param diagram_content: content of the generated Mermaid diagram.
    :param options: diagram options.

    :returns string with a generated buffer tag:
    '''
    caption = options.get('caption', '')

    result = f'<{BUFFER_TAG} content="{diagram_content}" caption="{caption}"></{BUFFER_TAG}>'

    return result


class Preprocessor(BasePreprocessorExt):
    defaults = {
        'parse_raw': False,
    }
    tags = ('structurizr', BUFFER_TAG)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('structurizr')
        self._queue = {}

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def process_structurizr(self, content: str) -> str:
        '''
        Find diagram definitions and replace them with buffer tags. These tags will be processed
        on the second pass.

        The definitions are saved into the queue which will be executed after the first pass
        is finished.

        :param content: chapter's markdown content

        :returns: Markdown content with diagrams definitions replaced with buffer tags.
        '''

        raw_pattern = re.compile(
            r'(?:^|\n)(?P<spaces>[ \t]*)(?P<body>!START:.*?!END)',
            flags=re.DOTALL
        )

        def _sub_tags(diagram) -> str:
            '''Sub-function for <structurizr> tags.'''
            options = CombinedOptions(
                {
                    'config': self.options,
                    'tag': self.get_options(diagram.group('options'))
                },
                priority='tag'
            )
            return self._process_diagram(options, diagram.group('body'))

        def _sub_raw(diagram) -> str:
            '''
            Sub-function for raw diagrams replacement (without ``<structurizr>``
            tags). Handles alternation and returns spaces which were used to
            filter out inline mentions of ``!START:``.
            '''

            spaces = diagram.group('spaces')
            body = diagram.group('body')
            return spaces + self._process_diagram(Options(self.options), body)

        processed = self.pattern.sub(_sub_tags, content)

        if self.options['parse_raw']:
            processed = raw_pattern.sub(_sub_raw, processed)

        return processed

    @allow_fail()
    def _process_diagram(self, options: Options, body: str) -> str:
        '''
        Add Structurizr diagram to execution queue. Save the diagram
        source into a variable for output as content.

        Finally, replace the diagram definition with a buffer tag. After the queue is processed,
        this tag will be replaced by the Mermaid diagram content.

        :param options: Options extracted from the diagram definition
        :param body: Structurizr diagram body

        :returns: Buffer tag to be processed on the second pass.
        '''

        diagram_source = parse_diagram_source(body)
        if not diagram_source:
            self._warning('Cannot parse diagram body. Have you forgotten !START: or !END?')
            return ''

        self.logger.debug(f'Processing Structurizr diagram, options: {options}, body: {body}')

        diagram_content = diagram_source

        buffer_tag = generate_buffer_tag(diagram_content, options)
        self.logger.debug(f'Generated buffer tag: {buffer_tag}')
        return buffer_tag

    def execute_queue(self):
        """
        Generate all diagrams which were scheduled in the queue. The queue is grouped by
        cmd_args so diagrams with the same settings will be processed by a single Structurizr
        instance.
        """

        self.logger.debug(f'Generating diagrams. Number of queues: {len(self._queue)}')
        pipe_args = ['--pipe', '--pipeNoStderr', '--pipedelimitor', PIPE_DELIMITER]

        for _, sources, _ in self._queue.values():
            self.logger.debug(f'Queue started. Number of diagrams: {len(sources)}')
            full_args = [*pipe_args]
            self.logger.debug(f'Generating diagrams from the queue, command: {" ".join(full_args)}')
            p = Popen(full_args, stdout=PIPE, stdin=PIPE, stderr=PIPE)

            input_str = '\n\n'.join(sources).encode()
            r = p.communicate(input_str)

            results = r[0].split(PIPE_DELIMITER.encode())[:-1]
            self.logger.debug(f'Queue processed. Number of results: {len(results)}.')

            for bytes_ in results:
                if bytes_.strip().startswith(b'ERROR'):
                    message = f'{"*"*10}\nFailed to generate diagram:\n{bytes_.decode()}'
                    self.logger.warning(message)
                    output(message, self.quiet)
                else:
                    diagram_content = bytes_.decode()
                    print(diagram_content)

    def replace_buffers(self, match):
        """
        re.sub function
        Replaces buffer tags, which were left in places of diagrams on the first pass, by
        Mermaid diagram content.
        """

        self.logger.debug(f'Processing buffer tag: {match.group(0)}')
        options_str = match.group('options')
        diagram_content = match.group('content')
        caption = options_str.get('caption', '')

        return f'```mermaid\n{diagram_content}\n```\n\n{caption}'


    def apply(self):
        self._process_all_files(func=self.process_structurizr)
        self.execute_queue()

        self._process_tags_for_all_files(func=self.replace_buffers)

        self.logger.info('Preprocessor applied')
