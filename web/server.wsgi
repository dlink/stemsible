import os, sys
sys.path.append('/home/dlink/stemsible/lib')
os.environ['VCONF'] = '/home/dlink/stemsible/config/prod.yml'

from server import app as application
