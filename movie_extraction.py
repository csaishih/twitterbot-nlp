#!/usr/bin/env python
from movie import Movie
from database import host, user, password, database
import _mysql, datetime, time

#Fetches movie titles from database
allmovies = []
connector = _mysql.connect(host,user,password,database)
for movie_table in ["moviesintheatres", "opening_movies", "upcomingmovies"]:
    connector.query("SELECT * FROM " + movie_table)
    allmovies_result = connector.store_result()
    allmovies_movie = allmovies_result.fetch_row()
    while allmovies_movie != ():
        allmovies.append(allmovies_movie[0])
        allmovies_movie = allmovies_result.fetch_row()

#Removes a word/token from a sentence
def remove_word(sentence, word):
    if ' ' + word in sentence:
        sentence = sentence.replace(' ' + word, '')
    elif word + ' ' in sentence:
        sentence = sentence.replace(word + ' ', '')
    return sentence

#Sets parental rating criteria
def parental_rating(sentence, movie):
    tokened = sentence.split(' ')
    for word in tokened:
        if word in open("movie/pg.txt").read().split('\n'):
            movie.set_parental_rating("PG")
            sentence = remove_word(sentence, word)
        elif word in open("movie/pg-13.txt").read().split('\n'):
            movie.set_parental_rating("PG-13")
            sentence = remove_word(sentence, word)
        elif word in open("movie/r.txt").read().split('\n'):
            movie.set_parental_rating("R")
            sentence = remove_word(sentence, word)
    return sentence

#Sets genre criteria
def genre(sentence, movie):
    genre_list = []
    genres = open("movie/genre.txt").read().split('\n')
    for genre in genres:
        if genre in sentence:
            genre_list.append(genre)
            sentence = remove_word(sentence, genre)
    movie.set_genre(genre_list)
    return sentence

#Sets directors criteria
def directors(sentence, movie):
    if "directed by" in sentence:
        index = sentence.index("directed by")
        sentence = sentence[index + 12:]
        name_length = 0
        sentence = sentence.replace(', ', ' ').replace(',', ' ').split(' ')
        temp = []
        for item in sentence:
            if name_length == 0:
                name = item
                name_length += 1
            elif name_length < 3:
                if item == "and" or item == "or":
                    temp.append(name)
                    temp.append(item)
                    name_length = 0
                else:
                    name += ' ' + item
                    name_length += 1
            elif name_length == 3:
                if item == "and" or item == "or":
                    temp.append(name)
                    temp.append(item)
                    name_length = 0
        temp.append(name)
        movie.set_directors(temp)
        sentence = remove_word(sentence, "directed by")
        sentence = remove_word(sentence, temp)
    return sentence

#Sets stars criteria
def stars(sentence, movie):
    if "starring" in sentence or "with" in sentence:
        if "starring" in sentence:
            keyword = "starring"
            index = sentence.index("starring")
            sentence = sentence[index + 9:]
        elif "with" in sentence:
            keyword = "with"
            index = sentence.index("with")
            sentence = sentence[index + 5:]
        name_length = 0
        sentence = sentence.replace(', ', ' ').replace(',', ' ').split(' ')
        temp = []
        for item in sentence:
            if name_length == 0:
                name = item
                name_length += 1
            elif name_length < 3:
                if item == "and" or item == "or":
                    temp.append(name)
                    temp.append(item)
                    name_length = 0
                else:
                    name += ' ' + item
                    name_length += 1
            elif name_length == 3:
                if item == "and" or item == "or":
                    temp.append(name)
                    temp.append(item)
                    name_length = 0
        temp.append(name)
        movie.set_stars(temp)
        sentence = remove_word(sentence, keyword)
        sentence = remove_word(sentence, name)
    return sentence

def get_date_interval(sentence):
    if "tomorrow" in sentence:
        if int(datetime.date.today().strftime("%m")) in [1, 3, 5, 7, 8, 10, 12] and int(datetime.date.today().strftime("%d")) == 31:
            date_interval = (time.mktime(datetime.date(int(datetime.date.today().strftime("%y")) + 2000, int(datetime.date.today().strftime("%m")) + 1, 1).timetuple()), time.mktime(datetime.date(int(datetime.date.today().strftime("%y")) + 2000, int(datetime.date.today().strftime("%m")) + 1, 1).timetuple()))
        elif int(datetime.date.today().strftime("%m")) in [4, 6, 9, 11] and int(datetime.date.today().strftime("%d")) == 30:
            date_interval = (time.mktime(datetime.date(int(datetime.date.today().strftime("%y")) + 2000, int(datetime.date.today().strftime("%m")) + 1, 1).timetuple()), time.mktime(datetime.date(int(datetime.date.today().strftime("%y")) + 2000, int(datetime.date.today().strftime("%m")) + 1, 1).timetuple()))
        elif int(datetime.date.today().strftime("%m")) == 2 and int(datetime.date.today().strftime("%d")) == 28:
            date_interval = (time.mktime(datetime.date(int(datetime.date.today().strftime("%y")) + 2000, int(datetime.date.today().strftime("%m")) + 1, 1).timetuple()), time.mktime(datetime.date(int(datetime.date.today().strftime("%y")) + 2000, int(datetime.date.today().strftime("%m")) + 1, 1).timetuple()))
        else:
            date_interval = (time.mktime(datetime.date(int(datetime.date.today().strftime("%y")) + 2000, int(datetime.date.today().strftime("%m")), int(datetime.date.today().strftime("%d")) + 1).timetuple()), time.mktime(datetime.date(int(datetime.date.today().strftime("%y")) + 2000, int(datetime.date.today().strftime("%m")), int(datetime.date.today().strftime("%d")) + 1).timetuple()))
    elif "new" in sentence:
        #Check for all new movies this month
        if int(datetime.date.today().strftime("%m")) in [1, 3, 5, 7, 8, 10, 12]:
            date_interval = ((int(time.mktime(datetime.date.today().timetuple())) - int(datetime.date.today().strftime("%d")) * 86400, int(time.mktime(datetime.date.today().timetuple())) + (31 - int(datetime.date.today().strftime("%d"))) * 86400))
        elif int(datetime.date.today().strftime("%m")) in [4, 6, 9, 11]:
            date_interval = ((int(time.mktime(datetime.date.today().timetuple())) - int(datetime.date.today().strftime("%d")) * 86400, int(time.mktime(datetime.date.today().timetuple())) + (30 - int(datetime.date.today().strftime("%d"))) * 86400))
        elif int(datetime.date.today().strftime("%m")) == 2:
            date_interval = ((int(time.mktime(datetime.date.today().timetuple())) - int(datetime.date.today().strftime("%d")) * 86400, int(time.mktime(datetime.date.today().timetuple())) + (28 - int(datetime.date.today().strftime("%d"))) * 86400))
    else:
        date_interval = (time.mktime(datetime.date.today().timetuple()), time.mktime(datetime.date.today().timetuple()))
    return date_interval

def fix_time(sentence):
    i = 0
    while len(sentence) > i:
        if sentence[i].isdigit():
            if i + 1 == len(sentence):
                if sentence[i] == '0' and i > 1 and sentence[i - 1].isdigit():
                    if len(sentence) > 2:
                        if sentence[i - 2] != ':':
                            sentence = sentence[:i + 1] + ":00"
                    elif sentence[i - 1] != '0':
                        sentence = sentence[:i + 1] + ":00"
                else:
                    if len(sentence) > 2:
                        if sentence[i - 2] != ':':
                            sentence = sentence[:i + 1] + ":00"
                    else:
                        sentence = sentence[:i + 1] + ":00"
            elif sentence[i + 1] == ' ':
                if sentence[i] == '0' and i > 1 and sentence[i - 1].isdigit():
                    if len(sentence) > 2:
                        if sentence[i - 2] != ':':
                            sentence = sentence[:i + 1] + ":00" + sentence[i + 1:]
                    elif sentence[i - 1] != '0':
                        sentence = sentence[:i + 1] + ":00" + sentence[i + 1:]
                else:
                    if len(sentence) > 2:
                        if sentence[i - 2] != ':':
                            sentence = sentence[:i + 1] + ":00" + sentence[i + 1:]
                    else:
                        sentence = sentence[:i + 1] + ":00" + sentence[i + 1:]
        i += 1
    return sentence

def get_time_interval(sentence):
    sentence = fix_time(sentence)
    i = 0
    lis = []
    if ':' in sentence:
        while len(sentence) > i:
            if sentence[i] == ':':
                lis.append([sentence[i - 2: i], sentence[i + 1: i + 3]])
            i += 1
    for time in lis:
        time[0] = time[0].rstrip()
        time[0] = int(time[0])
        if time[0] < 12:
            time[0] += 12
        time[1] = int(time[1])
    return lis

def check_product(name_list, sentence, p, g, d, s):
    offsettime = 1
    before = "before" in sentence
    after = "after" in sentence
    around = "around" in sentence
    filtered = []
    showtime_results = []
    showtime_theatres = []
    connector.query("SELECT title,theatre_name,date_time,product_id FROM onconnect")
    showtime_result = connector.store_result()
    showtime_movie = showtime_result.fetch_row()
    while showtime_movie != ():
        showtime_results.append(showtime_movie[0])
        theatre = showtime_movie[0][1].lower().replace("the ", "").replace(" cinemas", "").replace(" cinema", "").replace(" theatre", "").replace('-', ' ').replace(" and", "").replace(" in", "").replace(" at", "").replace(" for", "").split(" ")
        if (theatre, showtime_movie[0][1]) not in showtime_theatres:
            showtime_theatres.append((theatre, showtime_movie[0][1]))
        showtime_movie = showtime_result.fetch_row()
    theatre_list = []
    matchmax = 0
    count = 0
    for theatre in showtime_theatres:
        for word in theatre[0]:
            if word in sentence:
                count += 1
        theatre[0].append(count)
        if count > matchmax:
            matchmax = count
        count = 0
    if matchmax != 0:
        for theatre in showtime_theatres:
            if theatre[0][-1] == matchmax:
                theatre_list.append(theatre[1])

    date_interval = get_date_interval(sentence)
    time_interval = get_time_interval(sentence)
    if len(time_interval) == 1:
        time_interval.append([23, 59])

    if name_list != []:
        if theatre_list == []:
            for mov in showtime_results:
                t = mov[2][:mov[2].index("T")].split('-')
                h = mov[2][mov[2].index("T") + 1:].split(':')
                h[0] = int(h[0])
                h[1] = int(h[1])
                if mov[0] in name_list and time.mktime(datetime.date(int(t[0]), int(t[1]), int(t[2])).timetuple()) >= date_interval[0] and date_interval[1] >= time.mktime(datetime.date(int(t[0]), int(t[1]), int(t[2])).timetuple()):
                    if time_interval == []:
                        filtered.append(mov)
                    else:
                        if before:
                            if h[0] < time_interval[0][0]:
                                filtered.append(mov)
                            elif h[0] == time_interval[0][0] and h[1] < time_interval[0][1]:
                                filtered.append(mov)
                        elif after:
                            if h[0] > time_interval[0][0]:
                                filtered.append(mov)
                            elif h[0] == time_interval[0][0] and h[1] > time_interval[0][1]:
                                filtered.append(mov)
                        elif around:
                            if h[0] - offsettime < time_interval[0][0] or h[0] + offsettime > time_interval[0][0]:
                                filtered.append(mov)
                        else:
                            if h[0] >= time_interval[0][0] and h[0] <= time_interval[1][0]:
                                if h[0] == time_interval[0][0] and h[0] == time_interval[1][0]:
                                    if h[1] >= time_interval[0][1] and h[1] <= time_interval[1][1]:
                                        filtered.append(mov)
                                elif h[0] == time_interval[0][0]:
                                    if h[1] >= time_interval[0][1]:
                                        filtered.append(mov)
                                elif h[0] == time_interval[1][0]:
                                    if h[1] >= time_interval[1][1]:
                                        filtered.append(mov)
                                elif h[0] > time_interval[0][0]:
                                    filtered.append(mov)
                                elif h[0] < time_interval[1][0]:
                                    filtered.append(mov)
        else:
            for mov in showtime_results:
                t = mov[2][:mov[2].index("T")].split('-')
                h = mov[2][mov[2].index("T") + 1:].split(':')
                h[0] = int(h[0])
                h[1] = int(h[1])
                if mov[0] in name_list and mov[1] in theatre_list and time.mktime(datetime.date(int(t[0]), int(t[1]), int(t[2])).timetuple()) >= date_interval[0] and date_interval[1] >= time.mktime(datetime.date(int(t[0]), int(t[1]), int(t[2])).timetuple()):
                    if time_interval == []:
                        filtered.append(mov)
                    else:
                        if before:
                            if h[0] < time_interval[0][0]:
                                filtered.append(mov)
                            elif h[0] == time_interval[0][0] and h[1] < time_interval[0][1]:
                                filtered.append(mov)
                        elif after:
                            if h[0] > time_interval[0][0]:
                                filtered.append(mov)
                            elif h[0] == time_interval[0][0] and h[1] > time_interval[0][1]:
                                filtered.append(mov)
                        elif around:
                            if h[0] - offsettime < time_interval[0][0] or h[0] + offsettime > time_interval[0][0]:
                                filtered.append(mov)
                        else:
                            if h[0] >= time_interval[0][0] and h[0] <= time_interval[1][0]:
                                if h[0] == time_interval[0][0] and h[0] == time_interval[1][0]:
                                    if h[1] >= time_interval[0][1] and h[1] <= time_interval[1][1]:
                                        filtered.append(mov)
                                elif h[0] == time_interval[0][0]:
                                    if h[1] >= time_interval[0][1]:
                                        filtered.append(mov)
                                elif h[0] == time_interval[1][0]:
                                    if h[1] >= time_interval[1][1]:
                                        filtered.append(mov)
                                elif h[0] > time_interval[0][0]:
                                    filtered.append(mov)
                                elif h[0] < time_interval[1][0]:
                                    filtered.append(mov)

    elif name_list == [] and p and g and d and s:
        if theatre_list == []:
            for mov in showtime_results:
                t = mov[2][:mov[2].index("T")].split('-')
                h = mov[2][mov[2].index("T") + 1:].split(':')
                h[0] = int(h[0])
                h[1] = int(h[1])
                if time.mktime(datetime.date(int(t[0]), int(t[1]), int(t[2])).timetuple()) >= date_interval[0] and date_interval[1] >= time.mktime(datetime.date(int(t[0]), int(t[1]), int(t[2])).timetuple()):
                    if time_interval == []:
                        filtered.append(mov)
                    else:
                        if before:
                            if h[0] < time_interval[0][0]:
                                filtered.append(mov)
                            elif h[0] == time_interval[0][0] and h[1] < time_interval[0][1]:
                                filtered.append(mov)
                        elif after:
                            if h[0] > time_interval[0][0]:
                                filtered.append(mov)
                            elif h[0] == time_interval[0][0] and h[1] > time_interval[0][1]:
                                filtered.append(mov)
                        elif around:
                            if h[0] - offsettime < time_interval[0][0] or h[0] + offsettime > time_interval[0][0]:
                                filtered.append(mov)
                        else:
                            if h[0] >= time_interval[0][0] and h[0] <= time_interval[1][0]:
                                if h[0] == time_interval[0][0] and h[0] == time_interval[1][0]:
                                    if h[1] >= time_interval[0][1] and h[1] <= time_interval[1][1]:
                                        filtered.append(mov)
                                elif h[0] == time_interval[0][0]:
                                    if h[1] >= time_interval[0][1]:
                                        filtered.append(mov)
                                elif h[0] == time_interval[1][0]:
                                    if h[1] >= time_interval[1][1]:
                                        filtered.append(mov)
                                elif h[0] > time_interval[0][0]:
                                    filtered.append(mov)
                                elif h[0] < time_interval[1][0]:
                                    filtered.append(mov)
        else:
            for mov in showtime_results:
                t = mov[2][:mov[2].index("T")].split('-')
                h = mov[2][mov[2].index("T") + 1:].split(':')
                h[0] = int(h[0])
                h[1] = int(h[1])

                if mov[1] in theatre_list and time.mktime(datetime.date(int(t[0]), int(t[1]), int(t[2])).timetuple()) >= date_interval[0] and date_interval[1] >= time.mktime(datetime.date(int(t[0]), int(t[1]), int(t[2])).timetuple()):
                    if time_interval == []:
                        filtered.append(mov)
                    else:
                        if before:
                            if h[0] < time_interval[0][0]:
                                filtered.append(mov)
                            elif h[0] == time_interval[0][0] and h[1] < time_interval[0][1]:
                                filtered.append(mov)
                        elif after:
                            if h[0] > time_interval[0][0]:
                                filtered.append(mov)
                            elif h[0] == time_interval[0][0] and h[1] > time_interval[0][1]:
                                filtered.append(mov)
                        elif around:
                            if h[0] - offsettime < time_interval[0][0] or h[0] + offsettime > time_interval[0][0]:
                                filtered.append(mov)
                        else:
                            if h[0] >= time_interval[0][0] and h[0] <= time_interval[1][0]:
                                if h[0] == time_interval[0][0] and h[0] == time_interval[1][0]:
                                    if h[1] >= time_interval[0][1] and h[1] <= time_interval[1][1]:
                                        filtered.append(mov)
                                elif h[0] == time_interval[0][0]:
                                    if h[1] >= time_interval[0][1]:
                                        filtered.append(mov)
                                elif h[0] == time_interval[1][0]:
                                    if h[1] >= time_interval[1][1]:
                                        filtered.append(mov)
                                elif h[0] > time_interval[0][0]:
                                    filtered.append(mov)
                                elif h[0] < time_interval[1][0]:
                                    filtered.append(mov)
    if filtered == []:
        return "none"
    else:
        connector.query("SELECT response_id FROM bi_response ORDER BY response_id DESC LIMIT 1")
        results = connector.store_result()
        answer = results.fetch_row()
        if answer == ():
            res_id = 0
        else:
            res_id = int(answer[0][0])
        res_id += 1
        for product in filtered:
            connector.query("INSERT INTO bi_response (response_id,tweet_id,user_id,product_id,price,created_at) VALUES (" + str(res_id) + ",0,0," + str(product[3]) + ",0,0)")
        return res_id

def movie(sentence):
    sentence = sentence.lower()
    movie_list = []
    m = Movie()
    sentence = parental_rating(sentence, m)
    sentence = genre(sentence, m)
    sentence = directors(sentence, m)
    sentence = stars(sentence, m)

    p = m.get_parental_rating() == ''
    g = m.get_genre() == []
    d = m.get_directors() == []
    s = m.get_stars() == []

    for movie in allmovies:
        parental_rating_pass = p
        genre_pass = g
        director_pass = d
        stars_pass = s
        if not parental_rating_pass:
            parental_rating_pass = m.get_parental_rating() == movie[2]

        if not genre_pass:
            for m_genre in m.get_genre():
                genre_pass = m_genre in movie[4].lower()

        if not director_pass:
            i = 1
            if movie[6].lower() != '':
                temp = movie[6].lower().split(', ')
                for actor in temp:
                    director_pass = actor in m.get_directors()[i-1].lower()
                    if director_pass:
                        break;
                while i < len(m.get_directors()):
                    temp1 = False
                    temp2 = False
                    for actor in temp:
                        temp1 = actor in m.get_directors()[i-1].lower()
                        if temp1:
                            break;
                    for actor in temp:
                        temp2 = actor in m.get_directors()[i+1].lower()
                        if temp2:
                            break;
                    if m.get_directors()[i].lower() == 'and':
                        director_pass = temp1 and temp2
                    elif m.get_directors()[i].lower() == 'or':
                        director_pass = temp1 or temp2
                    if director_pass and i + 2 < len(m.get_directors()) and m.get_directors()[i + 2].lower() == 'or':
                        break;
                    i += 2

        if not stars_pass:
            i = 1
            if movie[8].lower() != '':
                temp = movie[8].lower().split(', ')
                for actor in temp:
                    stars_pass = actor in m.get_stars()[i-1].lower()
                    if stars_pass:
                        break;
                while i < len(m.get_stars()):
                    temp1 = False
                    temp2 = False
                    for actor in temp:
                        temp1 = actor in m.get_stars()[i-1].lower()
                        if temp1:
                            break;
                    for actor in temp:
                        temp2 = actor in m.get_stars()[i+1].lower()
                        if temp2:
                            break;
                    if m.get_stars()[i].lower() == 'and':
                        stars_pass = temp1 and temp2
                    elif m.get_stars()[i].lower() == 'or':
                        stars_pass = temp1 or temp2
                    if stars_pass and i + 2 < len(m.get_stars()) and m.get_stars()[i + 2].lower() == 'or':
                        break;
                    i += 2

        if parental_rating_pass and genre_pass and director_pass and stars_pass:
            if p and g and d and s:
                return check_product([], sentence, p, g, d, s)
            movie_list.append(movie[1])
    return check_product(movie_list, sentence, p, g, d, s)

connector = _mysql.connect(host,user,password,database)
connector.query("SELECT * FROM mentions ORDER BY mention_id DESC LIMIT 1")
results = connector.store_result()
tweet = results.fetch_row()[0][1]
response = movie(tweet)
print(response)
