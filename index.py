from flask import Flask, request, render_template, jsonify, abort
import gge_wrapper

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False


# http://127.0.0.1:5000/?video_id=orJSJGHjBLI&max_comments=50
@app.route('/', methods=['GET'])
def collect_youtube_video_comments_request():
    video_id = request.args.get('video_id')
    max_comments = request.args.get('max_comments', default=1, type=int)

    status, results = gge_wrapper.get_all_comments_from_youtube_video(video_id, max_comments)
    if status:
        abort(results["Status"], results["Type"])

    resp = jsonify(results)
    resp.status_code = 200
    return resp


# Unit tests
with app.test_client() as c:
    rv = c.get('/', query_string={
        'video_id': 'orJSJGHjBLI', 'max_comments': 50
    })
    assert len(rv.get_json()["comments"]) == 50

with app.test_client() as c:
    rv = c.get('/', query_string={
        'video_id': '@@@@@@@@@@@@@@@@', 'max_comments': 50
    })
    assert rv.status_code == 404

with app.test_client() as c:
    rv = c.get('/', query_string={
        'video_id': 'orJSJGHjBLI', 'max_comments': 2
    })
    comments = rv.get_json()["comments"]
    assert comments[0]['publishedAt'] >= comments[1]['publishedAt']
