.. _net_openwrt:

.. include:: ../_include/head.rst

=======
OpenWRT
=======


.. include:: ../_include/wip.rst


Intro
#####

OpenWRT is an Operating System for network devices like routers, switches and wlan access points.

See also: :ref:`OpenWRT Hardware & Firmware Flashing <net_openwrt_hw>`

----

Useful Commands
###############

* Show installed packages: :code:`opkg list-installed`
* Get Mac-addresses of all connected clients:

.. code-block::

    for iface in `iw dev | grep Interface | cut -f 2 -s -d" "`; do iw dev $iface station dump | grep Station | cut -f 2 -s -d" ";done

* Get connected clients with connection-quality:

.. code-block::

    for iface in `iw dev | grep Interface | cut -f 2 -s -d" "`; do iw dev $iface station dump | grep -E 'Station|signal|bitrate|expected';done

* Check hardware: :code:`cat /proc/cpuinfo` or :code:`ubus call system board`
* Check release: :code:`cat /etc/openwrt_release`
* Show running network-config: :code:`cat /etc/config/network`
* Show unsaved network config: :code:`uci show network`
* Show running wlan-config: :code:`cat /etc/config/wireless`
* Show unsaved wlan config: :code:`uci show wireless`
* Live follow logs: :code:`logread -f`

----

UCI CLI
#######

See: `OpenWRT UCI Documentation <https://openwrt.org/docs/guide-user/base-system/uci>`_

We recommend to use the :code:`uci` command-line-interface to modify your systems configuration as it has some validation built-in.

OpenWRT has a unsaved and running config.

Whenever you configure something using :code:`uci` it is unsaved. You need to :code:`apply` the changes for them to take effect. This allows you to rebuild your configuration and apply many changes at once when you're done.

Changes can also just be applied for certain parts of configuration - like: :code:`uci apply network` or :code:`uci apply wireless`

You can check the unsaved configuration using: :code:`uci show`. You can also limit the output: :code:`uci show network`

The saved/running configuration can be seen in the config files: :code:`/etc/config/*`. You can check their content like this: :code:`cat /etc/config/network`

----

Configuration
#############

SSH
***

See: `OpenWRT SSH Documentation <https://openwrt.org/docs/guide-user/base-system/dropbear>`_

* Set SSH Port: :code:`uci set dropbear.dropbear1.Port=22`
* Add SSH public keys to :code:`/etc/dropbear/authorized_keys`
* Disable password authentication: :code:`uci set dropbear.dropbear1.PasswordAuth=0`

  **WARNING**: Make sure to test the authentication beforehand: :code:`ssh -o PasswordAuthentication=no root@192.168.1.1`

* Disable Root login: :code:`uci set dropbear.dropbear1.RootLogin=0`

Save & reload: :code:`uci commit dropbear && /etc/init.d/dropbear reload`

----

Network
*******

See: `OpenWRT Network Documentation <https://openwrt.org/docs/guide-user/network/network_configuration>`_

The network interface naming might differ depending on your systems hardware.

Also: Some hardware has an internal switch. If that is the case the vlan tagging is a little more complex. See: `OpenWRT Switch Documentation <https://openwrt.org/docs/guide-user/network/vlan/switch>`_

* Configure a Bridge management-interface:

  .. code-block::

      uci set network.lan=interface
      uci set network.lan.device='br-lan'
      uci set network.lan.proto='dhcp'
      uci set network.lan.delegate='0'
      uci set network.lan.force_link='1'
      uci set network.device[0]=device
      uci set network.device[0].bridge_empty='1'
      uci set network.device[0].ipv6='0'
      uci set network.device[0].multicast='0'
      uci set network.device[0].name='br-lan'
      uci set network.device[0].ports='eth0'
      uci set network.device[0].rpfilter='loose'
      uci set network.device[0].sendredirects='0'
      uci set network.device[0].type='bridge'

* Configure a bridge to a tagged VLAN:

  .. code-block::

      uci set network.lan_intern=interface
      uci set network.lan_intern.proto='none'
      uci set network.lan_intern.device='br-intern'
      uci set network.lan_intern.defaultroute='0'
      uci set network.lan_intern.peerdns='0'
      uci set network.lan_intern.delegate='0'
      uci set network.vlan59=device
      uci set network.vlan59.name='br-intern'
      uci set network.vlan59.ports='eth0.59'
      uci set network.vlan59.ipv6='0'
      uci set network.vlan59.multicast='0'
      uci set network.vlan59.sendredirects='0'
      uci set network.vlan59.bridge_empty='1'
      uci set network.vlan59.type='bridge'

* Save config: :code:`uci apply network`
* Apply config: :code:`/etc/init.d/network restart`

----

Wireless
********

See: `OpenWRT Wireless Documentation <https://openwrt.org/docs/guide-user/network/wifi/basic>`_

* Example: Configure 5GHz WLAN radio:

  .. code-block::

      uci set wireless.radio0=wifi-device
      uci set wireless.radio0.type='mac80211'
      uci set wireless.radio0.band='5g'
      uci set wireless.radio0.country='AT'
      uci set wireless.radio0.country_ie='1'
      uci set wireless.radio0.channel='auto'
      uci set wireless.radio0.disabled='0'
      uci set wireless.radio0.htmode='VHT40'
      uci set wireless.radio0.cell_density='1'
      uci set wireless.radio0.beacon_int='100'
      uci set wireless.radio0.log_level='2'

* Example: Configure 2.4GHz WLAN radio:

  .. code-block::

      uci set wireless.radio1=wifi-device
      uci set wireless.radio1.type='mac80211'
      uci set wireless.radio1.band='2g'
      uci set wireless.radio1.country='AT'
      uci set wireless.radio1.country_ie='1'
      uci set wireless.radio1.channel='auto'
      uci set wireless.radio1.disabled='0'
      uci set wireless.radio1.htmode='HT20'
      uci set wireless.radio1.cell_density='1'
      uci set wireless.radio1.beacon_int='200'
      uci set wireless.radio1.log_level='2'

* Configure 5GHz WLAN:

  .. code-block::

      uci set wireless.intern5=wifi-iface
      uci set wireless.intern5.device='radio0'
      uci set wireless.intern5.mode='ap'
      uci set wireless.intern5.ssid='SuperWIFI'
      uci set wireless.intern5.key='<SECRET>'
      uci set wireless.intern5.network='lan_intern'
      uci set wireless.intern5.encryption='psk2+aes'
      uci set wireless.intern5.disabled='0'

* Configure 2.4GHz WLAN:

  .. code-block::

      uci set wireless.intern2=wifi-iface
      uci set wireless.intern2.device='radio1'
      uci set wireless.intern2.mode='ap'
      uci set wireless.intern2.ssid='SuperWIFI'
      uci set wireless.intern2.key='<SECRET>'
      uci set wireless.intern2.network='lan_intern'
      uci set wireless.intern2.encryption='psk2+aes'
      uci set wireless.intern2.disabled='0'

* Configure 802.11r - fast-roaming:

  .. code-block::

      uci set wireless.intern2.ieee80211r='1'
      uci set wireless.intern2.mobility_domain='1111'
      uci set wireless.intern2.reassociation_deadline='20000'
      uci set wireless.intern2.pmk_r1_push='1'
      uci set wireless.intern2.ft_psk_generate_local='1'

* Enable client-isolation: :code:`uci set wireless.intern2.isolate='1'`

* Set WLAN to be hidden: :code:`uci set wireless.intern2.hidden=0`

* Set encryption: :code:`uci set wireless.intern2.encryption=psk2+aes`

  For options see: `OpenWRT Wireless Encryption <https://openwrt.org/docs/guide-user/network/wifi/basic#encryption_modes>`_

* Settings we like to use:

  .. code-block::

      uci set wireless.intern5.ieee80211w='0'
      uci set wireless.intern5.wpa_group_rekey='3600'
      uci set wireless.intern5.max_inactivity='3600'
      uci set wireless.intern5.disassoc_low_ack='0'
      uci set wireless.intern5.wpa_disable_eapol_key_retries='1'

      # disable high-throughput (802.11n) if not stable on your hardware
      uci set wireless.intern5.wmm='0'

      # 802.11k
      uci set wireless.intern5.ieee80211k='1'
      uci set wireless.intern5.rrm_neighbor_report='1'
      uci set wireless.intern5.rrm_beacon_report='1'

      # 802.11v
      uci set wireless.intern5.ieee80211v='1'
      uci set wireless.intern5.time_advertisement='2'
      uci set wireless.intern5.wnm_sleep_mode='0'
      uci set wireless.intern5.bss_transition='1'

      # 802.11r - fast roaming
      uci set wireless.intern5.ieee80211r='1'
      uci set wireless.intern5.mobility_domain='1111'
      uci set wireless.intern5.reassociation_deadline='20000'
      uci set wireless.intern5.pmk_r1_push='1'
      uci set wireless.intern5.ft_psk_generate_local='1'

* Save config: :code:`uci commit wireless`
* Reload config: :code:`wifi down & wifi up`


----

System
******

See: `OpenWRT System Documentation <https://openwrt.org/docs/guide-user/base-system/system_configuration>`_

* Update package catalogue: :code:`opkg update`

  **WARNING**: This will take up some disk space!

* Install a package: :code:`opkg install curl`

* Set the timezone :code:`uci set system.system.timezone=CET-1CEST,M3.5.0,M10.5.0/3` and :code:`uci set system.system.zonename=Europe/Vienna`

  For available timezone-formats see: `OpenWRT Timezones <https://github.com/openwrt/luci/blob/master/modules/luci-lua-runtime/luasrc/sys/zoneinfo/tzdata.lua>`_

* Configure Syslog logging:

  .. code-block::

      uci set system.system.log_proto=udp
      uci set system.system.log_port=514
      uci set system.system.log_ip=192.168.1.10

* Set the hostname :code:`uci set system.@system[0].hostname=<HOSTNAME>`

* Save: :code:`uci commit system`

* Add a daily reboot job: (in `crontab format <https://crontab.guru/>`_)

  .. code-block:: bash

      # simple
      echo '30 2 * * * touch /etc/banner && reboot' > /etc/crontabs/root

      # or with a random delay (between 1 and 999 seconds)
      echo '30 2 * * * sleep `head /dev/urandom | tr -dc \"0123456789\" | head -c3` && touch /etc/banner && reboot' > /etc/crontabs/root

      service cron restart

----

Firewall
********

* Disable the firewall: :code:`/etc/init.d/firewall stop && service firewall disable`

----

Ansible
#######

Without Inventory
*****************

* Create a dummy inventory like this:

  .. code-block:: yaml

      ---

      openwrt:
        hosts:
          '192.168.1.1':

* Run the playbook targeting an IP: :code:`ansible-playbook -i dummy_inventory.yml -k playbook.yml -e ansible_host=<YOUR-AP-IP>`

----

Dynamic Inventory
*****************

We recommend using the `nmap dynamic inventory <https://docs.ansible.com/ansible/latest/collections/community/general/nmap_inventory.html>`_.

To use it:

* Install the Ansible collection: :code:`ansible-galaxy install community.general`
* Install nmap on your controller: :code:`apt install nmap`
* Add the line :code:`fact_caching_connection = /tmp/.ansible-${USER}/inventory` to your ansible.cfg [default]-section
* Use a inventory file like this:

  .. code-block:: yaml

      ---

      # change the port 9822 to your custom ssh port

      plugin: community.general.nmap
      address: 192.168.20.0/24
      exclude: 192.168.20.1
      port: 443, 22
      ipv4: true
      ipv6: false
      cache: true
      cache_plugin: jsonfile
      cache_timeout: 3600
      groups:
        openwrt: "ports | selectattr('port', 'equalto', '9822')"

* Run: :code:`ansible-playbook -i inventory_nmap.yml -k playbook.yml [--limit <YOUR-AP-IP>]`

----

Usage
*****

We like to manage OpenWRT using the :code:`ansible.builtin.raw` module which is basically executing a command over SSH.

* We first get the current configuration so we can only make changes when needed

  .. code-block:: yaml

      - name: Get running config
        ansible.builtin.raw: 'uci show'
        changed_when: false
        check_mode: false
        register: owrt_run

* You can also make decisions on hardware-basis

  .. code-block:: yaml

      - name: Get hardware
        ansible.builtin.raw: 'ubus call system board'
        changed_when: false
        check_mode: false
        register: owrt_hw

      - name: Hardware | Mikrotik wAP
        ansible.builtin.include_tasks: 'hw_mikrotik_wap.yml'
        vars:
          ap_device_net: 'eth0'
        when: "'MikroTik RouterBOARD wAP' in owrt_hw.stdout"

* You can easily configure your needed settings - example:

  .. code-block:: yaml

      # defaults
      vlan_settings:
        bridge:
          ipv6: '0'
          multicast: '0'
          sendredirects: '0'
          bridge_empty: '1'
          type: 'bridge'

        network:
          proto: 'none'
          defaultroute: '0'
          peerdns: '0'
          delegate: '0'

      # tasks
      - name: Configure VLAN bridge
        ansible.builtin.raw: "uci set {{ setting }}"
        when: setting not in owrt_run.stdout
        vars:
          setting: "network.vlan59.{{ option.key }}='{{ option.value }}'"
        loop_control:
          loop_var: option
        with_dict: "{{ vlan_settings.bridge }}"
        notify: apply-network

      - name: Configure VLAN Network
        ansible.builtin.raw: "uci set {{ setting }}"
        when: setting not in owrt_run.stdout
        vars:
          setting: "network.lan_intern.{{ option.key }}='{{ option.value }}'"
        loop_control:
          loop_var: option
        with_dict: "{{ vlan_settings.network }}"
        notify: apply-network

      # handler
      - name: apply-network
        ansible.builtin.raw: |
          uci commit network &&
          /etc/init.d/network restart

Example Role for managing OpenWRT APs: `ansibleguy/net_openwrt_ap <https://github.com/ansibleguy/net_openwrt-ap>`_

Modules: `community.general.openwrt_init <https://docs.ansible.com/ansible/latest/collections/community/general/openwrt_init_module.html#ansible-collections-community-general-openwrt-init-module>`_, `community.general.opkg <https://docs.ansible.com/ansible/latest/collections/community/general/opkg_module.html#ansible-collections-community-general-opkg-module>`_
