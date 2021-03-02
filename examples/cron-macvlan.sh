# This script is for OpenWRT to create virtual interface
# First of all, you need to install kmod-macvlan
# once the master interface restart, the slave interface will be deleted, so use crontab execute once a minute
*/1 * * * * ip link add link eth0.2 dev wan1 type macvlan
*/1 * * * * ip link add link eth0.2 dev wan2 type macvlan

