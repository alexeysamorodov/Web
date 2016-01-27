import bottle
import bleach
import datetime
import time
import io
import user_agents
import os
from PIL import Image, ImageDraw
from bottle.ext import sqlite

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile=os.path.join(BASE_PATH, 'database.sqlite3'))
app.install(plugin)
bottle.TEMPLATE_PATH.insert(0 ,os.path.join(BASE_PATH, 'templates'))

def xss_filter(text):
    return bleach.clean(
        text,
        ['b', 'i', 'u', 's', 'img'],  # tags
        {'img': ['src', 'alt']},  # attributes
        []  # styles
    )

    
def time_format(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d.%m.%y %H:%M')

  
@app.route('/counter')
def counter(db):
    bottle.response.content_type = 'image/png'
    views = next(db.execute('SELECT * FROM Views'))
    today_views = views['today']
    total_views = views['total']
    ts = views['timestamp']
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    today_ts = time.mktime(today.timetuple())
    if today_ts > ts:
        today_views = 0
        ts = today_ts
    total_views += 1
    today_views += 1
    db.execute('UPDATE Views SET total=?, today=?, timestamp=?', (total_views, today_views, ts))
    
    
    ip = bottle.request.environ.get('REMOTE_ADDR')
    user_agent = bottle.request.headers.get('User-Agent')
    ts = time.time() + 5*60*60
    ts_limit = ts - 30*60
    visits_count = db.execute(
        'SELECT COUNT(*) FROM Visits WHERE ip=? AND user_agent=? AND timestamp>?',
        (ip, user_agent, ts_limit)).fetchone()[0]
    if visits_count == 0:
        db.execute('INSERT INTO Visits(ip, user_agent, timestamp) VALUES (?, ?, ?)',
            (ip, user_agent, ts))
    total_visits = db.execute('SELECT COUNT(*) FROM Visits').fetchone()[0]
    today_visits = db.execute('SELECT COUNT(*) FROM Visits WHERE timestamp>?',
        (today_ts,)).fetchone()[0]
    
    # drawing
    buffer = io.BytesIO()
    image = Image.new('RGBA', (120, 40))
    draw = ImageDraw.Draw(image)
    text_color = 'black'
    draw.text((0, 12), 'visits', fill=text_color)
    draw.text((0, 23), 'views', fill=text_color)
    draw.text((40, 0), 'today', fill=text_color)
    draw.text((40, 12), '{}'.format(today_visits), fill=text_color)
    draw.text((40, 23), '{}'.format(today_views), fill=text_color)
    draw.text((80, 0), 'total', fill=text_color)
    draw.text((80, 12), '{}'.format(total_visits), fill=text_color)
    draw.text((80, 23), '{}'.format(total_views), fill=text_color)
    image.save(buffer, 'PNG')
    buffer.seek(0)
    return buffer.read()


@app.route('/visits')
def visits(db):
    visits = db.execute('SELECT * FROM Visits')
    return bottle.template('visits.html',
        visits=visits, time_format=time_format,
        ua_parse=user_agents.parse)


@app.route('/')
def index():
    return bottle.template('index.html')

    
@app.route('/gallery')
def gallery():
	return bottle.template('gallery.html')

    
@app.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, './static')

    
@app.route('/feedback')
def feedback(db):
    comments = db.execute('SELECT * FROM Comments')
    return bottle.template('feedback.html',
        comments=comments, xss_filter=xss_filter,
        time_format=time_format)

    
@app.route('/post_comment', method=['POST'])
def post_comment(db):
    text = bottle.request.forms.get('text')
    name = bottle.request.forms.get('name')
    if text and name:
        ip = bottle.request.environ.get('REMOTE_ADDR')
        user_agent = bottle.request.headers.get('User-Agent')
        timestamp = time.time() + 5*60*60
        db.execute('INSERT INTO Comments(ip, user_agent, timestamp, name, message) VALUES (?, ?, ?, ?, ?)',
            (ip, user_agent, timestamp, name, text))
        bottle.redirect('/feedback')
    else:
        return 'You should not pass'

        
@app.route('/test')
def test():
    return bottle.request.environ.get('HTTP_X_FORWARDED_FOR', 'None') + ' ' + bottle.request.environ.get('REMOTE_ADDR')
       
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, reloader=True)

