MapID = [
"Deathaura LE",
"Eternal Empire LE",
"Ever Dream LE",
"Golden Wall LE",
"Ice and Chrome LE",
"Pillars of Gold LE",
"Submarine LE",
"Acropolis LE",
"Cyber Forest LE",
"Kairos Junction LE",
"King's Cove LE",
"New Repugnancy LE",
"Thunderbird LE",
"Turbo Cruise'84 LE",
"Acid Plant LE",
"Blueshift LE",
"Cerulean Fall LE",
"Dreamcatcher LE",
"Fracture LE",
"Lost and Found LE",
"Para Site LE",
"Disco Bloodbath LE",
"Ephemeron LE",
"Triton LE",
"Winter's Gate LE",
"World of Sleepers LE",
"Nightshade LE",
"Simulacrum LE",
"Zen LE",
"Port Aleksander LE",
"Automaton LE"
]

MapSize = [
144*140,
140*140,
138*141,
168*140,
144*140,
136*138,
134*122,
140*136,
128*148,
120*140,
153*148,
152*120,
140*140,
140*116,
152*136,
136*136,
150*138,
136*136,
144*124,
144*130,
140*152,
148*132,
132*148,
144*144,
128*132,
144*144,
138*136,
144*124,
132*148,
158*140,
148*148
]
AppendMaps = []
PoolSize = len(MapID)
for i in range (PoolSize) :
	AppendMaps.append((MapID[i], MapSize[i]))

MapSize.sort()
SizesLength = PoolSize // 3
Sizes = [MapSize[i*SizesLength:(i+1)*SizesLength] for i in range(3)]
Sizes[-1].extend(MapSize[-(len(MapSize)%3):])

