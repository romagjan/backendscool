import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

module_name = 'products'

# Возможно, модуль еще не установлен (или установлена другая версия), поэтому
# необходимо загружать __init__.py с помощью machinery.
module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()

def load_requirements(fname: str) -> list:
    requirements = []
    req = '''alembic~=1.3.3
#asyncpgsa==0.27.1
ConfigArgParse~=1.0
psycopg2-binary==2.8.4
#pytz==2019.3
#setproctitle==1.1.10
SQLAlchemy==1.3.14
flask_sqlalchemy==2.5.1
sqlalchemy_mptt==0.2.5
'''
    reqdev = '''coverage==5.0.3
Faker==4.0.0
locust
pylama==7.7.1
pytest~=5.3.5
pytest-aiohttp~=0.3.0
pytest-cov==2.8.1
SQLAlchemy-Utils==0.36.1
    '''
    read_file = ''
    if fname=='requirements.txt':
        read_file = req
    else:
        read_file = reqdev
    #with open(fname, 'r') as fp:
    for req in parse_requirements(read_file):
        extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
        requirements.append(
            '{}{}{}'.format(req.name, extras, req.specifier)
        )
    return requirements

setup(
    name=module_name,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    #long_description=open('README.rst').read(),
    url='https://github.com/romagjan/backendschool2022',
    platforms='all',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    python_requires='>=3.8',
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    extras_require={'dev': load_requirements('requirements.dev.txt')},
    entry_points={
        'console_scripts': [
            # f-strings в setup.py не используются из-за соображений
            # совместимости.
            # Несмотря на то, что этот пакет требует Python 3.8, технически
            # source distribution для него может собираться с помощью более
            # ранних версий Python. Не стоит лишать пользователей этой
            # возможности.
            '{0}-api = {0}.api.__main__:main'.format(module_name),
            '{0}-db = {0}.db.__main__:main'.format(module_name)
        ]
    },
    include_package_data=True
)
