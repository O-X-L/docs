.. _linux_cheat_sheet:

.. include:: ../_include/head.rst

===================
Command Cheat Sheet
===================

General Shell Usage
###################

Refer to last word of the last command:

.. code-block:: bash

    !$

Refer to exit-code of last command:

.. code-block:: bash

    $?

Get Path to executable:

.. code-block:: bash

    which EXE

Find string in files recursively:

.. code-block:: bash

    grep -r 'SearchString'

Run command as other user:

.. code-block:: bash

    su --shell /bin/bash -c '$COMMAND' $USER

Start interactive shell in context of other user:

.. code-block:: bash

    su --login --shell /bin/bash $USER

Show Difference of directory contents:

.. code-block:: bash

    diff --recursive --unified=3 --color before/vars/ vars/

Log Difference with colors:

.. code-block:: bash

    unbuffer diff --recursive --unified=3 --color before/vars/ vars/ | tee log.txt

Show colored difference between two files:

.. code-block:: bash

    # sudo apt install git
    git diff --word-diff=color <file1> <file2>

Convert Datetime string to timestamp:

.. code-block:: bash

    date -d "$(get datetime string here)" +"%s"

Search and replace strings in files:

.. code-block:: bash

    sed -i 's|FIND_REGEX|REPLACE|g' FILE

Search and replace strings in files with usage of variables:

.. code-block::

    FIND_REGEX='my regex'
    REPLACE='replace'

    sed -i "s|$FIND_REGEX|$REPLACE|g" FILE

Remove all empty lines from a file:

.. code-block::

    sed -i '/^$/d' FILE

APT Upgrade single package:

.. code-block:: bash

    sudo apt-get --only-upgrade install PKG

Create ssh keys:

.. code-block:: bash

    ssh-keygen -t ed25519 -C 'comment'

Get last 100 lines of a systemd-service:

.. code-block:: bash

    journalctl -u SERVICE.service --no-pager -n 100

Get nice postfix log overview:

.. code-block:: bash

    pflogsumm -u 50 -h 50 -i --verbose-msg-detail mail.log mail.log.? > mail_report.log

Get last logins:

.. code-block:: bash

    last

    lastlog

Get current open user sessions:

.. code-block:: bash

    w

Quick source-code overview:

.. code-block:: bash

    # sudo apt install cloc
    cd <REPO_BASE> && cloc

Create QR-Code:

.. code-block:: bash

    # sudo apt install qrencode
    qrencode https://www.oxl.at -o qr.png

Create QR business-card (`RFC6350 <https://datatracker.ietf.org/doc/html/rfc6350>`_):

.. code-block:: bash

    # add a file with this content:
    BEGIN:VCARD
    VERSION:3.0
    N:Rath;Pascal
    FN:Pascal Rath
    ORG:OXL IT Services
    Tel;WORK;VOICE:+433115409000
    EMAIL;TYPE=work:rath@oxl.at
    URL:https://www.oxl.at
    END:VCARD

    # create qr
    qrencode < vcard.txt -q vcard.png

Loop in Bash-Script:

.. code-block:: bash

    APPS=('main' 'test')
    for app in "${APPS[@]}"
    do
      cp "./${app}"-*css "/var/random/app/${app}.css"
    done

Activate bash-history to handle multiple simultaneous terminal-sessions:

.. code-block:: bash

    echo "export PROMPT_COMMAND='history -a'" >> ~/.bashrc

Get a history of the systems active and offline times:

.. code-block:: bash

    last -x shutdown reboot

----

JSON Query
**********

Install:

.. code-block:: bash

    sudo apt install jq

Example JSON:

.. code-block:: bash

    {
        "test1": {
            "ip": {
                "ip4": [
                    "192.168.1.2"
                ],
                "ip6": []
            }
        },
        "test2": {
            "ip": {
                "ip4": [
                    "192.168.5.4"
                ],
                "ip6": []
            }
        }
    }

Get keys as flat list:

.. code-block:: bash

    cat test.json | jq 'keys | .[]'
    > "test1"
    > "test2"

Flatten data by one layer:

.. code-block:: bash

    cat test.json | jq '.[]'
    > {
    >   "ip": {
    >     "ip4": [
    >       "192.168.1.2"
    >     ],
    >     "ip6": []
    >   }
    > }
    > {
    >   "ip": {
    >     "ip4": [
    >       "192.168.5.4"
    >     ],
    >     "ip6": []
    >   }
    > }

Get all values nested inside sub-keys:

.. code-block:: bash

    cat test.json | jq '.[] | .ip | .ip4 | .[]'
    > 192.168.1.2
    > 192.168.5.4

Handle missing keys:

.. code-block:: bash

    # if '.ip' is missing for one+ entry
    cat test.json | jq '.[] | .ip | .ip4 | .[]'
    > Cannot iterate over null (null)

    cat test.json | jq '.[] | try .ip | .ip4 | .[]'

Filter by nested value:

.. code-block:: bash

    cat test.json | jq '.[] | select(.ip.ip4[] == "192.168.5.4")'

    > {
    >   "ip": {
    >     "ip4": [
    >       "192.168.5.4"
    >     ],
    >     "ip6": []
    >   }
    > }

Filter by nested value and handle non-existing entries:

.. code-block:: bash

    # get list of interfaces that have at least one inactive IP

    > {
    >   "rows": [
    >     {
    >       "description": "LAN",
    >       "carp": [
    >         {"status": "ACTIVE", "ipaddr": "192.168.0.1"}
    >       ]
    >     },
    >     {
    >       "description": "WAN",
    >       "carp": [
    >         {"status": "ACTIVE", "ipaddr": "10.10.5.1"}
    >       ]
    >     },
    >     {
    >       "description": "TEST"
    >     },
    >     {
    >       "description": "DMZ",
    >       "carp": [
    >         {"status": "ACTIVE", "ipaddr": "192.168.100.1"},
    >         {"status": "BACKUP", "ipaddr": "192.168.100.10"}
    >       ]
    >     }
    >   ]
    > }

    cat /tmp/test.json | jq '.rows[] | try select(.carp[].status == "BACKUP") | .description'

    > "DMZ"

----

Resource Management
###################

Get size of directory:

.. code-block:: bash

    du -sh DIR

Get size of sub-dirs of directory:

.. code-block:: bash

    du -h --max-depth=1 DIR | sort -hr

Get actual amount of data of directory:

.. code-block:: bash

    du -sh --apparent-size DIR

Get free RAM in MB and refresh every 5s:

.. code-block:: bash

    free -m -s 5

List open files:

.. code-block:: bash

    lsof

Search for open file of a specific service:

.. code-block:: bash

    lsof -i -P | grep SERVICE

Get open files at path:

.. code-block:: bash

    lsof /var/data

Get cpu usage of specific processes:

.. code-block:: bash

    ps -eo size,pcpu,pid,user,command --sort -pcpu | grep fpm

Get ram usage of specific processes in B:

.. code-block:: bash

    ps -eo rss,pid,user,command --sort -rss | grep php-fpm

Get ram usage of specific process(es) in MB:

.. code-block:: bash

    ps -eo rss,pid,user,command --sort -rss | awk '{ hr=$1/1024 ; printf("%13.2f Mb ",hr) } { for ( x=4 ; x<=NF ; x++ ) { printf("%s ",$x) } print "" }' | grep php-fpm

Log Disk I/O via iotop (process-level):

.. code-block:: bash

    iotop -P -o -t -a -d 10 -n 10 -b > iotop_output.txt

Log Disk I/O:

.. code-block:: bash

    iostat -d -k -t -N -x 10 10 > iostat_output.txt

Lower swap usage:

.. code-block::

    sysctl vm.swappiness=1
    # add 'vm.swappiness=1' to /etc/sysctl.conf
    swapoff -a
    swapon

Interact with disk partitions:

.. code-block::

    fdisk /dev/sdX

Disk-usage analysis:

.. code-block::

    # sudo apt install ncdu

    # open interactive disk-usage browser
    ncdu /var

    # with excludes to save on time
    ncdu / --exclude /var/

----

Disks
#####

Logical Volume Manager (LVM)
****************************

Show volume groups:

.. code-block::

    vgs

    vgdisplay

Show volumes:

.. code-block::

    lvs

    lvdisplay

Scan for physical disks available to LVM:

.. code-block::

    pvs

    pvscan

Add physical disk to be available to LVM:

.. code-block::

    pvcreate /dev/sdX

Create volume:

.. code-block::

    lvcreate -n <lv-name> -L 50G <vg-name>

Create partition on volume:

.. code-block::

    # check
    ls -l /dev/mapper/

    mkfs.xfs /dev/mapper/<vg-name>-<lv-name>

Extend physical disk and volume group:

.. code-block::

    pvresize /dev/sdX
    vgextend <vg-name> /dev/sdX

Extend volume and partition:

.. code-block::

    lvextend /dev/<vg-name>/<lv-name> -L +20GB
    # or in %
    lvextend /dev/<vg-name>/<lv-name> -l +100%FREE

    resize2fs /dev/mapper/<vg-name>-<lv-name>

Remove:

.. code-block::

    umount <mountpoint>

    lvremove <lv-name>

    vgremove <vg-name>

----

Software RAID (MD)
******************

Create RAID1:

.. code-block::

    mdadm --create /dev/md1 --level=1 --raid-devices=2 /dev/nvme0n1 /dev/nvme1n1

Status:

.. code-block::

    mdadm --detail /dev/md1

Remove:

.. code-block::

    mdadm --stop /dev/md1
    mdadm --fail /dev/md1 --remove /dev/md1

    # clean disk superblock
    dd if=/dev/zero of=/dev/nvme0n1 bs=1M count=10

System Disk RAID1: (see `Hetzner installimage scripts <https://github.com/hetzneronline/installimage>`_)

.. code-block::

    lsblk
    > nvme0n1        259:1    0 953.9G  0 disk
    > ├─nvme0n1p1    259:5    0     1G  0 part
    > │ └─md0          9:0    0  1022M  0 raid1 /boot
    > └─nvme0n1p2    259:6    0    30G  0 part
    >   └─md1          9:1    0    30G  0 raid1
    >     ├─vg0-root 252:0    0    10G  0 lvm   /
    >     ├─vg0-swap 252:1    0     4G  0 lvm
    >     └─vg0-var  252:2    0    10G  0 lvm   /var
    >
    > nvme1n1        259:0    0 953.9G  0 disk
    > ├─nvme1n1p1    259:2    0     1G  0 part
    > │ └─md0          9:0    0  1022M  0 raid1 /boot
    > └─nvme1n1p2    259:3    0    30G  0 part
    >   └─md1          9:1    0    30G  0 raid1
    >     ├─vg0-root 252:0    0    10G  0 lvm   /
    >     ├─vg0-swap 252:1    0     4G  0 lvm
    >     └─vg0-var  252:2    0    10G  0 lvm   /var

    # hetzner install-image config:
    #   SWRAID 1
    #   SWRAIDLEVEL 1
    #   PART /boot ext3 1024M
    #   PART lvm vg0 30G
    #   LV vg0 root /     ext4 10G
    #   LV vg0 swap swap  swap  4G
    #   LV vg0  var /var  ext4 10G

----

ZFS
***

Create pool:

.. code-block::

    # RAID1-like
    zpool create -f -o ashift=12 <pool-name> mirror /dev/nvme0n1 /dev/nvme1n1

    # RAID10-like
    zpool create -f -o ashift=12 <pool-name> mirror /dev/nvme0n1 /dev/nvme1n1 mirror /dev/nvme2n1 /dev/nvme3n1

Status:

.. code-block::

    zpool list
    zpool status
    zfs list

Remove pool:

.. code-block::

    zpool destroy <pool-name>

ZFS on system disks: (*Proxmox VE usage*)

.. code-block::

    lsblk
    > nvme0n1        259:1    0 953.9G  0 disk
    > ├─nvme0n1p1    259:5    0     1G  0 part
    > │ └─md0          9:0    0  1022M  0 raid1 /boot
    > ├─nvme0n1p2    259:6    0    30G  0 part
    > │ └─md1          9:1    0    30G  0 raid1
    > │   ├─vg0-root 252:0    0    10G  0 lvm   /
    > │   ├─vg0-swap 252:1    0     4G  0 lvm
    > │   └─vg0-var  252:2    0    10G  0 lvm   /var
    > └─nvme0n1p3    259:7    0 922.9G  0 part  # ==> ZFS
    >
    > nvme1n1        259:1    0 953.9G  0 disk
    > ├─nvme1n1p1    259:5    0     1G  0 part
    > │ └─md0          9:0    0  1022M  0 raid1 /boot
    > ├─nvme1n1p2    259:6    0    30G  0 part
    > │ └─md1          9:1    0    30G  0 raid1
    > │   ├─vg0-root 252:0    0    10G  0 lvm   /
    > │   ├─vg0-swap 252:1    0     4G  0 lvm
    > │   └─vg0-var  252:2    0    10G  0 lvm   /var
    > └─nvme1n1p3    259:7    0 922.9G  0 part  # ==> ZFS

    zpool create -f -o ashift=12 <pool-name> mirror /dev/nvme0n1p3 /dev/nvme1n1p3

    zpool status
    > NAME                  STATE     READ WRITE CKSUM
    > pve                   ONLINE       0     0     0
    >   mirror-0            ONLINE       0     0     0
    >     nvme-eui.1-part3  ONLINE       0     0     0
    >     nvme-eui.2-part3  ONLINE       0     0     0

----

Networking
##########

Network statistics:

.. code-block:: bash

    netstat -s

Show all existing routes:

.. code-block:: bash

    ip route show table all

Show IP neighbors:

.. code-block:: bash

    ip neighbor

Show local listenports:

.. code-block:: bash

    netstat -tulpn

Check if port is open:

.. code-block:: bash

    nc -z -v -w5 $IP $PORT -s $SRC_IP

DNS Lookup:

.. code-block:: bash

    host DNS

    nslookup DNS

    dig DNS

Get all values of a DNS record type:

.. code-block:: bash

    dig +noall +answer +multiline _dmarc.oxl.at TXT

Try to get all subdomains: (*is blocked in most cases*)

.. code-block:: bash

    dig @NAMESERVER DOMAIN.TLD AXFR

Watch live-traffic:

.. code-block:: bash

    # sudo apt install tcpdump
    tcpdump -i <INTERFACE> host <IP> port <PORT>

    # record to file (for wireshark)
    tcpdump -i <INTERFACE> host <IP> port <PORT> -w <FILE>.pcap

Inform the whole Layer2-network that an IP-address is now on this system: (GARP/unsolicited ARP broadcast)

.. code-block:: bash

    # sudo apt install iputils-arping
    arping -U -I <INTERFACE> <IP>

----

Certificates
************

Check server certificate via OpenSSL:

.. code-block:: bash

    openssl s_client -showcerts -servername FQDN -connect IP/DNS:443 </dev/null

    # show status
    openssl s_client -connect IP/DNS:443 -status </dev/null 2>/dev/nu

Check if OCSP is still valid (status-age = min runtime in seconds):

.. code-block:: bash

    openssl ocsp -no_nonce -issuer chain.pem -verify_other chain.pem -cert cert.pem -respin ocsp.der -status_age 432000

Get timestamp of OCSP update time:

.. code-block:: bash

    date -d "$(openssl ocsp -respin "${tfile}.ocsp" -text -noverify | grep "This Update" | cut -d ':' -f2-)" +"%s"

Get server certificate (pem file content) from service via OpenSSL:

.. code-block:: bash

    openssl s_client -connect IP/DNS:443 </dev/null 2>/dev/null | openssl x509

Get information from PEM certificate:

.. code-block:: bash

    openssl x509 -in <PEM_FILE> -text

Script to validate active certificates: `ssl-validate.sh <https://gist.github.com/superstes/8e369be2c86bbbcbd1e64c57d34905f1>`_

Script to validate OCSP: `ssl-ocsp-check.sh <https://gist.github.com/superstes/5ca4f4c346ea18703f716307a05d286b>`_

----

Data recovery
*************

Check disk serial number:

.. code-block:: bash

    smartctl -x /dev/sdX

Clone disk:

.. code-block:: bash

    dd if=/dev/sdX of=/dev/sdX bs=1G status=progress

See: `Testdisk <https://www.cgsecurity.org/wiki/TestDisk_Download>`_

For SMART check see: `dbi-services.com/blog <https://www.dbi-services.com/blog/linux-disks-diagnostic-using-smarctl/>`_

----

VPN & Tunnels
*************

Libreswan IPSec
===============

Add ipsec-tunnel for manual startup:

.. code-block:: bash

    ipsec auto --add TUNNEL

Set ipsec-tunnel up manually:

.. code-block:: bash

    ipsec auto --up TUNNEL

Show ipsec tunnel stati:

.. code-block:: bash

    ipsec trafficstatus

Check basic ipsec config/functionality:

.. code-block:: bash

    ipsec verify

SSH
===

SSH Tunnel (remote resource on local port):

.. code-block:: bash

    ssh -L localPort:targetIP:targetPort USER@HOST

WireGuard
=========

Start WireGuard VPN:

.. code-block:: bash

    sudo wg-quick up CONFIG

Stop WireGuard VPN:

.. code-block:: bash

    sudo wg-quick down CONFIG

----

Pentesting
**********

Scan all TCP ports using syn-option:

.. code-block:: bash

    sudo nmap -vv -sS -p1-65535 -T5 --max-retries=1 -Pn <target>

Scan all TCP ports:

.. code-block:: bash

    sudo nmap -vv -p1-65535 -T5 --max-retries=1 -Pn <target>

Scan all TCP & UDP ports:

.. code-block:: bash

    sudo nmap -vv -p1-65535 -T5 --max-retries=1 -Pn -sU -sT <target>

Fast full-scan:

.. code-block:: bash

    sudo nmap -T4 -A -p- --min-rate 1000 --open -oN scan.txt <target>

    # --open = only show open ports
    # -oN = save output to file
    # -A = OS detection


----

Files
#####

Find Files
**********

Search for file by name:

.. code-block:: bash

    find -type f -name NAME*

Search for directory by name:

.. code-block:: bash

    find -type d -name NAME

----

Tar Archives
************

Create:

.. code-block:: bash

    tar -czvf ARCHIVE DIR

Extract:

.. code-block:: bash

    tar -xzvf ARCHIVE -C DIR

----

File Encryption
***************

Age
===

Download: `FiloSottile/age <https://github.com/FiloSottile/age/releases>`_

Encrypt file:

.. code-block:: bash

    age -R $AGE_PUB_KEY -o $OUTPUT

Decrypt file:

.. code-block:: bash

    age -d -i $AGE_PRIV_KEY $INPUT

----

S3-Storage
**********

Prepare for CLI-interation with S3-buckets and files that are saved in them:

.. code-block:: bash

    apt install awscli
    export AWS_ACCESS_KEY_ID="<YOUR-TOKEN-KEY>"
    export AWS_SECRET_ACCESS_KEY="<YOUR-SECRET>"
    S3_URL=https://s3.oxl.at

List existing buckets:

.. code-block:: bash

    aws --endpoint-url="$S3_URL" s3 ls

List existing files inside a bucket:

.. code-block:: bash

    S3_BUCKET='test'
    aws --endpoint-url="$S3_URL" s3 ls "s3://${S3_BUCKET}" --human-readable

Sync full content of a bucket to a local path:

.. code-block:: bash

    S3_BUCKET='test'
    SYNC_DIR='/data/s3/test'
    mkdir -p "$SYNC_DIR"
    aws --endpoint-url="$S3_URL" s3 sync "s3://${S3_BUCKET}" "$SYNC_DIR"


----

Ansible
#######

Ansible-Vault encrypt string:

.. code-block:: bash

     ansible-vault encrypt_string 'VAR_VALUE'

Ansible-Vault encrypt file:

.. code-block:: bash

    ansible-vault encrypt path/to/file.yml

Ansible-Vault show decrypted file-content:

.. code-block:: bash

    ansible-vault view path/to/file.yml

----

Image Manipulation
##################

JPEG Compress Images
********************

Install:

.. code-block:: bash

    apt-get install imagemagick

Single
======

.. code-block:: bash

    convert IMG.png -quality 70 IMG.jpg

Multiple
========

.. code-block:: bash

    for img in *.jpg; do convert "$img" -quality 70 "$img"; done

    # or from png
    for img in *.png; do convert "$img" -quality 70 "${img%.png}.jpg"; done

----

Video Manipulation
##################

FFMPEG
******

Replace audio of a video:

.. code-block:: bash

    ffmpeg -i video_in.mp4 -i audio_in.wav -c:v copy -map 0:v:0 -map 1:a:0 video_out.mp4

Extract part of a video:

.. code-block:: bash

    ffmpeg -ss ${START_SEC} -i in.mp4 -t ${DURATION_SEC} -map 0 -c copy out.mp4

Rotate Video: (Transpose = Rotation)

* 0 = 90° counterclockwise and vertical flip (default)
* 1 = 90° clockwise
* 2 = 90° counterclockwise
* 3 = 90° clockwise and vertical flip

.. code-block:: bash

    ffmpeg -i in.mp4 -c:a copy -vf "transpose=1" out.mp4

Create a slideshow-video with audio:

* framerate = Duration of a single image (0.3 = 3sec)
* loop = Endless-loop for the images
* glob '*.jpg' = Use all images with jpg extension (ordered by filename)
* ${IN_MUSIC} = Music track
* shortest = End the video after the music has stopped
* -vf "scale=1920:1080..." = Makes sure the images are not warped

.. code-block:: bash

    ffmpeg -framerate 0.3 -loop 1 -pattern_type glob -i '*.jpg' -i ${IN_MUSIC} -shortest -c:v libx264 -vf "scale=1920:1080:force_original_aspect_ratio=decrease:eval=frame,pad=1920:1080:-1:-1:eval=frame" -r 30 -pix_fmt yuv420p out.mp4

Extract part of a video:

.. code-block:: bash

    ffmpeg -i input.mp4 -ss 00:05:10 -to 00:15:30 -c:v copy -c:a copy output2.mp4

Join multiple videos together:

.. code-block:: bash

    echo "file 'video1.mp4'" > concat.txt
    echo "file 'video2.mp4'" >> concat.txt
    echo "file 'video3.mp4'" >> concat.txt

    ffmpeg -f concat -i concat.txt -c copy output.mp4

----

Webp Compress Images
********************

Install:

.. code-block:: bash

    apt-get install webp

Alternative Download:

.. code-block:: bash

    wget -c https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-0.6.1-linux-x86-32.tar.gz

Single
======

.. code-block::

    cwebp -q 70 IMG.png -o IMG.webp

Multiple
========

.. code-block::

    for img in *.jpg; do cwebp -q 70 "$img" -o "${img%.jpg}.webp"; done

----

Databases
#########

MySQL/MariaDB
*************

Change database:

.. code-block:: bash

    use DATABASE;

List tables:

.. code-block:: bash

    show TABLES;

Show table schema:

.. code-block:: bash

    desc TABLE;

Show all current processes:

.. code-block:: bash

    SHOW FULL PROCESSLIST;

Show all users of mysql instance:

.. code-block:: bash

    select host, user from mysql.user;

Binlog/Query analysis:

.. code-block:: bash

    mysqlbinlog /var/lib/mysql/mysql-bin.NNNNN -v

Get replication status:

.. code-block:: bash

    SHOW SLAVE STATUS\G

----

PostgreSQL
**********

Enter:

.. code-block:: bash

    sudo -u postgres psql

Change database:

.. code-block:: bash

    \c DATABASE;

List tables:

.. code-block:: bash

    \dt

----

CockroachDB
***********

See: `CockroachDB Releases <https://www.cockroachlabs.com/docs/releases/>`_

Download client:

.. code-block:: bash

    curl -s -L https://binaries.cockroachdb.com/cockroach-sql-v24.1.4.linux-amd64.tgz | tar -xz --strip-components=1 -C /tmp/ && sudo mv /tmp/cockroach /usr/local/bin/cockroach

Connect:

.. code-block:: bash

    cockroach-sql --url "postgres://root@servername:26257/mydb?sslmode=disable"

----

Containers
##########

Docker
******

Start an interactive shell inside a temporary container:

.. code-block:: bash

    docker run --rm -it alpine /bin/sh

Send the container-logs to the systemd-journal and set the container-name as log-application-name:

.. code-block:: bash

    docker run --log-driver=journald --log-opt tag="{{.Name}}" ...

Pipe host ports to container ports:

.. code-block:: bash

    docker run -p <host-port>:<container-port> ...

    docker run -p 8888:8080 ...

    # only listen on localhost
    docker run -p 127.0.0.1:8888:8080 ...

    # udp
    docker run -p 1053:1053/udp ...

Connect the container to a directory on the host:

.. code-block:: bash

    docker run -v <host-path>:<container-path> ...

    docker run -v /etc/oxl-riskdb/dnsbl/:/app/ ...

    # WARNING: the permissions between host and container are simply matching the user- and group-id's => so if the container runs unprivileged you will have to match the user-id and give that user permissions on the host-directory

Update the image on every restart to the latest state of the configured tag:

.. code-block:: bash

    docker run --pull=always ... <image>:<tag>

.. include:: ../_include/user_rath.rst
