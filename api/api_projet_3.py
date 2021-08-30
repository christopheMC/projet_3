from flask import Flask
from flask import make_response
from flask import abort
from flask import jsonify
import requests
from flask import request

api = Flask(import_name= 'my_api')

url = 'http://0.0.0.0:9200/projet_3/_search'
url1 = 'http://0.0.0.0:9200/projet_3/_search?size=0'
headers = {'Content-Type': 'application/json'}

@api.errorhandler(404)
def resource_not_found(error):
	return make_response(jsonify({'error': 'Resource not found'}), 404)

@api.errorhandler(401)
def bad_request(error):
	return make_response(jsonify({'error': 'Unauthorized'}), 401)

@api.errorhandler(403)
def dont_have_right(error):
	return make_response(jsonify({'error': 'You dont have right'}), 403)

@api.route('/', methods=['GET'])
def hello():
	return jsonify({'App': 'API PROJET 3'})

@api.route('/status', methods=['GET'])
def return_status():
	return jsonify({'On Air': 1})
	abort(404)

@api.route('/projet_3/all', methods=['GET'])
def return_all():
	r = requests.get(url)
	return r.json()
	abort(404)

@api.route('/projet_3/match/<field>/<query>', methods=['GET'])
def return_field(field,query):
	data = {"query":{'match':{field:query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/projet_3/range/<field>/less/<query>', methods=['GET'])
def return_range_less(field,query):
        data = {"query":{'range':{field:{'lte':query}}}}
        r = requests.get(url, headers=headers, json=data)
        return r.json()
        abort(404)

@api.route('/projet_3/range/<field>/more/<query>', methods=['GET'])
def return_range_more(field,query):
        data = {"query":{'range':{field:{'gte':query}}}}
        r = requests.get(url, headers=headers, json=data)
        return r.json()
        abort(404)

@api.route('/projet_3/range/<field>/in/<query1>/<query2>', methods=['GET'])
def return_range_in(field,query1,query2):
        data = {"query":{'range':{field:{'gte':query1,'lte':query2}}}}
        r = requests.get(url, headers=headers, json=data)
        return r.json()
        abort(404)

@api.route('/projet_3/range/<field>/out/<query1>/<query2>', methods=['GET'])
def return_range_out(field,query1,query2):
        data = {"query":{'bool':{'must_not':{'range':{field:{'gte':query1,'lte':query2}}}}}}
        r = requests.get(url, headers=headers, json=data)
        return r.json()
        abort(404)

@api.route('/projet_3/avg/<field>', methods=['GET'])
def return_avg(query):
        data = {"aggs":{'avg':{'avg':{"field":field}}}}
        r = requests.get(url1, headers=headers, json=data)
        return r.json()
        abort(404)

@api.route('/projet_3/min/<field>', methods=['GET'])
def return_min(query):
        data = {"aggs":{'min':{'min':{"field":field}}}}
        r = requests.get(url1, headers=headers, json=data)
        return r.json()
        abort(404)

@api.route('/projet_3/max/<field>', methods=['GET'])
def return_max(query):
        data = {"aggs":{'max':{'max':{"field":field}}}}
        r = requests.get(url1, headers=headers, json=data)
        return r.json()
        abort(404)

@api.route('/projet_3/sum/<field>', methods=['GET'])
def return_sum(query):
        data = {"aggs":{'sum':{'sum':{"field":field}}}}
        r = requests.get(url1, headers=headers, json=data)
        return r.json()
        abort(404)

@api.route('/projet_3/stats/<field>', methods=['GET'])
def return_sum(query):
        data = {"aggs":{'stats':{'stats':{"field":field}}}}
        r = requests.get(url1, headers=headers, json=data)
        return r.json()
        abort(404)

if __name__ == '__main__':
	api.run(host="0.0.0.0", port=5000)

