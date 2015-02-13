import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='curie_finish')
cur = conn.cursor()
title="겨울 사랑"
artist="유진영"
album="고백"
beat="12fef"
query = "INSERT INTO link_ids(`song_id`, `app_id`, `link_id`, `usable`) VALUES((SELECT id FROM curie_finish.song_info WHERE `title`=\'" + title + "\' AND `artist`=\'" + artist + "\' AND `album` = \'" + album + "\' limit 1), 1, \'" + beat + "\', True)"
cur.execute(query)
