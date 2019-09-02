from flask import render_template, request, flash
from app.forms.article import ArctileForm
from .base import web
import pdb


@web.route('/write')
def article_write():
    article = {
        'title':'你好!',
        'content': """[TOC]
#### Disabled options

- TeX (Based on KaTeX);
- Emoji;
- Task lists;
- HTML tags decode;
- Flowchart and Sequence Diagram;

#### Editor.md directory

    editor.md/
            lib/
            css/
            scss/
            tests/
            fonts/
            images/
            plugins/
            examples/
            languages/
            editormd.js
            ...
```html
<!-- English -->
<script src="../dist/js/languages/en.js"></script>

<!-- 繁體中文 -->
<script src="../dist/js/languages/zh-tw.js"></script>
```"""
    }
    return render_template('write.html', article=article)
