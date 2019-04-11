PREFIX?=/opt

install:
	mkdir -p ${PREFIX}/check_url
	for file in check_url.py config.py; do install -o root -g root -m 755 $$file ${PREFIX}/check_url/; done
	install -o root -g root -m 755 check_url /etc/init.d/
	update-rc.d check_url defaults

uninstall:
	rm -rf ${PREFIX}/check_url
	service check_url stop
	update-rc.d check_url remove
	rm /etc/init.d/check_url

