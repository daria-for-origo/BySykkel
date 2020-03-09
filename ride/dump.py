import BySykkelModel
import BySykkelParams

args = BySykkelParams.parser.parse_args()
model = BySykkelModel.Source(args.gbfs, args.client_id)
model.update(BySykkelModel.GPSLocation.parse(args.location))

for row in model.status:
    if row.bikes >= args.bikes:
        if row.docks >= args.docks:
            print(row.format(args.dump_format))
