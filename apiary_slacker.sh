eval "$(rbenv init -)"
rbenv shell 2.2.2
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
python $DIR/apiary_slacker.py $1
