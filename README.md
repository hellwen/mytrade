# mytrade

# install

    pyenv install 2.7.10
    
    pyenv virtualenv 2.7.10 mytrade
    
    pyenv activate mytrade
    
    git clone git@github.com:hellwen/mytrade.git
    
    cd mytrade
    
    pip install -r requirements.txt
    
    python manage.py runserver


## Heroku 


    heroku config:set MYTRADE_ENV=prod
    
    heroku config:set MYTRADE_SECRET=12345678
    
    heroku run python manage.py db upgrade
    
    heroku pg:psql --app mytrade DATABASE
    
    
