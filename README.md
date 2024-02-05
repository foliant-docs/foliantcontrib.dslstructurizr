# Structurizr DSL Preprocessor for Foliant

The preprocessor renders diagrams, using [Structurizr DSL](https://docs.structurizr.com/dsl).

## Installation

> This section is for reference. The Gibberish preprocessor is currently not available in PyPi.

```bash
$ pip install foliantcontrib.dslstructurizr
```

## Config

To enable the preprocessor, add `dslstructurizr` to the `preprocessors` section in the project config:

```yaml
preprocessors:
    - dslstructurizr
```

<!-- The preprocessor has just one option:

```yaml
preprocessors:
    - gibberish:
        default_size: 10
```

`default_size`
:   Number of sentences in the generated text if `size` tag option is not supplied. Default: `10` -->

## Usage

To insert a placeholder text into your Markdown source, add the `{{ dsl_struct }}` XML tag:

```html
This is a {{ dsl_struct }} example.

```

After applying the preprocessor it will replace the tag with placeholder text. 

```html
This is a DSL STRUCTURIZR example.

```
