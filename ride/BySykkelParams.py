import argparse

parser = argparse.ArgumentParser(description='BySykkel Demo App Parameters')

parser.add_argument('--gbfs', dest='gbfs', type=str, default="https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json",
                    help='vei til auto discovery fil')

parser.add_argument('--id', dest='client_id', type=str, default="Daria-Klukin-for-Origo",
                    help='Client-Identifier for API forespørsel')

parser.add_argument('--bikes', dest='bikes', type=int, default=0,
                    help='stasjoner med  tilgjengelige sykkler')

parser.add_argument('--docks', dest='docks', type=int, default=0,
                    help='stasjoner med ledige plasser')

parser.add_argument('--gps', dest='location', type=str, default="[59.915096,10.7312715]",
                    help='GPS posisjon [lat,lon]')

parser.add_argument('--interval', dest='interval',  type=int, default=10,
                    help='oppdatering intervallet i sekunder')

parser.add_argument('--demo', dest='demo', action='store_true',
                    help='interaktiv demo (bare manuell oppdatering)')

parser.add_argument('--silent', dest='silent', action='store_true', default=False,
                    help='No error messages')

parser.add_argument('--dump_format', dest='dump_format', type=str, 
                    default="{0:20.20s}\t{1:.3f}\t{2:.6f}\t{3:.6f}\t{4}\t{5}",
                    help='format string where  {0}=name, {1}=distance, {2}=lat, {3}=lon, {4}=bikes, {5}=docks')