import config
id = config.start()
dshi = "http://feeds.dshield.org/top10-2.txt"
config.add_ip(config.get_ip_url(dshi),"dshi")

