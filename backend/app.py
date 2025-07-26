from functools import wraps

from flask import Flask, request, g, jsonify, send_from_directory

import os

from werkzeug.utils import secure_filename

import sqlite3

from uuid import uuid4

from setup_db import create_connection

from insert_queries import (
    add_user,
    add_meal_to_calender,
    add_ingredient,
    add_ingredient_to_meal,
    add_meal,
)

from delete_queries import (
    delete_meal,
    delete_meal_from_calender,
    delete_ingredient,
    delete_ingredient_from_specific_meal_with_ingredient_and_meal_id,
    delete_ingredient_from_meals_with_ingredient_id,
    delete_ingredients_from_meal_with_meal_id,
)

from select_queries import (
    select_all_users_username,
    select_all_users_username_except_one,
    select_all_users_emails_except_one,
    select_calender_data,
    select_ingredient_and_meal_entry_in_meal_ingredients,
    select_personal_meals_with_ingredients,
    select_user_by_token,
    select_user_id_and_password,
    select_user_no_by_username,
    select_meals_the_ingredient_were_in,
    select_user_profile_picture_name,
    select_users_image_name_by_id,
    select_users_meals,
    select_users_ingredients,
    select_users_calender_entries,
    select_info_for_user_by_id,
    select_personal_ingredients,
    select_ingredient_by_id,
    select_password_by_id,
    select_all_users_emails,
    select_user_by_id,
)

from update_queries import (
    update_user_info,
    update_personal_meal,
    update_password_by_user_id,
    update_ingredient,
    update_personal_meal_name,
    update_total_macros_of_meal_ingredient_was_used_for,
    UPDATE_reCalcMacrosForMeals,
    update_user_profile_picture,
    update_user_token,
)

from inputValidation import (
    isUsernameValid,
    isPasswordValid,
    validateUserInfo,
    isIngredientValid,
    isMealNameValid,
    validateIngredients_for_meal,
    validateOwnership,
    isCalenderDateAndTimeValid,
    validatePicture,
)

from encryption import get_hashed_password, check_password

from flask_cors import CORS

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.secret_key = os.environ.get("API_KEY")
app.config["picture_folder"] = "./user-images"


def get_db():
    if "db" not in g:
        g.db = create_connection(r"./database.db")
    return g.db


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.headers.get("Authorization")

        if auth == "1":  # Bypassing token auth for example account
            user = select_user_by_id(get_db(), auth)
        else:
            if not auth:
                return jsonify({"message": "Token is missing!"}), 401

            user = select_user_by_token(get_db(), auth)

            if user is None:
                return jsonify({"message": "Invalid token!"}), 401

        g.user = {"id": user[0], "username": user[1]}

        return f(*args, **kwargs)

    return decorator


def api_key_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        api_key = None
        if request.is_json:
            api_key = request.json.get("Authorization")

        if not api_key:
            api_key = request.headers.get("Authorization")

        if not api_key:
            return jsonify({"message": "API key is missing!"}), 400

        if api_key == app.secret_key:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Unauthorized"}), 401

    return decorator


@app.route("/login", methods=["POST"])
@api_key_required
def loginPage():
    username = request.json["username"]
    password = request.json["password"]

    user = select_user_id_and_password(get_db(), username)  # Indexing the tuple

    if not user:
        return jsonify({"message": "Invalid Username, user not found"}), 406

    username_validation = isUsernameValid(username)
    if isinstance(username_validation, str):
        return jsonify({"message:": username_validation}), 406

    password_validation = isPasswordValid(password)
    if isinstance(password_validation, str):
        return jsonify({"message": password_validation}), 406

    users_password = user[1]
    if check_password(password, users_password):
        token = str(uuid4())
        # The example account wont be affected by multiple people logging into the account
        result = update_user_token(get_db(), token, username)

        if result:
            return jsonify(
                {
                    "message": "Logged in successfully",
                    "token": token,
                    "user_id": user[0],
                    "username": username,
                }
            ), 200
        else:
            return jsonify({"message": "Error handling token"}), 422

    else:
        return jsonify({"message": "Wrong password"}), 406


@app.route("/logout", methods=["POST"])
@token_required
def logout():
    result = update_user_token(get_db(), None, g.user.get("username"))

    if result:
        return jsonify({"message": "Successfully logged you out"}), 200
    else:
        return jsonify({"message": "Error handling token"}), 422


@app.route("/register", methods=["GET", "POST"])
@api_key_required
def register():
    username = request.json["username"]
    usernames = select_all_users_username(get_db())

    for nickname in usernames:
        if username == nickname[0]:
            return jsonify({"message": "Username is already taken"}), 406

    password = request.json["password"]
    confirm_password = request.json["confirm_password"]
    gender = int(request.json["gender"])
    activity_lvl = int(request.json["activity_lvl"])
    email = request.json["email"]
    name = request.json["name"]
    weight = float(request.json["weight"])
    height = float(request.json["height"])
    age = int(request.json["age"])

    for user_email in select_all_users_emails(get_db()):
        if email == user_email:
            return jsonify({"message": "Email is already taken"}), 406

    register_validation = validateUserInfo(
        username, gender, activity_lvl, email, name, weight, height, age
    )

    if isinstance(register_validation, str):
        return jsonify({"message": register_validation}), 406

    for value in [password, confirm_password]:
        passwordValid = isPasswordValid(value)
        if isinstance(passwordValid, str):
            return jsonify({"message": passwordValid}), 406

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 406

    ## Adding a new user ##
    result = add_user(
        get_db(),
        username,
        get_hashed_password(password),
        gender,
        activity_lvl,
        email,
        name,
        weight,
        height,
        age,
    )

    if result:
        return jsonify({"message": "Successfully registered your account"}), 200
    else:
        return jsonify({"message": "Failed registration"}), 400


@app.route("/password/<user_id>", methods=["PUT"])
@token_required
def change_password(user_id):
    if int(user_id) != g.user.get(
        "id"
    ):  # Cant change the password of the example account
        return jsonify({"message": "Unauthorized"}), 401

    old_password = request.json["old_password"]
    new_password = request.json["new_password"]
    confirm_new_password = request.json["new_confirm_password"]

    arr = [old_password, new_password, confirm_new_password]

    for password in arr:
        result = isPasswordValid(password)
        if isinstance(result, str):
            return jsonify({"message": result}), 406

    old_password_in_database = select_password_by_id(get_db(), user_id)
    if not check_password(old_password, old_password_in_database):
        return jsonify({"message": "Old password is incorrect"}), 406

    if new_password != confirm_new_password:
        return jsonify({"message": "The new passwords does not match"}), 406

    if new_password == old_password:
        return jsonify(
            {"message": "The new password cant be the same as your old password"}
        ), 406

    update_password_by_user_id(get_db(), get_hashed_password(new_password), user_id)

    return jsonify({"message": "Successfully changed your password"}), 200


@app.route("/user_info", methods=["PUT"])
@token_required
def update_user_information():
    try:
        user_id = g.user.get("id")
        username = g.user.get("username")

        # Prevent people from changing the username of the example account
        if user_id != 1:
            u = request.json.get("username")
            if not u:
                return jsonify({"message": "Could not find username"}), 400
            else:
                username = u

        name = request.json["name"]
        age = int(request.json["age"])
        height = float(request.json["height"])
        weight = float(request.json["weight"])
        gender = int(request.json["gender"])
        activity_lvl = int(request.json["activity_lvl"])
        email = request.json["email"]

        user_id = select_user_no_by_username(get_db(), username)

        if user_id != g.user.get("id"):
            return jsonify({"message": "Unauthorized"}), 401

        usernames = select_all_users_username_except_one(get_db(), user_id)

        if usernames:
            for nickname in usernames:
                if username == nickname[0]:
                    return jsonify({"message": "Username is already taken"}), 406

        emails = select_all_users_emails_except_one(get_db(), user_id)

        if emails:
            for user_email in emails:
                if email == user_email[0]:
                    return jsonify({"message": "Email is already taken"}), 406

        user_info_validation = validateUserInfo(
            username, gender, activity_lvl, email, name, weight, height, age
        )

        if isinstance(user_info_validation, str):
            return jsonify({"message": user_info_validation}), 406

        update_user_info(
            get_db(),
            user_id,
            name,
            username,
            age,
            email,
            height,
            weight,
            gender,
            activity_lvl,
        )

        return jsonify({"message": "Successfully updated your user information"}), 200

    except sqlite3.Error as err:
        print("Error: {}".format(err))


@app.route("/profile_picture", methods=["POST"])
@token_required
def upload_profile_picture():
    try:
        if "file" not in request.files:
            return jsonify({"message": "No file found"}), 404

        file = request.files["file"]

        if not validatePicture(file.filename):
            return jsonify(
                {
                    "message": "File format is not accepted, only; .png, .jpg, .jpeg, .gif"
                }
            ), 406

        if file:
            user_id = g.user.get("id")
            filename = secure_filename(f"{user_id}_${file.filename}")

            if not os.path.exists(app.config["picture_folder"]):
                os.mkdir(app.config["picture_folder"])

            file_path = os.path.join(app.config["picture_folder"], filename)

            file.save(file_path)
            result = update_user_profile_picture(get_db(), filename, user_id)

            if result:
                return jsonify(
                    {"message": "Profile picture uploaded successfully"}
                ), 200
            else:
                return jsonify({"message": "Error when uploading picture"}), 500

        else:
            return jsonify({"message": "Did not receive any file"}), 400

    except Exception as e:
        print("Error uploading profile picture:", e)
        return jsonify({"message": "Error uploading profile picture"}), 500


@app.route("/profile_picture", methods=["DELETE"])
@token_required
def delete_profile_picture():
    try:
        user_id = g.user.get("id")
        db = get_db()
        file_name = select_user_profile_picture_name(db, user_id)

        file_path = (
            os.path.join(app.config["picture_folder"], file_name) if file_name else None
        )

        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        result = update_user_profile_picture(db, None, user_id)

        if result:
            return jsonify({"message": "Profile picture successfully deleted"}), 200
        else:
            return jsonify({"message": "Error when deleting picture"}), 500

    except Exception as e:
        print("Error deleting profile picture:", e)
        return jsonify({"message": "Error deleting profile picture"}), 500


@app.route("/meal/<meal_id>", methods=["DELETE"])
@token_required
def deleteMeal(meal_id):
    try:
        user_id = g.user.get("id")

        meal_ids = select_users_meals(get_db(), user_id)
        if validateOwnership(meal_id, meal_ids):
            delete_ingredients_from_meal_with_meal_id(get_db(), meal_id)
            delete_meal(get_db(), meal_id)

            return jsonify({"message": "Deleted meal successfully"}), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401

    except sqlite3.Error as err:
        print("Error: {}".format(err))


@app.route("/meal/<ingredient_id>/<meal_id>", methods=["DELETE"])
@token_required
def delete_ingredient_from_meal(ingredient_id, meal_id):
    try:
        user_id = g.user.get("id")

        ingredient_ids = select_users_ingredients(get_db(), user_id)
        meal_ids = select_users_meals(get_db(), user_id)
        if validateOwnership(ingredient_id, ingredient_ids) and validateOwnership(
            meal_id, meal_ids
        ):
            ingredient_info = select_ingredient_by_id(get_db(), ingredient_id)

            update_total_macros_of_meal_ingredient_was_used_for(
                get_db(), meal_id, ingredient_info
            )

            delete_ingredient_from_specific_meal_with_ingredient_and_meal_id(
                get_db(), ingredient_id, meal_id
            )

            return jsonify(
                {"message": f"Deleted {ingredient_info[2]} from the meal, successfully"}
            ), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401

    except sqlite3.Error as err:
        print("Error: {}".format(err))


@app.route("/calender/<calender_id>", methods=["DELETE"])
@token_required
def delete_meal_fromCalender(calender_id):
    try:
        user_id = g.user.get("id")

        meal_ids = select_users_meals(get_db(), user_id)

        calender_ids = []
        for id in meal_ids:
            calender_ids += select_users_calender_entries(get_db(), id)

        if validateOwnership(calender_id, calender_ids):
            delete_meal_from_calender(get_db(), calender_id)

            return jsonify({"message": "Deleted calender entry successfully"}), 200

        else:
            return jsonify({"message": "Unauthorized"}), 401

    except sqlite3.Error as err:
        print("Error: {}".format(err))


def findIngredients_for_meal(data):
    ingredients_for_meal = []
    for index in range(int(len(data) / 8)):
        ingredients_for_meal.append(
            {
                "ingredient_id": data[str(index) + "-ingredient_id"],
                "name": data[str(index) + "-name"],
                "amount": data[str(index) + "-amount"],
                "protein": float(data[str(index) + "-protein"]),
                "calories": float(data[str(index) + "-calories"]),
                "carbohydrates": float(data[str(index) + "-carbohydrates"]),
                "fat": float(data[str(index) + "-fat"]),
                "sugar": float(data[str(index) + "-sugar"]),
            }
        )

    return ingredients_for_meal


def addNewIngredientsAndUpdateOldOnes(ingredients_for_meal, meal_id):
    user_id = g.user.get("id")

    for ingredient in ingredients_for_meal:
        if ingredient["ingredient_id"] == "":
            ingredient_id = add_ingredient(
                get_db(),
                user_id,
                ingredient["name"],
                ingredient["amount"],
                ingredient["protein"],
                ingredient["calories"],
                ingredient["carbohydrates"],
                ingredient["fat"],
                ingredient["sugar"],
            )
            add_ingredient_to_meal(get_db(), meal_id, ingredient_id)
        else:
            update_ingredient(
                get_db(),
                ingredient["ingredient_id"],
                ingredient["name"],
                ingredient["amount"],
                ingredient["protein"],
                ingredient["calories"],
                ingredient["carbohydrates"],
                ingredient["fat"],
                ingredient["sugar"],
            )
            ingredientAddedToMeal = (
                select_ingredient_and_meal_entry_in_meal_ingredients(
                    get_db(), meal_id, ingredient["ingredient_id"]
                )
            )

            if not ingredientAddedToMeal:
                add_ingredient_to_meal(get_db(), meal_id, ingredient["ingredient_id"])


def updatePersonalMeal(ingredients_for_meal, meal_name, isMealInDatabase, meal_id):
    user_id = g.user.get("id")

    meal_info = {
        "name": meal_name,
        "protein": 0,
        "calories": 0,
        "carbohydrates": 0,
        "fat": 0,
        "sugar": 0,
    }

    # calculating total nutrients
    for nutrient in ingredients_for_meal:
        meal_info["protein"] += nutrient["protein"]
        meal_info["calories"] += nutrient["calories"]
        meal_info["carbohydrates"] += nutrient["carbohydrates"]
        meal_info["fat"] += nutrient["fat"]
        meal_info["sugar"] += nutrient["sugar"]

    if isMealInDatabase:
        update_personal_meal(
            get_db(),
            meal_id,
            meal_name,
            meal_info["protein"],
            meal_info["calories"],
            meal_info["carbohydrates"],
            meal_info["fat"],
            meal_info["sugar"],
        )
    else:
        return add_meal(
            get_db(),
            meal_name,
            user_id,
            round(meal_info["protein"], 2),
            round(meal_info["calories"], 2),
            round(meal_info["carbohydrates"], 2),
            round(meal_info["fat"], 2),
            round(meal_info["sugar"], 2),
        )


@app.route("/meal", methods=["POST"])
@token_required
def addMeal():
    try:
        data = request.get_json()

        meal_name = data["meal_name"]

        result = isMealNameValid(meal_name)
        if isinstance(result, str):
            return jsonify({"message": result}), 406

        data.pop("meal_name")
        ingredients_for_meal = findIngredients_for_meal(data)

        result = validateIngredients_for_meal(ingredients_for_meal)
        if isinstance(result, str):
            return jsonify({"message": result}), 200

        meal_id = updatePersonalMeal(ingredients_for_meal, meal_name, False, None)

        addNewIngredientsAndUpdateOldOnes(ingredients_for_meal, meal_id)

        return jsonify({"message": f"Created {meal_name} successfully"}), 200
    except sqlite3.Error as err:
        print("Error: {}".format(err))


@app.route("/meal/<meal_id>", methods=["PUT"])
@token_required
def editMeal(meal_id):
    try:
        user_id = g.user.get("id")
        meal_ids = select_users_meals(get_db(), user_id)
        if not validateOwnership(meal_id, meal_ids):
            return jsonify({"message": "Unauthorized"}), 401

        data = request.get_json()
        meal_name = data["meal_name"]

        if len(data) == 1:
            update_personal_meal_name(get_db(), meal_id, meal_name)

            return jsonify({"message": f"Modified {meal_name} successfully"}), 200

        result = isMealNameValid(meal_name)
        if not result:
            return jsonify({"message": result}), 406

        data.pop("meal_name")

        ingredients_for_meal = findIngredients_for_meal(data)

        result = validateIngredients_for_meal(ingredients_for_meal)
        if result is not True:
            return jsonify({"message": result}), 406

        updatePersonalMeal(ingredients_for_meal, meal_name, True, meal_id)
        addNewIngredientsAndUpdateOldOnes(ingredients_for_meal, meal_id)

        return jsonify({"message": f"Modified {meal_name} successfully"}), 200
    except sqlite3.Error as err:
        print("Error: {}".format(err))


@app.route("/calender", methods=["POST"])
@token_required
def add_meal_to_given_date():
    try:
        data = request.json

        result = isCalenderDateAndTimeValid(data["date"], data["time"])
        if not result:
            return jsonify({"message": result}), 406

        add_meal_to_calender(get_db(), data["id"], data["date"], data["time"])

        return jsonify({"message": "Meal added successfully"}), 200
    except sqlite3.Error as err:
        print("Error: {}".format(err))


@app.route("/ingredient", methods=["POST"])
@token_required
def addIngredient():
    data = request.json

    name = data["name"]
    amount = data["amount"]
    protein = float(data["protein"])
    calories = float(data["calories"])
    carbohydrates = float(data["carbohydrates"])
    fat = float(data["fat"])
    sugar = float(data["sugar"])

    validate_ingredient = isIngredientValid(
        name, amount, protein, calories, carbohydrates, fat, sugar
    )

    if validate_ingredient is not True:
        return validate_ingredient, 406

    user_id = g.user.get("id")
    add_ingredient(
        get_db(), user_id, name, amount, protein, calories, carbohydrates, fat, sugar
    )

    return jsonify({"message": f"Created {name} successfully"}), 200


@app.route("/ingredient/<ingredient_id>", methods=["PUT"])
@token_required
def editIngredient(ingredient_id):
    ingredient_ids = select_users_ingredients(get_db(), g.user.get("id"))
    if validateOwnership(ingredient_id, ingredient_ids) is not True:
        return jsonify({"message": "Unauthorized"}), 401

    new_data = request.json

    old_ingredient_info = select_ingredient_by_id(get_db(), ingredient_id)

    name = new_data["name"]
    amount = new_data["amount"]
    protein = float(new_data["protein"])
    calories = float(new_data["calories"])
    carbohydrates = float(new_data["carbohydrates"])
    fat = float(new_data["fat"])
    sugar = float(new_data["sugar"])

    validate_ingredient = isIngredientValid(
        name, amount, protein, calories, carbohydrates, fat, sugar
    )

    if validate_ingredient is not True:
        return jsonify({"message": validate_ingredient}), 406

    update_ingredient(
        get_db(),
        ingredient_id,
        name,
        amount,
        protein,
        calories,
        carbohydrates,
        fat,
        sugar,
    )

    macros_diff = {
        "protein": old_ingredient_info[4] - protein,
        "calories": old_ingredient_info[5] - calories,
        "carbohydrates": old_ingredient_info[6] - carbohydrates,
        "fat": old_ingredient_info[7] - fat,
        "sugar": old_ingredient_info[8] - sugar,
    }

    personal_meal_ids = select_meals_the_ingredient_were_in(get_db(), ingredient_id)

    UPDATE_reCalcMacrosForMeals(get_db(), personal_meal_ids, macros_diff)

    return jsonify({"message": f"Ingredient {name} edited successfully"}), 200


@app.route("/ingredient/<ingredient_id>", methods=["DELETE"])
@token_required
def deleteIngredient(ingredient_id):
    try:
        user_id = g.user.get("id")

        ingredient_ids = select_users_ingredients(get_db(), user_id)
        if validateOwnership(ingredient_id, ingredient_ids) is True:
            ingredient_info = select_ingredient_by_id(get_db(), ingredient_id)
            meals_the_ingredient_were_in = select_meals_the_ingredient_were_in(
                get_db(), ingredient_id
            )

            update_total_macros_of_meal_ingredient_was_used_for(
                get_db(), meals_the_ingredient_were_in, ingredient_info
            )

            if len(meals_the_ingredient_were_in) >= 1:
                delete_ingredient_from_meals_with_ingredient_id(get_db(), ingredient_id)

            delete_ingredient(get_db(), ingredient_id)

            return jsonify(
                {"message": f"Deleted {ingredient_info[2]} successfully"}
            ), 200
        else:
            return jsonify({"message": "Unauthorized"}), 401

    except sqlite3.Error as err:
        print("Error: {}".format(err))


##### GET #####
@app.route("/user_info/<user_id>", methods=["GET"])
@token_required
def user_info(user_id):
    if int(user_id) == g.user.get("id"):
        user_info = select_info_for_user_by_id(get_db(), user_id)

        if not user_info:
            return jsonify({"message": "Error when getting user information"}), 500

        response = {
            "Name": user_info[0],
            "Username": user_info[1],
            "Email": user_info[2],
            "Age": user_info[3],
            "Weight": user_info[4],
            "Height": user_info[5],
            "Gender": user_info[6],
            "Activity lvl": user_info[7],
        }

        return response, 200
    else:
        return jsonify({"message": "Unauthorized"}), 401


@app.route("/user_picture/<user_id>", methods=["GET"])
@token_required
def user_picture(user_id):
    if int(user_id) == g.user.get("id"):
        image_name = select_users_image_name_by_id(get_db(), user_id)
        if not image_name:
            return jsonify({"message": "Feel free to upload a profile picture"}), 200

        path = os.path.join(app.config["picture_folder"], image_name)
        if not os.path.exists(path):
            return jsonify(
                {"message": "We could not find your Profile picture, sorry"}
            ), 404

        return send_from_directory(
            directory=app.config["picture_folder"], path=image_name, as_attachment=True
        ), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401


@app.route("/personal_meals/<user_id>", methods=["GET"])
@token_required
def personal_meals(user_id):
    if int(user_id) == g.user.get("id"):
        result = select_personal_meals_with_ingredients(get_db(), user_id)
        if isinstance(result, list):
            return result, 200
        else:
            return jsonify({"message": "Error when getting meals"}), 500
    else:
        return jsonify({"message": "Unauthorized"}), 401


@app.route("/personal_ingredients/<user_id>", methods=["GET"])
@token_required
def personal_ingredients(user_id):
    if int(user_id) == g.user.get("id"):
        result = select_personal_ingredients(get_db(), user_id)
        if isinstance(result, list):
            return result, 200
        else:
            return jsonify({"message": "Error when getting ingredients"}), 500
    else:
        return jsonify({"message": "Unauthorized"}), 401


@app.route("/calender_data/<user_id>", methods=["GET"])
@token_required
def average_macros(user_id):
    if int(user_id) == g.user.get("id"):
        result = select_calender_data(get_db(), user_id)
        if isinstance(result, dict):
            return result, 200
        else:
            return jsonify({"message": "Error when getting calender data"}), 500
    else:
        return jsonify({"message": "Unauthorized"}), 401


if __name__ == "__main__":
    app.run()
