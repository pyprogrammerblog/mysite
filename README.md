# mysite

[PyProgrammer.com](https://pyprogrammer.com)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
git clone https://github.com/pyprogrammerblog/mysite
virtualenv -p python3
pip install -r requirements.txt
python3 manage.py collectstatics
python3 manage.py migrate
python3 manage.py runserver
```

## Usage

```bash

celery --app=mysite.celery:app worker --loglevel=INFO
celery -A mysite beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
