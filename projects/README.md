# Tools For Writing Latex

## Convert Markdown to LaTeX

### Install
```bash
wget "https://github.com/jgm/pandoc/releases/download/3.3/pandoc-3.3-linux-amd64.tar.gz"
tar zxvf pandoc-3.3-linux-amd64.tar.gz
export PATH=$PATH:pandoc-3.3/bin/
```

### Usage
```bash
# --wrap=none: avoid split one line into multi lines
pandoc reviewer_PXUu.md -o output_letex/reviewer_PXUu.tex --wrap=none
```

<!-- or in Python

```python
import pypandoc
output = pypandoc.convert_file('input.md', 'latex', outputfile='output.tex')
``` -->

### Convert with template

use `pandoc -v` to see default template path.

LaTeX template
- [latex_template_full.tex](latex_template_full.tex)
- [latex_template_simple.tex](latex_template_simple.tex)

1. read arguments from markdown
```bash
pandoc input.md -o output.pdf --template=pandoc_template.tex
```

2. pass arguments from command lines [Use this]

```bash
# pandoc output can be .pdf
# --write=latex -M tex_math_single_backslash will use $$ for inline equotion instead of \(\)
pandoc \
    response_to_all_reviewers.md \
    -o output_letex/response_to_all_reviewer.tex \
    --template=pandoc_template.tex \
    --wrap=none --write=latex -M tex_math_single_backslash  --lua-filter=inline_math.lua \
    -V title="Response to Reviewer"

sed -i 's/\\(\([^)]*\)\\)/$\1$/g' output_letex/response_to_all_reviewer.tex
```
