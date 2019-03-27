pip install --user virtualenv
pip install --user virtualenvwrapper
export WORKON_HOME=~/Envs
source /home/bdlc/.local/bin/virtualenvwrapper.sh
workon psychoSite
pip install -r requirements.txt
export FLASK_CONFIG=development
export FLASK_APP=run.py