# Structurizr DSL Preprocessor for Foliant

The preprocessor renders diagrams, using [Structurizr DSL](https://docs.structurizr.com/dsl).

# Installation

As of now, the Structurizr DSL Preprocessor is not available on PyPi. However, you can still install it using the following command:

```bash
$ pip install foliantcontrib.dslstructurizr
```

## Configuration

To enable the preprocessor, add `dslstructurizr` to the preprocessors section in your project configuration file (`foliant.yml` or `foliant.yaml`):

```yaml
preprocessors:
    - dslstructurizr
```

## Options

The Structurizr DSL Preprocessor supports the following options:

- `cache_dir` (default: `.diagramscache`): Specifies the directory where the preprocessor caches generated diagrams.
- `structurizr_path` (default: `structurizr`): The path to the Structurizr executable. Ensure that Structurizr is installed on your system.
- `parse_raw` (default: `False`): If set to `True`, the preprocessor will attempt to parse raw Structurizr DSL diagrams without the `structurizr` tag.
- `format` (default: `png`): The output format of the generated diagrams (e.g., `png`, `svg`, etc.).
- `as_image` (default: `True`): If set to `True`, the generated diagrams will be treated as images; otherwise, they will be treated as inline code.

## Usage

To insert a Structurizr DSL diagram into your Markdown source, add the `structurizr` XML tag:

```html
This is a structurizr example.

```

After applying the preprocessor, this tag will be replaced with the rendered Structurizr DSL diagram.

```html
This is a rendered Structurizr DSL diagram.

```

## Example

Consider the following example of a Foliant project configuration file (`foliant.yml`):

```yaml
preprocessors:
    - dslstructurizr:
        cache_dir: .diagrams
        structurizr_path: /path/to/structurizr
        parse_raw: True
        format: svg
        as_image: False

```

n this example, the preprocessor is configured to cache diagrams in the `.diagrams` directory, use the specified path to the Structurizr executable, parse raw Structurizr DSL, generate diagrams in SVG format, and treat them as inline code.

Feel free to customize the options based on your project requirements.

