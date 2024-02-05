# Structurizr DSL Preprocessor for Foliant

The preprocessor renders diagrams, using [Structurizr DSL](https://docs.structurizr.com/dsl).

## Installation

> This section is for reference. The Gibberish preprocessor is currently not available in PyPi.

```bash
$ pip install foliantcontrib.gibberish
```

## Config

To enable the preprocessor, add `gibberish` to the `preprocessors` section in the project config:

```yaml
preprocessors:
    - gibberish
```

The preprocessor has just one option:

```yaml
preprocessors:
    - gibberish:
        default_size: 10
```

`default_size`
:   Number of sentences in the generated text if `size` tag option is not supplied. Default: `10`

## Usage

To insert a placeholder text into your Markdown source, add the `gibberish` XML tag:

```html
Here’s the placeholder text:

<gibberish></gibberish>
```

After applying the preprocessor it will replace the tag with placeholder text. The text will contain the number of sentences defined in the `default_size` option.

```html
Here’s the placeholder text:

Yxz izyuo sjo iir tewo qvqc etosaeeuo iecaizaso aaeoeuo iyey. Apavaiqfu eqaaa eecyo ioiiyuoay ah caou iets. Yooyofa iiynndea yiuqehlq uizu yca. Pi iuld ixuaeqei ousogp yu ushggxyq yiia uiuyjo. Ofoemct ciyfuup uufiy avkfeqa ehtjoj ietwohoo xqgif. Iwohqoeao snf uozlw qeasoqzu gevuywxui ou xypikyyqu on hrx. Ruagoisia ivga ovzho da oziazioic. Iqeswsg ouoq ecserixo ueza icykifuzo pipzuyny aid cq ihxiwi eme eejxwt iuak. Oui goido yduz eeyfahxil dyiya mezifeo iym xuuvyiy. Iii yucnyyyq eono qyqu uu ioo sqwcjuhip.

```

If you want a different number of sentences in a specific tag, add the `size` option

```html
Here’s the placeholder text:

<gibberish size="5"></gibberish>
```
