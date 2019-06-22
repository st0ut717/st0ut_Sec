#!/usr/bin/bash
#
# Script to scan 2 vlans and optain all active IPs on that vlan
#
# nmap ports: 22,389,636, 3268, 3269, 88, 445,
#
# nmap -p 22,88,389,445,636,3268,3269 10.1.166.0/23
# Guy W. Smallwood
#
#set veriables
nscan=/opt/nscan
bin=$nscan/bin
conf=$nscan/conf
log=$nscan/log
temp=$nscan/temp
reports=$nscan/reports
sectool=$reports/sectool
#
#
# Support files
# 
# Test and create directories needed
if [ -d $conf ]
  then
    echo "$conf exist" > /dev/null
  else
    echo "$conf does not exist exiting"
    mkdir $conf
    exit
fi
if [ -f $conf/vlans.csv ]
  then
    echo "$conf/vlans.csv" > /dev/null
  else
    echo "$conf/vlans.csv does not exist exiting"
    exit
fi
#
if [ -d $reports ]
  then
    echo "$reports" > /dev/null
  else
    echo "$reports does not exist creating"
    mkdir $reports
fi
if [ -d $reports/new ]
  then
    echo "$reports/new" > /dev/null
  else
    echo "$reports/new does not exist creating"
    mkdir $reports/new
fi
if [ -d $sectool ]
  then
    echo "$sectool" > /dev/null
  else
    echo "$sectool does not exist creating"
    mkdir $sectool
fi
# Test and create directories needed complete
# Start work
# stop start networking
# get input file for for vlans
cat $conf/vlans.csv|awk -F, '{print $1"/"$2}'
# for vlan in `cat $conf/vlans.csv|awk -F, '{print $1","$2","$7}'`
for vlan in `cat $conf/vlans.csv|awk -F, '{print $1","$2","$7","$8}'`
do
  cidr=`echo $vlan|awk -F, '{print $1"/"$2}'`
  vln=`echo $vlan|awk -F, '{print $3}'`
  ethX=`echo $vlan|awk -F, '{print $4}'`
  echo "$ethX"
  sleep 5
  if [ -f $conf/baseline_$vln ]
    then
      echo "$conf/baseline_$vln.txt" > /dev/null
    else
      echo "$conf/baseline_$vln.txt creating"
      touch $conf/baseline_$vln.txt
  fi
  ###   put checking code here ###
  /usr/sbin/ifup $ethX
  ip a show
  sleep 20
  ###   put checking code here ###
  nmap -p 22,88,389,445,636,3268,3269, $cidr -oG $temp/$vln.txt
  for host in `cat $temp/$vln.txt|grep Up|awk '{print $2}'`
  do
    #see if host is known
    if grep $host $conf/baseline_$vln.txt > /dev/null
    then
      echo "null" > /dev/null
    else
      # start host interigation commands
      hname=`nmap -Pn -R -p 22 $host|grep $host|awk '{print $5}'`
      nmap -A $host -oX $reports/new/$hname.xml
      # Alert MTOC 
      echo "sendmail or smtp setup for mtoc needed here"
      echo "NEW HOST DETECTED!!!!!"
      echo "HOSTNAME = $hname IPADDR = $host"
      # append to ip and host name to baseline
      echo "HOSTNAME = $hname IPADDR = $host" >> $conf/baseline_$vln.txt
      # append to sectool file
      # site,in stock, hostname,device type,operating system,network, CMDB ID,  application,AD Domain, managed by, is GXP, IPADDR,  phys location, Environment,is virtual
      #get OS type
      #osmatch=`cat $reports/new/hname.xml|grep "osmatch name="|awk -F= '{print$2}'`
      echo "$osmatch"
      echo "Framingham Biologics,yes,$hname,$osmatch,$host" >> $sectool/discovered_host.csv
      # sectool export complete
    fi
  done
  /usr/sbin/ifdown $ethX
done
mv $reports/new/*.xml $reports/
exit
