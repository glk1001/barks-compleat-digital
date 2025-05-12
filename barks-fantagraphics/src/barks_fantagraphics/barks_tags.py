from collections import defaultdict
from enum import Enum, auto

from barks_titles import Titles


class Tags(Enum):
    ALGERIA = auto()
    ANDES = auto()
    ARABIAN_PENINSULA = auto()
    AUSTRALIA = auto()
    CENTRAL_AFRICA = auto()
    CHINA = auto()
    CONGO = auto()
    DUCKBURG = auto()
    EGYPT = auto()
    FRANCE = auto()
    GERMANY = auto()
    GREECE = auto()
    HIMALAYAS = auto()
    INDIA = auto()
    INDIAN_OCEAN = auto()
    INDO_CHINA = auto()
    IRAQ = auto()
    LIBYA = auto()
    MALI = auto()
    MONGOLIA = auto()
    MOROCCO = auto()
    NIAGARA_FALLS = auto()
    PAKISTAN = auto()
    PERSIA = auto()
    PLAIN_AWFUL = auto()
    RUSSIA = auto()
    SOUTH_AFRICA = auto()
    SOUTH_AMERICA = auto()
    SUDAN = auto()
    SYRIA = auto()
    TANGANYIKA = auto()

    AIRPLANE = auto()
    FIRE = auto()
    SQUARE_EGGS = auto()

    ARGUS_MCFIENDY = auto()
    BEAGLE_BOYS = auto()
    FLINTHEART_GLOMGOLD = auto()
    GENERAL_SNOZZIE = auto()
    GLADSTONE_GANDER = auto()
    GYRO_GEARLOOSE = auto()
    HERBERT = auto()
    MAGICA_DE_SPELL = auto()
    NEIGHBOR_JONES = auto()


TAG_TEXT = {
    "algeria": (Tags.ALGERIA, "Algeria"),
    # "africa": (Tags.ALGERIA, "Algeria"),
    "andes": (Tags.ANDES, "Andes"),
    "arabian peninsula": (Tags.ARABIAN_PENINSULA, "Arabian Peninsula"),
    "arabia": (Tags.ARABIAN_PENINSULA, "Arabian Peninsula"),
    "australia": (Tags.AUSTRALIA, "Australia"),
    "central africa": (Tags.CENTRAL_AFRICA, "Central Africa"),
    "china": (Tags.CHINA, "China"),
    "congo": (Tags.CONGO, "Congo"),
    "duckburg": (Tags.DUCKBURG, "Duckburg"),
    "egypt": (Tags.EGYPT, "Egypt"),
    "france": (Tags.FRANCE, "France"),
    "germany": (Tags.GERMANY, "Germany"),
    "greece": (Tags.GREECE, "Greece"),
    "himalayas": (Tags.HIMALAYAS, "Himalayas"),
    "india": (Tags.INDIA, "India"),
    "indian ocean": (Tags.INDIAN_OCEAN, "Indian Ocean"),
    "indo-china": (Tags.INDO_CHINA, "Indo-China"),
    "iraq": (Tags.IRAQ, "Iraq"),
    "libya": (Tags.MOROCCO, "Libya"),
    "mali": (Tags.MOROCCO, "Mali"),
    "mongolia": (Tags.MONGOLIA, "Mongolia"),
    "morocco": (Tags.MOROCCO, "Morocco"),
    "niagara falls": (Tags.NIAGARA_FALLS, "Niagara Falls"),
    "niagara": (Tags.NIAGARA_FALLS, "Niagara Falls"),
    "pakistan": (Tags.PAKISTAN, "Pakistan"),
    "persia": (Tags.PERSIA, "Persia"),
    "plain awful": (Tags.PLAIN_AWFUL, "Plain Awful"),
    "russia": (Tags.RUSSIA, "Russia"),
    "south africa": (Tags.SOUTH_AFRICA, "South Africa"),
    "south america": (Tags.SOUTH_AMERICA, "South America"),
    "sudan": (Tags.SUDAN, "Sudan"),
    "syria": (Tags.SYRIA, "Syria"),
    "tanganyika": (Tags.TANGANYIKA, "Tanganyika"),
    "airplane": (Tags.AIRPLANE, "airplane"),
    "aeroplane": (Tags.AIRPLANE, "airplane"),
    "fire": (Tags.FIRE, "fire"),
    "square eggs": (Tags.SQUARE_EGGS, "square eggs"),
    "argus mcfiendy": (Tags.ARGUS_MCFIENDY, "Argus McFiendy"),
    "argus": (Tags.ARGUS_MCFIENDY, "Argus"),
    "mcfiendy": (Tags.ARGUS_MCFIENDY, "McFiendy"),
    "beagle boys": (Tags.BEAGLE_BOYS, "The Beagle Boys"),
    "the beagle boys": (Tags.BEAGLE_BOYS, "The Beagle Boys"),
    "beagles": (Tags.BEAGLE_BOYS, "The Beagle Boys"),
    "flintheart glomgold": (Tags.FLINTHEART_GLOMGOLD, "Flintheart Glomgold"),
    "flintheart": (Tags.FLINTHEART_GLOMGOLD, "Flintheart Glomgold"),
    "glomgold": (Tags.FLINTHEART_GLOMGOLD, "Flintheart Glomgold"),
    "general snozzie": (Tags.GENERAL_SNOZZIE, "General Snozzie"),
    "snozzie": (Tags.GENERAL_SNOZZIE, "General Snozzie"),
    "gladstone gander": (Tags.GLADSTONE_GANDER, "Gladstone Gander"),
    "gladstone": (Tags.GLADSTONE_GANDER, "Gladstone Gander"),
    "gyro gearloose": (Tags.GYRO_GEARLOOSE, "Gyro Gearloose"),
    "gyro": (Tags.GYRO_GEARLOOSE, "Gyro Gearloose"),
    "gearloose": (Tags.GYRO_GEARLOOSE, "Gyro Gearloose"),
    "herbert": (Tags.HERBERT, "Herbert"),
    "magica de spell": (Tags.MAGICA_DE_SPELL, "Magica de Spell"),
    "magica": (Tags.MAGICA_DE_SPELL, "Magica de Spell"),
    "spell": (Tags.MAGICA_DE_SPELL, "Magica de Spell"),
    "neighbor jones": (Tags.NEIGHBOR_JONES, "Neighbor Jones"),
    "jones": (Tags.NEIGHBOR_JONES, "Neighbor Jones"),
}


BARKS_TAGS = defaultdict(list)

BARKS_TAGS[Tags.ALGERIA].append((Titles.ROCKET_RACE_AROUND_THE_WORLD, []))
BARKS_TAGS[Tags.ANDES].append((Titles.LOST_IN_THE_ANDES, []))
BARKS_TAGS[Tags.ARABIAN_PENINSULA].append((Titles.MINES_OF_KING_SOLOMON_THE, []))
BARKS_TAGS[Tags.ARABIAN_PENINSULA].append((Titles.MONEY_CHAMP_THE, []))
BARKS_TAGS[Tags.ARABIAN_PENINSULA].append((Titles.PIPELINE_TO_DANGER, []))
BARKS_TAGS[Tags.ARABIAN_PENINSULA].append((Titles.CAVE_OF_ALI_BABA, []))
BARKS_TAGS[Tags.ARABIAN_PENINSULA].append((Titles.MCDUCK_OF_ARABIA, []))
BARKS_TAGS[Tags.AUSTRALIA].append((Titles.ADVENTURE_DOWN_UNDER, []))
BARKS_TAGS[Tags.AUSTRALIA].append((Titles.RICHES_RICHES_EVERYWHERE, []))
BARKS_TAGS[Tags.AUSTRALIA].append((Titles.QUEEN_OF_THE_WILD_DOG_PACK_THE, []))
BARKS_TAGS[Tags.CENTRAL_AFRICA].append((Titles.DARKEST_AFRICA, []))
BARKS_TAGS[Tags.CENTRAL_AFRICA].append((Titles.VOODOO_HOODOO, []))
BARKS_TAGS[Tags.CENTRAL_AFRICA].append((Titles.JUNGLE_HI_JINKS, []))
BARKS_TAGS[Tags.CENTRAL_AFRICA].append((Titles.WISHING_WELL_THE, []))
BARKS_TAGS[Tags.CENTRAL_AFRICA].append((Titles.JUNGLE_BUNGLE, []))
BARKS_TAGS[Tags.CENTRAL_AFRICA].append((Titles.SO_FAR_AND_NO_SAFARI, []))
BARKS_TAGS[Tags.CHINA].append((Titles.MONEY_CHAMP_THE, []))
BARKS_TAGS[Tags.CONGO].append((Titles.BONGO_ON_THE_CONGO, []))
BARKS_TAGS[Tags.EGYPT].append((Titles.DONALD_DUCK_AND_THE_MUMMYS_RING, []))
BARKS_TAGS[Tags.FRANCE].append((Titles.DANGEROUS_DISGUISE, []))
BARKS_TAGS[Tags.GERMANY].append((Titles.FABULOUS_PHILOSOPHERS_STONE_THE, []))
BARKS_TAGS[Tags.GREECE].append((Titles.FABULOUS_PHILOSOPHERS_STONE_THE, []))
BARKS_TAGS[Tags.GREECE].append((Titles.GOLDEN_FLEECING_THE, []))
BARKS_TAGS[Tags.GREECE].append((Titles.ODDBALL_ODYSSEY, []))
BARKS_TAGS[Tags.GREECE].append((Titles.INSTANT_HERCULES, []))
BARKS_TAGS[Tags.HIMALAYAS].append((Titles.TRAIL_OF_THE_UNICORN, []))
BARKS_TAGS[Tags.HIMALAYAS].append((Titles.TRALLA_LA, []))
BARKS_TAGS[Tags.HIMALAYAS].append((Titles.LOST_CROWN_OF_GENGHIS_KHAN_THE, []))
BARKS_TAGS[Tags.INDIA].append((Titles.MAHARAJAH_DONALD, []))
BARKS_TAGS[Tags.INDIA].append((Titles.TRAIL_OF_THE_UNICORN, []))
BARKS_TAGS[Tags.INDIA].append((Titles.MINES_OF_KING_SOLOMON_THE, []))
BARKS_TAGS[Tags.INDIA].append((Titles.BILLION_DOLLAR_SAFARI_THE, []))
BARKS_TAGS[Tags.INDIA].append((Titles.ROCKET_RACE_AROUND_THE_WORLD, []))
BARKS_TAGS[Tags.INDIAN_OCEAN].append((Titles.MANY_FACES_OF_MAGICA_DE_SPELL_THE, []))
BARKS_TAGS[Tags.INDIAN_OCEAN].append((Titles.DOOM_DIAMOND_THE, []))
BARKS_TAGS[Tags.INDO_CHINA].append((Titles.CITY_OF_GOLDEN_ROOFS, []))
BARKS_TAGS[Tags.INDO_CHINA].append((Titles.MCDUCK_OF_ARABIA, []))
BARKS_TAGS[Tags.INDO_CHINA].append((Titles.TREASURE_OF_MARCO_POLO, []))
BARKS_TAGS[Tags.INDO_CHINA].append((Titles.MONKEY_BUSINESS, []))
BARKS_TAGS[Tags.IRAQ].append((Titles.FABULOUS_PHILOSOPHERS_STONE_THE, []))
BARKS_TAGS[Tags.IRAQ].append((Titles.RUG_RIDERS_IN_THE_SKY, []))
BARKS_TAGS[Tags.LIBYA].append((Titles.ROCKET_RACE_AROUND_THE_WORLD, []))
BARKS_TAGS[Tags.MALI].append((Titles.DAY_DUCKBURG_GOT_DYED_THE, []))
BARKS_TAGS[Tags.MALI].append((Titles.CANDY_KID_THE, []))
BARKS_TAGS[Tags.MONGOLIA].append((Titles.MONEY_CHAMP_THE, []))
BARKS_TAGS[Tags.MOROCCO].append((Titles.MAGIC_HOURGLASS_THE, []))
BARKS_TAGS[Tags.NIAGARA_FALLS].append((Titles.HIGH_WIRE_DAREDEVILS, []))
BARKS_TAGS[Tags.PAKISTAN].append((Titles.LOST_CROWN_OF_GENGHIS_KHAN_THE, []))
BARKS_TAGS[Tags.PERSIA].append((Titles.IN_ANCIENT_PERSIA, []))
BARKS_TAGS[Tags.PLAIN_AWFUL].append((Titles.LOST_IN_THE_ANDES, []))
BARKS_TAGS[Tags.RUSSIA].append((Titles.CITY_OF_GOLDEN_ROOFS, []))
BARKS_TAGS[Tags.SOUTH_AFRICA].append((Titles.SECOND_RICHEST_DUCK_THE, []))
BARKS_TAGS[Tags.SOUTH_AFRICA].append((Titles.SO_FAR_AND_NO_SAFARI, []))
BARKS_TAGS[Tags.SOUTH_AMERICA].append((Titles.LOST_IN_THE_ANDES, []))
BARKS_TAGS[Tags.SUDAN].append((Titles.MINES_OF_KING_SOLOMON_THE, []))
BARKS_TAGS[Tags.SYRIA].append((Titles.FABULOUS_PHILOSOPHERS_STONE_THE, []))
BARKS_TAGS[Tags.TANGANYIKA].append((Titles.UNSAFE_SAFE_THE, []))

BARKS_TAGS[Tags.DUCKBURG].append((Titles.HIGH_WIRE_DAREDEVILS, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.CHRISTMAS_IN_DUCKBURG, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.TITANIC_ANTS_THE, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.LAND_BENEATH_THE_GROUND, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.HIS_HANDY_ANDY, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.DUCKBURGS_DAY_OF_PERIL, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.GIANT_ROBOT_ROBBERS_THE, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.GREAT_DUCKBURG_FROG_JUMPING_CONTEST_THE, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.OLYMPIC_HOPEFUL_THE, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.DAY_DUCKBURG_GOT_DYED_THE, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.CODE_OF_DUCKBURG_THE, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.BLACK_WEDNESDAY, []))
BARKS_TAGS[Tags.DUCKBURG].append((Titles.DUCKBURG_PET_PARADE_THE, []))

BARKS_TAGS[Tags.AIRPLANE].append((Titles.TRUANT_NEPHEWS_THE, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.MASTER_RAINMAKER_THE, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.CROWN_OF_THE_MAYAS, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.ADVENTURE_DOWN_UNDER, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.NORTH_OF_THE_YUKON, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.TRAIL_OF_THE_UNICORN, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.TWO_WAY_LUCK, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.GREAT_WIG_MYSTERY_THE, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.BALLOONATICS, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.FROZEN_GOLD, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.LOST_FRONTIER, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.FRAIDY_FALCON_THE, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.TRALLA_LA, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.SO_FAR_AND_NO_SAFARI, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.VOLCANO_VALLEY, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.VOODOO_HOODOO, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.SPICY_TALE_A, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.LAND_OF_THE_PYGMY_INDIANS, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.GOOD_DEEDS_THE, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.SECRET_OF_ATLANTIS_THE, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.SMOKE_WRITER_IN_THE_SKY, []))
BARKS_TAGS[Tags.AIRPLANE].append((Titles.QUEEN_OF_THE_WILD_DOG_PACK_THE, []))

BARKS_TAGS[Tags.FIRE].append((Titles.FIREBUG_THE, []))
BARKS_TAGS[Tags.SQUARE_EGGS].append((Titles.LOST_IN_THE_ANDES, []))

BARKS_TAGS[Tags.ARGUS_MCFIENDY].append((Titles.DARKEST_AFRICA, []))

BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.TERROR_OF_THE_BEAGLE_BOYS, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.BIG_BIN_ON_KILLMOTOR_HILL_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.ONLY_A_POOR_OLD_MAN, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.ROUND_MONEY_BIN_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.MENEHUNE_MYSTERY_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.SEVEN_CITIES_OF_CIBOLA_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.MYSTERIOUS_STONE_RAY_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.FANTASTIC_RIVER_RACE_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.MONEY_WELL_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.CHRISTMAS_IN_DUCKBURG, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.STRANGE_SHIPWRECKS_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.TWENTY_FOUR_CARAT_MOON_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.PAUL_BUNYAN_MACHINE_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.ALL_AT_SEA, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.TREE_TRICK, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.BILLIONS_IN_THE_HOLE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.GIFT_LION, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.DEEP_DOWN_DOINGS, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.UNSAFE_SAFE_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.TRICKY_EXPERIMENT, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.STATUS_SEEKER_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.CASE_OF_THE_STICKY_MONEY_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.ISLE_OF_GOLDEN_GEESE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.HOW_GREEN_WAS_MY_LETTUCE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.GIANT_ROBOT_ROBBERS_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.HOUSE_OF_HAUNTS, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.HEEDLESS_HORSEMAN_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.DOOM_DIAMOND_THE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.MR_PRIVATE_EYE, []))
BARKS_TAGS[Tags.BEAGLE_BOYS].append((Titles.DELIVERY_DILEMMA, []))

BARKS_TAGS[Tags.GENERAL_SNOZZIE].append((Titles.PHANTOM_OF_NOTRE_DUCK_THE, []))
BARKS_TAGS[Tags.GENERAL_SNOZZIE].append((Titles.DODGING_MISS_DAISY, []))
BARKS_TAGS[Tags.GENERAL_SNOZZIE].append((Titles.BLACK_FOREST_RESCUE_THE, []))
BARKS_TAGS[Tags.GENERAL_SNOZZIE].append((Titles.HOUND_HOUNDER, []))
BARKS_TAGS[Tags.GENERAL_SNOZZIE].append((Titles.MEDALING_AROUND, []))
BARKS_TAGS[Tags.GENERAL_SNOZZIE].append((Titles.BEACH_BOY, []))
BARKS_TAGS[Tags.GENERAL_SNOZZIE].append((Titles.DUCK_OUT_OF_LUCK, []))

BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.YOU_CANT_GUESS, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.SECRET_OF_HONDORICA, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.RACE_TO_THE_SOUTH_SEAS, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.LUCK_OF_THE_NORTH, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.TRAIL_OF_THE_UNICORN, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.CHRISTMAS_FOR_SHACKTOWN_A, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GILDED_MAN_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.LOST_RABBIT_FOOT_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.BEAR_TAMER_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GOING_TO_PIECES, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.KITTY_GO_ROUND, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GOLDEN_NUGGET_BOAT_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.SEEING_IS_BELIEVING, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.BILLION_DOLLAR_SAFARI_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.WINTERTIME_WAGER, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GLADSTONE_RETURNS, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.LINKS_HIJINKS, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.RIVAL_BEACHCOMBERS, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GOLDILOCKS_GAMBIT_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.DONALDS_LOVE_LETTERS, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.WILD_ABOUT_FLOWERS, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.FINANCIAL_FABLE_A, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.KNIGHTLY_RIVALS, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GLADSTONES_LUCK, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GLADSTONES_USUAL_VERY_GOOD_YEAR, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GLADSTONES_TERRIBLE_SECRET, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GEMSTONE_HUNTERS, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.CHARITABLE_CHORE_A, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.MY_LUCKY_VALENTINE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.EASTER_ELECTION_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.SOME_HEIR_OVER_THE_RAINBOW, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.MASTER_RAINMAKER_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.RAFFLE_REVERSAL, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.SALMON_DERBY, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.DAFFY_TAFFY_PULL_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.GOOD_CANOES_AND_BAD_CANOES, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.SEARCHING_FOR_A_SUCCESSOR, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.RED_APPLE_SAP, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.TENDERFOOT_TRAP_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.CODE_OF_DUCKBURG_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.ROCKET_RACE_AROUND_THE_WORLD, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.MOCKING_BIRD_RIDGE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.DRAMATIC_DONALD, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.BEACHCOMBERS_PICNIC_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.LOVELORN_FIREMAN_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.TURKEY_TROUBLE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.DUCK_LUCK, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.JINXED_JALOPY_RACE_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.DUCKBURG_PET_PARADE_THE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.HERO_OF_THE_DIKE, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.DUCK_OUT_OF_LUCK, []))
BARKS_TAGS[Tags.GLADSTONE_GANDER].append((Titles.NOT_SO_ANCIENT_MARINER_THE, []))

BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.GRANDMAS_PRESENT, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.HOBBLIN_GOBLINS, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.FORBIDIUM_MONEY_BIN_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.AUGUST_ACCIDENT, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.WEATHER_WATCHERS_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.GAB_MUFFER_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.STUBBORN_STORK_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.MILKTIME_MELODIES, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.LOST_RABBIT_FOOT_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.BIRD_CAMERA_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.ODD_ORDER_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.CALL_OF_THE_WILD_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.CAVE_OF_THE_WINDS, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.MIXED_UP_MIXER, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.MADBALL_PITCHER_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.BEAR_TAMER_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.TALE_OF_THE_TAPE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.HIS_SHINING_HOUR, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.PICNIC, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.SEVEN_CITIES_OF_CIBOLA_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.HEIRLOOM_WATCH, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.TRAPPED_LIGHTNING, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.INVENTOR_OF_ANYTHING, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.CAT_BOX_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.FORECASTING_FOLLIES, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.FISHING_MYSTERY, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.SURE_FIRE_GOLD_FINDER_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.GYRO_BUILDS_A_BETTER_HOUSE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.ROSCOE_THE_ROBOT, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.GETTING_THOR, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.KNOW_IT_ALL_MACHINE_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.GYRO_GOES_FOR_A_DIP, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.HOUSE_ON_CYCLONE_HILL_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.WISHING_WELL_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.KRANKENSTEIN_GYRO, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.FIREFLY_TRACKER_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.INVENTORS_CONTEST_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.OODLES_OF_OOMPH, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.WAR_PAINT, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.FISHY_WARDEN, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.THAT_SMALL_FEELING, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.YOU_CANT_WIN, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.WILY_RIVAL, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.FAST_AWAY_CASTAWAY, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.DUCKBURGS_DAY_OF_PERIL, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.GREAT_POP_UP_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.MADCAP_INVENTORS, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.FINNY_FUN, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.POSTHASTY_POSTMAN, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.SNOW_DUSTER, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.HELPERS_HELPING_HAND_A, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.MAN_VERSUS_MACHINE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.JONAH_GYRO, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.GLADSTONES_TERRIBLE_SECRET, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.THINK_BOX_BOLLIX_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.TALKING_DOG_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.WORM_WEARY, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.TOO_SAFE_SAFE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.SMOKE_WRITER_IN_THE_SKY, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.GYROS_IMAGINATION_INVENTION, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.DAY_DUCKBURG_GOT_DYED_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.ROCKET_RACE_AROUND_THE_WORLD, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.BLACK_WEDNESDAY, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.KNIGHTS_OF_THE_FLYING_SLEDS, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.VILLAGE_BLACKSMITH_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.BALLOONATICS, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.MISSILE_FIZZLE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.MADCAP_MARINER_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.STRANGER_THAN_FICTION, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.JET_WITCH, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.DUCKBURG_PET_PARADE_THE, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.CAPN_BLIGHTS_MYSTERY_SHIP, []))
BARKS_TAGS[Tags.GYRO_GEARLOOSE].append((Titles.FUN_WHATS_THAT, []))

BARKS_TAGS[Tags.HERBERT].append((Titles.THREE_DIRTY_LITTLE_DUCKS, []))
BARKS_TAGS[Tags.HERBERT].append((Titles.TEN_CENTS_WORTH_OF_TROUBLE, []))
BARKS_TAGS[Tags.HERBERT].append((Titles.SMUGSNORKLE_SQUATTIE_THE, []))

BARKS_TAGS[Tags.MAGICA_DE_SPELL].append((Titles.MIDAS_TOUCH_THE, []))
BARKS_TAGS[Tags.MAGICA_DE_SPELL].append((Titles.UNSAFE_SAFE_THE, []))
BARKS_TAGS[Tags.MAGICA_DE_SPELL].append((Titles.ODDBALL_ODYSSEY, []))
BARKS_TAGS[Tags.MAGICA_DE_SPELL].append((Titles.FOR_OLD_DIMES_SAKE, []))
BARKS_TAGS[Tags.MAGICA_DE_SPELL].append((Titles.ISLE_OF_GOLDEN_GEESE, []))
BARKS_TAGS[Tags.MAGICA_DE_SPELL].append((Titles.MANY_FACES_OF_MAGICA_DE_SPELL_THE, []))
BARKS_TAGS[Tags.MAGICA_DE_SPELL].append((Titles.RUG_RIDERS_IN_THE_SKY, []))
BARKS_TAGS[Tags.MAGICA_DE_SPELL].append((Titles.TEN_CENT_VALENTINE, []))
BARKS_TAGS[Tags.MAGICA_DE_SPELL].append((Titles.RAVEN_MAD, []))

BARKS_TAGS[Tags.NEIGHBOR_JONES].append((Titles.GOOD_DEEDS, []))
BARKS_TAGS[Tags.NEIGHBOR_JONES].append((Titles.GOOD_NEIGHBORS, []))
BARKS_TAGS[Tags.NEIGHBOR_JONES].append((Titles.PURLOINED_PUTTY_THE, []))
BARKS_TAGS[Tags.NEIGHBOR_JONES].append((Titles.TEN_DOLLAR_DITHER, []))
BARKS_TAGS[Tags.NEIGHBOR_JONES].append((Titles.GOOD_DEEDS_THE, []))
BARKS_TAGS[Tags.NEIGHBOR_JONES].append((Titles.FEUD_AND_FAR_BETWEEN, []))
BARKS_TAGS[Tags.NEIGHBOR_JONES].append((Titles.UNFRIENDLY_ENEMIES, []))
