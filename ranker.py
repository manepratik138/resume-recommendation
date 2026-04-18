from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_resume(resume, job):

    vec = TfidfVectorizer()
    x = vec.fit_transform([resume, job])

    score = cosine_similarity(x[0], x[1])[0][0]

    return round(score * 100, 2)
