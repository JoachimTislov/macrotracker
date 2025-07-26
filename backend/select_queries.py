import sqlite3


#### SELECT QUERIES, Retrieving data####
def run_select_query(conn, sql_query, identifier):
    cur = conn.cursor()
    try:
        cur.execute(sql_query, (identifier,))
        result = cur.fetchone()
        cur.close()

        if result:
            return result
        else:
            return None
    except sqlite3.Error as err:
        print("Error: {}. When running the query: {}".format(err, sql_query))


#### FetchOne ####
def select_user_by_id(conn, user_id):
    sql = "SELECT user_no, username FROM users WHERE user_no=?"
    return run_select_query(conn, sql, user_id)


def select_user_by_token(conn, token):
    sql = "SELECT user_no, username FROM users WHERE token=?"
    return run_select_query(conn, sql, token)


def select_user_by_id(conn, user_id):
    sql = "SELECT user_no, username FROM users WHERE user_no=?"
    return run_select_query(conn, sql, user_id)


def select_info_for_user_by_id(conn, user_id):
    sql = "SELECT name, username, email, age, weight, height, gender, activity_lvl FROM users WHERE user_no=?"
    return run_select_query(conn, sql, user_id)


def select_users_image_name_by_id(conn, user_id):
    sql = "SELECT profile_picture_name FROM users WHERE user_no=?"
    return run_select_query(conn, sql, user_id)[0]


def select_user_no_by_username(conn, username):
    sql = "SELECT user_no FROM users WHERE username=?"
    return run_select_query(conn, sql, username)[0]  # Indexing the tuple


def select_password_for_given_user(conn, username):
    sql = "SELECT password FROM users WHERE username=?"
    return run_select_query(conn, sql, username)


def select_user_id_and_username(conn, username):
    sql = "SELECT user_no, username FROM users WHERE username=?"
    return run_select_query(conn, sql, username)


def select_user_id_and_password(conn, username):
    sql = "SELECT user_no, password FROM users WHERE username=?"
    return run_select_query(conn, sql, username)


##### fetchAll #####
def select_all_users_username(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT username FROM users")
        result = cur.fetchall()
        cur.close()

        if result:
            return result
        else:
            return None
    except sqlite3.Error as err:
        print("Error, selecting all_users_username: {}".format(err))


def select_all_users_emails(conn):
    cur = conn.cursor()
    try:
        result = []
        cur.execute("SELECT email FROM users")
        result = [row[0] for row in cur.fetchall()]
        cur.close()

        if result:
            return result
        else:
            return None
    except sqlite3.Error as err:
        print("Error, selecting all_users_emails: {}".format(err))


def select_all_users_username_except_one(conn, user_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT username FROM users WHERE user_no != ?", (user_id,))
        result = cur.fetchall()
        cur.close()

        if result:
            return result
        else:
            return None
    except sqlite3.Error as err:
        print("Error, selecting all_users_username_except_one: {}".format(err))


def select_all_users_emails_except_one(conn, user_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT email FROM users WHERE user_no != ?", (user_id,))
        result = cur.fetchall()
        cur.close()

        if result:
            return result
        else:
            return None
    except sqlite3.Error as err:
        print("Error, selecting all_users_emails_except_one: {}".format(err))


def select_meal_ingredients_by_id(conn, id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM personal_ingredients WHERE personal_meal_no=?", (id,)
        )
        result = cur.fetchall()
        cur.close()

        if result:
            return result
        else:
            return None
    except sqlite3.Error as err:
        print("Error: {}".format(err))


def select_personal_meals_with_ingredients(conn, user_no):
    cur = conn.cursor()
    try:
        personal_meals_with_ingredients = []
        cur.execute(
            """SELECT mi.personal_meal_no, pi.personal_ingredient_no, pi.ingredient_name, 
                    pi.amount, pi.protein, pi.calories, pi.carbohydrates, pi.fat, pi.sugar
                    FROM meal_ingredients mi 
                    LEFT JOIN personal_ingredients pi ON mi.personal_ingredient_no == pi.personal_ingredient_no
                    WHERE mi.personal_meal_no IN 
                    (SELECT pm.personal_meal_no 
                    FROM personal_meals pm 
                    WHERE pm.user_no =?) """,
            (user_no,),
        )
        personal_meals_with_ingredients += [list(row) for row in cur.fetchall()]

        personal_meals = []
        cur.execute("SELECT * FROM personal_meals pm WHERE pm.user_no = ?", (user_no,))
        personal_meals += [list(row) for row in cur.fetchall()]

        meals_with_ingredients = []
        for i, entry in enumerate(personal_meals):
            meals_with_ingredients.append(
                {
                    "meal_id": entry[0],
                    "name": entry[1],
                    "user_id": entry[2],
                    "protein": entry[3],
                    "calories": entry[4],
                    "carbohydrates": entry[5],
                    "fat": entry[6],
                    "sugar": entry[7],
                    "ingredients": [],
                }
            )

            for ingredient in personal_meals_with_ingredients:
                if ingredient[0] == entry[0]:
                    meals_with_ingredients[i]["ingredients"].append(
                        {
                            "ingredient_id": ingredient[1],
                            "name": ingredient[2],
                            "amount": ingredient[3],
                            "protein": ingredient[4],
                            "calories": ingredient[5],
                            "carbohydrates": ingredient[6],
                            "fat": ingredient[7],
                            "sugar": ingredient[8],
                        }
                    )

        return meals_with_ingredients
    except sqlite3.Error as err:
        print("Error, selecting personal_meals_with_ingredients: {},".format(err))
        return False


def select_personal_ingredients(conn, user_no):
    cur = conn.cursor()
    try:
        ingredients_data = []
        cur.execute(
            "SELECT * FROM personal_ingredients pi WHERE pi.user_no =?", (user_no,)
        )
        ingredients_data += [list(row) for row in cur.fetchall()]
        cur.close()

        ingredients_arr = []
        for ingredient in ingredients_data:
            ingredients_arr.append(
                {
                    "ingredient_id": ingredient[0],
                    "name": ingredient[2],
                    "amount": ingredient[3],
                    "protein": ingredient[4],
                    "calories": ingredient[5],
                    "carbohydrates": ingredient[6],
                    "fat": ingredient[7],
                    "sugar": ingredient[8],
                }
            )

        return ingredients_arr
    except sqlite3.Error as err:
        print("Error, selecting personal_ingredients: {}".format(err))
        return False


def select_calender_data(conn, user_no):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM personal_meals pm WHERE pm.user_no =?", (user_no,))
        meal_data = [list(row) for row in cur.fetchall()]  # Converting tuples to lists

        calender = []
        for entry in meal_data:
            cur.execute(
                "SELECT * FROM meal_calender WHERE personal_meal_no = ?", (entry[0],)
            )
            calender += [
                {
                    "calender_id": row[0],
                    "meal": row[1],
                    "date": row[2],
                    "time_of_day": row[3],
                }
                for row in cur.fetchall()
            ]

        cur.close()

        hashMap = {}

        for entry in calender:
            for row in meal_data:
                if entry["meal"] == row[0]:
                    entry["meal"] = {
                        "meal_id": row[0],
                        "name": row[1],
                        "user_id": row[2],
                        "protein": row[3],
                        "calories": row[4],
                        "carbohydrates": row[5],
                        "fat": row[6],
                        "sugar": row[7],
                    }

            date = entry["date"]
            if date not in hashMap:
                hashMap[date] = []

            hashMap[date].append(entry)

        return hashMap

    except sqlite3.Error as err:
        print("Error, selecting average macros: {}".format(err))
        return False


def select_meals_the_ingredient_were_in(conn, ingredient_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT personal_meal_no FROM meal_ingredients mi WHERE mi.personal_ingredient_no =?",
            (ingredient_id,),
        )
        meal_ids = [row[0] for row in cur.fetchall()]
        cur.close()

        return meal_ids
    except sqlite3.Error as err:
        print("Error, selecting meals the ingredient were in: {}".format(err))


def select_users_meals(conn, user_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT personal_meal_no FROM personal_meals pm WHERE pm.user_no =?",
            (user_id,),
        )
        meal_ids = [row[0] for row in cur.fetchall()]
        cur.close()

        return meal_ids
    except sqlite3.Error as err:
        print("Error, selecting users meals the ingredient were in: {}".format(err))


def select_ingredient_and_meal_entry_in_meal_ingredients(conn, meal_id, ingredient_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT personal_meal_no, personal_ingredient_no FROM meal_ingredients mi WHERE mi.personal_meal_no =? AND mi.personal_ingredient_no =?",
            (meal_id, ingredient_id),
        )
        entry = cur.fetchone()
        cur.close()

        return entry
    except sqlite3.Error as err:
        print("Error, selecting users meals the ingredient were in: {}".format(err))


def select_users_ingredients(conn, user_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT personal_ingredient_no FROM personal_ingredients pm WHERE pm.user_no =?",
            (user_id,),
        )
        meal_ids = [row[0] for row in cur.fetchall()]
        cur.close()

        return meal_ids
    except sqlite3.Error as err:
        print("Error, selecting users meals the ingredient were in: {}".format(err))


def select_users_calender_entries(conn, meal_id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT calender_id FROM meal_calender pm WHERE pm.personal_meal_no =?",
            (meal_id,),
        )
        meal_ids = [row[0] for row in cur.fetchall()]
        cur.close()

        return meal_ids
    except sqlite3.Error as err:
        print("Error, selecting users meals the ingredient were in: {}".format(err))


def select_ingredient_by_id(conn, id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM personal_ingredients pi WHERE pi.personal_ingredient_no =?",
            (id,),
        )
        ingredient = list(cur.fetchone())
        cur.close()

        return ingredient
    except sqlite3.Error as err:
        print("Error, selecting ingredient by id: Error --- {}".format(err))


def select_meal_by_id(conn, id):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM personal_meals pm WHERE pm.personal_meal_no =?", (id,)
        )
        meal = list(cur.fetchone())
        cur.close()

        return meal
    except sqlite3.Error as err:
        print("Error, selecting ingredient by id: {}".format(err))


def select_password_by_id(conn, id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT password FROM users u WHERE u.user_no =?", (id,))
        result = cur.fetchone()[0]
        cur.close()
        return result
    except sqlite3.Error as err:
        print("Error, selecting password by user id: {}".format(err))


def select_user_profile_picture_name(conn, user_no):
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT profile_picture_name FROM users WHERE user_no = ?", (user_no,)
        )
        result = cur.fetchone()[0]
        cur.close()
        return result

    except sqlite3.Error as err:
        print("Error, selecting profile picture link: {}".format(err))
