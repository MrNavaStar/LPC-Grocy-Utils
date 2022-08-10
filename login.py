from requests import Session


def getCookie(base_url, user, password):
    session = Session()
    session.post(f"{base_url.replace('/api', '')}/login", data={"username": user, "password": password}, headers={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'})
    return session.cookies.get("grocy_session")