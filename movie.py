class Movie:
    def __init__(self,
                 title = '',
                 parental_rating = '',
                 duration = '',
                 genre = [],
                 rating = -1,
                 directors = [],
                 writers = [],
                 stars = [],
                 cast = [],
                 language = '',
                 release_date = 0,
                 keywords = [],
                 release_interval = (0, 0)):
        self.title = title
        self.parental_rating = parental_rating
        self.duration = duration
        self.genre = genre
        self.rating = rating
        self.directors = directors
        self.writers = writers
        self.stars = stars
        self.cast = cast
        self.keywords = keywords
        self.language = language
        self.release_date = release_date
        self.release_interval = release_interval

    def set_title(self, title):
        self.title = title

    def set_parental_rating(self, parental_rating):
        self.parental_rating = parental_rating

    def set_duration(self, duration):
        self.duration = duration

    def set_genre(self, genre):
        self.genre = genre

    def set_rating(self, rating):
        self.rating = rating

    def set_directors(self, directors):
        self.directors = directors

    def set_writers(self, writers):
        self.writers = writers

    def set_stars(self, stars):
        self.stars = stars

    def set_cast(self, cast):
        self.cast = cast

    def set_keywords(self, keywords):
        self.keywords = keywords

    def set_language(self, language):
        self.language = language

    def set_release_date(self, release_date):
        self.release_date = release_date

    def set_release_interval(self, release_interval):
        self.release_interval = release_interval

    def get_title(self):
        return self.title

    def get_parental_rating(self):
        return self.parental_rating

    def get_duration(self):
        return self.duration

    def get_genre(self):
        return self.genre

    def get_rating(self):
        return self.rating

    def get_directors(self):
        return self.directors

    def get_writers(self):
        return self.writers

    def get_stars(self):
        return self.stars

    def get_cast(self):
        return self.cast

    def get_keywords(self):
        return self.keywords

    def get_language(self):
        return self.language

    def get_release_date(self):
        return self.release_date

    def get_release_interval(self):
        return self.release_interval

    def __repr__(self):
        if self.parental_rating == '':
            self.parental_rating = "Not available"
        if self.duration == '':
            self.duration = "Not available"
        if self.rating == -1:
            self.rating = "Not available"
        if self.language == '':
            self.language = "Not available"
        if self.release_date == 0:
            self.release_date = "Not available"
        else:
            self.release_date = datetime.datetime.fromtimestamp(int(self.release_date)).strftime('%d-%m-%Y')
        return "Title: " + self.title + "\nParental rating: " + self.parental_rating + "\nDuration: " + self.duration + "\nGenre: " + str(self.genre) + "\nRating -/10: " + str(self.rating) + "\nDirectors: " + str(self.directors) + "\nWriters: " + str(self.writers) + "\nStars: " + str(self.stars) + "\nCast: " + str(self.cast) + "\nRelease date: " + str(self.release_date) + "\nKeywords: " + str(self.keywords) + "\nLanguage: " + self.language + "\nRelease interval: " + str(self.release_interval)
