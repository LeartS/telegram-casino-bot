antiscam_text = """
Ho un sistema antitruffa incorporato; esso garantisce che le
estrazioni sono casuali e determinate prima di qualsiasi puntata, rendendo così
impossibile per me "barare" e creare estrazioni in base alle puntate.


COME FUNZIONA:

Per generare numeri casuali, uso un PRNG (Pseudo Random Number Generator),
un algoritmo che dato un <i>seed</i> iniziale genera una sequenza
deterministica di numeri che possono essere considerati statisticamente
casuali.
Ciò che significa che con lo stesso seed verrà generata sempre la stessa
sequenza, da qualsiasi programma che utilizzi lo stesso algoritmo con gli
stessi parametri! Potete pure provare a copiare il seed
e usarlo per Python `random.seed()` sul vostro computer e otterrete anche lì
la stessa sequenza!

Per ogni giro genero un seed diverso e all'inizio di ogni giro,
<b>prima di qualsiasi puntata</b>, mostro i primi 8 caratteri dell'hash MD5
del seed che verrà utilizzato per le estrazioni.


PERCHÈ MD5

Se mostrassi direttamente il seed, come detto, potreste barare voi usandolo
sul vostro computer per sapere in anticipo quali numeri verranno generati.
Con MD5 invece non potete risalire al seed originale (per cui non potete
barare) ma quando vi do il seed originale (alla fine dell'estrazione) potete
facilmente verificare, anche usando generatori MD5 online
come http://www.md5.cz/, che combaciano e che quindi ho effettivamente
utilizzato quel seed (stabilito prima di qualsiasi puntata) per generare i
numeri casuali.
""".replace('\n', ' ').replace('   ', '\n\n').replace('  ', '\n')


news = """
<b>2016-04-07:</b>

- Fix di /spiega GUESS e alcuni piccoli cambiamenti/fix a vari messaggi


<b>2016-04-06:</b>

- Tre nuovi giochi: FIRST, MIDDLE e LAST. Rispettivamente vinci se escono i
primi due numeri (1 o 2), i due in mezzo (3 o 4) o gli ultimi due (5 o 6).
Payout 2.8 volte quello puntato!

- Sistemato /trasferisci che non funzionava più!

- Introdotto il comando /news che mostra gli ultimi aggiornamenti del bot

- Cambiato il payout di DEVIL da 100 a 130 per essere paragonabile (poco più)
a quello della puntata equivalente GUESS 666

- Un po' di colore con emoticons nei messaggi

- Sistemato /spiega non funzionante per alcuni giochi


<b>Ancora prima:</b>

- I giochi non sono più case sensitive e i nomi dei giochi si possono
scrivere in maiuscolo, minuscolo, mixed..

- I messaggi di conferma puntata ora arrivano con qualche secondi di ritardo
e confermano tutte le puntate fatte nel frattempo. Così manda meno messaggi
e dovrebbe bloccarsi meno.

- Nuovo gioco: GUESS. Indovina i lanci esatti e vinci 5^n_lanci quello
puntato! es: /punta 20 G 324

- Modifica giochi: rinominato SUICIDE in BULLDOZER, inoltre ora INSURANCE e
BULLDOZER sono con numero a scelta anzichè numero fisso!
""".replace('\n', ' ').replace('   ', '\n\n').replace('  ', '\n')
