WITH SerienRings AS (
    SELECT
        ScheibenID,
        SUM(CASE WHEN serie = 1 THEN Ring END) Serie1,
        SUM(CASE WHEN serie = 2 THEN Ring END) Serie2,
        SUM(CASE WHEN serie = 3 THEN Ring END) Serie3
    FROM Serien
    GROUP BY ScheibenID
), SerienTreffers AS (
    SELECT
        ScheibenID,
        SUM(Innenzehner) AS Innenzehner
    FROM Treffer
    GROUP BY ScheibenID
)
SELECT
    sb.SportpassID AS sport_pass_id,
    sb.Vorname AS first_name,
    sb.Nachname AS last_name,
    sb.Verein AS club,
    sb.VereinsID AS club_id,
    sb.Starterliste AS starter_list,
    sb.StarterlistenID AS starter_list_id,
    sb.StartNr AS start_number,
    sb.Standnr AS target_number,
    sb.Disziplin AS discipline,
    sb.Rangliste AS ranking,
    sr.Serie1 AS series1,
    sr.Serie2 AS series2,
    sr.Serie3 AS series3,
    st.Innenzehner AS inner_tens,
    sb.TotalRing AS total
FROM SerienRings sr
LEFT JOIN Scheiben sb
ON sr.ScheibenID = sb.ScheibenID
LEFT JOIN SerienTreffers st
ON st.ScheibenID = sb.ScheibenID
WHERE sb.Zeitstempel LIKE ?;