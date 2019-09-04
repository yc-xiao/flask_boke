from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.models.base import db
# from app.models.article import Article

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

'''
manager.py db init    //创建迁移存储库
python37 manager.py db migrate    //模型改变后先执行迁移
python37 manager.py db upgrade    //将迁移应用于数据库
'''
