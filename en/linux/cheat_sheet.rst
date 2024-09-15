.. _linux_cheat_sheet:

.. include:: ../_include/head.rst

===================
Command Cheat Sheet
===================


General Shell Usage
###################

Refer to last word of the last command: :code:`!$`

Refer to exit-code of last command: :code:`$?`

Get Path to executable: :code:`which EXE`

Find string in files recursively: :code:`grep -r 'SearchString'`

Run command as other user: :code:`su --shell /bin/bash -c '$COMMAND' $USER`

Start interactive shell in context of other user: :code:`su --login --shell /bin/bash $USER`

Show Difference of directory contents: :code:`diff --recursive --unified=3 --color before/vars/ vars/`

Log Difference with colors: :code:`unbuffer diff --recursive --unified=3 --color before/vars/ vars/ | tee log.txt`

Convert Datetime string to timestamp: :code:`date -d "$(get datetime string here)" +"%s"`

Search and replace strings in files: :code:`sed -i 's|FIND_REGEX|REPLACE|g' FILE`

Search and replace strings in files with usage of variables:

.. code-block::

    FIND_REGEX='my regex'
    REPLACE='replace'

    sed -i "s|$FIND_REGEX|$REPLACE|g" FILE

APT Upgrade single package: :code:`sudo apt-get --only-upgrade install PKG`

Create ssh keys: :code:`ssh-keygen -t ed25519 -C 'comment'`

Get last 100 lines of a systemd-service: :code:`journalctl -u SERVICE.service --no-pager -n 100`

Get nice postfix log overview: :code:`pflogsumm -u 50 -h 50 -i --verbose-msg-detail mail.log mail.log.? > mail_report.log`

Get last logins: :code:`last`, :code:`lastlog`

Get current open user sessions: :code:`w`

----

Resource Management
###################

Get size of directory: :code:`du -sh DIR`

Get size of sub-dirs of directory: :code:`du -h --max-depth=1 DIR | sort -hr`

Get actual amount of data of directory: :code:`du -sh --apparent-size DIR`

Get free RAM in MB and refresh every 5s: :code:`free -m -s 5`

List open files: :code:`lsof`

Search for open file of a specific service: :code:`lsof -i -P | grep SERVICE`

Get open files at path: :code:`lsof /var/data`

Get cpu usage of specific processes: :code:`ps -eo size,pcpu,pid,user,command --sort -pcpu | grep fpm`

Get ram usage of specific processes in B: :code:`ps -eo rss,pid,user,command --sort -rss | grep php-fpm`

Get ram usage of specific process(es) in MB: :code:`ps -eo rss,pid,user,command --sort -rss | awk '{ hr=$1/1024 ; printf("%13.2f Mb ",hr) } { for ( x=4 ; x<=NF ; x++ ) { printf("%s ",$x) } print "" }' | grep php-fpm`

Log Disk I/O via iotop (process-level): :code:`iotop -P -o -t -a -d 10 -n 10 -b > iotop_output.txt `

Log Disk I/O: :code:`iostat -d -k -t -N -x 10 10 > iostat_output.txt`

----

Networking
##########

Network statistics: :code:`netstat -s`

Show all existing routes: :code:`ip route show table all`

Show IP neighbors: :code:`ip neighbor`

Show local listenports: :code:`netstat -tulpn`

Check if port is open: :code:`nc -z -v -w5 $IP $PORT -s $SRC_IP`

DNS Lookup: :code:`host DNS`, :code:`nslookup DNS`, :code:`dig DNS`

Get all values of a DNS record type: :code:`dig +noall +answer +multiline _dmarc.oxl.at TXT`

Try to get all subdomains: :code:`dig @NAMESERVER DOMAIN.TLD AXFR`

----

Certificates
************

Check server certificate via OpenSSL: :code:`openssl s_client -showcerts -servername FQDN -connect IP/DNS:443 </dev/null`

Check if OCSP is still valid (status-age = min runtime in seconds): :code:`openssl ocsp -no_nonce -issuer chain.pem -verify_other chain.pem -cert cert.pem -respin ocsp.der -status_age 432000`

Get timestamp of OCSP update time: :code:`date -d "$(openssl ocsp -respin "${tfile}.ocsp" -text -noverify | grep "This Update" | cut -d ':' -f2-)" +"%s"`

Get server certificate (pem file content) from service via OpenSSL: :code:`openssl s_client -connect IP/DNS:443 </dev/null 2>/dev/null | openssl x509`

----

VPN & Tunnels
*************

Libreswan IPSec
===============

Add ipsec-tunnel for manual startup: :code:`ipsec auto --add TUNNEL`

Set ipsec-tunnel up manually: :code:`ipsec auto --up TUNNEL`

Show ipsec tunnel stati: :code:`ipsec trafficstatus`

Check basic ipsec config/functionality: :code:`ipsec verify`

SSH
===

SSH Tunnel (remote resource on local port): :code:`ssh -L localPort:targetIP:targetPort USER@HOST`

WireGuard
=========

Start WireGuard VPN: :code:`sudo wg-quick up CONFIG`

Stop WireGuard VPN: :code:`sudo wg-quick down CONFIG`

----

Pentesting
**********

Scan all TCP ports using syn-option: :code:`sudo nmap -vv -sS -p1-65535 -T5 --max-retries=1 -Pn <target>`

Scan all TCP ports: :code:`sudo nmap -vv -p1-65535 -T5 --max-retries=1 -Pn <target>`

Scan all TCP & UDP ports: :code:`sudo nmap -vv -p1-65535 -T5 --max-retries=1 -Pn -sU -sT <target>`

----

Files
#####

Find Files
**********

Search for file by name: :code:`find -type f -name NAME*`

Search for directory by name: :code:`find -type d -name NAME`

----

Tar Archives
************

Create: :code:`tar -czvf ARCHIVE DIR`

Extract: :code:`tar -xzvf ARCHIVE -C DIR`

----

File Encryption
***************

Age
===

Download: `FiloSottile/age <https://github.com/FiloSottile/age/releases>`_

Encrypt file: :code:`age -R $AGE_PUB_KEY -o $OUTPUT`

Decrypt file: :code:`age -d -i $AGE_PRIV_KEY $INPUT`

----

Ansible
#######

Ansible-Vault encrypt string: :code:` ansible-vault encrypt_string 'VAR_VALUE'`

Ansible-Vault encrypt file: :code:`ansible-vault encrypt path/to/file.yml`

----

Image Manipulation
##################

JPEG Compress Images
********************

Install: :code:`apt-get install imagemagick`

Single
======

.. code-block::

    convert IMG.png -quality 70 IMG.jpg

Multiple
========

.. code-block::

    for img in IMG_*.jpg; do convert "$img" -quality 70 "$img"; done

----

Webp Compress Images
********************

Install: :code:`apt-get install webp`

Alternative Download: :code:`wget -c https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-0.6.1-linux-x86-32.tar.gz`

Single
======

.. code-block::

    cwebp -q 70 IMG.png -o IMG.webp

----

Databases
#########

MySQL/MariaDB
*************

Change database: :code:`use DATABASE;`

List tables: :code:`show TABLES;`

Show table schema: :code:`desc TABLE;`

Show all current processes: :code:`SHOW FULL PROCESSLIST;`

Show all users of mysql instance: :code:`select host, user from mysql.user;`

Binlog/Query analysis: :code:`mysqlbinlog /var/lib/mysql/mysql-bin.NNNNN -v`

Get replication status: :code:`SHOW SLAVE STATUS\G`

----

PostgreSQL
**********

Enter: :code:`sudo -u postgres psql`

Change database: :code:`\c DATABASE;`

List tables: :code:`\dt`

----

CockroachDB
***********

See: `CockroachDB Releases <https://www.cockroachlabs.com/docs/releases/>`_

Download client: :code:`curl -s -L https://binaries.cockroachdb.com/cockroach-sql-v24.1.4.linux-amd64.tgz | tar -xz --strip-components=1 -C /tmp/ && sudo mv /tmp/cockroach /usr/local/bin/cockroach`

Connect: :code:`cockroach-sql --url "postgres://root@servername:26257/mydb?sslmode=disable"`

.. include:: ../_include/user_rath.rst
