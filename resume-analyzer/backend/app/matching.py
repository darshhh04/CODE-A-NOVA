from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.cleaning import full_clean_resume

def compute_match(resume_text, jd_text, top_n_missing: int = 10) -> dict:
    
    resume_clean = full_clean_resume(resume_text)
    jd_clean = full_clean_resume(jd_text)

    
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])


    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    match_score = round(float(similarity) * 100, 2)

    missing_keywords = find_missing_keywords(
        vectorizer, tfidf_matrix, top_n_missing
    )

    return {
        "match_score": match_score,
        "missing_keywords": missing_keywords,
    }


def find_missing_keywords(vectorizer, tfidf_matrix, top_n: int) -> list[str]:
    
    feature_names = vectorizer.get_feature_names_out()
    resume_vector = tfidf_matrix[0].toarray()[0] 
    jd_vector = tfidf_matrix[1].toarray()[0]      

    candidates = []
    for idx, term in enumerate(feature_names):
        if jd_vector[idx] > 0 and resume_vector[idx] == 0:
            candidates.append((term, jd_vector[idx]))

    candidates.sort(key=lambda pair: pair[1], reverse=True)
    return [term for term, _weight in candidates[:top_n]]