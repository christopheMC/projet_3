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

list= []
players =[]
teams = []
leagues = []

@api.errorhandler(404)
def resource_not_found(error):
	return make_response(jsonify({'error': 'Resource not found'}), 404)

@api.errorhandler(401)
def bad_request(error):
	return make_response(jsonify({'error': 'Unauthorized'}), 401)

@api.errorhandler(403)
def dont_have_right(error):
	return make_response(jsonify({'error': 'You dont have right'}), 403)

@api.route('/status', methods=['GET'])
def return_status():
	return jsonify({'On Air': 1})
	abort(404)

@api.route('/all_transfers', methods=['GET'])
def return_all():
	list = []
	data = {"query":{"match_all":{}}}
	r = requests.get(url, headers=headers, json=data)
	text = r.json()['hits']['hits']
	for i in range(len(text)):
		list.append({f"{i}":f"{text[i]['_source']['csv_line']}"})
	return jsonify(list)
	abort(404)

@api.route('/Name/<query>', methods=['GET'])
def return_name(query):
	query = str(query)
	data = {"query":{'match':{"Name":query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Position/<query>', methods=['GET'])
def return_position(query):
	query = str(query)
	data = {"query":{'match':{"Position":query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Age/<query>', methods=['GET'])
def return_age(query):
	query = int(query)
	data = {"query":{'match':{"Age":query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Team_from/<query>', methods=['GET'])
def return_team_from(query):
	query = str(query)
	data = {"query":{'match':{"Team_from":query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/League_from/<query>', methods=['GET'])
def return_league_from(query):
	query = str(query)
	data = {"query":{'match':{"League_from":query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Team_to/<query>', methods=['GET'])
def return_team_to(query):
	query = str(query)
	data = {"query":{'match':{"Team_to":query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/League_to/<query>', methods=['GET'])
def return_league_to(query):
	query = str(query)
	data = {"query":{'match':{"League_to":query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Season/<query>', methods=['GET'])
def return_season(query):
	query = str(query)
	data = {"query":{'match':{"Season":query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Transfer_fee/<query>', methods=['GET'])
def return_transfer_fee(query):
	query = int(query)
	data = {"query":{'match':{"Transfer_fee":query}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Age/less/<query>', methods=['GET'])
def return_age_less(query):
	query = int(query)
	data = {"query":{'range':{"Age":{'lte':query}}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Transfer_fee/less/<query>', methods=['GET'])
def return_transfer_fee_less(query):
	query = int(query)
	data = {"query":{'range':{"Transfer_fee":{'lte':query}}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Age/more/<query>', methods=['GET'])
def return_age_more(query):
	query = int(query)
	data = {"query":{'range':{'Age':{'gte':query}}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Transfer_fee/more/<query>', methods=['GET'])
def return_transfer_fee_more(query):
	query = int(query)
	data = {"query":{'range':{'Transfer_fee':{'gte':query}}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Age/<query1>/<query2>', methods=['GET'])
def return_age_in(query1,query2):
	query1 = int(query1)
	query2 = int(query2)
	data = {"query":{'range':{'Age':{'gte':query1,'lte':query2}}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Transfer_fee/<query1>/<query2>', methods=['GET'])
def return_transfer_fee_in(query1,query2):
	query1 = int(query1)
	query2 = int(query2)
	data = {"query":{'range':{'Transfer_fee':{'gte':query1,'lte':query2}}}}
	r = requests.get(url, headers=headers, json=data)
	return r.json()
	abort(404)

@api.route('/Age/avg', methods=['GET'])
def return_age_avg():
	data = {"aggs":{'avg':{'avg':{"field":'Age'}}}}
	r = requests.get(url1, headers=headers, json=data)
	text = r.json()['aggregations']['avg']
	return jsonify({f"avg_age":f"{text['value']}"})
	abort(404)

@api.route('/Transfer_fee/avg', methods=['GET'])
def return_transfer_fee_avg():
	data = {"aggs":{'avg':{'avg':{"field":'Transfer_fee'}}}}
	r = requests.get(url1, headers=headers, json=data)
	text = r.json()['aggregations']['avg']
	return jsonify({f"avg_transfer_fee":f"{text['value']}"})
	abort(404)

@api.route('/Age/min', methods=['GET'])
def return_age_min():
	data = {"aggs":{'min':{'min':{"field":'Age'}}}}
	r = requests.get(url1, headers=headers, json=data)
	text = r.json()['aggregations']['min']
	return jsonify({f"min_age":f"{text['value']}"})
	abort(404)

@api.route('/Transfer_fee/min', methods=['GET'])
def return_transfer_fee_min():
	data = {"aggs":{'min':{'min':{"field":'Transfer_fee'}}}}
	r = requests.get(url1, headers=headers, json=data)
	text = r.json()['aggregations']['min']
	return jsonify({f"min_transfer_fee":f"{text['value']}"})
	abort(404)

@api.route('/Age/max', methods=['GET'])
def return_age_max():
	data = {"aggs":{'max':{'max':{"field":"Age"}}}}
	r = requests.get(url1, headers=headers, json=data)
	text = r.json()['aggregations']['max']
	return jsonify({f"max_age":f"{text['value']}"})
	abort(404)

@api.route('/Transfer_fee/max', methods=['GET'])
def return_transfer_fee_max():
	data = {"aggs":{'max':{'max':{"field":'Transfer_fee'}}}}
	r = requests.get(url1, headers=headers, json=data)
	text = r.json()['aggregations']['max']
	return jsonify({f"max_transfer_fee":f"{text['value']}"})
	abort(404)

@api.route('/Transfers/stats', methods=['GET'])
def return_stats():
	data = {"aggs":{'stats_age':{"stats":{"field":"Age"}}}}
	r = requests.get(url, headers=headers, json=data)
	text = r.json()['aggregations']['stats_age']
	data = {"aggs":{'stats_transfer_fee':{"stats":{"field":"Transfer_fee"}}}}
	r = requests.get(url, headers=headers, json=data)
	text1 = r.json()['aggregations']['stats_transfer_fee']
	return jsonify({f"stats_age":text,f"stats_transfer_fee":text1})
	abort(404)

@api.route('/Players', methods=['GET'])
def return_players():
	players = []
	data = {"query":{"match_all":{}}}
	r = requests.get(url, headers=headers, json=data)
	text = r.json()['hits']['hits']
	for i in range(len(text)):
		if text[i]['_source']['Name'] not in players:
			players.append(text[i]['_source']['Name'])
	return jsonify(players)
	abort(404)

@api.route('/Teams', methods=['GET'])
def return_teams():
	teams = []
	data = {"query":{"match_all":{}}}
	r = requests.get(url, headers=headers, json=data)
	text = r.json()['hits']['hits']
	for i in range(len(text)):
		if text[i]['_source']['Team_from'] not in teams:
			teams.append(text[i]['_source']['Team_from'])
			if text[i]['_source']['Team_to'] not in teams:
				teams.append(text[i]['_source']['Team_to'])
	return jsonify(teams)
	abort(404)

@api.route('/Leagues', methods=['GET'])
def return_leagues():
	leagues = []
	data = {"query":{"match_all":{}}}
	r = requests.get(url, headers=headers, json=data)
	text = r.json()['hits']['hits']
	for i in range(len(text)):
		if text[i]['_source']['League_to'] not in leagues:
			leagues.append(text[i]['_source']['League_to'])
			if text[i]['_source']['League_from'] not in leagues:
				leagues.append(text[i]['_source']['League_from'])
	return jsonify(leagues)
	abort(404)

if __name__ == '__main__':
	api.run(host="0.0.0.0", port=5000)

