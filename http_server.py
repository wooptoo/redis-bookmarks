from sanic import Sanic
from sanic.response import json
from sanic.log import logger as log

import bookmarks

app = Sanic(__name__)


@app.route('/entries')
async def index(request):
    return json(bookmarks.get_all_entries())


@app.route('/entries/day/<day:int>')
async def get_day(request, day):
    """Get entries paged by day"""
    page = bookmarks.get_page_by_day(day)
    if request.args.get('group'):
        page = bookmarks.group_by_domain(page)
    return json(page)


@app.route('/entries/tag/<tag>')
async def get_entries_for_tag(request, tag):
    return json(bookmarks.get_entries_for_tag(tag))


@app.route('/entries/domain/<domain>')
async def get_entries_for_domain(request, domain):
    log.debug('Fetching domain {}'.format(domain))
    return json(bookmarks.get_entries_for_domain(domain))


@app.route('/tags')
async def get_all_tags(request):
    return json(bookmarks.get_all_tags())


@app.route('/domains')
async def get_all_domains(request):
    return json(bookmarks.get_all_domains())


@app.route('/entry/<hashid>', methods=['GET', 'DELETE'])
async def entry(request, hashid):
    if request.method == 'GET':
        entry = bookmarks.get_entry(hashid)
        if entry:
            return json(entry)
        else:
            return json('Entry does not exist', 404)

    if request.method == 'DELETE':
        was_removed = bookmarks.remove_entry(hashid)
        if was_removed:
            return json('Deleted entry {}'.format(hashid))
        else:
            return json('Entry does not exist', 404)


app.run(host='0.0.0.0', port=8000, debug=True)
