from flask import (
    render_template,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from app.weather import weather_bp

from app.extensions import db

from app.models import (
    FavoriteCity,
    SearchHistory
)

from app.utils.weather import (
    get_current_weather,
    get_forecast,
    get_air_quality
)

from config import Config



@weather_bp.route("/")
@login_required
def dashboard():

    favorites = FavoriteCity.query.filter_by(
        user_id=current_user.id
    ).all()

    recent_searches = (
        SearchHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(
            SearchHistory.searched_at.desc()
        )
        .all()
    )

    return render_template(
        "dashboard.html",
        favorites=favorites,
        recent_searches=recent_searches,
        selected_city=request.args.get("city", "")
    )
        
    
    
@weather_bp.route(
    "/api/weather",
    methods=["GET"]
)
@login_required
def weather_api():

    city = request.args.get("city")

    if not city:
        return jsonify({
            "success": False,
            "message": "City required"
        }), 400

    try:
        

        current = get_current_weather(
            city,
            Config.API_KEY
        )

        forecast = get_forecast(
            city,
            Config.API_KEY
        )

        lat = current["coord"]["lat"]
        lon = current["coord"]["lon"]

        air_quality = get_air_quality(
            lat,
            lon,
            Config.API_KEY
        )

        search = SearchHistory(

            city_name=city,

            temperature=current["main"]["temp"],

            weather_condition=current["weather"][0]["main"],

            user_id=current_user.id

        )

        db.session.add(search)

        db.session.commit()

        user_searches = (
            SearchHistory.query
            .filter_by(user_id=current_user.id)
            .order_by(
                SearchHistory.searched_at.desc()
            )
            .all()
        )

        if len(user_searches) > 100:

            for item in user_searches[100:]:

                db.session.delete(item)

            db.session.commit()

        return jsonify({
            "success": True,
            "current": current,
            "forecast": forecast,
            "air_quality": air_quality
        })

    except Exception as e:
        
        print("ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Unable to fetch weather data."
        }), 500
        
        


@weather_bp.route(
    "/favorites/add",
    methods=["POST"]
)
@login_required
def add_favorite():

    city = request.form.get("city")

    if not city:
        return jsonify({
            "success": False
        })

    existing = FavoriteCity.query.filter_by(
        city_name=city,
        user_id=current_user.id
    ).first()

    if existing:

        return jsonify({
            "success": False,
            "message": "Already exists"
        })

    favorite = FavoriteCity(
        city_name=city,
        user_id=current_user.id
    )

    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "success": True
    })
    
    
    
@weather_bp.route(
    "/favorites/delete/<int:id>",
    methods=["DELETE"]
)
@login_required
def delete_favorite(id):

    favorite = FavoriteCity.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    if not favorite:

        return jsonify({
            "success": False
        }), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({
        "success": True
    })
    
    







@weather_bp.route(
    "/api/history"
)
@login_required
def history():

    searches = (
        SearchHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(
            SearchHistory.searched_at.desc()
        )
        .all()
    )

    data = []

    for item in searches:
        data.append({
            "city": item.city_name,
            "searched_at": item.searched_at.strftime(
                "%d-%m-%Y %H:%M"
            )
        })

    return jsonify(data)


