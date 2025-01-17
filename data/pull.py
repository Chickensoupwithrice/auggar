import asyncio
import httpx
import xml.etree.ElementTree as ET
import psycopg2

#[WHAT IS THIS]
#It scrapes the URL's list below for their rss XML feeds and commits them to a postgres db.
#It also uses an exception to do this which is emphasiszed for flow control in Python. Wild right? 

#open initial connection
conn = psycopg2.connect("")

#open initial cursor
cur = conn.cursor()

URLS =  [
        "http://nonmateria.com/rss.xml",
        "https://notes.neeasade.net/rss.xml",
        "https://aless.co/rss.xml",
        "https://writing.natwelch.com/feed.rss",
        "https://resevoir.net/rss.xml",
        "https://szymonkaliski.com/feed.xml",
        "https://xj-ix.luxe/feed.atom",
        "http://nonmateria.com/rss.xml",
        "https://oddworlds.org/rss.xml",
        "https://chad.is/rss.xml",
        "https://bismuth.garden/feed.xml",
        "https://xvw.github.io/atom.xml",
        "https://now.lectronice.com/feed.xml",
        "https://longest.voyage/index.xml",
        "https://kokorobot.ca/links/rss.xml",
        "https://ameyama.com/blog/rss.xml",
        "https://phse.net/post/index.xml",
        "https://rosano.ca/feed",
        "https://teknari.com/feed.xml",
        "https://serocell.com/feeds/serocell.xml",
        "https://gueorgui.net/feed.xml",
        "https://sixey.es/feed.xml",
        "https://icyphox.sh/blog/feed.xml",
        "https://royniang.com/rss.xml",
        "https://crlf.site/feed.xml",
        "https://system32.simone.computer/rss.xml",
        "https://simply.personal.jenett.org/feed/",
        "https://q.pfiffer.org/feed.xml",
        "https://www.edwinwenink.xyz/index.xml",
        "https://www.mentalnodes.com/sitemap.xml",
        "https://materialfuture.net/rss.xml",
        "https://travisshears.com/index.xml",
        "https://ix5.org/thoughts/feeds/all.atom.xml",
        "https://nor.the-rn.info/feed.xml",
        "https://inqlab.net/posts.xml",
        "https://metasyn.pw/rss.xml",
        "https://milofultz.com/atom.xml",
        "https://wolfmd.me/feed.xml",
        "https://irimi.one/atom.xml",
        "https://natehn.com/index.xml",
        "https://www.gr0k.net/blog/feed.xml",
        "https://tendigits.space/feed.xml",
        "https://wiki.xxiivv.com/links/rss.xml"]

async def main():
    async with httpx.AsyncClient() as client:
        for url in URLS:
            try: 
                response = await client.get(url, timeout=30.0)
                
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")
                continue
            
            try:
                #give root a body of XML as a string.
                root = ET.fromstring(response.text)
            except:
                continue
            
            #there is a variety of XML namespaces we have to deal with, the ones that
            #are not handled in the first try will get caught in the exception and 
            #and sent to the code in the next for loops exception. They required extra
            #indexing. 
            
            try:
                links = [x for x in root if x.tag.split("}")[1] in ("entry", "item")]
            except IndexError:
                links = [x for x in root[0] if x.tag in ("entry", "item")]  

            for link in links:
                title = [x.text for x in link if x.tag.split("}")[1] == "title"]
                link_url = [x.attrib["href"] for x in link if x.tag.split("}")[1] == "link"]

                if title and link_url:
                    print("Found {} with HREF {}".format(title, link_url))
                    try:
                        cur.execute("INSERT INTO posts (host_title, post_url) VALUES (%s, %s)", 
                                   (title[0], link_url[0]))
                        conn.commit()
                    except: # TODO: Find the exact exception
                        create_database()
                        cur.execute("INSERT INTO posts (host_title, post_url) VALUES (%s, %s)", 
                                   (title[0], link_url[0]))
                        conn.commit()
                    print("committed")
                    print(f"{title} and {link_url} submitted to database.")

    cur.execute("SELECT * FROM posts;")
    rows = cur.fetchall()
    for r in rows:
        print(f"{r[0]} and {r[1]}") 
    cur.close()
    conn.close()  

def create_database():
    tableName = "posts"
    createTable = "create table " + tableName + "(id bigserial, host_title TEXT, post_url TEXT, post_date DATE)"

    curr.execute(createTable)
    conn.commit()
    return

if __name__ == '__main__':
    asyncio.run(main())
