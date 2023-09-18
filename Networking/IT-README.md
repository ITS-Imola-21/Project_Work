# Il gruppo di Networking ha utilizzato i seguenti software ed eseguito le seguenti procedure

## <span>Draw.io</span>

[Draw.io](https://www.drawio.com/) è un software di disegno grafico gratuito multipiattaforma.
La sua interfaccia può essere utilizzata per creare diagrammi come diagrammi di flusso, wireframe, diagrammi UML, organigrammi e diagrammi di rete.
Per creare tutti i grafici della infrastruttura di rete del progetto abbiamo usato il suddetto software.
## Wireshark

[Wireshark](https://www.wireshark.org/) è un software per analisi di protocollo o packet sniffer (letteralmente annusa-pacchetti) utilizzato per la soluzione di problemi di rete, per l'analisi (troubleshooting) e lo sviluppo di protocolli o di software di comunicazione e per la didattica, possedendo tutte le caratteristiche di un analizzatore di protocollo standard.
In particolare lo abbiamo utilizzato per analizzare il traffico di rete tra il dispositivo Echo Dot ed i server di Amazon Alexa.
Abbiamo analizzato la comunicazione tra sorgente e destinazione  mettendoci semplicemente in ascolto su i 2 indirizzi IP utilizzando questo comando all’interno di Wireshark:

```wireshark
 **ip.src** <ip echo dot> **and ip.dst** <ip Server Amazon Alexa>
```

Sono state fatte due registrazioni della durata di 5 minuti.
Nella prima siamo stati semplicemente in ascolto senza impartire ordini ad Echo Dot, mentre invece nella seconda abbiamo detto 5 volte ad Echo Dot di accendere la luce.
Alla fine delle registrazioni, in base ai dati acquisiti, abbiamo potuto evidenziare la differenza di banda consumata e di pacchetti inviati da Echo Dot verso i Server di Amazon Alexa. Ovviamente abbiamo riscontrato un maggiore consumo di banda e un maggiore numero di pacchetti durante la seconda registrazione, ovvero quella con 5 input vocali impartiti.
Per visualizzare i dati di ogni registrazione dentro Wireshark abbiamo utilizzato il menù *Conversations* presente nella barra dei comandi:
> Statistics>Conversations

Da questo menù abbiamo estrapolato i dati delle conversazioni per essere per poi riportati su un foglio Excel.

## Microsoft Power BI Desktop
[Microsoft Power BI](https://powerbi.microsoft.com/) è un servizio d'analisi aziendale prodotto da Microsoft. Fornisce visualizzazioni di dati interattive e funzionalità di business intelligence con un'interfaccia grafica, per consentire agli utenti di creare report e dashboard utilizzando fogli elettronici o tabelle database SQL ed altre fonti.

Dopo aver creato il foglio Excel con i dati delle registrazioni abbiamo importato quest'ultimo dentro Power BI Desktop per creare i grafici in base ai dati ottenuti.
I grafici sono visualizzabili sul [sito web del Project Work](https://pw2023.itsimola.it/) oppure direttamente scaricabili dalla pagina GitHub del progetto.
Per quanto concerne l'utilizzo di Power BI Desktop e su come creare grafici utilizzando fogli elettronici invito la visone di questo utile tutorial su Youtube:

>[How to use Microsoft Power BI - Tutorial for Beginners](https://www.youtube.com/watch?v=TmhQCQr_DCA)



## Let's Encrypt Certbot

Abbiamo installato ed utilizzato [Certbot](https://certbot.eff.org/) sul server dove è ospitato il [sito web del Project Work](https://pw2023.itsimola.it/) per generare un certificato SSL "self signed" per il dominio *pw2023.itsimola<nolink>.it* in modo da avere una connessione sicura mediante il protocollo **HTTPS**.

Per prima cosa ci siamo connessi in SSH (come utente **root**) al server utilizzando Putty seguendo questa procedura:

1. Scarica Putty qui: [https://www.putty.org/](https://www.putty.org/), installa ed avvia Putty.
2. Inserisci l'indirizzo IP del server Alma Linux nel campo "Host Name (or IP address)".
3. Seleziona "SSH" come "Connection type".
4. Nella sezione "Saved Sessions", assegna un nome alla sessione che intendi salvare (ad esempio "Alma Linux SSH").
5. Clicca su "Open" per avviare la connessione SSH.
6. Inserisci le credenziali di accesso al server (nome utente e password).
7. Se la connessione viene stabilita correttamente, vedrai una schermata del terminale del server Alma Linux attraverso la finestra di Putty. A questo punto, sei pronto per interagire con il tuo server Alma Linux tramite comandi da terminale.

Una volta dentro al server, per installare Certbot, abbiamo utilizzato i seguenti comandi:

1. Aggiorna il sistema utilizzando il comando:

    ```bash
    sudo apt-get update
    ```

2. Abilita il repository EPEL utilizzando il comando:

    ```bash
    sudo apt install epel-release.
    ```

3. Installa Certbot utilizzando il comando:

    ```bash
    sudo apt-get install certbot python3-certbot-apache apache2
    ```

    Una volta completata l'installazione, puoi utilizzare Certbot per ottenere e rinnovare i certificati SSL per il tuo server Alma Linux. Assicurati di configurare correttamente Certbot per il tuo specifico caso d'uso, seguendo le istruzioni dettagliate sulla [documentazione ufficiale di Certbot](https://eff-certbot.readthedocs.io/en/stable/).

4. Il seguente comando serve per generare ed installare il certificato per il tuo dominio:

    ```bash
    sudo certbot --apache -d <example.com>
    ```

    In questo caso, sostituire *<example.<nolink>com>* con il proprio dominio.
    Seguire le istruzioni per completare la procedura di generazione del certificato.

5. Il seguente comando serve per rinnovare il certificato SSL del dominio (un certificato generato con [Let's Encrypt](https://letsencrypt.org/) ha una durata di 3 mesi, ecco perchè necessita di essere rinnovato periodicamente):

    ```bash
    sudo certbot renew
    ```

    Dopo aver eseguito il comando eseguire le operazioni che verrano elencate a schermo.

6. Il seguente comando permette di simulare il rinnovo automatico del certificato SSL, senza effettuare alcuna modifica.

    ```bash
    sudo certbot renew --dry-run
    ```

## Come impostare un cron job per il rinnovo automatico del certificato SSL

Per impostare un cron job su un server Alma Linux (o su qualsiasi sistema Linux) per il rinnovo automatico di un certificato SSL generato con Certbot, puoi seguire questi passaggi:

1. Per impostare il cron job, usa questo comando per modificare il tuo crontab:

    ```bash
    sudo crontab -e
    ```

    Questo aprirà il tuo crontab in un editor di testo.

2. Aggiungi una riga come questa al tuo crontab per eseguire il rinnovo automatico ogni giorno:

    ```bash
    0 0 * * * /usr/bin/certbot renew --quiet
    ```

    Cosi facendo il rinnovo verrà eseguito ogni giorno alle 00:00. Puoi personalizzare l'orario a tuo piacimento seguendo la sintassi del cron job.

3. Nel tuo editor, salva il file e chiudilo

4. Puoi verificare che il tuo cron job sia stato aggiunto correttamente eseguendo:

    ```bash
    sudo crontab -l
    ```

Redatto da:
Lorenzo Galvani - Princess Fernandez - Andrea Guidetti
