-- Show all teams in DB ordered by name
SELECT COALESCE(home, away) AS teams FROM matches ORDER BY teams;
