import argparse

parser = argparse.ArgumentParser(description='BySykkel Demo App Parameters')

parser.add_argument('--gbfs', dest='gbfs', type=str, default="https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json",
                    help='vei til auto discovery fil')

parser.add_argument('--id', dest='client_id', type=str, default="Daria-Klukin-for-Origo",
                    help='Client-Identifier for API forespørsel')

parser.add_argument('--sykkler', dest='bikes', type=int, default=1,
                    help='stasjoner med  tilgjengelige sykkler')

parser.add_argument('--plasser', dest='docks', type=int, default=0,
                    help='stasjoner med ledige plasser')

parser.add_argument('--gps', dest='location', type=str, default="[59.915096,10.7312715]",
                    help='GPS posisjon [lat,lon]')

parser.add_argument('--interval', dest='interval',  type=int, default=10,
                    help='oppdatering intervallet i sekunder')

parser.add_argument('--demo', dest='demo', action='store_true',
                    help='interaktiv demo (bare manuell oppdatering)')
