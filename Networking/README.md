# The Networking group used the following software and performed the following procedures.

## Wireshark

[Wireshark](https://www.wireshark.org/) is a protocol analysis or packet sniffer software used for network troubleshooting, analysis and development of protocols or communication software and for education, possessing all the features of a standard protocol analyzer.
In particular, we used it to analyze the network traffic between the Echo Dot device and Amazon Alexa servers.
We analyzed the communication between source and destination by simply listening on the 2 IP addresses using this command within Wireshark:

```wireshark
**ip.src** <ip echo dot> **and ip.dst** <ip Server Amazon Alexa>
```

Two 5 minute recordings were made.
In the first we were simply listening without giving orders to Echo Dot, while in the second one we told Echo Dot to turn on the light 5 times.
At the end of the recordings, based on the acquired data, we could highlight the difference in bandwidth consumed and packets sent by Echo Dot to Amazon Alexa Servers. Obviously, we found higher bandwidth consumption and more packets during the second recording, i.e., the one with 5 voice inputs given.
To view the data of each recording inside Wireshark we used the *Conversations* menu found in the command bar:
> Statistics>Conversations

From this menu we extrapolated the data of the conversations to be exported to an Excel sheet.

## Microsoft Power BI Desktop
[Microsoft Power BI](https://powerbi.microsoft.com/) is a business analysis service produced by Microsoft. It provides interactive data visualizations and business intelligence features with a graphical interface to enable users to create reports and dashboards using spreadsheets or SQL database tables and other sources.

After creating the Excel sheet with the record data, we imported it inside Power BI Desktop to create the charts based on the data obtained.
The graphs can be viewed on the [Project Work website](https://pw2023.itsimola.it/) or directly downloaded from the project's GitHub page.
Regarding the use of Power BI Desktop and how to create graphs using spreadsheets I encourage the vison of this useful Youtube tutorial:

>[How to use Microsoft Power BI - Tutorial for Beginners](https://www.youtube.com/watch?v=TmhQCQr_DCA)

## <span>Draw.io</span>

[Draw.io](https://www.drawio.com/) is a software of graphical design and diagramming multiplatform.
Its interface can be used to create diagrams such as flowcharts, wireframes, UML diagrams, organizational charts and network diagrams.
We used the aforementioned software to create all the network infrastructure diagrams of the project.

## Let's Encrypt Certbot

We installed and used [Certbot](https://certbot.eff.org/) on the server where the [Project Work website](https://pw2023.itsimola.it/) is hosted to generate a "self signed" SSL certificate for the domain *pw2023.itsimola<nolink>.it* in order to have a secure connection using the **HTTPS** protocol.

First we connected in SSH (as user **root**) to the server using Putty following this procedure:

1. Download Putty here:[https://www.putty.org/](https://www.putty.org/) install, and start Putty.
2. Enter the IP address of the Alma Linux server in the "Host Name (or IP address)" field.
3. Select "SSH" as the "Connection type."
4. In the "Saved Sessions" section, give a name to the session you intend to save (e.g., "Alma Linux SSH").
5. Click on "Open" to start the SSH connection.
6. Enter your server login credentials (username and password).
7. If the connection is successfully established, you will see a terminal screen of the Alma Linux server through the Putty window. At this point, you are ready to interact with your Alma Linux server via terminal commands.

Once inside the server, we used the following commands to install Certbot:

1. Update the system using the command:

    ```bash
    sudo apt-get update
    ``

2. Enable the EPEL repository using the command:

    ```bash
    sudo apt install epel-release.
    ```

3. Install Certbot using the command:

    ```bash
    sudo apt-get install certbot python3-certbot-apache apache2
    ```

    Once the installation is complete, you can use Certbot to obtain and renew SSL certificates for your Alma Linux server. Be sure to properly configure Certbot for your specific use case by following the detailed instructions on the official [Certbot documentation](https://eff-certbot.readthedocs.io/en/stable/).

4. The following command is used to generate and install the certificate for your domain:

   ```bash
    sudo certbot --apache -d <example.com>
    ```

    In this case, replace *<example.<nolink>com>* with your domain.
    Follow the instructions to complete the certificate generation procedure.

5. The following command is used to renew the domain's SSL certificate (certificates generated with [Let's Encrypt](https://letsencrypt.org/) have a duration of 3 months, that's why it needs to be renewed periodically):

    ```bash
    sudo certbot renew
    ```

    After running the command perform the operations that will come up on screen.

6. The following command allows you to simulate the automatic renewal of the SSL certificate, without making any changes.

    ```bash
    sudo certbot renew --dry-run

## How to set up a cron job for automatic renewal of SSL certificate 

To set up a cron job on an Alma Linux server (or any Linux system) to automatically renew an SSL certificate generated with Certbot, you can follow these steps:

1. To set up the cron job, use this command to edit your crontab:

    ```bash
    sudo crontab -e
    ```

    This will open your crontab in a text editor.

2. Add a line like this to your crontab to run auto-renewal every day:

    ```bash
    0 0 * * * /usr/bin/certbot renew --quiet
    ```

    This line means that the renewal will run every day at 00:00. You can customize the time to your liking by following the syntax of the cron job.

3. In your editor, save the file and close it.

4. You can verify that your cron job has been added correctly by running:

    ```bash
    sudo crontab -l
    ```
Lorenzo Galvani - Princess Fernandez - Andrea Guidetti
