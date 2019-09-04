from wtforms import Form, StringField, TextField, IntegerField
from wtforms.validators import Length, DataRequired

class ArticleForm(Form):
    title = StringField(validators=[
        Length(min=1, max=30, message='标题长度在1~30之间')
    ])
    content = TextField(validators=[
        DataRequired(message='内容不为空')
    ])
    # writer_id = IntegerField(validators=[DataRequired(message='必须要有作者!')])
    # TODO: 如果文章被修改，则修改者必须是作者
