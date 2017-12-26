Heralding |travis badge| |version badge| |codacy badge|
=======================

.. |travis badge| image:: https://img.shields.io/travis/johnnykv/heralding/master.svg
   :target: https://travis-ci.org/johnnykv/heralding
.. |codacy badge| image:: https://api.codacy.com/project/badge/Grade/cd64aa20bce5474ba565fa3691710773 
   :target: https://www.codacy.com/app/johnnykv/heralding?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=johnnykv/heralding&amp;utm_campaign=Badge_Grade
.. |version badge| image:: https://img.shields.io/pypi/v/heralding.svg
   :target: https://pypi.python.org/pypi/Heralding/

About
-----

Sometimes you just want a simple honeypot that collects credentials, nothing more. Heralding is that honeypot!
Currently the following protocols are supported: ftp, telnet, ssh, http, https, pop3, pop3s, imap, imaps, smtp and postgresql.

**You need Python 3.5.0 or higher.**

Starting the honeypot
-----------------------

.. code-block:: shell
  $ sudo heralding
  2017-05-14 21:55:55,948 (root) Initializing Heralding version 0.2.0
  2017-05-14 21:55:55,968 (root) Using default config file: "/home/kajoj/heralding/bin/heralding/heralding.yml", if you want to customize values please copy this file to the current working directory
  2017-05-14 21:55:55,998 (heralding.reporting.file_logger) File logger started, using file: heralding_activity.log
  2017-05-14 21:55:55,999 (heralding.honeypot) Started Telnet capability listening on port 23
  2017-05-14 21:55:55,999 (heralding.honeypot) Started Http capability listening on port 80
  2017-05-14 21:55:55,999 (heralding.honeypot) Started Pop3 capability listening on port 110
  2017-05-14 21:55:56,000 (heralding.honeypot) Started https capability listening on port 443
  2017-05-14 21:55:56,000 (heralding.honeypot) Started Imap capability listening on port 143
  2017-05-14 21:55:56,000 (heralding.honeypot) Started ftp capability listening on port 21
  2017-05-14 21:55:56,000 (heralding.honeypot) Started Imaps capability listening on port 993
  2017-05-14 21:55:56,001 (heralding.honeypot) Started Pop3S capability listening on port 995
  2017-05-14 21:55:56,116 (heralding.honeypot) Started SSH capability listening on port 22
  2017-05-14 21:55:56,117 (heralding.honeypot) Started smtp capability listening on port 25
  2017-05-14 21:55:56,118 (root) Privileges dropped, running as nobody/nogroup.

Viewing the collected data
--------------------------

Heralding logs relevant data in two files, log_session.csv and log_auth.csv.

**log_session.csv**

This log file contains log entries for all connections to the honeypot. The data includes timestamp, duration, IP information and the number of authentication attempts. Be aware that the log entry for an specific session will appear in the log fil **after** the session has ended. 

   $ tail log_session.csv
   timestamp,duration,session_id,source_ip,source_port,destination_ip,destination_port,protocol,auth_attempts
   2017-12-26 20:38:19.683713,16,0841e3aa-241b-4da0-b85e-e5a5524cc836,127.0.0.1,53161,,23,telnet,3
   2017-12-26 22:17:33.140742,6,d20c30c1-6765-4ab5-9144-a8be02385018,127.0.0.1,55149,,21,ftp,1
   2017-12-26 22:17:48.088281,0,e0f50505-af93-4234-b82c-5477d8d88546,127.0.0.1,55151,,22,ssh,0
   2017-12-26 22:18:06.284689,0,6c7d653f-d02d-4717-9973-d9b2e4a41d24,127.0.0.1,55153,,22,ssh,0
   2017-12-26 22:18:13.043327,30,f3af2c8c-b63f-4873-ac7f-28c73b9e3e92,127.0.0.1,55155,,22,ssh,3

**log_auth.csv**

This log file contains information for all authentication attempts where it was possible to log a username and plaintext password. Log entries will appear in this file as soon as the password has been transmitted.

  $ tail log_auth.csv
  timestamp,auth_id,auth_type,session_id,source_ip,source_port,destination_port,protocol,username,password
  2016-03-12 20:35:02.258198,192.168.2.129,51551,23,telnet,bond,james
  2016-03-12 20:35:09.658593,192.168.2.129,51551,23,telnet,clark,P@SSw0rd123
  2016-03-18 19:31:38.064700,192.168.2.129,53416,22,ssh,NOP_Manden,M@MS3
  2016-03-18 19:31:38.521047,192.168.2.129,53416,22,ssh,guest,guest
  2016-03-18 19:31:39.376768,192.168.2.129,53416,22,ssh,HundeMad,katNIPkat
  2016-03-18 19:33:07.064504,192.168.2.129,53431,110,pop3,charles,N00P1SH
  2016-03-18 19:33:12.504483,192.168.2.129,53431,110,pop3,NektarManden,mANDENnEktar
  2016-03-18 19:33:24.952645,192.168.2.129,53433,21,ftp,Jamie,brainfreeze
  2016-03-18 19:33:47.008562,192.168.2.129,53436,21,ftp,NektarKongen,SuperS@cretP4ssw0rd1
  2016-03-18 19:36:56.077840,192.168.2.129,53445,21,ftp,Joooop,Pooop


Installing Heralding
---------------------

For step by step instructions on how to install and run heralding in a Python virtual environment using Ubuntu, see this `guide <https://github.com/johnnykv/heralding/blob/master/INSTALL.md>`_. Otherwise, the basic installation instructions are below.

To install the latest stable (well, semi-stable) version, use pip:

.. code-block:: shell

  pip install heralding

Make sure that requirements and pip is installed.
Simple way to do this on a Debian-based OS is:

.. code-block:: shell

  sudo apt-get install python-pip python-dev build-essential libssl-dev libffi-dev
  sudo pip install -r requirements.txt
  
And finally start the honeypot:
  
.. code-block:: shell

  mkdir tmp
  cd tmp
  sudo heralding
  
