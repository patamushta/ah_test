virtualenv env
source env/bin/activate
pip install -r requirements.txt
for name in `ls data`; do 
    python analizer.py data/$name;
done
