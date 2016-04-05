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
Con MD5 invece non potete risalire al seed originale (per cui non potete barare)
ma quando vi do il seed originale (alla fine dell'estrazione) potete facilmente
verificare, anche usando generatori MD5 online come http://www.md5.cz/,
che combaciano e che quindi ho effettivamente utilizzato quel seed (stabilito
prima di qualsiasi puntata) per generare i numeri casuali.
""".replace('\n', ' ').replace('   ', '\n\n').replace('  ', '\n')
