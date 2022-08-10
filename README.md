# giorgiopoibot

È un semplicissimo bot telegram che restituisce in modo pseudorandomico canzoni del cantante indie [Giorgio Poi](https://it.wikipedia.org/wiki/Giorgio_Poi). Nasce come parte di un regalo di Natale e, per i vincoli imposti da questa <del>imminente</del> deadline, mantiene una struttura elementare.
## Giorgiopoibot: diagramma di sequenza
```mermaid
sequenceDiagram
    participant telegram
    participant giorgiopoibot
    telegram->>giorgiopoibot: /giorgiopls
    giorgiopoibot->>database: SELECT * from Songs
    giorgiopoibot->>giorgiopoibot: generate random_id
    giorgiopoibot->>database: SELECT * from Songs where Id = random_id
    database->>giorgiopoibot: get record
    giorgiopoibot->>telegram: send song url
```


## to-do:
* ~~Renderlo scalabile (appoggiarsi alle API di youtube?)~~: fatto
