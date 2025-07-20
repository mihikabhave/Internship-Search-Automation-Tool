import random
import time
import sqlite3
import requests
import pandas as pd
import urllib.parse

 
def build_query(file, shuffle=False):
    df = pd.read_excel(file)
    keywords = [str(value).strip() for value in df['keywords'] if pd.notna(value) and str(value).strip().lower() != "nan"]
    if shuffle:
        random.shuffle(keywords)
    parts = [f'"{x}"' if ' ' in x else x for x in keywords]

    alternatives = []
    df['alternatives'] = df['alternatives'].astype(str).fillna('')
    for alt_string in df['alternatives']:
        if alt_string and alt_string.lower() != 'nan':
            terms = [x.strip() for x in alt_string.split(',') if x.strip() and x.strip().lower() != 'nan']
            alternatives.extend(terms)
    if shuffle:
        random.shuffle(alternatives)
    alternatives = [f'"{term}"' if ' ' in term else term for term in alternatives]
    if alternatives:
        or_group = ' OR '.join(alternatives)
        parts.append(f'({or_group})')

    restricted = []
    df['restrict'] = df['restrict'].astype(str).fillna('')
    for restrict_string in df['restrict']:
        if restrict_string and restrict_string.lower() != 'nan':
            terms = [x.strip() for x in restrict_string.split(',') if x.strip()]
            restricted.extend(terms)
    if shuffle:
        random.shuffle(restricted)
    parts += [f'-"{term}"' if ' ' in term else f'-{term}' for term in restricted]
    query = ' '.join(parts)
    return query

def create_table():
    conn = sqlite3.connect("results.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            url TEXT UNIQUE
        )
    """)
    conn.commit()
    return conn, cursor

def save_results_sql(results, conn, cursor):
    for url in results:
        try:
            cursor.execute("INSERT OR IGNORE INTO urls (url) VALUES (?)", (url,))
        except:
            pass
    conn.commit()

def run_new(q,key,se_id,pages=10):
    
    if not key or not se_id:
        raise ValueError("Missing API key or CX ID.")

    results = set()
    for page in range(1, pages + 1):

        start = (page - 1) * 10 + 1
        if start > 91:
            print("Reached Google search limit (start > 91). Stopping search.")
            break
        encoded_query = urllib.parse.quote_plus(q)
        url = (
            f"https://www.googleapis.com/customsearch/v1?"
            f"key={key}&cx={se_id}&q={encoded_query}&start={start}"
        )
        print("Request URL:", url)

        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print("Response:", response.text)

    
        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
            break

        data = response.json()

        if "error" in data:
            print(f"API Error: {data['error']['message']}")
            break

        items = data.get("items", [])
        if not items:
            print("No more items returned.")
            break

        for item in items:
         link = item.get("link")
         if link:
          l = link.lower()
          if (not any(x in l for x in ['reddit','tiktok', 'youtube','quora'])):
            results.add(link)
        time.sleep(1)  

    conn, cursor = create_table()
    save_results_sql(results, conn, cursor)
    return results

def save_database():
    conn = sqlite3.connect("results.db")
    df = pd.read_sql_query("SELECT * FROM urls", conn)
    return df

def download():
   conn = sqlite3.connect("results.db")
   df = pd.read_sql_query("SELECT * FROM urls", conn)
   conn.close()
   df.to_csv('results.csv')


