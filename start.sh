echo "=> Starting webpack server"
cd /vagrant/frontend
npm run dev &

echo "=> Starting backend"
cd /vagrant/backend
~/.pyenv/bin/python fitoemanews.py

echo "=> Stopping webpack server"
kill $!