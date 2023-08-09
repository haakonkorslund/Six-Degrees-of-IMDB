# Six-Degrees-of-IMDB
Gitt to skuespillere finner en korteste sti som forbinder dem via felles filmer.

Filen findPath.py leser inn movies.tsv og actors.tsv og skriver ut svaret på de forkjellige skuespillere.

Leser først inn filmene også skuespillerene. Om en skuespiller er i en film legger den til alle andre skuespillere
som osgå har hatt filmen, og oppdaterer den forrige skuespilleren sine naboer med seg selv inkludert.

makeFilmList
Har O(n) kjøretid ettersom den bare legger inn filmene i en liste i 1 for-loop.

makeActorList
Har først en for og en while som går for antall filmer skuespilleren skal legget til.
Dette gir oss O(|E|· log(n))

Videre har den 3 for-løkker nøstet i hverander som gir den
O(n^3)

Totalt : n +|E|log(n) + n^30


findPath(start, target):
BDF søk

starter med å sette parent for alle naboer av start:
O(n)
Bruker så BDF søk 
O(|V| +|E|)
Skriver så ut pathen med en lenket liste
O(n)

Totalt: O(2n+|V| +|E|)


findChillPath(start, target):
DIJKSTRA

Bruker Dijkstra algoritmen
O(|E| · log(|V|))

Bruker så en lenket liste
O(n)

Totalt: O(n+ (|E| · log(|V|)))

allComponents():
BDF
Går gjennom alle noder, men om en node har vært besøkt blir den ikke gått gjennom.
O(log(n))

Går gjennom naboene til alle noder som ikke har blitt gått gjennom ennå ved et BDF søk
O(|V| +|E|)

toatlt: O(log(n)+(|V| +|E|))
