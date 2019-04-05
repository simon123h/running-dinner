# Algorithmus 1: Im Graph sortieren


teams = [...]


für jede mahlzeit in range(nspeisen):
    sortiere teams nach position oder randomisiere
    für jedes team in teams:
        wenn route[mahlzeit] noch ungeklärt:
            erstelle dictionary mit abstand zu anderen teams
            sortiere dictionary: kleinster abstand zuerst
            versuche gast bei team mit kleinstem abstand zu sein:
                es sei denn, (team B war vorher schon mal host eines vollen treffens || ein anderes team würde dann zum 2. mal getroffen || anzahl an hosts für diese mahlzeit überschritten):
                    dann nächsthöherer abstand etc.
                lege fest, dass team B bei route[mahlzeit] host ist
                lege meeting bei team B als route[mahlzeit] von team A fest
                wenn meeting voll:
                    setze boolean team B nimmt keine mehr an

    