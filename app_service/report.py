from app_service.utils import *
from app_service.api_base import *

# http://127.0.0.1:5000/users
@app.route("/users", methods=['GET'])
def get_users_cnt_freq():
	users_count, users_frequency = get_users()
	return jsonify({
		'count': users_count,
		'data': users_frequency
	})

# http://127.0.0.1:5000/hotels
@app.route("/hotels", methods=['GET'])
def get_hotels_cnt_freq():
	hotels_count, hotels_frequency = get_hotels()
	return jsonify({
		'count': hotels_count,
		'data': hotels_frequency
	})

# http://127.0.0.1:5000/advertisers
@app.route("/advertisers", methods=['GET'])
def get_advertisers_cnt_freq():
	advertisers_count, advertisers_frequency = get_advertisers()
	return jsonify({
		'count': advertisers_count,
		'data': advertisers_frequency
	})

# http://127.0.0.1:5000/advertisers
@app.route("/hotel_min_offer_per_advertiser", methods=['GET'])
def get_hotels_min_offers():
	hotels_min_offers = get_hotel_per_advertiser_min_offer()
	return jsonify(
		hotels_min_offers
	)