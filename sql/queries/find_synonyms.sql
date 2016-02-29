SELECT m.home, m.away, m.date FROM matches m, (SELECT away, date FROM matches GROUP BY away, date HAVING COUNT(*) > 1) q WHERE q.away = m.away AND q.date = m.date ORDER BY q.away, q.date;

SELECT m.home, m.away, m.date FROM matches m, (SELECT home, date FROM matches GROUP BY home, date HAVING COUNT(*) > 1) q WHERE q.home = m.home AND q.date = m.date ORDER BY q.home, q.date;
