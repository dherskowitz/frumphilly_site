# Docker Compose Commands
alias dc="docker-compose $1"
alias up="docker-compose up -d"
alias rs="docker-compose restart"
alias build="docker-compose up -d --build"
alias log="docker-compose logs > logs.txt"

# Django Commands
alias new="python manage.py startapp $1"
alias mk="python manage.py makemigrations"
alias mg="python manage.py migrate"
alias super="python manage.py createsuperuser"

# Python Commands
alias freeze="pip freeze > requirements.txt"
alias pir="pip install -r requirements.txt"
alias manage="python manage.py $1"

# Node Commands
alias watch="npm run watch"