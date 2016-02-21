(SELECT home as team FROM matches) UNION ALL (SELECT away as team FROM matches) ORDER BY team;
