from dataclasses import dataclass
from datetime import date
from enum import IntEnum, auto, verify, CONTINUOUS, UNIQUE
from typing import List

from .comic_issues import (
    SHORT_ISSUE_NAME,
    CH,
    CID,
    CP,
    CS,
    DD,
    FC,
    FG,
    KI,
    MC,
    MMA,
    SF,
    US,
    USGTD,
    VP,
)

NUM_TITLES = 601

ADVENTURE_DOWN_UNDER = "Adventure Down Under"
ALL_AT_SEA = "All at Sea"
ALL_CHOKED_UP = "All Choked Up"
ALL_SEASON_HAT = "All Season Hat"
APRIL_FOOLERS_THE = "The April Foolers"
ARMORED_RESCUE = "Armored Rescue"
ART_APPRECIATION = "Art Appreciation"
ART_OF_SECURITY_THE = "The Art of Security"
ATTIC_ANTICS = "Attic Antics"
AUGUST_ACCIDENT = "August Accident"
AWASH_IN_SUCCESS = "Awash in Success"
BACKYARD_BONANZA = "Backyard Bonanza"
BACK_TO_LONG_AGO = "Back to Long Ago!"
BACK_TO_THE_KLONDIKE = "Back to the Klondike"
BALLET_EVASIONS = "Ballet Evasions"
BALLOONATICS = "Balloonatics"
BALMY_SWAMI_THE = "The Balmy Swami"
BARBER_COLLEGE = "Barber College"
BEACHCOMBERS_PICNIC_THE = "The Beachcombers' Picnic"
BEACH_BOY = "Beach Boy"
BEAN_TAKEN = "Bean Taken"
BEAUTY_BUSINESS_THE = "The Beauty Business"
BEE_BUMBLES = "Bee Bumbles"
BEST_LAID_PLANS = "Best Laid Plans"
BICEPS_BLUES = "Biceps Blues"
BIGGER_THE_BEGGAR_THE = "The Bigger the Beggar"
BIG_BIN_ON_KILLMOTOR_HILL_THE = "The Big Bin on Killmotor Hill"
BIG_BOBBER_THE = "The Big Bobber"
BIG_TOP_BEDLAM = "Big-Top Bedlam"
BILLIONS_IN_THE_HOLE = "Billions in the Hole"
BILLIONS_TO_SNEEZE_AT = "Billions to Sneeze At"
BILLION_DOLLAR_SAFARI_THE = "The Billion Dollar Safari"
BILL_COLLECTORS_THE = "The Bill Collectors"
BILL_WIND = "Bill Wind"
BIRD_WATCHING = "Bird Watching"
BLACK_FOREST_RESCUE_THE = "The Black Forest Rescue"
BLACK_PEARLS_OF_TABU_YAMA_THE = "The Black Pearls of Tabu Yama"
BLACK_WEDNESDAY = "Black Wednesday"
BLANKET_INVESTMENT = "Blanket Investment"
BOAT_BUSTER = "Boat Buster"
BONGO_ON_THE_CONGO = "Bongo on the Congo"
BORDERLINE_HERO = "Borderline Hero"
BOXED_IN = "Boxed-In"
BUBBLEWEIGHT_CHAMP = "Bubbleweight Champ"
BUFFO_OR_BUST = "Buffo or Bust"
BUM_STEER = "Bum Steer"
CAMERA_CRAZY = "Camera Crazy"
CAMPAIGN_OF_NOTE_A = "A Campaign of Note"
CAMPING_CONFUSION = "Camping Confusion"
CAMP_COUNSELOR = "Camp Counselor"
CANDY_KID_THE = "The Candy Kid"
CANTANKEROUS_CAT_THE = "The Cantankerous Cat"
CAPN_BLIGHTS_MYSTERY_SHIP = "Cap'n Blight's Mystery Ship"
CASE_OF_THE_STICKY_MONEY_THE = "The Case of the Sticky Money"
CASH_ON_THE_BRAIN = "Cash on the Brain"
CAST_OF_THOUSANDS = "Cast of Thousands"
CATTLE_KING_THE = "The Cattle King"
CAT_BOX_THE = "The Cat Box"
CAVE_OF_ALI_BABA = "Cave of Ali Baba"
CHARITABLE_CHORE_A = "A Charitable Chore"
CHEAPEST_WEIGH_THE = "The Cheapest Weigh"
CHECKER_GAME_THE = "The Checker Game"
CHELTENHAMS_CHOICE = "Cheltenham's Choice"
CHICKADEE_CHALLENGE_THE = "The Chickadee Challenge"
CHINA_SHOP_SHAKEUP = "China Shop Shakeup"
CHRISTMAS_CHEERS = "Christmas Cheers"
CHRISTMAS_FOR_SHACKTOWN_A = "A Christmas for Shacktown"
CHRISTMAS_IN_DUCKBURG = "Christmas in Duckburg"
CHRISTMAS_KISS = "Christmas Kiss"
CHRISTMAS_ON_BEAR_MOUNTAIN = "Christmas on Bear Mountain"
CHUGWAGON_DERBY = "Chugwagon Derby"
CITY_OF_GOLDEN_ROOFS = "City of Golden Roofs"
CLASSY_TAXI = "Classy Taxi!"
CLOTHES_MAKE_THE_DUCK = "Clothes Make the Duck"
CODE_OF_DUCKBURG_THE = "The Code of Duckburg"
COFFEE_FOR_TWO = "Coffee for Two"
COLD_BARGAIN_A = "A Cold Bargain"
COLLECTION_DAY = "Collection Day"
COLOSSALEST_SURPRISE_QUIZ_SHOW_THE = "The Colossalest Surprise Quiz Show"
COME_AS_YOU_ARE = "Come as You are"
COURTSIDE_HEATING = "Courtside Heating"
CRAFTY_CORNER = "Crafty Corner"
CRAWLS_FOR_CASH = "Crawls for Cash"
CRAZY_QUIZ_SHOW_THE = "The Crazy Quiz Show"
CROWN_OF_THE_MAYAS = "Crown of the Mayas"
CUSTARD_GUN_THE = "The Custard Gun"
DAFFY_TAFFY_PULL_THE = "The Daffy Taffy Pull"
DANGEROUS_DISGUISE = "Dangerous Disguise"
DARKEST_AFRICA = "Darkest Africa"
DAYS_AT_THE_LAZY_K = "Days at the Lazy K"
DAY_DUCKBURG_GOT_DYED_THE = "The Day Duckburg Got Dyed"
DEEP_DECISION = "Deep Decision"
DEEP_DOWN_DOINGS = "Deep Down Doings"
DELIVERY_DILEMMA = "Delivery Dilemma"
DESCENT_INTERVAL_A = "A Descent Interval"
DIG_IT = "Dig it!"
DINER_DILEMMA = "Diner Dilemma"
DODGING_MISS_DAISY = "Dodging Miss Daisy"
DOGCATCHER_DUCK = "Dogcatcher Duck"
DOGGED_DETERMINATION = "Dogged Determination"
DOG_SITTER_THE = "The Dog-sitter"
DONALDS_BAY_LOT = "Donald's Bay Lot"
DONALDS_GRANDMA_DUCK = "Donald's Grandma Duck"
DONALDS_LOVE_LETTERS = "Donald's Love Letters"
DONALDS_MONSTER_KITE = "Donald's Monster Kite"
DONALDS_PET_SERVICE = "Donald's Pet Service"
DONALDS_POSY_PATCH = "Donald's Posy Patch"
DONALDS_RAUCOUS_ROLE = "Donald's Raucous Role"
DONALD_DUCKS_ATOM_BOMB = "Donald Duck's Atom Bomb"
DONALD_DUCKS_BEST_CHRISTMAS = "Donald Duck's Best Christmas"
DONALD_DUCKS_WORST_NIGHTMARE = "Donald Duck's Worst Nightmare"
DONALD_DUCK_AND_THE_MUMMYS_RING = "Donald Duck and the Mummy's Ring"
DONALD_DUCK_FINDS_PIRATE_GOLD = "Donald Duck Finds Pirate Gold"
DONALD_DUCK_TELLS_ABOUT_KITES = "Donald Duck Tells About Kites"
DONALD_MINES_HIS_OWN_BUSINESS = "Donald Mines His Own Business"
DONALD_OF_THE_COAST_GUARD = "Donald of the Coast Guard"
DONALD_TAMES_HIS_TEMPER = "Donald Tames His Temper"
DOOM_DIAMOND_THE = "The Doom Diamond"
DOUBLE_MASQUERADE = "Double Masquerade"
DOUGHNUT_DARE = "Doughnut Dare"
DOWN_FOR_THE_COUNT = "Down for the Count"
DOWSING_DUCKS = "Dowsing Ducks"
DRAMATIC_DONALD = "Dramatic Donald"
DUCKBURGS_DAY_OF_PERIL = "Duckburg's Day of Peril"
DUCKBURG_PET_PARADE_THE = "The Duckburg Pet Parade"
DUCKS_EYE_VIEW_OF_EUROPE_A = "A Duck's-eye View of Europe"
DUCK_IN_THE_IRON_PANTS_THE = "The Duck in the Iron Pants"
DUCK_LUCK = "Duck Luck"
DUCK_OUT_OF_LUCK = "Duck Out of Luck"
DUELING_TYCOONS = "Dueling Tycoons"
EARLY_TO_BUILD = "Early to Build"
EASTER_ELECTION_THE = "The Easter Election"
EASY_MOWING = "Easy Mowing"
EYES_HAVE_IT_THE = "The Eyes Have It"
EYES_IN_THE_DARK = "Eyes in the Dark"
FABULOUS_PHILOSOPHERS_STONE_THE = "The Fabulous Philosopher's Stone"
FABULOUS_TYCOON_THE = "The Fabulous Tycoon"
FANTASTIC_RIVER_RACE_THE = "The Fantastic River Race"
FARE_DELAY = "Fare Delay"
FARRAGUT_THE_FALCON = "Farragut the Falcon"
FASHION_FORECAST = "Fashion Forecast"
FASHION_IN_FLIGHT = "Fashion in Flight"
FAST_AWAY_CASTAWAY = "Fast Away Castaway"
FAULTY_FORTUNE = "Faulty Fortune"
FEARSOME_FLOWERS = "Fearsome Flowers"
FERTILE_ASSETS = "Fertile Assets"
FETCHING_PRICE_A = "A Fetching Price"
FEUD_AND_FAR_BETWEEN = "Feud and Far Between"
FINANCIAL_FABLE_A = "A Financial Fable"
FINNY_FUN = "Finny Fun"
FIREBUG_THE = "The Firebug"
FIREFLIES_ARE_FREE = "Fireflies are Free"
FIREFLY_TRACKER_THE = "The Firefly Tracker"
FIREMAN_DONALD = "Fireman Donald"
FIREMAN_SCROOGE = "Fireman Scrooge"
FISHING_MYSTERY = "Fishing Mystery"
FISHY_WARDEN = "Fishy Warden"
FIX_UP_MIX_UP = "Fix-up Mix-up"
FLIP_DECISION = "Flip Decision"
FLOATING_ISLAND_THE = "The Floating Island"
FLOUR_FOLLIES = "Flour Follies"
FLOWERS_ARE_FLOWERS = "Flowers Are Flowers"
FLYING_DUTCHMAN_THE = "The Flying Dutchman"
FLYING_FARMHAND_THE = "The Flying Farmhand"
FOLLOW_THE_RAINBOW = "Follow the Rainbow"
FORBIDDEN_VALLEY = "Forbidden Valley"
FORECASTING_FOLLIES = "Forecasting Follies"
FORGOTTEN_PRECAUTION = "Forgotten Precaution"
FOR_OLD_DIMES_SAKE = "For Old Dime's Sake"
FOXY_RELATIONS = "Foxy Relations"
FRACTIOUS_FUN = "Fractious Fun"
FRAIDY_FALCON_THE = "The Fraidy Falcon"
FRIGHTFUL_FACE = "Frightful Face"
FROGGY_FARMER = "Froggy Farmer"
FROZEN_GOLD = "Frozen Gold"
FULL_SERVICE_WINDOWS = "Full-Service Windows"
GALL_OF_THE_WILD = "Gall of the Wild"
GEMSTONE_HUNTERS = "Gemstone Hunters"
GENUINE_ARTICLE_THE = "The Genuine Article"
GETTING_THE_BIRD = "Getting the Bird"
GETTING_THOR = "Getting Thor"
GHOST_OF_THE_GROTTO_THE = "The Ghost of the Grotto"
GHOST_SHERIFF_OF_LAST_GASP_THE = "The Ghost Sheriff of Last Gasp"
GIANT_ROBOT_ROBBERS_THE = "The Giant Robot Robbers"
GIFT_LION = "Gift Lion"
GILDED_MAN_THE = "The Gilded Man"
GLADSTONES_LUCK = "Gladstone's Luck"
GLADSTONES_TERRIBLE_SECRET = "Gladstone's Terrible Secret"
GLADSTONES_USUAL_VERY_GOOD_YEAR = "Gladstone's Usual Very Good Year"
GLADSTONE_RETURNS = "Gladstone Returns"
GOING_APE = "Going Ape"
GOING_BUGGY = "Going Buggy"
GOING_TO_PIECES = "Going to Pieces"
GOLDEN_CHRISTMAS_TREE_THE = "The Golden Christmas Tree"
GOLDEN_FLEECING_THE = "The Golden Fleecing"
GOLDEN_HELMET_THE = "The Golden Helmet"
GOLDEN_NUGGET_BOAT_THE = "The Golden Nugget Boat"
GOLDEN_RIVER_THE = "The Golden River"
GOLDILOCKS_GAMBIT_THE = "The Goldilocks Gambit"
GOLD_FINDER_THE = "The Gold-Finder"
GOLD_RUSH = "Gold Rush"
GOOD_CANOES_AND_BAD_CANOES = "Good Canoes and Bad Canoes"
GOOD_DEEDS = "Good Deeds"
GOOD_DEEDS_THE = "The Good Deeds"
GOOD_NEIGHBORS = "Good Neighbors"
GOPHER_GOOF_UPS = "Gopher Goof-Ups"
GRANDMAS_PRESENT = "Grandma's Present"
GREAT_DUCKBURG_FROG_JUMPING_CONTEST_THE = "The Great Duckburg Frog-Jumping Contest"
GREAT_POP_UP_THE = "The Great Pop Up"
GREAT_SKI_RACE_THE = "The Great Ski Race"
GREAT_STEAMBOAT_RACE_THE = "The Great Steamboat Race"
GREAT_WIG_MYSTERY_THE = "The Great Wig Mystery"
GYROS_IMAGINATION_INVENTION = "Gyro's Imagination Invention"
GYRO_BUILDS_A_BETTER_HOUSE = "Gyro Builds a Better House"
GYRO_GOES_FOR_A_DIP = "Gyro Goes for a Dip"
HALF_BAKED_BAKER_THE = "The Half-Baked Baker"
HALL_OF_THE_MERMAID_QUEEN = "Hall of the Mermaid Queen"
HAMMY_CAMEL_THE = "The Hammy Camel"
HARD_LOSER_THE = "The Hard Loser"
HAVE_GUN_WILL_DANCE = "Have Gun, Will Dance"
HEEDLESS_HORSEMAN_THE = "The Heedless Horseman"
HEIRLOOM_WATCH = "Heirloom Watch"
HELPERS_HELPING_HAND_A = "A Helper's Helping Hand"
HERO_OF_THE_DIKE = "Hero of the Dike"
HIGH_RIDER = "High Rider"
HIGH_WIRE_DAREDEVILS = "High-wire Daredevils"
HISTORY_TOSSED = "History Tossed"
HIS_HANDY_ANDY = "His Handy Andy"
HOBBLIN_GOBLINS = "Hobblin' Goblins"
HONEY_OF_A_HEN_A = "A Honey of a Hen"
HORSERADISH_STORY_THE = "The Horseradish Story"
HORSESHOE_LUCK = "Horseshoe Luck"
HOSPITALITY_WEEK = "Hospitality Week"
HOUND_HOUNDER = "Hound Hounder"
HOUND_OF_THE_WHISKERVILLES = "Hound of the Whiskervilles"
HOUSEBOAT_HOLIDAY = "Houseboat Holiday"
HOUSE_OF_HAUNTS = "House of Haunts"
HOUSE_ON_CYCLONE_HILL_THE = "The House on Cyclone Hill"
HOW_GREEN_WAS_MY_LETTUCE = "How Green Was My Lettuce"
HYPNO_GUN_THE = "The Hypno-Gun"
ICEBOAT_TO_BEAVER_ISLAND = "Iceboat to Beaver Island"
ICEBOX_ROBBER_THE = "The Icebox Robber"
ICE_TAXIS_THE = "The Ice Taxis"
IF_THE_HAT_FITS = "If the Hat Fits"
IMMOVABLE_MISER = "Immovable Miser"
INSTANT_HERCULES = "Instant Hercules"
INTERPLANETARY_POSTMAN = "Interplanetary Postman"
INVENTORS_CONTEST_THE = "The Inventors' Contest"
INVENTOR_OF_ANYTHING = "Inventor of Anything"
INVISIBLE_INTRUDER_THE = "The Invisible Intruder"
IN_ANCIENT_PERSIA = "In Ancient Persia"
IN_KAKIMAW_COUNTRY = "In Kakimaw Country"
IN_OLD_CALIFORNIA = "In Old California!"
IN_THE_SWIM = "In the Swim"
ISLAND_IN_THE_SKY = "Island in the Sky"
ISLE_OF_GOLDEN_GEESE = "Isle of Golden Geese"
ITCHING_TO_SHARE = "Itching to Share"
IT_HAPPENED_ONE_WINTER = "It Happened One Winter"
JAM_ROBBERS = "Jam Robbers"
JET_RESCUE = "Jet Rescue"
JET_WITCH = "Jet Witch"
JINXED_JALOPY_RACE_THE = "The Jinxed Jalopy Race"
JONAH_GYRO = "Jonah Gyro"
JUMPING_TO_CONCLUSIONS = "Jumping to Conclusions"
JUNGLE_BUNGLE = "Jungle Bungle"
JUNGLE_HI_JINKS = "Jungle Hi-Jinks"
KING_SCROOGE_THE_FIRST = "King Scrooge the First"
KING_SIZE_CONE = "King-Size Cone"
KITE_WEATHER = "Kite Weather"
KITTY_GO_ROUND = "Kitty-Go-Round"
KNIGHTLY_RIVALS = "Knightly Rivals"
KNIGHTS_OF_THE_FLYING_SLEDS = "Knights of the Flying Sleds"
KNIGHT_IN_SHINING_ARMOR = "Knight in Shining Armor"
KNOW_IT_ALL_MACHINE_THE = "The Know-It-All Machine"
KRANKENSTEIN_GYRO = "Krankenstein Gyro"
LAND_BENEATH_THE_GROUND = "Land Beneath the Ground!"
LAND_OF_THE_PYGMY_INDIANS = "Land of the Pygmy Indians"
LAND_OF_THE_TOTEM_POLES = "Land of the Totem Poles"
LAUNDRY_FOR_LESS = "Laundry for Less"
LEMMING_WITH_THE_LOCKET_THE = "The Lemming with the Locket"
LEMONADE_FLING_THE = "The Lemonade Fling"
LETTER_TO_SANTA = "Letter to Santa"
LIFEGUARD_DAZE = "Lifeguard Daze"
LIGHTS_OUT = "Lights Out"
LIMBER_W_GUEST_RANCH_THE = "The Limber W. Guest Ranch"
LINKS_HIJINKS = "Links Hijinks"
LITTLEST_CHICKEN_THIEF_THE = "The Littlest Chicken Thief"
LOCK_OUT_THE = "The Lock Out"
LOG_JOCKEY = "Log Jockey"
LONG_DISTANCE_COLLISION = "Long Distance Collision"
LONG_RACE_TO_PUMPKINBURG_THE = "The Long Race to Pumpkinburg"
LOONY_LUNAR_GOLD_RUSH_THE = "The Loony Lunar Gold Rush"
LOSING_FACE = "Losing Face"
LOST_BENEATH_THE_SEA = "Lost Beneath the Sea"
LOST_CROWN_OF_GENGHIS_KHAN_THE = "The Lost Crown of Genghis Khan!"
LOST_FRONTIER = "Lost Frontier"
LOST_IN_THE_ANDES = "Lost in the Andes!"
LOST_PEG_LEG_MINE_THE = "The Lost Peg Leg Mine"
LOVELORN_FIREMAN_THE = "The Lovelorn Fireman"
LUCK_OF_THE_NORTH = "Luck of the North"
LUNCHEON_LAMENT = "Luncheon Lament"
MACHINE_MIX_UP = "Machine Mix-Up"
MADCAP_INVENTORS = "Madcap Inventors"
MADCAP_MARINER_THE = "The Madcap Mariner"
MAD_CHEMIST_THE = "The Mad Chemist"
MAGICAL_MISERY = "Magical Misery"
MAGIC_HOURGLASS_THE = "The Magic Hourglass"
MAGIC_INK_THE = "The Magic Ink"
MAHARAJAH_DONALD = "Maharajah Donald"
MANAGING_THE_ECHO_SYSTEM = "Managing the Echo System"
MANY_FACES_OF_MAGICA_DE_SPELL_THE = "The Many Faces of Magica de Spell"
MAN_VERSUS_MACHINE = "Man Versus Machine"
MASTERS_OF_MELODY_THE = "The Masters of Melody"
MASTER_GLASSER_THE = "The Master Glasser"
MASTER_ICE_FISHER = "Master Ice Fisher"
MASTER_MOVER_THE = "The Master Mover"
MASTER_RAINMAKER_THE = "The Master Rainmaker"
MASTER_THE = "The Master"
MASTER_WRECKER = "Master Wrecker"
MATINEE_MADNESS = "Matinee Madness"
MATTER_OF_FACTORY_A = "A Matter of Factory"
MCDUCK_OF_ARABIA = "McDuck of Arabia"
MCDUCK_TAKES_A_DIVE = "McDuck Takes a Dive"
MEDALING_AROUND = "Medaling Around"
MENEHUNE_MYSTERY_THE = "The Menehune Mystery"
MENTAL_FEE = "Mental Fee"
MERRY_FERRY = "Merry Ferry"
MICRO_DUCKS_FROM_OUTER_SPACE = "Micro-Ducks from Outer Space"
MIDAS_TOUCH_THE = "The Midas Touch"
MIDGETS_MADNESS = "Midgets Madness"
MIGHTY_TRAPPER_THE = "The Mighty Trapper"
MIGRATING_MILLIONS = "Migrating Millions"
MILKMAN_THE = "The Milkman"
MILLION_DOLLAR_PIGEON = "Million Dollar Pigeon"
MILLION_DOLLAR_SHOWER = "Million-Dollar Shower"
MINES_OF_KING_SOLOMON_THE = "The Mines of King Solomon"
MISSILE_FIZZLE = "Missile Fizzle"
MOCKING_BIRD_RIDGE = "Mocking Bird Ridge"
MONEY_BAG_GOAT = "Money Bag Goat"
MONEY_CHAMP_THE = "The Money Champ"
MONEY_HAT_THE = "The Money Hat"
MONEY_LADDER_THE = "The Money Ladder"
MONEY_STAIRS_THE = "The Money Stairs"
MONEY_WELL_THE = "The Money Well"
MONKEY_BUSINESS = "Monkey Business"
MOOLA_ON_THE_MOVE = "Moola on the Move"
MOVIE_MAD = "Movie Mad"
MR_PRIVATE_EYE = "Mr. Private Eye"
MUCH_ADO_ABOUT_QUACKLY_HALL = "Much Ado about Quackly Hall"
MUCH_LUCK_MCDUCK = "Much Luck McDuck"
MUSH = "Mush!"
MYSTERIOUS_STONE_RAY_THE = "The Mysterious Stone Ray"
MYSTERY_OF_THE_GHOST_TOWN_RAILROAD = "Mystery of the Ghost Town Railroad"
MYSTERY_OF_THE_LOCH = "Mystery of the Loch"
MYSTERY_OF_THE_SWAMP = "Mystery of the Swamp"
MYTHTIC_MYSTERY = "Mythtic Mystery"
MY_LUCKY_VALENTINE = "My Lucky Valentine"
NEST_EGG_COLLECTOR = "Nest Egg Collector"
NET_WORTH = "Net Worth"
NEW_TOYS = "New Toys"
NEW_YEARS_REVOLUTIONS = "New Year's Revolutions"
NOBLE_PORPOISES = "Noble Porpoises"
NOISE_NULLIFIER = "Noise Nullifier"
NORTHEASTER_ON_CAPE_QUACK = "Northeaster on Cape Quack"
NORTH_OF_THE_YUKON = "North of the Yukon"
NOT_SO_ANCIENT_MARINER_THE = "The Not-so-Ancient Mariner"
NO_BARGAIN = "No Bargain"
NO_NOISE_IS_GOOD_NOISE = "No Noise is Good Noise"
NO_PLACE_TO_HIDE = "No Place to Hide"
NO_SUCH_VARMINT = "No Such Varmint"
ODDBALL_ODYSSEY = "Oddball Odyssey"
OIL_THE_NEWS = "Oil the News"
OLD_CASTLES_SECRET_THE = "The Old Castle's Secret"
OLD_FROGGIE_CATAPULT = "Old Froggie Catapult"
OLYMPIAN_TORCH_BEARER_THE = "The Olympian Torch Bearer"
OLYMPIC_HOPEFUL_THE = "The Olympic Hopeful"
OMELET = "Omelet"
ONCE_UPON_A_CARNIVAL = "Once Upon a Carnival"
ONLY_A_POOR_OLD_MAN = "Only a Poor Old Man"
OODLES_OF_OOMPH = "Oodles of Oomph"
OPERATION_ST_BERNARD = "Operation St. Bernard"
ORNAMENTS_ON_THE_WAY = "Ornaments on the Way"
OSOGOOD_SILVER_POLISH = "Osogood Silver Polish"
OUTFOXED_FOX = "Outfoxed Fox"
PAUL_BUNYAN_MACHINE_THE = "The Paul Bunyan Machine"
PEACEFUL_HILLS_THE = "The Peaceful Hills"
PEARLS_OF_WISDOM = "Pearls of Wisdom"
PECKING_ORDER = "Pecking Order"
PERSISTENT_POSTMAN_THE = "The Persistent Postman"
PHANTOM_OF_NOTRE_DUCK_THE = "The Phantom of Notre Duck"
PICNIC = "Picnic"
PICNIC_TRICKS = "Picnic Tricks"
PIPELINE_TO_DANGER = "Pipeline to Danger"
PIXILATED_PARROT_THE = "The Pixilated Parrot"
PIZEN_SPRING_DUDE_RANCH = "Pizen Spring Dude Ranch"
PLAYIN_HOOKEY = "Playin' Hookey"
PLAYMATES = "Playmates"
PLENTY_OF_PETS = "Plenty of Pets"
PLUMMETING_WITH_PRECISION = "Plummeting with Precision"
POOL_SHARKS = "Pool Sharks"
POOR_LOSER = "Poor Loser"
POSTHASTY_POSTMAN = "Posthasty Postman"
POUND_FOR_SOUND = "Pound for Sound"
POWER_PLOWING = "Power Plowing"
PRANK_ABOVE_A = "A Prank Above"
PRICE_OF_FAME_THE = "The Price of Fame"
PRIZE_OF_PIZARRO_THE = "The Prize of Pizarro"
PROJECTING_DESIRES = "Projecting Desires"
PURLOINED_PUTTY_THE = "The Purloined Putty"
PYRAMID_SCHEME = "Pyramid Scheme"
QUEEN_OF_THE_WILD_DOG_PACK_THE = "The Queen of the Wild Dog Pack"
RABBITS_FOOT_THE = "The Rabbit's Foot"
RACE_TO_THE_SOUTH_SEAS = "Race to the South Seas!"
RAFFLE_REVERSAL = "Raffle Reversal"
RAGS_TO_RICHES = "Rags to Riches"
RANTS_ABOUT_ANTS = "Rants About Ants"
RAVEN_MAD = "Raven Mad"
RED_APPLE_SAP = "Red Apple Sap"
RELATIVE_REACTION = "Relative Reaction"
REMEMBER_THIS = "Remember This"
RESCUE_ENHANCEMENT = "Rescue Enhancement"
RETURN_TO_PIZEN_BLUFF = "Return to Pizen Bluff"
RICHES_RICHES_EVERYWHERE = "Riches, Riches, Everywhere!"
RIDDLE_OF_THE_RED_HAT_THE = "The Riddle of the Red Hat"
RIDING_THE_PONY_EXPRESS = "Riding the Pony Express"
RIGGED_UP_ROLLER = "Rigged-Up Roller"
RIP_VAN_DONALD = "Rip Van Donald"
RIVAL_BEACHCOMBERS = "Rival Beachcombers"
RIVAL_BOATMEN = "Rival Boatmen"
ROCKET_RACE_AROUND_THE_WORLD = "Rocket Race Around the World"
ROCKET_RACE_TO_THE_MOON = "Rocket Race to the Moon"
ROCKET_ROASTED_CHRISTMAS_TURKEY = "Rocket-Roasted Christmas Turkey"
ROCKET_WING_SAVES_THE_DAY = "Rocket Wing Saves the Day"
ROCKS_TO_RICHES = "Rocks to Riches"
ROSCOE_THE_ROBOT = "Roscoe the Robot"
ROUNDABOUT_HANDOUT = "Roundabout Handout"
ROUND_MONEY_BIN_THE = "The Round Money Bin"
RUG_RIDERS_IN_THE_SKY = "Rug Riders in the Sky"
RUNAWAY_TRAIN_THE = "The Runaway Train"
SAGMORE_SPRINGS_HOTEL = "Sagmore Springs Hotel"
SALESMAN_DONALD = "Salesman Donald"
SALMON_DERBY = "Salmon Derby"
SANTAS_STORMY_VISIT = "Santa's Stormy Visit"
SAVED_BY_THE_BAG = "Saved by the Bag!"
SCREAMING_COWBOY_THE = "The Screaming Cowboy"
SEALS_ARE_SO_SMART = "Seals Are So Smart!"
SEARCHING_FOR_A_SUCCESSOR = "Searching for a Successor"
SEARCH_FOR_THE_CUSPIDORIA = "Search for the Cuspidoria"
SECOND_RICHEST_DUCK_THE = "The Second-Richest Duck"
SECRET_BOOK_THE = "The Secret Book"
SECRET_OF_ATLANTIS_THE = "The Secret of Atlantis"
SECRET_OF_HONDORICA = "Secret of Hondorica"
SECRET_RESOLUTIONS = "Secret Resolutions"
SEEING_IS_BELIEVING = "Seeing is Believing"
SEPTEMBER_SCRIMMAGE = "September Scrimmage"
SERUM_TO_CODFISH_COVE = "Serum to Codfish Cove"
SEVEN_CITIES_OF_CIBOLA_THE = "The Seven Cities of Cibola"
SHEEPISH_COWBOYS_THE = "The Sheepish Cowboys"
SHERIFF_OF_BULLET_VALLEY = "Sheriff of Bullet Valley"
SIDEWALK_OF_THE_MIND = "Sidewalk of the Mind"
SILENT_NIGHT = "Silent Night"
SINGAPORE_JOE = "Singapore Joe"
SITTING_HIGH = "Sitting High"
SKI_LIFT_LETDOWN = "Ski Lift Letdown"
SLEEPIES_THE = "The Sleepies"
SLEEPY_SITTERS = "Sleepy Sitters"
SLIPPERY_SHINE = "Slippery Shine"
SLIPPERY_SIPPER = "Slippery Sipper"
SMASH_SUCCESS = "Smash Success"
SMOKE_WRITER_IN_THE_SKY = "Smoke Writer in the Sky"
SMUGSNORKLE_SQUATTIE_THE = "The Smugsnorkle Squattie"
SNAKE_TAKE = "Snake Take"
SNOW_DUSTER = "Snow Duster"
SNOW_FUN = "Snow Fun"
SOMETHIN_FISHY_HERE = "Somethin' Fishy Here"
SOME_HEIR_OVER_THE_RAINBOW = "Some Heir Over the Rainbow"
SORRY_TO_BE_SAFE = "Sorry to be Safe"
SOUPLINE_EIGHT = "Soupline Eight"
SO_FAR_AND_NO_SAFARI = "So Far and No Safari"
SPARE_THAT_HAIR = "Spare That Hair"
SPECIAL_DELIVERY = "Special Delivery"
SPENDING_MONEY = "Spending Money"
SPICY_TALE_A = "A Spicy Tale"
SPOIL_THE_ROD = "Spoil the Rod"
SPRING_FEVER = "Spring Fever"
STABLE_PRICES = "Stable Prices"
STALWART_RANGER = "Stalwart Ranger"
STATUESQUE_SPENDTHRIFTS = "Statuesque Spendthrifts"
STATUES_OF_LIMITATIONS = "Statues of Limitations"
STATUS_SEEKER_THE = "The Status Seeker"
STONES_THROW_FROM_GHOST_TOWN_A = "A Stone's Throw from Ghost Town"
STRANGER_THAN_FICTION = "Stranger than Fiction"
STRANGE_SHIPWRECKS_THE = "The Strange Shipwrecks"
SUNKEN_YACHT_THE = "The Sunken Yacht"
SUPER_SNOOPER = "Super Snooper"
SURE_FIRE_GOLD_FINDER_THE = "The Sure-Fire Gold Finder"
SWAMP_OF_NO_RETURN_THE = "The Swamp of No Return"
SWEAT_DEAL_A = "A Sweat Deal"
SWIMMING_SWINDLERS = "Swimming Swindlers"
TALKING_DOG_THE = "The Talking Dog"
TALKING_PARROT = "Talking Parrot"
TAMING_THE_RAPIDS = "Taming the Rapids"
TEMPER_TAMPERING = "Temper Tampering"
TENDERFOOT_TRAP_THE = "The Tenderfoot Trap"
TEN_CENTS_WORTH_OF_TROUBLE = "Ten Cents' Worth of Trouble"
TEN_CENT_VALENTINE = "Ten-Cent Valentine"
TEN_DOLLAR_DITHER = "Ten-Dollar Dither"
TEN_STAR_GENERALS = "Ten-Star Generals"
TERRIBLE_TOURIST = "Terrible Tourist"
TERRIBLE_TURKEY_THE = "The Terrible Turkey"
TERROR_OF_THE_BEAGLE_BOYS = "Terror of the Beagle Boys"
TERROR_OF_THE_RIVER_THE = "The Terror of the River!!"
THATS_NO_FABLE = "That's No Fable!"
THAT_SINKING_FEELING = "That Sinking Feeling"
THAT_SMALL_FEELING = "That Small Feeling"
THIEVERY_AFOOT = "Thievery Afoot"
THINK_BOX_BOLLIX_THE = "The Think Box Bollix"
THREE_DIRTY_LITTLE_DUCKS = "Three Dirty Little Ducks"
THREE_GOOD_LITTLE_DUCKS = "Three Good Little Ducks"
THREE_UN_DUCKS = "Three Un-Ducks"
THRIFTY_SPENDTHRIFT_THE = "The Thrifty Spendthrift"
THRIFT_GIFT_A = "A Thrift Gift"
THUG_BUSTERS = "Thug Busters"
THUMBS_UP = "Thumbs Up"
TICKING_DETECTOR = "Ticking Detector"
TIED_DOWN_TOOLS = "Tied-Down Tools"
TITANIC_ANTS_THE = "The Titanic Ants!"
TOASTY_TOYS = "Toasty Toys"
TOO_FIT_TO_FIT = "Too Fit to Fit"
TOO_MANY_PETS = "Too Many Pets"
TOO_SAFE_SAFE = "Too Safe Safe"
TOP_WAGES = "Top Wages"
TOYLAND = "Toyland"
TRACKING_SANDY = "Tracking Sandy"
TRAIL_OF_THE_UNICORN = "Trail of the Unicorn"
TRALLA_LA = "Tralla La"
TRAMP_STEAMER_THE = "The Tramp Steamer"
TRAPPED_LIGHTNING = "Trapped Lightning"
TRAVELLING_TRUANTS = "Travelling Truants"
TRAVEL_TIGHTWAD_THE = "The Travel Tightwad"
TREASURE_OF_MARCO_POLO = "Treasure of Marco Polo"
TREEING_OFF = "Treeing Off"
TREE_TRICK = "Tree Trick"
TRICKY_EXPERIMENT = "Tricky Experiment"
TRICK_OR_TREAT = "Trick or Treat"
TROUBLE_INDEMNITY = "Trouble Indemnity"
TROUBLE_WITH_DIMES_THE = "The Trouble With Dimes"
TRUANT_NEPHEWS_THE = "The Truant Nephews"
TRUANT_OFFICER_DONALD = "Truant Officer Donald"
TRUE_TEST_THE = "The True Test"
TUCKERED_TIGER_THE = "The Tuckered Tiger"
TUNNEL_VISION = "Tunnel Vision"
TURKEY_RAFFLE = "Turkey Raffle"
TURKEY_TROT_AT_ONE_WHISTLE = "Turkey Trot at One Whistle"
TURKEY_TROUBLE = "Turkey Trouble"
TURKEY_WITH_ALL_THE_SCHEMINGS = "Turkey with All the Schemings"
TURN_FOR_THE_WORSE = "Turn for the Worse"
TWENTY_FOUR_CARAT_MOON_THE = "The Twenty-four Carat Moon"
TWO_WAY_LUCK = "Two-Way Luck"
UNCLE_SCROOGE___MONKEY_BUSINESS = "Uncle Scrooge - Monkey Business"
UNDER_THE_POLAR_ICE = "Under the Polar Ice"
UNFRIENDLY_ENEMIES = "Unfriendly Enemies"
UNORTHODOX_OX_THE = "The Unorthodox Ox"
UNSAFE_SAFE_THE = "The Unsafe Safe"
UP_AND_AT_IT = "Up and at It"
VACATION_MISERY = "Vacation Misery"
VACATION_TIME = "Vacation Time"
VICTORY_GARDEN_THE = "The Victory Garden"
VILLAGE_BLACKSMITH_THE = "The Village Blacksmith"
VOLCANO_VALLEY = "Volcano Valley"
VOODOO_HOODOO = "Voodoo Hoodoo"
WALTZ_KING_THE = "The Waltz King"
WANT_TO_BUY_AN_ISLAND = "Want to Buy an Island?"
WAR_PAINT = "War Paint"
WASTED_WORDS = "Wasted Words"
WATCHFUL_PARENTS_THE = "The Watchful Parents"
WATCHING_THE_WATCHMAN = "Watching the Watchman"
WATER_SKI_RACE = "Water Ski Race"
WATT_AN_OCCASION = "Watt an Occasion"
WAX_MUSEUM_THE = "The Wax Museum"
WAY_OUT_YONDER = "Way Out Yonder"
WEATHER_WATCHERS_THE = "The Weather Watchers"
WEBFOOTED_WRANGLER = "Webfooted Wrangler"
WHALE_OF_A_STORY_A = "A Whale of a Story"
WILD_ABOUT_FLOWERS = "Wild about Flowers"
WILY_RIVAL = "Wily Rival"
WINDFALL_OF_THE_MIND = "Windfall of the Mind"
WINDY_STORY_THE = "The Windy Story"
WINTERTIME_WAGER = "Wintertime Wager"
WIRED = "Wired"
WISHFUL_EXCESS = "Wishful Excess"
WISHING_STONE_ISLAND = "Wishing Stone Island"
WISHING_WELL_THE = "The Wishing Well"
WISPY_WILLIE = "Wispy Willie"
WITCHING_STICK_THE = "The Witching Stick"
WORM_WEARY = "Worm Weary"
WRONG_NUMBER = "Wrong Number"
YOICKS_THE_FOX = "Yoicks! The Fox!"
YOU_CANT_GUESS = "You Can't Guess!"
YOU_CANT_WIN = "You Can't Win"
ZERO_HERO = "Zero Hero"


@verify(CONTINUOUS, UNIQUE)
class Titles(IntEnum):
    DONALD_DUCK_FINDS_PIRATE_GOLD = 0
    VICTORY_GARDEN_THE = auto()
    RABBITS_FOOT_THE = auto()
    LIFEGUARD_DAZE = auto()
    GOOD_DEEDS = auto()
    LIMBER_W_GUEST_RANCH_THE = auto()
    MIGHTY_TRAPPER_THE = auto()
    DONALD_DUCK_AND_THE_MUMMYS_RING = auto()
    HARD_LOSER_THE = auto()
    TOO_MANY_PETS = auto()
    GOOD_NEIGHBORS = auto()
    SALESMAN_DONALD = auto()
    SNOW_FUN = auto()
    DUCK_IN_THE_IRON_PANTS_THE = auto()
    KITE_WEATHER = auto()
    THREE_DIRTY_LITTLE_DUCKS = auto()
    MAD_CHEMIST_THE = auto()
    RIVAL_BOATMEN = auto()
    CAMERA_CRAZY = auto()
    FARRAGUT_THE_FALCON = auto()
    PURLOINED_PUTTY_THE = auto()
    HIGH_WIRE_DAREDEVILS = auto()
    TEN_CENTS_WORTH_OF_TROUBLE = auto()
    DONALDS_BAY_LOT = auto()
    FROZEN_GOLD = auto()
    THIEVERY_AFOOT = auto()
    MYSTERY_OF_THE_SWAMP = auto()
    TRAMP_STEAMER_THE = auto()
    LONG_RACE_TO_PUMPKINBURG_THE = auto()
    WEBFOOTED_WRANGLER = auto()
    ICEBOX_ROBBER_THE = auto()
    PECKING_ORDER = auto()
    TAMING_THE_RAPIDS = auto()
    EYES_IN_THE_DARK = auto()
    DAYS_AT_THE_LAZY_K = auto()
    RIDDLE_OF_THE_RED_HAT_THE = auto()
    THUG_BUSTERS = auto()
    GREAT_SKI_RACE_THE = auto()
    FIREBUG_THE = auto()
    TEN_DOLLAR_DITHER = auto()
    DONALD_DUCKS_BEST_CHRISTMAS = auto()
    SILENT_NIGHT = auto()
    DONALD_TAMES_HIS_TEMPER = auto()
    SINGAPORE_JOE = auto()
    MASTER_ICE_FISHER = auto()
    JET_RESCUE = auto()
    DONALDS_MONSTER_KITE = auto()
    TERROR_OF_THE_RIVER_THE = auto()
    SEALS_ARE_SO_SMART = auto()
    BICEPS_BLUES = auto()
    SMUGSNORKLE_SQUATTIE_THE = auto()
    SANTAS_STORMY_VISIT = auto()
    SWIMMING_SWINDLERS = auto()
    PLAYIN_HOOKEY = auto()
    GOLD_FINDER_THE = auto()
    BILL_COLLECTORS_THE = auto()
    TURKEY_RAFFLE = auto()
    MAHARAJAH_DONALD = auto()
    CANTANKEROUS_CAT_THE = auto()
    DONALD_DUCKS_ATOM_BOMB = auto()
    GOING_BUGGY = auto()
    PEACEFUL_HILLS_THE = auto()
    JAM_ROBBERS = auto()
    PICNIC_TRICKS = auto()
    VOLCANO_VALLEY = auto()
    IF_THE_HAT_FITS = auto()
    DONALDS_POSY_PATCH = auto()
    DONALD_MINES_HIS_OWN_BUSINESS = auto()
    MAGICAL_MISERY = auto()
    THREE_GOOD_LITTLE_DUCKS = auto()
    VACATION_MISERY = auto()
    ADVENTURE_DOWN_UNDER = auto()
    GHOST_OF_THE_GROTTO_THE = auto()
    WALTZ_KING_THE = auto()
    MASTERS_OF_MELODY_THE = auto()
    FIREMAN_DONALD = auto()
    CHRISTMAS_ON_BEAR_MOUNTAIN = auto()
    FASHION_IN_FLIGHT = auto()
    TURN_FOR_THE_WORSE = auto()
    MACHINE_MIX_UP = auto()
    TERRIBLE_TURKEY_THE = auto()
    WINTERTIME_WAGER = auto()
    WATCHING_THE_WATCHMAN = auto()
    DARKEST_AFRICA = auto()
    WIRED = auto()
    GOING_APE = auto()
    OLD_CASTLES_SECRET_THE = auto()
    SPOIL_THE_ROD = auto()
    BIRD_WATCHING = auto()
    HORSESHOE_LUCK = auto()
    BEAN_TAKEN = auto()
    ROCKET_RACE_TO_THE_MOON = auto()
    DONALD_OF_THE_COAST_GUARD = auto()
    GLADSTONE_RETURNS = auto()
    SHERIFF_OF_BULLET_VALLEY = auto()
    LINKS_HIJINKS = auto()
    SORRY_TO_BE_SAFE = auto()
    BEST_LAID_PLANS = auto()
    GENUINE_ARTICLE_THE = auto()
    PEARLS_OF_WISDOM = auto()
    FOXY_RELATIONS = auto()
    CRAZY_QUIZ_SHOW_THE = auto()
    GOLDEN_CHRISTMAS_TREE_THE = auto()
    TOYLAND = auto()
    JUMPING_TO_CONCLUSIONS = auto()
    TRUE_TEST_THE = auto()
    ORNAMENTS_ON_THE_WAY = auto()
    TRUANT_OFFICER_DONALD = auto()
    DONALD_DUCKS_WORST_NIGHTMARE = auto()
    PIZEN_SPRING_DUDE_RANCH = auto()
    RIVAL_BEACHCOMBERS = auto()
    LOST_IN_THE_ANDES = auto()
    TOO_FIT_TO_FIT = auto()
    TUNNEL_VISION = auto()
    SLEEPY_SITTERS = auto()
    SUNKEN_YACHT_THE = auto()
    RACE_TO_THE_SOUTH_SEAS = auto()
    MANAGING_THE_ECHO_SYSTEM = auto()
    PLENTY_OF_PETS = auto()
    VOODOO_HOODOO = auto()
    SLIPPERY_SHINE = auto()
    FRACTIOUS_FUN = auto()
    KING_SIZE_CONE = auto()
    SUPER_SNOOPER = auto()
    GREAT_DUCKBURG_FROG_JUMPING_CONTEST_THE = auto()
    DOWSING_DUCKS = auto()
    GOLDILOCKS_GAMBIT_THE = auto()
    LETTER_TO_SANTA = auto()
    NO_NOISE_IS_GOOD_NOISE = auto()
    LUCK_OF_THE_NORTH = auto()
    NEW_TOYS = auto()
    TOASTY_TOYS = auto()
    NO_PLACE_TO_HIDE = auto()
    TIED_DOWN_TOOLS = auto()
    DONALDS_LOVE_LETTERS = auto()
    RIP_VAN_DONALD = auto()
    TRAIL_OF_THE_UNICORN = auto()
    LAND_OF_THE_TOTEM_POLES = auto()
    NOISE_NULLIFIER = auto()
    MATINEE_MADNESS = auto()
    FETCHING_PRICE_A = auto()
    SERUM_TO_CODFISH_COVE = auto()
    WILD_ABOUT_FLOWERS = auto()
    IN_ANCIENT_PERSIA = auto()
    VACATION_TIME = auto()
    DONALDS_GRANDMA_DUCK = auto()
    CAMP_COUNSELOR = auto()
    PIXILATED_PARROT_THE = auto()
    MAGIC_HOURGLASS_THE = auto()
    BIG_TOP_BEDLAM = auto()
    YOU_CANT_GUESS = auto()
    DANGEROUS_DISGUISE = auto()
    NO_SUCH_VARMINT = auto()
    BILLIONS_TO_SNEEZE_AT = auto()
    OPERATION_ST_BERNARD = auto()
    FINANCIAL_FABLE_A = auto()
    APRIL_FOOLERS_THE = auto()
    IN_OLD_CALIFORNIA = auto()
    KNIGHTLY_RIVALS = auto()
    POOL_SHARKS = auto()
    TROUBLE_WITH_DIMES_THE = auto()
    GLADSTONES_LUCK = auto()
    TEN_STAR_GENERALS = auto()
    CHRISTMAS_FOR_SHACKTOWN_A = auto()
    ATTIC_ANTICS = auto()
    TRUANT_NEPHEWS_THE = auto()
    TERROR_OF_THE_BEAGLE_BOYS = auto()
    TALKING_PARROT = auto()
    TREEING_OFF = auto()
    CHRISTMAS_KISS = auto()
    PROJECTING_DESIRES = auto()
    BIG_BIN_ON_KILLMOTOR_HILL_THE = auto()
    GLADSTONES_USUAL_VERY_GOOD_YEAR = auto()
    SCREAMING_COWBOY_THE = auto()
    STATUESQUE_SPENDTHRIFTS = auto()
    ROCKET_WING_SAVES_THE_DAY = auto()
    GLADSTONES_TERRIBLE_SECRET = auto()
    ONLY_A_POOR_OLD_MAN = auto()
    OSOGOOD_SILVER_POLISH = auto()
    COFFEE_FOR_TWO = auto()
    SOUPLINE_EIGHT = auto()
    THINK_BOX_BOLLIX_THE = auto()
    GOLDEN_HELMET_THE = auto()
    FULL_SERVICE_WINDOWS = auto()
    RIGGED_UP_ROLLER = auto()
    AWASH_IN_SUCCESS = auto()
    HOUSEBOAT_HOLIDAY = auto()
    GEMSTONE_HUNTERS = auto()
    GILDED_MAN_THE = auto()
    STABLE_PRICES = auto()
    ARMORED_RESCUE = auto()
    CRAFTY_CORNER = auto()
    SPENDING_MONEY = auto()
    HYPNO_GUN_THE = auto()
    TRICK_OR_TREAT = auto()
    PRANK_ABOVE_A = auto()
    FRIGHTFUL_FACE = auto()
    HOBBLIN_GOBLINS = auto()
    OMELET = auto()
    CHARITABLE_CHORE_A = auto()
    TURKEY_WITH_ALL_THE_SCHEMINGS = auto()
    FLIP_DECISION = auto()
    MY_LUCKY_VALENTINE = auto()
    FARE_DELAY = auto()
    SOMETHIN_FISHY_HERE = auto()
    BACK_TO_THE_KLONDIKE = auto()
    MONEY_LADDER_THE = auto()
    CHECKER_GAME_THE = auto()
    EASTER_ELECTION_THE = auto()
    TALKING_DOG_THE = auto()
    WORM_WEARY = auto()
    MUCH_ADO_ABOUT_QUACKLY_HALL = auto()
    SOME_HEIR_OVER_THE_RAINBOW = auto()
    MASTER_RAINMAKER_THE = auto()
    MONEY_STAIRS_THE = auto()
    MILLION_DOLLAR_PIGEON = auto()
    TEMPER_TAMPERING = auto()
    DINER_DILEMMA = auto()
    HORSERADISH_STORY_THE = auto()
    ROUND_MONEY_BIN_THE = auto()
    BARBER_COLLEGE = auto()
    FOLLOW_THE_RAINBOW = auto()
    ITCHING_TO_SHARE = auto()
    WISPY_WILLIE = auto()
    HAMMY_CAMEL_THE = auto()
    BALLET_EVASIONS = auto()
    CHEAPEST_WEIGH_THE = auto()
    BUM_STEER = auto()
    BEE_BUMBLES = auto()
    MENEHUNE_MYSTERY_THE = auto()
    TURKEY_TROT_AT_ONE_WHISTLE = auto()
    RAFFLE_REVERSAL = auto()
    FIX_UP_MIX_UP = auto()
    SECRET_OF_ATLANTIS_THE = auto()
    HOSPITALITY_WEEK = auto()
    MCDUCK_TAKES_A_DIVE = auto()
    SLIPPERY_SIPPER = auto()
    FLOUR_FOLLIES = auto()
    PRICE_OF_FAME_THE = auto()
    MIDGETS_MADNESS = auto()
    SALMON_DERBY = auto()
    TRALLA_LA = auto()
    OIL_THE_NEWS = auto()
    DIG_IT = auto()
    MENTAL_FEE = auto()
    OUTFOXED_FOX = auto()
    CHELTENHAMS_CHOICE = auto()
    TRAVELLING_TRUANTS = auto()
    RANTS_ABOUT_ANTS = auto()
    SEVEN_CITIES_OF_CIBOLA_THE = auto()
    WRONG_NUMBER = auto()
    TOO_SAFE_SAFE = auto()
    SEARCH_FOR_THE_CUSPIDORIA = auto()
    NEW_YEARS_REVOLUTIONS = auto()
    ICEBOAT_TO_BEAVER_ISLAND = auto()
    MYSTERIOUS_STONE_RAY_THE = auto()
    CAMPAIGN_OF_NOTE_A = auto()
    CASH_ON_THE_BRAIN = auto()
    CLASSY_TAXI = auto()
    BLANKET_INVESTMENT = auto()
    DAFFY_TAFFY_PULL_THE = auto()
    TUCKERED_TIGER_THE = auto()
    DONALD_DUCK_TELLS_ABOUT_KITES = auto()
    LEMMING_WITH_THE_LOCKET_THE = auto()
    EASY_MOWING = auto()
    SKI_LIFT_LETDOWN = auto()
    CAST_OF_THOUSANDS = auto()
    GHOST_SHERIFF_OF_LAST_GASP_THE = auto()
    DESCENT_INTERVAL_A = auto()
    SECRET_OF_HONDORICA = auto()
    DOGCATCHER_DUCK = auto()
    COURTSIDE_HEATING = auto()
    POWER_PLOWING = auto()
    REMEMBER_THIS = auto()
    FABULOUS_PHILOSOPHERS_STONE_THE = auto()
    HEIRLOOM_WATCH = auto()
    DONALDS_RAUCOUS_ROLE = auto()
    GOOD_CANOES_AND_BAD_CANOES = auto()
    DEEP_DECISION = auto()
    SMASH_SUCCESS = auto()
    TROUBLE_INDEMNITY = auto()
    CHICKADEE_CHALLENGE_THE = auto()
    UNORTHODOX_OX_THE = auto()
    GREAT_STEAMBOAT_RACE_THE = auto()
    COME_AS_YOU_ARE = auto()
    ROUNDABOUT_HANDOUT = auto()
    FAULTY_FORTUNE = auto()
    RICHES_RICHES_EVERYWHERE = auto()
    CUSTARD_GUN_THE = auto()
    THREE_UN_DUCKS = auto()
    SECRET_RESOLUTIONS = auto()
    ICE_TAXIS_THE = auto()
    SEARCHING_FOR_A_SUCCESSOR = auto()
    OLYMPIC_HOPEFUL_THE = auto()
    GOLDEN_FLEECING_THE = auto()
    WATT_AN_OCCASION = auto()
    DOUGHNUT_DARE = auto()
    SWEAT_DEAL_A = auto()
    GOPHER_GOOF_UPS = auto()
    IN_THE_SWIM = auto()
    LAND_BENEATH_THE_GROUND = auto()
    TRAPPED_LIGHTNING = auto()
    ART_OF_SECURITY_THE = auto()
    FASHION_FORECAST = auto()
    MUSH = auto()
    CAMPING_CONFUSION = auto()
    MASTER_THE = auto()
    WHALE_OF_A_STORY_A = auto()
    SMOKE_WRITER_IN_THE_SKY = auto()
    INVENTOR_OF_ANYTHING = auto()
    LOST_CROWN_OF_GENGHIS_KHAN_THE = auto()
    LUNCHEON_LAMENT = auto()
    RUNAWAY_TRAIN_THE = auto()
    GOLD_RUSH = auto()
    FIREFLIES_ARE_FREE = auto()
    EARLY_TO_BUILD = auto()
    STATUES_OF_LIMITATIONS = auto()
    BORDERLINE_HERO = auto()
    SECOND_RICHEST_DUCK_THE = auto()
    MIGRATING_MILLIONS = auto()
    CAT_BOX_THE = auto()
    CHINA_SHOP_SHAKEUP = auto()
    BUFFO_OR_BUST = auto()
    POUND_FOR_SOUND = auto()
    FERTILE_ASSETS = auto()
    GRANDMAS_PRESENT = auto()
    KNIGHT_IN_SHINING_ARMOR = auto()
    FEARSOME_FLOWERS = auto()
    DONALDS_PET_SERVICE = auto()
    BACK_TO_LONG_AGO = auto()
    COLOSSALEST_SURPRISE_QUIZ_SHOW_THE = auto()
    FORECASTING_FOLLIES = auto()
    BACKYARD_BONANZA = auto()
    ALL_SEASON_HAT = auto()
    EYES_HAVE_IT_THE = auto()
    RELATIVE_REACTION = auto()
    SECRET_BOOK_THE = auto()
    TREE_TRICK = auto()
    IN_KAKIMAW_COUNTRY = auto()
    LOST_PEG_LEG_MINE_THE = auto()
    LOSING_FACE = auto()
    DAY_DUCKBURG_GOT_DYED_THE = auto()
    PICNIC = auto()
    FISHING_MYSTERY = auto()
    COLD_BARGAIN_A = auto()
    GYROS_IMAGINATION_INVENTION = auto()
    RED_APPLE_SAP = auto()
    SURE_FIRE_GOLD_FINDER_THE = auto()
    SPECIAL_DELIVERY = auto()
    CODE_OF_DUCKBURG_THE = auto()
    LAND_OF_THE_PYGMY_INDIANS = auto()
    NET_WORTH = auto()
    FORBIDDEN_VALLEY = auto()
    FANTASTIC_RIVER_RACE_THE = auto()
    SAGMORE_SPRINGS_HOTEL = auto()
    TENDERFOOT_TRAP_THE = auto()
    MINES_OF_KING_SOLOMON_THE = auto()
    GYRO_BUILDS_A_BETTER_HOUSE = auto()
    HISTORY_TOSSED = auto()
    BLACK_PEARLS_OF_TABU_YAMA_THE = auto()
    AUGUST_ACCIDENT = auto()
    SEPTEMBER_SCRIMMAGE = auto()
    WISHING_STONE_ISLAND = auto()
    ROCKET_RACE_AROUND_THE_WORLD = auto()
    ROSCOE_THE_ROBOT = auto()
    CITY_OF_GOLDEN_ROOFS = auto()
    GETTING_THOR = auto()
    DOGGED_DETERMINATION = auto()
    FORGOTTEN_PRECAUTION = auto()
    BIG_BOBBER_THE = auto()
    WINDFALL_OF_THE_MIND = auto()
    TITANIC_ANTS_THE = auto()
    RESCUE_ENHANCEMENT = auto()
    PERSISTENT_POSTMAN_THE = auto()
    HALF_BAKED_BAKER_THE = auto()
    DODGING_MISS_DAISY = auto()
    MONEY_WELL_THE = auto()
    MILKMAN_THE = auto()
    MOCKING_BIRD_RIDGE = auto()
    OLD_FROGGIE_CATAPULT = auto()
    GOING_TO_PIECES = auto()
    HIGH_RIDER = auto()
    THAT_SINKING_FEELING = auto()
    WATER_SKI_RACE = auto()
    BALMY_SWAMI_THE = auto()
    WINDY_STORY_THE = auto()
    GOLDEN_RIVER_THE = auto()
    MOOLA_ON_THE_MOVE = auto()
    THUMBS_UP = auto()
    KNOW_IT_ALL_MACHINE_THE = auto()
    STRANGE_SHIPWRECKS_THE = auto()
    FABULOUS_TYCOON_THE = auto()
    GYRO_GOES_FOR_A_DIP = auto()
    BILL_WIND = auto()
    TWENTY_FOUR_CARAT_MOON_THE = auto()
    HOUSE_ON_CYCLONE_HILL_THE = auto()
    NOBLE_PORPOISES = auto()
    MAGIC_INK_THE = auto()
    SLEEPIES_THE = auto()
    TRACKING_SANDY = auto()
    LITTLEST_CHICKEN_THIEF_THE = auto()
    BEACHCOMBERS_PICNIC_THE = auto()
    LIGHTS_OUT = auto()
    DRAMATIC_DONALD = auto()
    CHRISTMAS_IN_DUCKBURG = auto()
    ROCKET_ROASTED_CHRISTMAS_TURKEY = auto()
    MASTER_MOVER_THE = auto()
    SPRING_FEVER = auto()
    FLYING_DUTCHMAN_THE = auto()
    PYRAMID_SCHEME = auto()
    WISHING_WELL_THE = auto()
    IMMOVABLE_MISER = auto()
    RETURN_TO_PIZEN_BLUFF = auto()
    KRANKENSTEIN_GYRO = auto()
    MONEY_CHAMP_THE = auto()
    HIS_HANDY_ANDY = auto()
    FIREFLY_TRACKER_THE = auto()
    PRIZE_OF_PIZARRO_THE = auto()
    LOVELORN_FIREMAN_THE = auto()
    KITTY_GO_ROUND = auto()
    POOR_LOSER = auto()
    FLOATING_ISLAND_THE = auto()
    CRAWLS_FOR_CASH = auto()
    BLACK_FOREST_RESCUE_THE = auto()
    GOOD_DEEDS_THE = auto()
    BLACK_WEDNESDAY = auto()
    ALL_CHOKED_UP = auto()
    WATCHFUL_PARENTS_THE = auto()
    WAX_MUSEUM_THE = auto()
    PAUL_BUNYAN_MACHINE_THE = auto()
    KNIGHTS_OF_THE_FLYING_SLEDS = auto()
    WITCHING_STICK_THE = auto()
    INVENTORS_CONTEST_THE = auto()
    JUNGLE_HI_JINKS = auto()
    FLYING_FARMHAND_THE = auto()
    HONEY_OF_A_HEN_A = auto()
    WEATHER_WATCHERS_THE = auto()
    SHEEPISH_COWBOYS_THE = auto()
    OODLES_OF_OOMPH = auto()
    MASTER_GLASSER_THE = auto()
    MONEY_HAT_THE = auto()
    ISLAND_IN_THE_SKY = auto()
    UNDER_THE_POLAR_ICE = auto()
    HOUND_OF_THE_WHISKERVILLES = auto()
    RIDING_THE_PONY_EXPRESS = auto()
    WANT_TO_BUY_AN_ISLAND = auto()
    FROGGY_FARMER = auto()
    PIPELINE_TO_DANGER = auto()
    YOICKS_THE_FOX = auto()
    WAR_PAINT = auto()
    DOG_SITTER_THE = auto()
    MYSTERY_OF_THE_LOCH = auto()
    VILLAGE_BLACKSMITH_THE = auto()
    FRAIDY_FALCON_THE = auto()
    ALL_AT_SEA = auto()
    FISHY_WARDEN = auto()
    TWO_WAY_LUCK = auto()
    BALLOONATICS = auto()
    TURKEY_TROUBLE = auto()
    MISSILE_FIZZLE = auto()
    ROCKS_TO_RICHES = auto()
    SITTING_HIGH = auto()
    THATS_NO_FABLE = auto()
    CLOTHES_MAKE_THE_DUCK = auto()
    THAT_SMALL_FEELING = auto()
    MADCAP_MARINER_THE = auto()
    TERRIBLE_TOURIST = auto()
    THRIFT_GIFT_A = auto()
    LOST_FRONTIER = auto()
    YOU_CANT_WIN = auto()
    BILLIONS_IN_THE_HOLE = auto()
    BONGO_ON_THE_CONGO = auto()
    STRANGER_THAN_FICTION = auto()
    BOXED_IN = auto()
    CHUGWAGON_DERBY = auto()
    MYTHTIC_MYSTERY = auto()
    WILY_RIVAL = auto()
    DUCK_LUCK = auto()
    MR_PRIVATE_EYE = auto()
    HOUND_HOUNDER = auto()
    GOLDEN_NUGGET_BOAT_THE = auto()
    FAST_AWAY_CASTAWAY = auto()
    GIFT_LION = auto()
    JET_WITCH = auto()
    BOAT_BUSTER = auto()
    MIDAS_TOUCH_THE = auto()
    MONEY_BAG_GOAT = auto()
    DUCKBURGS_DAY_OF_PERIL = auto()
    NORTHEASTER_ON_CAPE_QUACK = auto()
    MOVIE_MAD = auto()
    TEN_CENT_VALENTINE = auto()
    CAVE_OF_ALI_BABA = auto()
    DEEP_DOWN_DOINGS = auto()
    GREAT_POP_UP_THE = auto()
    JUNGLE_BUNGLE = auto()
    MERRY_FERRY = auto()
    UNSAFE_SAFE_THE = auto()
    MUCH_LUCK_MCDUCK = auto()
    UNCLE_SCROOGE___MONKEY_BUSINESS = auto()
    COLLECTION_DAY = auto()
    SEEING_IS_BELIEVING = auto()
    PLAYMATES = auto()
    RAGS_TO_RICHES = auto()
    ART_APPRECIATION = auto()
    FLOWERS_ARE_FLOWERS = auto()
    MADCAP_INVENTORS = auto()
    MEDALING_AROUND = auto()
    WAY_OUT_YONDER = auto()
    CANDY_KID_THE = auto()
    SPICY_TALE_A = auto()
    FINNY_FUN = auto()
    GETTING_THE_BIRD = auto()
    NEST_EGG_COLLECTOR = auto()
    MILLION_DOLLAR_SHOWER = auto()
    TRICKY_EXPERIMENT = auto()
    MASTER_WRECKER = auto()
    RAVEN_MAD = auto()
    STALWART_RANGER = auto()
    LOG_JOCKEY = auto()
    SNOW_DUSTER = auto()
    ODDBALL_ODYSSEY = auto()
    POSTHASTY_POSTMAN = auto()
    STATUS_SEEKER_THE = auto()
    MATTER_OF_FACTORY_A = auto()
    CHRISTMAS_CHEERS = auto()
    JINXED_JALOPY_RACE_THE = auto()
    FOR_OLD_DIMES_SAKE = auto()
    STONES_THROW_FROM_GHOST_TOWN_A = auto()
    SPARE_THAT_HAIR = auto()
    DUCKS_EYE_VIEW_OF_EUROPE_A = auto()
    CASE_OF_THE_STICKY_MONEY_THE = auto()
    DUELING_TYCOONS = auto()
    WISHFUL_EXCESS = auto()
    SIDEWALK_OF_THE_MIND = auto()
    NO_BARGAIN = auto()
    UP_AND_AT_IT = auto()
    GALL_OF_THE_WILD = auto()
    ZERO_HERO = auto()
    BEACH_BOY = auto()
    CROWN_OF_THE_MAYAS = auto()
    INVISIBLE_INTRUDER_THE = auto()
    ISLE_OF_GOLDEN_GEESE = auto()
    TRAVEL_TIGHTWAD_THE = auto()
    DUCKBURG_PET_PARADE_THE = auto()
    HELPERS_HELPING_HAND_A = auto()
    HAVE_GUN_WILL_DANCE = auto()
    LOST_BENEATH_THE_SEA = auto()
    LEMONADE_FLING_THE = auto()
    FIREMAN_SCROOGE = auto()
    SAVED_BY_THE_BAG = auto()
    ONCE_UPON_A_CARNIVAL = auto()
    DOUBLE_MASQUERADE = auto()
    MAN_VERSUS_MACHINE = auto()
    TICKING_DETECTOR = auto()
    IT_HAPPENED_ONE_WINTER = auto()
    THRIFTY_SPENDTHRIFT_THE = auto()
    FEUD_AND_FAR_BETWEEN = auto()
    BUBBLEWEIGHT_CHAMP = auto()
    JONAH_GYRO = auto()
    MANY_FACES_OF_MAGICA_DE_SPELL_THE = auto()
    CAPN_BLIGHTS_MYSTERY_SHIP = auto()
    LOONY_LUNAR_GOLD_RUSH_THE = auto()
    OLYMPIAN_TORCH_BEARER_THE = auto()
    RUG_RIDERS_IN_THE_SKY = auto()
    HOW_GREEN_WAS_MY_LETTUCE = auto()
    GREAT_WIG_MYSTERY_THE = auto()
    HERO_OF_THE_DIKE = auto()
    INTERPLANETARY_POSTMAN = auto()
    UNFRIENDLY_ENEMIES = auto()
    BILLION_DOLLAR_SAFARI_THE = auto()
    DELIVERY_DILEMMA = auto()
    INSTANT_HERCULES = auto()
    MCDUCK_OF_ARABIA = auto()
    MYSTERY_OF_THE_GHOST_TOWN_RAILROAD = auto()
    DUCK_OUT_OF_LUCK = auto()
    LOCK_OUT_THE = auto()
    BIGGER_THE_BEGGAR_THE = auto()
    PLUMMETING_WITH_PRECISION = auto()
    SNAKE_TAKE = auto()
    SWAMP_OF_NO_RETURN_THE = auto()
    MONKEY_BUSINESS = auto()
    GIANT_ROBOT_ROBBERS_THE = auto()
    LAUNDRY_FOR_LESS = auto()
    LONG_DISTANCE_COLLISION = auto()
    TOP_WAGES = auto()
    NORTH_OF_THE_YUKON = auto()
    DOWN_FOR_THE_COUNT = auto()
    WASTED_WORDS = auto()
    PHANTOM_OF_NOTRE_DUCK_THE = auto()
    SO_FAR_AND_NO_SAFARI = auto()
    QUEEN_OF_THE_WILD_DOG_PACK_THE = auto()
    HOUSE_OF_HAUNTS = auto()
    TREASURE_OF_MARCO_POLO = auto()
    BEAUTY_BUSINESS_THE = auto()
    MICRO_DUCKS_FROM_OUTER_SPACE = auto()
    NOT_SO_ANCIENT_MARINER_THE = auto()
    HEEDLESS_HORSEMAN_THE = auto()
    HALL_OF_THE_MERMAID_QUEEN = auto()
    DOOM_DIAMOND_THE = auto()
    CATTLE_KING_THE = auto()
    KING_SCROOGE_THE_FIRST = auto()


assert NUM_TITLES == len(Titles)


@dataclass
class ComicBookInfo:
    title: Titles
    title_str: str
    is_barks_title: bool
    issue_name: str
    issue_number: int
    issue_month: int
    issue_year: int
    submitted_day: int
    submitted_month: int
    submitted_year: int
    chronological_number: int

    def get_short_issue_title(self):
        short_issue_name = SHORT_ISSUE_NAME[self.issue_name]
        return f"{short_issue_name} {self.issue_number}"


# fmt: off
# noinspection LongLine
BARKS_TITLE_INFO: List[ComicBookInfo] = [
    ComicBookInfo(Titles.DONALD_DUCK_FINDS_PIRATE_GOLD, DONALD_DUCK_FINDS_PIRATE_GOLD, True, FC, 9, 10, 1942, -1, 5, 1942, 1),
    ComicBookInfo(Titles.VICTORY_GARDEN_THE, VICTORY_GARDEN_THE, False, CS, 31, 4, 1943, -1, 12, 1942, 2),
    ComicBookInfo(Titles.RABBITS_FOOT_THE, RABBITS_FOOT_THE, False, CS, 32, 5, 1943, 23, 12, 1942, 3),
    ComicBookInfo(Titles.LIFEGUARD_DAZE, LIFEGUARD_DAZE, False, CS, 33, 6, 1943, 29, 1, 1943, 4),
    ComicBookInfo(Titles.GOOD_DEEDS, GOOD_DEEDS, False, CS, 34, 7, 1943, 24, 2, 1943, 5),
    ComicBookInfo(Titles.LIMBER_W_GUEST_RANCH_THE, LIMBER_W_GUEST_RANCH_THE, False, CS, 35, 8, 1943, 17, 3, 1943, 6),
    ComicBookInfo(Titles.MIGHTY_TRAPPER_THE, MIGHTY_TRAPPER_THE, True, CS, 36, 9, 1943, 20, 4, 1943, 7),
    ComicBookInfo(Titles.DONALD_DUCK_AND_THE_MUMMYS_RING, DONALD_DUCK_AND_THE_MUMMYS_RING, True, FC, 29, 9, 1943, 10, 5, 1943, 8),
    ComicBookInfo(Titles.HARD_LOSER_THE, HARD_LOSER_THE, True, FC, 29, 9, 1943, 10, 5, 1943, 9),
    ComicBookInfo(Titles.TOO_MANY_PETS, TOO_MANY_PETS, True, FC, 29, 9, 1943, 29, 5, 1943, 10),
    ComicBookInfo(Titles.GOOD_NEIGHBORS, GOOD_NEIGHBORS, True, CS, 38, 11, 1943, 22, 6, 1943, 11),
    ComicBookInfo(Titles.SALESMAN_DONALD, SALESMAN_DONALD, True, CS, 39, 12, 1943, 23, 7, 1943, 12),
    ComicBookInfo(Titles.SNOW_FUN, SNOW_FUN, True, CS, 40, 1, 1944, 28, 8, 1943, 13),
    ComicBookInfo(Titles.DUCK_IN_THE_IRON_PANTS_THE, DUCK_IN_THE_IRON_PANTS_THE, True, CS, 41, 2, 1944, 22, 9, 1943, 14),
    ComicBookInfo(Titles.KITE_WEATHER, KITE_WEATHER, True, CS, 42, 3, 1944, 20, 10, 1943, 15),
    ComicBookInfo(Titles.THREE_DIRTY_LITTLE_DUCKS, THREE_DIRTY_LITTLE_DUCKS, True, CS, 43, 4, 1944, 27, 11, 1943, 16),
    ComicBookInfo(Titles.MAD_CHEMIST_THE, MAD_CHEMIST_THE, True, CS, 44, 5, 1944, 30, 12, 1943, 17),
    ComicBookInfo(Titles.RIVAL_BOATMEN, RIVAL_BOATMEN, True, CS, 45, 6, 1944, 19, 1, 1944, 18),
    ComicBookInfo(Titles.CAMERA_CRAZY, CAMERA_CRAZY, True, CS, 46, 7, 1944, 29, 2, 1944, 19),
    ComicBookInfo(Titles.FARRAGUT_THE_FALCON, FARRAGUT_THE_FALCON, False, CS, 47, 8, 1944, 1, 4, 1944, 20),
    ComicBookInfo(Titles.PURLOINED_PUTTY_THE, PURLOINED_PUTTY_THE, False, CS, 48, 9, 1944, 26, 4, 1944, 21),
    ComicBookInfo(Titles.HIGH_WIRE_DAREDEVILS, HIGH_WIRE_DAREDEVILS, False, CS, 49, 10, 1944, 26, 5, 1944, 22),
    ComicBookInfo(Titles.TEN_CENTS_WORTH_OF_TROUBLE, TEN_CENTS_WORTH_OF_TROUBLE, False, CS, 50, 11, 1944, 22, 6, 1944, 23),
    ComicBookInfo(Titles.DONALDS_BAY_LOT, DONALDS_BAY_LOT, False, CS, 51, 12, 1944, 27, 7, 1944, 24),
    ComicBookInfo(Titles.FROZEN_GOLD, FROZEN_GOLD, True, FC, 62, 1, 1945, 9, 8, 1944, 25),
    ComicBookInfo(Titles.THIEVERY_AFOOT, THIEVERY_AFOOT, False, CS, 52, 1, 1945, 26, 8, 1944, 26),
    ComicBookInfo(Titles.MYSTERY_OF_THE_SWAMP, MYSTERY_OF_THE_SWAMP, True, FC, 62, 1, 1945, 23, 9, 1944, 27),
    ComicBookInfo(Titles.TRAMP_STEAMER_THE, TRAMP_STEAMER_THE, False, CS, 53, 2, 1945, 6, 10, 1944, 28),
    ComicBookInfo(Titles.LONG_RACE_TO_PUMPKINBURG_THE, LONG_RACE_TO_PUMPKINBURG_THE, False, CS, 54, 3, 1945, 27, 10, 1944, 29),
    ComicBookInfo(Titles.WEBFOOTED_WRANGLER, WEBFOOTED_WRANGLER, False, CS, 55, 4, 1945, 1, 12, 1944, 30),
    ComicBookInfo(Titles.ICEBOX_ROBBER_THE, ICEBOX_ROBBER_THE, False, CS, 56, 5, 1945, -1, 1, 1945, 31),
    ComicBookInfo(Titles.PECKING_ORDER, PECKING_ORDER, False, CS, 57, 6, 1945, 2, 2, 1945, 32),
    ComicBookInfo(Titles.TAMING_THE_RAPIDS, TAMING_THE_RAPIDS, False, CS, 58, 7, 1945, 9, 3, 1945, 33),
    ComicBookInfo(Titles.EYES_IN_THE_DARK, EYES_IN_THE_DARK, False, CS, 60, 9, 1945, 12, 3, 1945, 34),
    ComicBookInfo(Titles.DAYS_AT_THE_LAZY_K, DAYS_AT_THE_LAZY_K, False, CS, 59, 8, 1945, 3, 4, 1945, 35),
    ComicBookInfo(Titles.RIDDLE_OF_THE_RED_HAT_THE, RIDDLE_OF_THE_RED_HAT_THE, True, FC, 79, 8, 1945, 27, 4, 1945, 36),
    ComicBookInfo(Titles.THUG_BUSTERS, THUG_BUSTERS, False, CS, 61, 10, 1945, 31, 5, 1945, 37),
    ComicBookInfo(Titles.GREAT_SKI_RACE_THE, GREAT_SKI_RACE_THE, False, CS, 62, 11, 1945, 27, 6, 1945, 38),
    ComicBookInfo(Titles.FIREBUG_THE, FIREBUG_THE, True, FC, 108, 1, 1946, 19, 7, 1945, 39),
    ComicBookInfo(Titles.TEN_DOLLAR_DITHER, TEN_DOLLAR_DITHER, False, CS, 63, 12, 1945, 2, 8, 1945, 40),
    ComicBookInfo(Titles.DONALD_DUCKS_BEST_CHRISTMAS, DONALD_DUCKS_BEST_CHRISTMAS, True, FG, 45, 12, 1945, 31, 8, 1945, 41),
    ComicBookInfo(Titles.SILENT_NIGHT, SILENT_NIGHT, False, CS, 64, 1, 1946, 31, 8, 1945, 42),
    ComicBookInfo(Titles.DONALD_TAMES_HIS_TEMPER, DONALD_TAMES_HIS_TEMPER, False, CS, 64, 1, 1946, 19, 9, 1945, 43),
    ComicBookInfo(Titles.SINGAPORE_JOE, SINGAPORE_JOE, False, CS, 65, 2, 1946, 4, 10, 1945, 44),
    ComicBookInfo(Titles.MASTER_ICE_FISHER, MASTER_ICE_FISHER, False, CS, 66, 3, 1946, 27, 10, 1945, 45),
    ComicBookInfo(Titles.JET_RESCUE, JET_RESCUE, False, CS, 67, 4, 1946, 23, 11, 1945, 46),
    ComicBookInfo(Titles.DONALDS_MONSTER_KITE, DONALDS_MONSTER_KITE, False, CS, 68, 5, 1946, 4, 1, 1946, 47),
    ComicBookInfo(Titles.TERROR_OF_THE_RIVER_THE, TERROR_OF_THE_RIVER_THE, True, FC, 108, 1, 1946, 25, 1, 1946, 48),
    ComicBookInfo(Titles.SEALS_ARE_SO_SMART, SEALS_ARE_SO_SMART, True, FC, 108, 1, 1946, 25, 1, 1946, 49),
    ComicBookInfo(Titles.BICEPS_BLUES, BICEPS_BLUES, False, CS, 69, 6, 1946, 1, 2, 1946, 50),
    ComicBookInfo(Titles.SMUGSNORKLE_SQUATTIE_THE, SMUGSNORKLE_SQUATTIE_THE, False, CS, 70, 7, 1946, 28, 2, 1946, 51),
    ComicBookInfo(Titles.SANTAS_STORMY_VISIT, SANTAS_STORMY_VISIT, True, FG, 46, 12, 1946, 8, 3, 1946, 52),
    ComicBookInfo(Titles.SWIMMING_SWINDLERS, SWIMMING_SWINDLERS, False, CS, 71, 8, 1946, 26, 3, 1946, 53),
    ComicBookInfo(Titles.PLAYIN_HOOKEY, PLAYIN_HOOKEY, False, CS, 72, 9, 1946, 25, 4, 1946, 54),
    ComicBookInfo(Titles.GOLD_FINDER_THE, GOLD_FINDER_THE, False, CS, 73, 10, 1946, 27, 5, 1946, 55),
    ComicBookInfo(Titles.BILL_COLLECTORS_THE, BILL_COLLECTORS_THE, False, CS, 74, 11, 1946, 14, 6, 1946, 56),
    ComicBookInfo(Titles.TURKEY_RAFFLE, TURKEY_RAFFLE, False, CS, 75, 12, 1946, 8, 7, 1946, 57),
    ComicBookInfo(Titles.MAHARAJAH_DONALD, MAHARAJAH_DONALD, True, MC, 4, -1, 1947, 13, 8, 1946, 58),
    ComicBookInfo(Titles.CANTANKEROUS_CAT_THE, CANTANKEROUS_CAT_THE, False, CS, 76, 1, 1947, 29, 8, 1946, 59),
    ComicBookInfo(Titles.DONALD_DUCKS_ATOM_BOMB, DONALD_DUCKS_ATOM_BOMB, True, CH, 1, -1, 1947, 9, 9, 1946, 60),
    ComicBookInfo(Titles.GOING_BUGGY, GOING_BUGGY, False, CS, 77, 2, 1947, 25, 9, 1946, 61),
    ComicBookInfo(Titles.PEACEFUL_HILLS_THE, PEACEFUL_HILLS_THE, True, MC, 4, -1, 1947, 4, 10, 1946, 62),
    ComicBookInfo(Titles.JAM_ROBBERS, JAM_ROBBERS, False, CS, 78, 3, 1947, 28, 10, 1946, 63),
    ComicBookInfo(Titles.PICNIC_TRICKS, PICNIC_TRICKS, False, CS, 79, 4, 1947, 18, 11, 1946, 64),
    ComicBookInfo(Titles.VOLCANO_VALLEY, VOLCANO_VALLEY, True, FC, 147, 5, 1947, 9, 12, 1946, 65),
    ComicBookInfo(Titles.IF_THE_HAT_FITS, IF_THE_HAT_FITS, False, FC, 147, 5, 1947, 30, 12, 1946, 66),
    ComicBookInfo(Titles.DONALDS_POSY_PATCH, DONALDS_POSY_PATCH, False, CS, 80, 5, 1947, 10, 1, 1947, 67),
    ComicBookInfo(Titles.DONALD_MINES_HIS_OWN_BUSINESS, DONALD_MINES_HIS_OWN_BUSINESS, False, CS, 81, 6, 1947, 28, 1, 1947, 68),
    ComicBookInfo(Titles.MAGICAL_MISERY, MAGICAL_MISERY, False, CS, 82, 7, 1947, 19, 2, 1947, 69),
    ComicBookInfo(Titles.THREE_GOOD_LITTLE_DUCKS, THREE_GOOD_LITTLE_DUCKS, True, FG, 47, 12, 1947, 28, 2, 1947, 70),
    ComicBookInfo(Titles.VACATION_MISERY, VACATION_MISERY, False, CS, 83, 8, 1947, 19, 3, 1947, 71),
    ComicBookInfo(Titles.ADVENTURE_DOWN_UNDER, ADVENTURE_DOWN_UNDER, True, FC, 159, 8, 1947, 4, 4, 1947, 72),
    ComicBookInfo(Titles.GHOST_OF_THE_GROTTO_THE, GHOST_OF_THE_GROTTO_THE, True, FC, 159, 8, 1947, 15, 4, 1947, 73),
    ComicBookInfo(Titles.WALTZ_KING_THE, WALTZ_KING_THE, False, CS, 84, 9, 1947, 1, 5, 1947, 74),
    ComicBookInfo(Titles.MASTERS_OF_MELODY_THE, MASTERS_OF_MELODY_THE, False, CS, 85, 10, 1947, 5, 5, 1947, 75),
    ComicBookInfo(Titles.FIREMAN_DONALD, FIREMAN_DONALD, False, CS, 86, 11, 1947, 23, 6, 1947, 76),
    ComicBookInfo(Titles.CHRISTMAS_ON_BEAR_MOUNTAIN, CHRISTMAS_ON_BEAR_MOUNTAIN, True, FC, 178, 12, 1947, 22, 7, 1947, 77),
    ComicBookInfo(Titles.FASHION_IN_FLIGHT, FASHION_IN_FLIGHT, False, FC, 178, 12, 1947, 22, 7, 1947, 78),
    ComicBookInfo(Titles.TURN_FOR_THE_WORSE, TURN_FOR_THE_WORSE, False, FC, 178, 12, 1947, 22, 7, 1947, 79),
    ComicBookInfo(Titles.MACHINE_MIX_UP, MACHINE_MIX_UP, False, FC, 178, 12, 1947, 22, 7, 1947, 80),
    ComicBookInfo(Titles.TERRIBLE_TURKEY_THE, TERRIBLE_TURKEY_THE, False, CS, 87, 12, 1947, 31, 7, 1947, 81),
    ComicBookInfo(Titles.WINTERTIME_WAGER, WINTERTIME_WAGER, False, CS, 88, 1, 1948, 15, 8, 1947, 82),
    ComicBookInfo(Titles.WATCHING_THE_WATCHMAN, WATCHING_THE_WATCHMAN, False, CS, 89, 2, 1948, 4, 9, 1947, 83),
    ComicBookInfo(Titles.DARKEST_AFRICA, DARKEST_AFRICA, True, MC, 20, -1, 1948, 26, 9, 1947, 84),
    ComicBookInfo(Titles.WIRED, WIRED, False, CS, 90, 3, 1948, 9, 10, 1947, 85),
    ComicBookInfo(Titles.GOING_APE, GOING_APE, False, CS, 91, 4, 1948, 28, 10, 1947, 86),
    ComicBookInfo(Titles.OLD_CASTLES_SECRET_THE, OLD_CASTLES_SECRET_THE, True, FC, 189, 6, 1948, 3, 12, 1947, 87),
    ComicBookInfo(Titles.SPOIL_THE_ROD, SPOIL_THE_ROD, False, CS, 92, 5, 1948, 30, 12, 1947, 88),
    ComicBookInfo(Titles.BIRD_WATCHING, BIRD_WATCHING, False, FC, 189, 6, 1948, 6, 1, 1948, 89),
    ComicBookInfo(Titles.HORSESHOE_LUCK, HORSESHOE_LUCK, False, FC, 189, 6, 1948, 6, 1, 1948, 90),
    ComicBookInfo(Titles.BEAN_TAKEN, BEAN_TAKEN, False, FC, 189, 6, 1948, 6, 1, 1948, 91),
    ComicBookInfo(Titles.ROCKET_RACE_TO_THE_MOON, ROCKET_RACE_TO_THE_MOON, False, CS, 93, 6, 1948, 16, 1, 1948, 92),
    ComicBookInfo(Titles.DONALD_OF_THE_COAST_GUARD, DONALD_OF_THE_COAST_GUARD, False, CS, 94, 7, 1948, 3, 2, 1948, 93),
    ComicBookInfo(Titles.GLADSTONE_RETURNS, GLADSTONE_RETURNS, False, CS, 95, 8, 1948, 19, 2, 1948, 94),
    ComicBookInfo(Titles.SHERIFF_OF_BULLET_VALLEY, SHERIFF_OF_BULLET_VALLEY, True, FC, 199, 10, 1948, 16, 3, 1948, 95),
    ComicBookInfo(Titles.LINKS_HIJINKS, LINKS_HIJINKS, False, CS, 96, 9, 1948, 25, 3, 1948, 96),
    ComicBookInfo(Titles.SORRY_TO_BE_SAFE, SORRY_TO_BE_SAFE, False, FC, 199, 10, 1948, 22, 4, 1948, 97),
    ComicBookInfo(Titles.BEST_LAID_PLANS, BEST_LAID_PLANS, False, FC, 199, 10, 1948, 22, 4, 1948, 98),
    ComicBookInfo(Titles.GENUINE_ARTICLE_THE, GENUINE_ARTICLE_THE, False, FC, 199, 10, 1948, 22, 4, 1948, 99),
    ComicBookInfo(Titles.PEARLS_OF_WISDOM, PEARLS_OF_WISDOM, False, CS, 97, 10, 1948, 29, 4, 1948, 100),
    ComicBookInfo(Titles.FOXY_RELATIONS, FOXY_RELATIONS, False, CS, 98, 11, 1948, 28, 5, 1948, 101),
    ComicBookInfo(Titles.CRAZY_QUIZ_SHOW_THE, CRAZY_QUIZ_SHOW_THE, False, CS, 99, 12, 1948, 10, 6, 1948, 102),
    ComicBookInfo(Titles.GOLDEN_CHRISTMAS_TREE_THE, GOLDEN_CHRISTMAS_TREE_THE, True, FC, 203, 12, 1948, 30, 6, 1948, 103),
    ComicBookInfo(Titles.TOYLAND, TOYLAND, True, FG, 48, 12, 1948, 8, 7, 1948, 104),
    ComicBookInfo(Titles.JUMPING_TO_CONCLUSIONS, JUMPING_TO_CONCLUSIONS, False, FC, 203, 12, 1948, 22, 7, 1948, 105),
    ComicBookInfo(Titles.TRUE_TEST_THE, TRUE_TEST_THE, False, FC, 203, 12, 1948, 22, 7, 1948, 106),
    ComicBookInfo(Titles.ORNAMENTS_ON_THE_WAY, ORNAMENTS_ON_THE_WAY, False, FC, 203, 12, 1948, 22, 7, 1948, 107),
    ComicBookInfo(Titles.TRUANT_OFFICER_DONALD, TRUANT_OFFICER_DONALD, False, CS, 100, 1, 1949, 29, 7, 1948, 108),
    ComicBookInfo(Titles.DONALD_DUCKS_WORST_NIGHTMARE, DONALD_DUCKS_WORST_NIGHTMARE, False, CS, 101, 2, 1949, 26, 8, 1948, 109),
    ComicBookInfo(Titles.PIZEN_SPRING_DUDE_RANCH, PIZEN_SPRING_DUDE_RANCH, False, CS, 102, 3, 1949, 9, 9, 1948, 110),
    ComicBookInfo(Titles.RIVAL_BEACHCOMBERS, RIVAL_BEACHCOMBERS, False, CS, 103, 4, 1949, 23, 9, 1948, 111),
    ComicBookInfo(Titles.LOST_IN_THE_ANDES, LOST_IN_THE_ANDES, True, FC, 223, 4, 1949, 21, 10, 1948, 112),
    ComicBookInfo(Titles.TOO_FIT_TO_FIT, TOO_FIT_TO_FIT, False, FC, 223, 4, 1949, 24, 11, 1948, 113),
    ComicBookInfo(Titles.TUNNEL_VISION, TUNNEL_VISION, False, FC, 223, 4, 1949, 24, 11, 1948, 114),
    ComicBookInfo(Titles.SLEEPY_SITTERS, SLEEPY_SITTERS, False, FC, 223, 4, 1949, 24, 11, 1948, 115),
    ComicBookInfo(Titles.SUNKEN_YACHT_THE, SUNKEN_YACHT_THE, False, CS, 104, 5, 1949, 24, 11, 1948, 116),
    ComicBookInfo(Titles.RACE_TO_THE_SOUTH_SEAS, RACE_TO_THE_SOUTH_SEAS, True, MC, 41, -1, 1949, 15, 12, 1948, 117),
    ComicBookInfo(Titles.MANAGING_THE_ECHO_SYSTEM, MANAGING_THE_ECHO_SYSTEM, False, CS, 105, 6, 1949, 13, 1, 1949, 118),
    ComicBookInfo(Titles.PLENTY_OF_PETS, PLENTY_OF_PETS, False, CS, 106, 7, 1949, 27, 1, 1949, 119),
    ComicBookInfo(Titles.VOODOO_HOODOO, VOODOO_HOODOO, True, FC, 238, 8, 1949, 3, 3, 1949, 120),
    ComicBookInfo(Titles.SLIPPERY_SHINE, SLIPPERY_SHINE, False, FC, 238, 8, 1949, 17, 3, 1949, 121),
    ComicBookInfo(Titles.FRACTIOUS_FUN, FRACTIOUS_FUN, False, FC, 238, 8, 1949, 17, 3, 1949, 122),
    ComicBookInfo(Titles.KING_SIZE_CONE, KING_SIZE_CONE, False, FC, 238, 8, 1949, 17, 3, 1949, 123),
    ComicBookInfo(Titles.SUPER_SNOOPER, SUPER_SNOOPER, False, CS, 107, 8, 1949, 22, 3, 1949, 124),
    ComicBookInfo(Titles.GREAT_DUCKBURG_FROG_JUMPING_CONTEST_THE, GREAT_DUCKBURG_FROG_JUMPING_CONTEST_THE, False, CS, 108, 9, 1949, 14, 4, 1949, 125),
    ComicBookInfo(Titles.DOWSING_DUCKS, DOWSING_DUCKS, False, CS, 109, 10, 1949, 28, 4, 1949, 126),
    ComicBookInfo(Titles.GOLDILOCKS_GAMBIT_THE, GOLDILOCKS_GAMBIT_THE, False, CS, 110, 11, 1949, 12, 5, 1949, 127),
    ComicBookInfo(Titles.LETTER_TO_SANTA, LETTER_TO_SANTA, True, CP, 1, 11, 1949, 1, 6, 1949, 128),
    ComicBookInfo(Titles.NO_NOISE_IS_GOOD_NOISE, NO_NOISE_IS_GOOD_NOISE, False, CP, 1, 11, 1949, 1, 6, 1949, 129),
    ComicBookInfo(Titles.LUCK_OF_THE_NORTH, LUCK_OF_THE_NORTH, True, FC, 256, 12, 1949, 29, 6, 1949, 130),
    ComicBookInfo(Titles.NEW_TOYS, NEW_TOYS, True, FG, 49, 12, 1949, 7, 7, 1949, 131),
    ComicBookInfo(Titles.TOASTY_TOYS, TOASTY_TOYS, False, FC, 256, 12, 1949, 21, 7, 1949, 132),
    ComicBookInfo(Titles.NO_PLACE_TO_HIDE, NO_PLACE_TO_HIDE, False, FC, 256, 12, 1949, 21, 7, 1949, 133),
    ComicBookInfo(Titles.TIED_DOWN_TOOLS, TIED_DOWN_TOOLS, False, FC, 256, 12, 1949, 21, 7, 1949, 134),
    ComicBookInfo(Titles.DONALDS_LOVE_LETTERS, DONALDS_LOVE_LETTERS, False, CS, 111, 12, 1949, 4, 8, 1949, 135),
    ComicBookInfo(Titles.RIP_VAN_DONALD, RIP_VAN_DONALD, False, CS, 112, 1, 1950, 24, 8, 1949, 136),
    ComicBookInfo(Titles.TRAIL_OF_THE_UNICORN, TRAIL_OF_THE_UNICORN, True, FC, 263, 2, 1950, 8, 9, 1949, 137),
    ComicBookInfo(Titles.LAND_OF_THE_TOTEM_POLES, LAND_OF_THE_TOTEM_POLES, True, FC, 263, 2, 1950, 29, 9, 1949, 138),
    ComicBookInfo(Titles.NOISE_NULLIFIER, NOISE_NULLIFIER, False, FC, 263, 2, 1950, 6, 10, 1949, 139),
    ComicBookInfo(Titles.MATINEE_MADNESS, MATINEE_MADNESS, False, FC, 263, 2, 1950, 6, 10, 1949, 140),
    ComicBookInfo(Titles.FETCHING_PRICE_A, FETCHING_PRICE_A, False, FC, 263, 2, 1950, 6, 10, 1949, 141),
    ComicBookInfo(Titles.SERUM_TO_CODFISH_COVE, SERUM_TO_CODFISH_COVE, False, CS, 114, 3, 1950, 13, 10, 1949, 142),
    ComicBookInfo(Titles.WILD_ABOUT_FLOWERS, WILD_ABOUT_FLOWERS, False, CS, 117, 6, 1950, 27, 10, 1949, 143),
    ComicBookInfo(Titles.IN_ANCIENT_PERSIA, IN_ANCIENT_PERSIA, True, FC, 275, 5, 1950, 23, 11, 1949, 144),
    ComicBookInfo(Titles.VACATION_TIME, VACATION_TIME, True, VP, 1, 7, 1950, 5, 1, 1950, 145),
    ComicBookInfo(Titles.DONALDS_GRANDMA_DUCK, DONALDS_GRANDMA_DUCK, True, VP, 1, 7, 1950, 19, 1, 1950, 146),
    ComicBookInfo(Titles.CAMP_COUNSELOR, CAMP_COUNSELOR, True, VP, 1, 7, 1950, 27, 1, 1950, 147),
    ComicBookInfo(Titles.PIXILATED_PARROT_THE, PIXILATED_PARROT_THE, True, FC, 282, 7, 1950, 23, 2, 1950, 148),
    ComicBookInfo(Titles.MAGIC_HOURGLASS_THE, MAGIC_HOURGLASS_THE, True, FC, 291, 9, 1950, 16, 3, 1950, 149),
    ComicBookInfo(Titles.BIG_TOP_BEDLAM, BIG_TOP_BEDLAM, True, FC, 300, 11, 1950, 20, 4, 1950, 150),
    ComicBookInfo(Titles.YOU_CANT_GUESS, YOU_CANT_GUESS, True, CP, 2, 11, 1950, 24, 5, 1950, 151),
    ComicBookInfo(Titles.DANGEROUS_DISGUISE, DANGEROUS_DISGUISE, True, FC, 308, 1, 1951, 29, 6, 1950, 152),
    ComicBookInfo(Titles.NO_SUCH_VARMINT, NO_SUCH_VARMINT, True, FC, 318, 3, 1951, 27, 7, 1950, 153),
    ComicBookInfo(Titles.BILLIONS_TO_SNEEZE_AT, BILLIONS_TO_SNEEZE_AT, False, CS, 124, 1, 1951, 10, 8, 1950, 154),
    ComicBookInfo(Titles.OPERATION_ST_BERNARD, OPERATION_ST_BERNARD, False, CS, 125, 2, 1951, 31, 8, 1950, 155),
    ComicBookInfo(Titles.FINANCIAL_FABLE_A, FINANCIAL_FABLE_A, False, CS, 126, 3, 1951, 14, 9, 1950, 156),
    ComicBookInfo(Titles.APRIL_FOOLERS_THE, APRIL_FOOLERS_THE, False, CS, 127, 4, 1951, 28, 9, 1950, 157),
    ComicBookInfo(Titles.IN_OLD_CALIFORNIA, IN_OLD_CALIFORNIA, True, FC, 328, 5, 1951, 2, 11, 1950, 158),
    ComicBookInfo(Titles.KNIGHTLY_RIVALS, KNIGHTLY_RIVALS, False, CS, 128, 5, 1951, 30, 11, 1950, 159),
    ComicBookInfo(Titles.POOL_SHARKS, POOL_SHARKS, False, CS, 129, 6, 1951, 7, 12, 1950, 160),
    ComicBookInfo(Titles.TROUBLE_WITH_DIMES_THE, TROUBLE_WITH_DIMES_THE, False, CS, 130, 7, 1951, 28, 12, 1950, 161),
    ComicBookInfo(Titles.GLADSTONES_LUCK, GLADSTONES_LUCK, False, CS, 131, 8, 1951, 11, 1, 1951, 162),
    ComicBookInfo(Titles.TEN_STAR_GENERALS, TEN_STAR_GENERALS, False, CS, 132, 9, 1951, 25, 1, 1951, 163),
    ComicBookInfo(Titles.CHRISTMAS_FOR_SHACKTOWN_A, CHRISTMAS_FOR_SHACKTOWN_A, True, FC, 367, 1, 1952, 15, 3, 1951, 164),
    ComicBookInfo(Titles.ATTIC_ANTICS, ATTIC_ANTICS, False, CS, 132, 9, 1951, 29, 3, 1951, 165),
    ComicBookInfo(Titles.TRUANT_NEPHEWS_THE, TRUANT_NEPHEWS_THE, False, CS, 133, 10, 1951, 12, 4, 1951, 166),
    ComicBookInfo(Titles.TERROR_OF_THE_BEAGLE_BOYS, TERROR_OF_THE_BEAGLE_BOYS, False, CS, 134, 11, 1951, 5, 5, 1951, 167),
    ComicBookInfo(Titles.TALKING_PARROT, TALKING_PARROT, False, FC, 356, 11, 1951, 24, 5, 1951, 168),
    ComicBookInfo(Titles.TREEING_OFF, TREEING_OFF, False, FC, 367, 1, 1952, 24, 5, 1951, 169),
    ComicBookInfo(Titles.CHRISTMAS_KISS, CHRISTMAS_KISS, False, FC, 367, 1, 1952, 24, 5, 1951, 170),
    ComicBookInfo(Titles.PROJECTING_DESIRES, PROJECTING_DESIRES, False, FC, 367, 1, 1952, 24, 5, 1951, 171),
    ComicBookInfo(Titles.BIG_BIN_ON_KILLMOTOR_HILL_THE, BIG_BIN_ON_KILLMOTOR_HILL_THE, False, CS, 135, 12, 1951, 31, 5, 1951, 172),
    ComicBookInfo(Titles.GLADSTONES_USUAL_VERY_GOOD_YEAR, GLADSTONES_USUAL_VERY_GOOD_YEAR, False, CS, 136, 1, 1952, 7, 6, 1951, 173),
    ComicBookInfo(Titles.SCREAMING_COWBOY_THE, SCREAMING_COWBOY_THE, False, CS, 137, 2, 1952, 21, 6, 1951, 174),
    ComicBookInfo(Titles.STATUESQUE_SPENDTHRIFTS, STATUESQUE_SPENDTHRIFTS, False, CS, 138, 3, 1952, 12, 7, 1951, 175),
    ComicBookInfo(Titles.ROCKET_WING_SAVES_THE_DAY, ROCKET_WING_SAVES_THE_DAY, False, CS, 139, 4, 1952, 26, 7, 1951, 176),
    ComicBookInfo(Titles.GLADSTONES_TERRIBLE_SECRET, GLADSTONES_TERRIBLE_SECRET, False, CS, 140, 5, 1952, 23, 8, 1951, 177),
    ComicBookInfo(Titles.ONLY_A_POOR_OLD_MAN, ONLY_A_POOR_OLD_MAN, True, FC, 386, 3, 1952, 27, 9, 1951, 178),
    ComicBookInfo(Titles.OSOGOOD_SILVER_POLISH, OSOGOOD_SILVER_POLISH, False, FC, 386, 3, 1952, 27, 9, 1951, 179),
    ComicBookInfo(Titles.COFFEE_FOR_TWO, COFFEE_FOR_TWO, False, FC, 386, 3, 1952, 27, 9, 1951, 180),
    ComicBookInfo(Titles.SOUPLINE_EIGHT, SOUPLINE_EIGHT, False, FC, 386, 3, 1952, 27, 9, 1951, 181),
    ComicBookInfo(Titles.THINK_BOX_BOLLIX_THE, THINK_BOX_BOLLIX_THE, False, CS, 141, 6, 1952, 18, 10, 1951, 182),
    ComicBookInfo(Titles.GOLDEN_HELMET_THE, GOLDEN_HELMET_THE, True, FC, 408, 7, 1952, 3, 12, 1951, 183),
    ComicBookInfo(Titles.FULL_SERVICE_WINDOWS, FULL_SERVICE_WINDOWS, False, FC, 408, 7, 1952, 3, 1, 1952, 184),
    ComicBookInfo(Titles.RIGGED_UP_ROLLER, RIGGED_UP_ROLLER, False, FC, 408, 7, 1952, 3, 1, 1952, 185),
    ComicBookInfo(Titles.AWASH_IN_SUCCESS, AWASH_IN_SUCCESS, False, FC, 408, 7, 1952, 3, 1, 1952, 186),
    ComicBookInfo(Titles.HOUSEBOAT_HOLIDAY, HOUSEBOAT_HOLIDAY, False, CS, 142, 7, 1952, 10, 1, 1952, 187),
    ComicBookInfo(Titles.GEMSTONE_HUNTERS, GEMSTONE_HUNTERS, False, CS, 143, 8, 1952, 10, 1, 1952, 188),
    ComicBookInfo(Titles.GILDED_MAN_THE, GILDED_MAN_THE, True, FC, 422, 9, 1952, 31, 1, 1952, 189),
    ComicBookInfo(Titles.STABLE_PRICES, STABLE_PRICES, False, FC, 422, 9, 1952, 31, 1, 1952, 190),
    ComicBookInfo(Titles.ARMORED_RESCUE, ARMORED_RESCUE, False, FC, 422, 9, 1952, 31, 1, 1952, 191),
    ComicBookInfo(Titles.CRAFTY_CORNER, CRAFTY_CORNER, False, FC, 422, 9, 1952, 31, 1, 1952, 192),
    ComicBookInfo(Titles.SPENDING_MONEY, SPENDING_MONEY, False, CS, 144, 9, 1952, 21, 2, 1952, 193),
    ComicBookInfo(Titles.HYPNO_GUN_THE, HYPNO_GUN_THE, False, CS, 145, 10, 1952, 6, 3, 1952, 194),
    ComicBookInfo(Titles.TRICK_OR_TREAT, TRICK_OR_TREAT, True, DD, 26, 11, 1952, 31, 3, 1952, 195),
    ComicBookInfo(Titles.PRANK_ABOVE_A, PRANK_ABOVE_A, False, DD, 26, 11, 1952, 10, 4, 1952, 196),
    ComicBookInfo(Titles.FRIGHTFUL_FACE, FRIGHTFUL_FACE, False, DD, 26, 11, 1952, 10, 4, 1952, 197),
    ComicBookInfo(Titles.HOBBLIN_GOBLINS, HOBBLIN_GOBLINS, True, DD, 26, 11, 1952, 8, 5, 1952, 198),
    ComicBookInfo(Titles.OMELET, OMELET, False, CS, 146, 11, 1952, 15, 5, 1952, 199),
    ComicBookInfo(Titles.CHARITABLE_CHORE_A, CHARITABLE_CHORE_A, False, CS, 147, 12, 1952, 29, 5, 1952, 200),
    ComicBookInfo(Titles.TURKEY_WITH_ALL_THE_SCHEMINGS, TURKEY_WITH_ALL_THE_SCHEMINGS, False, CS, 148, 1, 1953, 12, 6, 1952, 201),
    ComicBookInfo(Titles.FLIP_DECISION, FLIP_DECISION, False, CS, 149, 2, 1953, 30, 6, 1952, 202),
    ComicBookInfo(Titles.MY_LUCKY_VALENTINE, MY_LUCKY_VALENTINE, False, CS, 150, 3, 1953, 30, 6, 1952, 203),
    ComicBookInfo(Titles.FARE_DELAY, FARE_DELAY, False, FC, 456, 3, 1953, 28, 8, 1952, 204),
    ComicBookInfo(Titles.SOMETHIN_FISHY_HERE, SOMETHIN_FISHY_HERE, True, FC, 456, 3, 1953, -1, 9, 1952, 205),
    ComicBookInfo(Titles.BACK_TO_THE_KLONDIKE, BACK_TO_THE_KLONDIKE, True, FC, 456, 3, 1953, 18, 9, 1952, 206),
    ComicBookInfo(Titles.MONEY_LADDER_THE, MONEY_LADDER_THE, False, FC, 456, 3, 1953, 16, 10, 1952, 207),
    ComicBookInfo(Titles.CHECKER_GAME_THE, CHECKER_GAME_THE, False, FC, 456, 3, 1953, 16, 10, 1952, 208),
    ComicBookInfo(Titles.EASTER_ELECTION_THE, EASTER_ELECTION_THE, False, CS, 151, 4, 1953, 23, 10, 1952, 209),
    ComicBookInfo(Titles.TALKING_DOG_THE, TALKING_DOG_THE, False, CS, 152, 5, 1953, 30, 10, 1952, 210),
    ComicBookInfo(Titles.WORM_WEARY, WORM_WEARY, False, CS, 153, 6, 1953, 27, 11, 1952, 211),
    ComicBookInfo(Titles.MUCH_ADO_ABOUT_QUACKLY_HALL, MUCH_ADO_ABOUT_QUACKLY_HALL, False, CS, 154, 7, 1953, 27, 11, 1952, 212),
    ComicBookInfo(Titles.SOME_HEIR_OVER_THE_RAINBOW, SOME_HEIR_OVER_THE_RAINBOW, False, CS, 155, 8, 1953, 24, 12, 1952, 213),
    ComicBookInfo(Titles.MASTER_RAINMAKER_THE, MASTER_RAINMAKER_THE, False, CS, 156, 9, 1953, 31, 12, 1952, 214),
    ComicBookInfo(Titles.MONEY_STAIRS_THE, MONEY_STAIRS_THE, False, CS, 157, 10, 1953, 15, 1, 1953, 215),
    ComicBookInfo(Titles.MILLION_DOLLAR_PIGEON, MILLION_DOLLAR_PIGEON, False, US, 7, 9, 1954, 25, 2, 1953, 216),
    ComicBookInfo(Titles.TEMPER_TAMPERING, TEMPER_TAMPERING, False, US, 7, 9, 1954, 25, 2, 1953, 217),
    ComicBookInfo(Titles.DINER_DILEMMA, DINER_DILEMMA, False, US, 7, 9, 1954, 25, 2, 1953, 218),
    ComicBookInfo(Titles.HORSERADISH_STORY_THE, HORSERADISH_STORY_THE, False, FC, 495, 9, 1953, 26, 2, 1953, 219),
    ComicBookInfo(Titles.ROUND_MONEY_BIN_THE, ROUND_MONEY_BIN_THE, False, FC, 495, 9, 1953, 26, 2, 1953, 220),
    ComicBookInfo(Titles.BARBER_COLLEGE, BARBER_COLLEGE, False, FC, 495, 9, 1953, 26, 2, 1953, 221),
    ComicBookInfo(Titles.FOLLOW_THE_RAINBOW, FOLLOW_THE_RAINBOW, False, FC, 495, 9, 1953, 26, 2, 1953, 222),
    ComicBookInfo(Titles.ITCHING_TO_SHARE, ITCHING_TO_SHARE, False, FC, 495, 9, 1953, 26, 2, 1953, 223),
    ComicBookInfo(Titles.WISPY_WILLIE, WISPY_WILLIE, False, CS, 159, 12, 1953, 6, 4, 1953, 224),
    ComicBookInfo(Titles.HAMMY_CAMEL_THE, HAMMY_CAMEL_THE, False, CS, 160, 1, 1954, 23, 4, 1953, 225),
    ComicBookInfo(Titles.BALLET_EVASIONS, BALLET_EVASIONS, False, US, 4, 12, 1953, 21, 5, 1953, 226),
    ComicBookInfo(Titles.CHEAPEST_WEIGH_THE, CHEAPEST_WEIGH_THE, False, US, 4, 12, 1953, 21, 5, 1953, 227),
    ComicBookInfo(Titles.BUM_STEER, BUM_STEER, False, US, 4, 12, 1953, 21, 5, 1953, 228),
    ComicBookInfo(Titles.BEE_BUMBLES, BEE_BUMBLES, False, CS, 158, 11, 1953, 26, 5, 1953, 229),
    ComicBookInfo(Titles.MENEHUNE_MYSTERY_THE, MENEHUNE_MYSTERY_THE, False, US, 4, 12, 1953, 28, 5, 1953, 230),
    ComicBookInfo(Titles.TURKEY_TROT_AT_ONE_WHISTLE, TURKEY_TROT_AT_ONE_WHISTLE, False, CS, 162, 3, 1954, 25, 6, 1953, 231),
    ComicBookInfo(Titles.RAFFLE_REVERSAL, RAFFLE_REVERSAL, False, CS, 163, 4, 1954, 2, 7, 1953, 232),
    ComicBookInfo(Titles.FIX_UP_MIX_UP, FIX_UP_MIX_UP, False, CS, 161, 2, 1954, 9, 7, 1953, 233),
    ComicBookInfo(Titles.SECRET_OF_ATLANTIS_THE, SECRET_OF_ATLANTIS_THE, False, US, 5, 3, 1954, 30, 7, 1953, 234),
    ComicBookInfo(Titles.HOSPITALITY_WEEK, HOSPITALITY_WEEK, False, US, 5, 3, 1954, 30, 7, 1953, 235),
    ComicBookInfo(Titles.MCDUCK_TAKES_A_DIVE, MCDUCK_TAKES_A_DIVE, False, US, 5, 3, 1954, 30, 7, 1953, 236),
    ComicBookInfo(Titles.SLIPPERY_SIPPER, SLIPPERY_SIPPER, False, US, 5, 3, 1954, 30, 7, 1953, 237),
    ComicBookInfo(Titles.FLOUR_FOLLIES, FLOUR_FOLLIES, False, CS, 164, 5, 1954, 27, 8, 1953, 238),
    ComicBookInfo(Titles.PRICE_OF_FAME_THE, PRICE_OF_FAME_THE, False, CS, 165, 6, 1954, 27, 8, 1953, 239),
    ComicBookInfo(Titles.MIDGETS_MADNESS, MIDGETS_MADNESS, False, CS, 166, 7, 1954, 17, 9, 1953, 240),
    ComicBookInfo(Titles.SALMON_DERBY, SALMON_DERBY, False, CS, 167, 8, 1954, 1, 10, 1953, 241),
    ComicBookInfo(Titles.TRALLA_LA, TRALLA_LA, False, US, 6, 6, 1954, 29, 10, 1953, 242),
    ComicBookInfo(Titles.OIL_THE_NEWS, OIL_THE_NEWS, False, US, 6, 6, 1954, 29, 10, 1953, 243),
    ComicBookInfo(Titles.DIG_IT, DIG_IT, False, US, 6, 6, 1954, 29, 10, 1953, 244),
    ComicBookInfo(Titles.MENTAL_FEE, MENTAL_FEE, False, US, 6, 6, 1954, 29, 10, 1953, 245),
    ComicBookInfo(Titles.OUTFOXED_FOX, OUTFOXED_FOX, False, US, 6, 6, 1954, 26, 11, 1953, 246),
    ComicBookInfo(Titles.CHELTENHAMS_CHOICE, CHELTENHAMS_CHOICE, False, CS, 168, 9, 1954, 3, 12, 1953, 247),
    ComicBookInfo(Titles.TRAVELLING_TRUANTS, TRAVELLING_TRUANTS, False, CS, 169, 10, 1954, 7, 1, 1954, 248),
    ComicBookInfo(Titles.RANTS_ABOUT_ANTS, RANTS_ABOUT_ANTS, False, CS, 170, 11, 1954, 7, 1, 1954, 249),
    ComicBookInfo(Titles.SEVEN_CITIES_OF_CIBOLA_THE, SEVEN_CITIES_OF_CIBOLA_THE, False, US, 7, 9, 1954, 28, 1, 1954, 250),
    ComicBookInfo(Titles.WRONG_NUMBER, WRONG_NUMBER, False, US, 7, 9, 1954, 25, 2, 1954, 251),
    ComicBookInfo(Titles.TOO_SAFE_SAFE, TOO_SAFE_SAFE, False, CS, 171, 12, 1954, 4, 3, 1954, 252),
    ComicBookInfo(Titles.SEARCH_FOR_THE_CUSPIDORIA, SEARCH_FOR_THE_CUSPIDORIA, False, CS, 172, 1, 1955, 18, 3, 1954, 253),
    ComicBookInfo(Titles.NEW_YEARS_REVOLUTIONS, NEW_YEARS_REVOLUTIONS, False, CS, 173, 2, 1955, 25, 3, 1954, 254),
    ComicBookInfo(Titles.ICEBOAT_TO_BEAVER_ISLAND, ICEBOAT_TO_BEAVER_ISLAND, False, CS, 174, 3, 1955, 22, 4, 1954, 255),
    ComicBookInfo(Titles.MYSTERIOUS_STONE_RAY_THE, MYSTERIOUS_STONE_RAY_THE, False, US, 8, 12, 1954, 20, 5, 1954, 256),
    ComicBookInfo(Titles.CAMPAIGN_OF_NOTE_A, CAMPAIGN_OF_NOTE_A, False, US, 8, 12, 1954, 10, 6, 1954, 257),
    ComicBookInfo(Titles.CASH_ON_THE_BRAIN, CASH_ON_THE_BRAIN, False, US, 8, 12, 1954, 10, 6, 1954, 258),
    ComicBookInfo(Titles.CLASSY_TAXI, CLASSY_TAXI, False, US, 8, 12, 1954, 10, 6, 1954, 259),
    ComicBookInfo(Titles.BLANKET_INVESTMENT, BLANKET_INVESTMENT, False, US, 8, 12, 1954, 10, 6, 1954, 260),
    ComicBookInfo(Titles.DAFFY_TAFFY_PULL_THE, DAFFY_TAFFY_PULL_THE, False, CS, 175, 4, 1955, 17, 6, 1954, 261),
    ComicBookInfo(Titles.TUCKERED_TIGER_THE, TUCKERED_TIGER_THE, True, US, 9, 3, 1955, 24, 6, 1954, 262),
    ComicBookInfo(Titles.DONALD_DUCK_TELLS_ABOUT_KITES, DONALD_DUCK_TELLS_ABOUT_KITES, True, KI, 2, 11, 1954, 8, 7, 1954, 263),
    ComicBookInfo(Titles.LEMMING_WITH_THE_LOCKET_THE, LEMMING_WITH_THE_LOCKET_THE, True, US, 9, 3, 1955, 15, 7, 1954, 264),
    ComicBookInfo(Titles.EASY_MOWING, EASY_MOWING, False, US, 9, 3, 1955, 22, 7, 1954, 265),
    ComicBookInfo(Titles.SKI_LIFT_LETDOWN, SKI_LIFT_LETDOWN, False, US, 9, 3, 1955, 22, 7, 1954, 266),
    ComicBookInfo(Titles.CAST_OF_THOUSANDS, CAST_OF_THOUSANDS, False, US, 9, 3, 1955, 22, 7, 1954, 267),
    ComicBookInfo(Titles.GHOST_SHERIFF_OF_LAST_GASP_THE, GHOST_SHERIFF_OF_LAST_GASP_THE, False, CS, 176, 5, 1955, 22, 7, 1954, 268),
    ComicBookInfo(Titles.DESCENT_INTERVAL_A, DESCENT_INTERVAL_A, False, CS, 177, 6, 1955, 29, 7, 1954, 269),
    ComicBookInfo(Titles.SECRET_OF_HONDORICA, SECRET_OF_HONDORICA, True, DD, 46, 3, 1956, 30, 9, 1954, 270),
    ComicBookInfo(Titles.DOGCATCHER_DUCK, DOGCATCHER_DUCK, False, DD, 45, 1, 1956, 14, 10, 1954, 271),
    ComicBookInfo(Titles.COURTSIDE_HEATING, COURTSIDE_HEATING, False, DD, 45, 1, 1956, 14, 10, 1954, 272),
    ComicBookInfo(Titles.POWER_PLOWING, POWER_PLOWING, False, DD, 45, 1, 1956, 14, 10, 1954, 273),
    ComicBookInfo(Titles.REMEMBER_THIS, REMEMBER_THIS, False, DD, 45, 1, 1956, 17, 10, 1954, 274),
    ComicBookInfo(Titles.FABULOUS_PHILOSOPHERS_STONE_THE, FABULOUS_PHILOSOPHERS_STONE_THE, True, US, 10, 6, 1955, 28, 10, 1954, 275),
    ComicBookInfo(Titles.HEIRLOOM_WATCH, HEIRLOOM_WATCH, True, US, 10, 6, 1955, 11, 11, 1954, 276),
    ComicBookInfo(Titles.DONALDS_RAUCOUS_ROLE, DONALDS_RAUCOUS_ROLE, False, CS, 178, 7, 1955, 26, 11, 1954, 277),
    ComicBookInfo(Titles.GOOD_CANOES_AND_BAD_CANOES, GOOD_CANOES_AND_BAD_CANOES, False, CS, 179, 8, 1955, 26, 11, 1954, 278),
    ComicBookInfo(Titles.DEEP_DECISION, DEEP_DECISION, False, US, 10, 6, 1955, 9, 12, 1954, 279),
    ComicBookInfo(Titles.SMASH_SUCCESS, SMASH_SUCCESS, False, US, 10, 6, 1955, 9, 12, 1954, 280),
    ComicBookInfo(Titles.TROUBLE_INDEMNITY, TROUBLE_INDEMNITY, False, CS, 180, 9, 1955, 6, 1, 1955, 281),
    ComicBookInfo(Titles.CHICKADEE_CHALLENGE_THE, CHICKADEE_CHALLENGE_THE, False, CS, 181, 10, 1955, 6, 1, 1955, 282),
    ComicBookInfo(Titles.UNORTHODOX_OX_THE, UNORTHODOX_OX_THE, False, CS, 182, 11, 1955, 6, 1, 1955, 283),
    ComicBookInfo(Titles.GREAT_STEAMBOAT_RACE_THE, GREAT_STEAMBOAT_RACE_THE, True, US, 11, 9, 1955, 3, 2, 1955, 284),
    ComicBookInfo(Titles.COME_AS_YOU_ARE, COME_AS_YOU_ARE, False, US, 11, 9, 1955, 24, 2, 1955, 285),
    ComicBookInfo(Titles.ROUNDABOUT_HANDOUT, ROUNDABOUT_HANDOUT, False, US, 11, 9, 1955, 24, 2, 1955, 286),
    ComicBookInfo(Titles.FAULTY_FORTUNE, FAULTY_FORTUNE, False, US, 14, 6, 1956, 24, 2, 1955, 287),
    ComicBookInfo(Titles.RICHES_RICHES_EVERYWHERE, RICHES_RICHES_EVERYWHERE, True, US, 11, 9, 1955, 10, 3, 1955, 288),
    ComicBookInfo(Titles.CUSTARD_GUN_THE, CUSTARD_GUN_THE, False, CS, 183, 12, 1955, 17, 3, 1955, 289),
    ComicBookInfo(Titles.THREE_UN_DUCKS, THREE_UN_DUCKS, False, CS, 184, 1, 1956, 31, 3, 1955, 290),
    ComicBookInfo(Titles.SECRET_RESOLUTIONS, SECRET_RESOLUTIONS, False, CS, 185, 2, 1956, 21, 4, 1955, 291),
    ComicBookInfo(Titles.ICE_TAXIS_THE, ICE_TAXIS_THE, False, CS, 186, 3, 1956, 21, 4, 1955, 292),
    ComicBookInfo(Titles.SEARCHING_FOR_A_SUCCESSOR, SEARCHING_FOR_A_SUCCESSOR, False, CS, 187, 4, 1956, 28, 4, 1955, 293),
    ComicBookInfo(Titles.OLYMPIC_HOPEFUL_THE, OLYMPIC_HOPEFUL_THE, False, CS, 188, 5, 1956, 28, 4, 1955, 294),
    ComicBookInfo(Titles.GOLDEN_FLEECING_THE, GOLDEN_FLEECING_THE, True, US, 12, 12, 1955, 2, 6, 1955, 295),
    ComicBookInfo(Titles.WATT_AN_OCCASION, WATT_AN_OCCASION, False, US, 12, 12, 1955, 2, 6, 1955, 296),
    ComicBookInfo(Titles.DOUGHNUT_DARE, DOUGHNUT_DARE, False, US, 12, 12, 1955, 2, 6, 1955, 297),
    ComicBookInfo(Titles.SWEAT_DEAL_A, SWEAT_DEAL_A, False, US, 12, 12, 1955, 2, 6, 1955, 298),
    ComicBookInfo(Titles.GOPHER_GOOF_UPS, GOPHER_GOOF_UPS, False, CS, 189, 6, 1956, 30, 6, 1955, 299),
    ComicBookInfo(Titles.IN_THE_SWIM, IN_THE_SWIM, False, CS, 190, 7, 1956, 14, 7, 1955, 300),
    ComicBookInfo(Titles.LAND_BENEATH_THE_GROUND, LAND_BENEATH_THE_GROUND, True, US, 13, 3, 1956, 18, 8, 1955, 301),
    ComicBookInfo(Titles.TRAPPED_LIGHTNING, TRAPPED_LIGHTNING, False, US, 13, 3, 1956, 1, 9, 1955, 302),
    ComicBookInfo(Titles.ART_OF_SECURITY_THE, ART_OF_SECURITY_THE, False, US, 13, 3, 1956, 1, 9, 1955, 303),
    ComicBookInfo(Titles.FASHION_FORECAST, FASHION_FORECAST, False, US, 13, 3, 1956, 1, 9, 1955, 304),
    ComicBookInfo(Titles.MUSH, MUSH, False, US, 13, 3, 1956, 1, 9, 1955, 305),
    ComicBookInfo(Titles.CAMPING_CONFUSION, CAMPING_CONFUSION, False, CS, 191, 8, 1956, 1, 9, 1955, 306),
    ComicBookInfo(Titles.MASTER_THE, MASTER_THE, False, CS, 192, 9, 1956, 22, 9, 1955, 307),
    ComicBookInfo(Titles.WHALE_OF_A_STORY_A, WHALE_OF_A_STORY_A, False, CS, 193, 10, 1956, 29, 9, 1955, 308),
    ComicBookInfo(Titles.SMOKE_WRITER_IN_THE_SKY, SMOKE_WRITER_IN_THE_SKY, False, CS, 194, 11, 1956, 29, 9, 1955, 309),
    ComicBookInfo(Titles.INVENTOR_OF_ANYTHING, INVENTOR_OF_ANYTHING, True, US, 14, 6, 1956, 1, 10, 1955, 310),
    ComicBookInfo(Titles.LOST_CROWN_OF_GENGHIS_KHAN_THE, LOST_CROWN_OF_GENGHIS_KHAN_THE, True, US, 14, 6, 1956, 3, 11, 1955, 311),
    ComicBookInfo(Titles.LUNCHEON_LAMENT, LUNCHEON_LAMENT, False, US, 14, 6, 1956, 17, 11, 1955, 312),
    ComicBookInfo(Titles.RUNAWAY_TRAIN_THE, RUNAWAY_TRAIN_THE, False, CS, 195, 12, 1956, 23, 11, 1955, 313),
    ComicBookInfo(Titles.GOLD_RUSH, GOLD_RUSH, False, US, 14, 6, 1956, 8, 12, 1955, 314),
    ComicBookInfo(Titles.FIREFLIES_ARE_FREE, FIREFLIES_ARE_FREE, False, US, 14, 6, 1956, 8, 12, 1955, 315),
    ComicBookInfo(Titles.EARLY_TO_BUILD, EARLY_TO_BUILD, False, US, 17, 3, 1957, 8, 12, 1955, 316),
    ComicBookInfo(Titles.STATUES_OF_LIMITATIONS, STATUES_OF_LIMITATIONS, False, CS, 196, 1, 1957, 22, 12, 1955, 317),
    ComicBookInfo(Titles.BORDERLINE_HERO, BORDERLINE_HERO, False, CS, 197, 2, 1957, 5, 1, 1956, 318),
    ComicBookInfo(Titles.SECOND_RICHEST_DUCK_THE, SECOND_RICHEST_DUCK_THE, True, US, 15, 9, 1956, 2, 2, 1956, 319),
    ComicBookInfo(Titles.MIGRATING_MILLIONS, MIGRATING_MILLIONS, False, US, 15, 9, 1956, 9, 2, 1956, 320),
    ComicBookInfo(Titles.CAT_BOX_THE, CAT_BOX_THE, False, US, 15, 9, 1956, 9, 2, 1956, 321),
    ComicBookInfo(Titles.CHINA_SHOP_SHAKEUP, CHINA_SHOP_SHAKEUP, False, US, 17, 3, 1957, 13, 2, 1956, 322),
    ComicBookInfo(Titles.BUFFO_OR_BUST, BUFFO_OR_BUST, False, US, 15, 9, 1956, 23, 2, 1956, 323),
    ComicBookInfo(Titles.POUND_FOR_SOUND, POUND_FOR_SOUND, False, US, 15, 9, 1956, 23, 2, 1956, 324),
    ComicBookInfo(Titles.FERTILE_ASSETS, FERTILE_ASSETS, False, US, 16, 12, 1956, 23, 2, 1956, 325),
    ComicBookInfo(Titles.GRANDMAS_PRESENT, GRANDMAS_PRESENT, True, CP, 8, 12, 1956, 1, 3, 1956, 326),
    ComicBookInfo(Titles.KNIGHT_IN_SHINING_ARMOR, KNIGHT_IN_SHINING_ARMOR, False, CS, 198, 3, 1957, 15, 3, 1956, 327),
    ComicBookInfo(Titles.FEARSOME_FLOWERS, FEARSOME_FLOWERS, False, CS, 214, 7, 1958, 15, 3, 1956, 328),
    ComicBookInfo(Titles.DONALDS_PET_SERVICE, DONALDS_PET_SERVICE, False, CS, 200, 5, 1957, 5, 4, 1956, 329),
    ComicBookInfo(Titles.BACK_TO_LONG_AGO, BACK_TO_LONG_AGO, True, US, 16, 12, 1956, 26, 4, 1956, 330),
    ComicBookInfo(Titles.COLOSSALEST_SURPRISE_QUIZ_SHOW_THE, COLOSSALEST_SURPRISE_QUIZ_SHOW_THE, False, US, 16, 12, 1956, 17, 5, 1956, 331),
    ComicBookInfo(Titles.FORECASTING_FOLLIES, FORECASTING_FOLLIES, False, US, 16, 12, 1956, 17, 5, 1956, 332),
    ComicBookInfo(Titles.BACKYARD_BONANZA, BACKYARD_BONANZA, False, US, 16, 12, 1956, 24, 5, 1956, 333),
    ComicBookInfo(Titles.ALL_SEASON_HAT, ALL_SEASON_HAT, False, DD, 51, 1, 1957, 24, 5, 1956, 334),
    ComicBookInfo(Titles.EYES_HAVE_IT_THE, EYES_HAVE_IT_THE, False, US, 17, 3, 1957, 24, 5, 1956, 335),
    ComicBookInfo(Titles.RELATIVE_REACTION, RELATIVE_REACTION, False, US, 18, 6, 1957, 24, 5, 1956, 336),
    ComicBookInfo(Titles.SECRET_BOOK_THE, SECRET_BOOK_THE, False, US, 31, 9, 1960, 24, 5, 1956, 337),
    ComicBookInfo(Titles.TREE_TRICK, TREE_TRICK, False, US, 33, 3, 1961, 24, 5, 1956, 338),
    ComicBookInfo(Titles.IN_KAKIMAW_COUNTRY, IN_KAKIMAW_COUNTRY, False, CS, 202, 7, 1957, 31, 5, 1956, 339),
    ComicBookInfo(Titles.LOST_PEG_LEG_MINE_THE, LOST_PEG_LEG_MINE_THE, True, DD, 52, 3, 1957, 14, 6, 1956, 340),
    ComicBookInfo(Titles.LOSING_FACE, LOSING_FACE, False, CS, 204, 9, 1957, 21, 6, 1956, 341),
    ComicBookInfo(Titles.DAY_DUCKBURG_GOT_DYED_THE, DAY_DUCKBURG_GOT_DYED_THE, False, CS, 201, 6, 1957, 5, 7, 1956, 342),
    ComicBookInfo(Titles.PICNIC, PICNIC, True, VP, 8, 7, 1957, 12, 7, 1956, 343),
    ComicBookInfo(Titles.FISHING_MYSTERY, FISHING_MYSTERY, False, US, 17, 3, 1957, -1, 8, 1956, 344),
    ComicBookInfo(Titles.COLD_BARGAIN_A, COLD_BARGAIN_A, True, US, 17, 3, 1957, 2, 8, 1956, 345),
    ComicBookInfo(Titles.GYROS_IMAGINATION_INVENTION, GYROS_IMAGINATION_INVENTION, False, CS, 199, 4, 1957, 20, 9, 1956, 346),
    ComicBookInfo(Titles.RED_APPLE_SAP, RED_APPLE_SAP, False, CS, 205, 10, 1957, 25, 9, 1956, 347),
    ComicBookInfo(Titles.SURE_FIRE_GOLD_FINDER_THE, SURE_FIRE_GOLD_FINDER_THE, False, US, 18, 6, 1957, 11, 10, 1956, 348),
    ComicBookInfo(Titles.SPECIAL_DELIVERY, SPECIAL_DELIVERY, False, CS, 203, 8, 1957, 11, 10, 1956, 349),
    ComicBookInfo(Titles.CODE_OF_DUCKBURG_THE, CODE_OF_DUCKBURG_THE, False, CS, 208, 1, 1958, 18, 10, 1956, 350),
    ComicBookInfo(Titles.LAND_OF_THE_PYGMY_INDIANS, LAND_OF_THE_PYGMY_INDIANS, True, US, 18, 6, 1957, 15, 11, 1956, 351),
    ComicBookInfo(Titles.NET_WORTH, NET_WORTH, False, US, 18, 6, 1957, 15, 11, 1956, 352),
    ComicBookInfo(Titles.FORBIDDEN_VALLEY, FORBIDDEN_VALLEY, True, DD, 54, 7, 1957, 13, 12, 1956, 353),
    ComicBookInfo(Titles.FANTASTIC_RIVER_RACE_THE, FANTASTIC_RIVER_RACE_THE, False, USGTD, 1, 8, 1957, 10, 1, 1957, 354),
    ComicBookInfo(Titles.SAGMORE_SPRINGS_HOTEL, SAGMORE_SPRINGS_HOTEL, False, CS, 206, 11, 1957, 17, 1, 1957, 355),
    ComicBookInfo(Titles.TENDERFOOT_TRAP_THE, TENDERFOOT_TRAP_THE, False, CS, 207, 12, 1957, 17, 1, 1957, 356),
    ComicBookInfo(Titles.MINES_OF_KING_SOLOMON_THE, MINES_OF_KING_SOLOMON_THE, True, US, 19, 9, 1957, 15, 2, 1957, 357),
    ComicBookInfo(Titles.GYRO_BUILDS_A_BETTER_HOUSE, GYRO_BUILDS_A_BETTER_HOUSE, False, US, 19, 9, 1957, 28, 2, 1957, 358),
    ComicBookInfo(Titles.HISTORY_TOSSED, HISTORY_TOSSED, False, US, 19, 9, 1957, 28, 2, 1957, 359),
    ComicBookInfo(Titles.BLACK_PEARLS_OF_TABU_YAMA_THE, BLACK_PEARLS_OF_TABU_YAMA_THE, False, CID, 1, 10, 1957, 14, 3, 1957, 360),
    ComicBookInfo(Titles.AUGUST_ACCIDENT, AUGUST_ACCIDENT, True, MMA, 1, 12, 1957, 21, 3, 1957, 361),
    ComicBookInfo(Titles.SEPTEMBER_SCRIMMAGE, SEPTEMBER_SCRIMMAGE, True, MMA, 1, 12, 1957, 21, 3, 1957, 362),
    ComicBookInfo(Titles.WISHING_STONE_ISLAND, WISHING_STONE_ISLAND, False, CS, 211, 4, 1958, 18, 4, 1957, 363),
    ComicBookInfo(Titles.ROCKET_RACE_AROUND_THE_WORLD, ROCKET_RACE_AROUND_THE_WORLD, False, CS, 212, 5, 1958, 18, 4, 1957, 364),
    ComicBookInfo(Titles.ROSCOE_THE_ROBOT, ROSCOE_THE_ROBOT, False, US, 20, 12, 1957, 25, 4, 1957, 365),
    ComicBookInfo(Titles.CITY_OF_GOLDEN_ROOFS, CITY_OF_GOLDEN_ROOFS, True, US, 20, 12, 1957, 23, 5, 1957, 366),
    ComicBookInfo(Titles.GETTING_THOR, GETTING_THOR, False, US, 21, 3, 1958, 6, 6, 1957, 367),
    ComicBookInfo(Titles.DOGGED_DETERMINATION, DOGGED_DETERMINATION, False, US, 21, 3, 1958, 6, 6, 1957, 368),
    ComicBookInfo(Titles.FORGOTTEN_PRECAUTION, FORGOTTEN_PRECAUTION, False, US, 21, 3, 1958, 6, 6, 1957, 369),
    ComicBookInfo(Titles.BIG_BOBBER_THE, BIG_BOBBER_THE, False, US, 33, 3, 1961, 6, 6, 1957, 370),
    ComicBookInfo(Titles.WINDFALL_OF_THE_MIND, WINDFALL_OF_THE_MIND, False, US, 21, 3, 1958, 20, 6, 1957, 371),
    ComicBookInfo(Titles.TITANIC_ANTS_THE, TITANIC_ANTS_THE, True, DD, 60, 7, 1958, 20, 6, 1957, 372),
    ComicBookInfo(Titles.RESCUE_ENHANCEMENT, RESCUE_ENHANCEMENT, False, US, 20, 12, 1957, 25, 7, 1957, 373),
    ComicBookInfo(Titles.PERSISTENT_POSTMAN_THE, PERSISTENT_POSTMAN_THE, False, CS, 209, 2, 1958, 25, 7, 1957, 374),
    ComicBookInfo(Titles.HALF_BAKED_BAKER_THE, HALF_BAKED_BAKER_THE, False, CS, 210, 3, 1958, 25, 7, 1957, 375),
    ComicBookInfo(Titles.DODGING_MISS_DAISY, DODGING_MISS_DAISY, False, CS, 213, 6, 1958, 25, 7, 1957, 376),
    ComicBookInfo(Titles.MONEY_WELL_THE, MONEY_WELL_THE, True, US, 21, 3, 1958, 22, 8, 1957, 377),
    ComicBookInfo(Titles.MILKMAN_THE, MILKMAN_THE, False, CS, 215, 8, 1958, 19, 9, 1957, 378),
    ComicBookInfo(Titles.MOCKING_BIRD_RIDGE, MOCKING_BIRD_RIDGE, False, CS, 215, 8, 1958, 19, 9, 1957, 379),
    ComicBookInfo(Titles.OLD_FROGGIE_CATAPULT, OLD_FROGGIE_CATAPULT, False, CS, 216, 9, 1958, 1, 10, 1957, 380),
    ComicBookInfo(Titles.GOING_TO_PIECES, GOING_TO_PIECES, False, US, 22, 6, 1958, 31, 10, 1957, 381),
    ComicBookInfo(Titles.HIGH_RIDER, HIGH_RIDER, False, US, 22, 6, 1958, 31, 10, 1957, 382),
    ComicBookInfo(Titles.THAT_SINKING_FEELING, THAT_SINKING_FEELING, False, US, 22, 6, 1958, 31, 10, 1957, 383),
    ComicBookInfo(Titles.WATER_SKI_RACE, WATER_SKI_RACE, False, DD, 60, 7, 1958, 31, 10, 1957, 384),
    ComicBookInfo(Titles.BALMY_SWAMI_THE, BALMY_SWAMI_THE, False, US, 31, 9, 1960, 31, 10, 1957, 385),
    ComicBookInfo(Titles.WINDY_STORY_THE, WINDY_STORY_THE, False, US, 37, 3, 1962, 31, 10, 1957, 386),
    ComicBookInfo(Titles.GOLDEN_RIVER_THE, GOLDEN_RIVER_THE, True, US, 22, 6, 1958, 21, 11, 1957, 387),
    ComicBookInfo(Titles.MOOLA_ON_THE_MOVE, MOOLA_ON_THE_MOVE, False, US, 23, 9, 1958, 5, 12, 1957, 388),
    ComicBookInfo(Titles.THUMBS_UP, THUMBS_UP, False, US, 33, 3, 1961, 5, 12, 1957, 389),
    # Typo in original US issue number, was 22, should be 24 for Dec 1958
    ComicBookInfo(Titles.KNOW_IT_ALL_MACHINE_THE, KNOW_IT_ALL_MACHINE_THE, False, US, 22, 3, 1958, 12, 12, 1957, 390),
    ComicBookInfo(Titles.STRANGE_SHIPWRECKS_THE, STRANGE_SHIPWRECKS_THE, False, US, 23, 9, 1958, 31, 12, 1957, 391),
    ComicBookInfo(Titles.FABULOUS_TYCOON_THE, FABULOUS_TYCOON_THE, False, US, 23, 9, 1958, 9, 1, 1958, 392),
    ComicBookInfo(Titles.GYRO_GOES_FOR_A_DIP, GYRO_GOES_FOR_A_DIP, False, US, 23, 9, 1958, 9, 1, 1958, 393),
    ComicBookInfo(Titles.BILL_WIND, BILL_WIND, False, US, 25, 3, 1959, 10, 1, 1958, 394),
    ComicBookInfo(Titles.TWENTY_FOUR_CARAT_MOON_THE, TWENTY_FOUR_CARAT_MOON_THE, False, US, 24, 12, 1958, 20, 1, 1958, 395),
    ComicBookInfo(Titles.HOUSE_ON_CYCLONE_HILL_THE, HOUSE_ON_CYCLONE_HILL_THE, False, US, 24, 12, 1958, 20, 1, 1958, 396),
    ComicBookInfo(Titles.NOBLE_PORPOISES, NOBLE_PORPOISES, False, CS, 218, 11, 1958, 14, 2, 1958, 397),
    ComicBookInfo(Titles.MAGIC_INK_THE, MAGIC_INK_THE, False, US, 24, 12, 1958, 17, 2, 1958, 398),
    ComicBookInfo(Titles.SLEEPIES_THE, SLEEPIES_THE, False, DD, 81, 1, 1962, 17, 2, 1958, 399),
    ComicBookInfo(Titles.TRACKING_SANDY, TRACKING_SANDY, False, CS, 221, 2, 1959, 5, 3, 1958, 400),
    ComicBookInfo(Titles.LITTLEST_CHICKEN_THIEF_THE, LITTLEST_CHICKEN_THIEF_THE, False, CS, 219, 12, 1958, 12, 3, 1958, 401),
    ComicBookInfo(Titles.BEACHCOMBERS_PICNIC_THE, BEACHCOMBERS_PICNIC_THE, False, CS, 224, 5, 1959, 19, 3, 1958, 402),
    # US issue 23 was Sep 1958
    ComicBookInfo(Titles.LIGHTS_OUT, LIGHTS_OUT, False, US, 23, 9, 1958, 25, 3, 1958, 403),
    ComicBookInfo(Titles.DRAMATIC_DONALD, DRAMATIC_DONALD, False, CS, 217, 10, 1958, 4, 4, 1958, 404),
    ComicBookInfo(Titles.CHRISTMAS_IN_DUCKBURG, CHRISTMAS_IN_DUCKBURG, True, CP, 9, 12, 1958, 6, 4, 1958, 405),
    ComicBookInfo(Titles.ROCKET_ROASTED_CHRISTMAS_TURKEY, ROCKET_ROASTED_CHRISTMAS_TURKEY, False, CS, 220, 1, 1959, 14, 4, 1958, 406),
    ComicBookInfo(Titles.MASTER_MOVER_THE, MASTER_MOVER_THE, False, CS, 222, 3, 1959, 14, 4, 1958, 407),
    ComicBookInfo(Titles.SPRING_FEVER, SPRING_FEVER, False, CS, 223, 4, 1959, 18, 4, 1958, 408),
    ComicBookInfo(Titles.FLYING_DUTCHMAN_THE, FLYING_DUTCHMAN_THE, False, US, 25, 3, 1959, 20, 4, 1958, 409),
    ComicBookInfo(Titles.PYRAMID_SCHEME, PYRAMID_SCHEME, False, US, 25, 3, 1959, 20, 4, 1958, 410),
    ComicBookInfo(Titles.WISHING_WELL_THE, WISHING_WELL_THE, False, US, 25, 3, 1959, 9, 6, 1958, 411),
    ComicBookInfo(Titles.IMMOVABLE_MISER, IMMOVABLE_MISER, False, US, 25, 3, 1959, 9, 6, 1958, 412),
    ComicBookInfo(Titles.RETURN_TO_PIZEN_BLUFF, RETURN_TO_PIZEN_BLUFF, False, US, 26, 6, 1959, 16, 6, 1958, 413),
    ComicBookInfo(Titles.KRANKENSTEIN_GYRO, KRANKENSTEIN_GYRO, False, US, 26, 6, 1959, 16, 6, 1958, 414),
    ComicBookInfo(Titles.MONEY_CHAMP_THE, MONEY_CHAMP_THE, False, US, 27, 9, 1959, 12, 7, 1958, 415),
    ComicBookInfo(Titles.HIS_HANDY_ANDY, HIS_HANDY_ANDY, False, US, 27, 9, 1959, 12, 7, 1958, 416),
    ComicBookInfo(Titles.FIREFLY_TRACKER_THE, FIREFLY_TRACKER_THE, False, US, 27, 9, 1959, 15, 7, 1958, 417),
    ComicBookInfo(Titles.PRIZE_OF_PIZARRO_THE, PRIZE_OF_PIZARRO_THE, False, US, 26, 6, 1959, 11, 8, 1958, 418),
    ComicBookInfo(Titles.LOVELORN_FIREMAN_THE, LOVELORN_FIREMAN_THE, False, CS, 225, 6, 1959, 15, 8, 1958, 419),
    ComicBookInfo(Titles.KITTY_GO_ROUND, KITTY_GO_ROUND, False, US, 25, 3, 1959, 9, 9, 1958, 420),
    ComicBookInfo(Titles.POOR_LOSER, POOR_LOSER, False, DD, 79, 9, 1961, 9, 9, 1958, 421),
    ComicBookInfo(Titles.FLOATING_ISLAND_THE, FLOATING_ISLAND_THE, False, CS, 226, 7, 1959, 16, 9, 1958, 422),
    ComicBookInfo(Titles.CRAWLS_FOR_CASH, CRAWLS_FOR_CASH, False, US, 27, 9, 1959, 1, 10, 1958, 423),
    ComicBookInfo(Titles.BLACK_FOREST_RESCUE_THE, BLACK_FOREST_RESCUE_THE, False, CS, 227, 8, 1959, 10, 10, 1958, 424),
    ComicBookInfo(Titles.GOOD_DEEDS_THE, GOOD_DEEDS_THE, False, CS, 229, 10, 1959, 15, 10, 1958, 425),
    ComicBookInfo(Titles.BLACK_WEDNESDAY, BLACK_WEDNESDAY, False, CS, 230, 11, 1959, 30, 10, 1958, 426),
    ComicBookInfo(Titles.ALL_CHOKED_UP, ALL_CHOKED_UP, False, US, 23, 9, 1958, 31, 10, 1958, 427),
    ComicBookInfo(Titles.WATCHFUL_PARENTS_THE, WATCHFUL_PARENTS_THE, False, CS, 228, 9, 1959, 10, 11, 1958, 428),
    ComicBookInfo(Titles.WAX_MUSEUM_THE, WAX_MUSEUM_THE, False, CS, 231, 12, 1959, 17, 11, 1958, 429),
    ComicBookInfo(Titles.PAUL_BUNYAN_MACHINE_THE, PAUL_BUNYAN_MACHINE_THE, False, US, 28, 12, 1959, 15, 12, 1958, 430),
    ComicBookInfo(Titles.KNIGHTS_OF_THE_FLYING_SLEDS, KNIGHTS_OF_THE_FLYING_SLEDS, False, CS, 233, 2, 1960, 2, 1, 1959, 431),
    ComicBookInfo(Titles.WITCHING_STICK_THE, WITCHING_STICK_THE, False, US, 28, 12, 1959, 16, 1, 1959, 432),
    ComicBookInfo(Titles.INVENTORS_CONTEST_THE, INVENTORS_CONTEST_THE, False, US, 28, 12, 1959, 16, 1, 1959, 433),
    ComicBookInfo(Titles.JUNGLE_HI_JINKS, JUNGLE_HI_JINKS, True, SF, 2, 8, 1959, 30, 1, 1959, 434),
    ComicBookInfo(Titles.FLYING_FARMHAND_THE, FLYING_FARMHAND_THE, True, FC, 1010, 7, 1959, 6, 3, 1959, 435),
    ComicBookInfo(Titles.HONEY_OF_A_HEN_A, HONEY_OF_A_HEN_A, True, FC, 1010, 7, 1959, 6, 3, 1959, 436),
    ComicBookInfo(Titles.WEATHER_WATCHERS_THE, WEATHER_WATCHERS_THE, True, FC, 1010, 7, 1959, 6, 3, 1959, 437),
    ComicBookInfo(Titles.SHEEPISH_COWBOYS_THE, SHEEPISH_COWBOYS_THE, True, FC, 1010, 7, 1959, 6, 3, 1959, 438),
    ComicBookInfo(Titles.OODLES_OF_OOMPH, OODLES_OF_OOMPH, False, US, 29, 3, 1960, 20, 4, 1959, 439),
    ComicBookInfo(Titles.MASTER_GLASSER_THE, MASTER_GLASSER_THE, False, DD, 68, 11, 1959, 20, 5, 1959, 440),
    ComicBookInfo(Titles.MONEY_HAT_THE, MONEY_HAT_THE, False, US, 28, 12, 1959, 20, 5, 1959, 441),
    ComicBookInfo(Titles.ISLAND_IN_THE_SKY, ISLAND_IN_THE_SKY, False, US, 29, 3, 1960, 15, 6, 1959, 442),
    ComicBookInfo(Titles.UNDER_THE_POLAR_ICE, UNDER_THE_POLAR_ICE, False, CS, 232, 1, 1960, 11, 7, 1959, 443),
    ComicBookInfo(Titles.HOUND_OF_THE_WHISKERVILLES, HOUND_OF_THE_WHISKERVILLES, False, US, 29, 3, 1960, 11, 7, 1959, 444),
    ComicBookInfo(Titles.RIDING_THE_PONY_EXPRESS, RIDING_THE_PONY_EXPRESS, False, CS, 234, 3, 1960, 17, 8, 1959, 445),
    ComicBookInfo(Titles.WANT_TO_BUY_AN_ISLAND, WANT_TO_BUY_AN_ISLAND, False, CS, 235, 4, 1960, 28, 9, 1959, 446),
    ComicBookInfo(Titles.FROGGY_FARMER, FROGGY_FARMER, False, CS, 236, 5, 1960, 14, 10, 1959, 447),
    ComicBookInfo(Titles.PIPELINE_TO_DANGER, PIPELINE_TO_DANGER, False, US, 30, 6, 1960, 13, 11, 1959, 448),
    ComicBookInfo(Titles.YOICKS_THE_FOX, YOICKS_THE_FOX, False, US, 30, 6, 1960, 9, 12, 1959, 449),
    ComicBookInfo(Titles.WAR_PAINT, WAR_PAINT, False, US, 30, 6, 1960, 9, 12, 1959, 450),
    ComicBookInfo(Titles.DOG_SITTER_THE, DOG_SITTER_THE, False, CS, 238, 7, 1960, 7, 1, 1960, 451),
    ComicBookInfo(Titles.MYSTERY_OF_THE_LOCH, MYSTERY_OF_THE_LOCH, False, CS, 237, 6, 1960, 15, 1, 1960, 452),
    ComicBookInfo(Titles.VILLAGE_BLACKSMITH_THE, VILLAGE_BLACKSMITH_THE, False, CS, 239, 8, 1960, 15, 1, 1960, 453),
    ComicBookInfo(Titles.FRAIDY_FALCON_THE, FRAIDY_FALCON_THE, False, CS, 240, 9, 1960, 15, 1, 1960, 454),
    ComicBookInfo(Titles.ALL_AT_SEA, ALL_AT_SEA, False, US, 31, 9, 1960, 12, 2, 1960, 455),
    ComicBookInfo(Titles.FISHY_WARDEN, FISHY_WARDEN, False, US, 31, 9, 1960, 16, 2, 1960, 456),
    ComicBookInfo(Titles.TWO_WAY_LUCK, TWO_WAY_LUCK, False, US, 31, 9, 1960, 26, 2, 1960, 457),
    ComicBookInfo(Titles.BALLOONATICS, BALLOONATICS, False, CS, 242, 11, 1960, 11, 3, 1960, 458),
    ComicBookInfo(Titles.TURKEY_TROUBLE, TURKEY_TROUBLE, False, CS, 243, 12, 1960, 11, 4, 1960, 459),
    ComicBookInfo(Titles.MISSILE_FIZZLE, MISSILE_FIZZLE, False, CS, 244, 1, 1961, 11, 4, 1960, 460),
    ComicBookInfo(Titles.ROCKS_TO_RICHES, ROCKS_TO_RICHES, False, CS, 241, 10, 1960, 18, 4, 1960, 461),
    ComicBookInfo(Titles.SITTING_HIGH, SITTING_HIGH, False, CS, 245, 2, 1961, 18, 4, 1960, 462),
    ComicBookInfo(Titles.THATS_NO_FABLE, THATS_NO_FABLE, False, US, 32, 12, 1960, 12, 5, 1960, 463),
    ComicBookInfo(Titles.CLOTHES_MAKE_THE_DUCK, CLOTHES_MAKE_THE_DUCK, False, US, 32, 12, 1960, 17, 5, 1960, 464),
    ComicBookInfo(Titles.THAT_SMALL_FEELING, THAT_SMALL_FEELING, False, US, 32, 12, 1960, 13, 6, 1960, 465),
    ComicBookInfo(Titles.MADCAP_MARINER_THE, MADCAP_MARINER_THE, False, CS, 247, 4, 1961, 11, 7, 1960, 466),
    ComicBookInfo(Titles.TERRIBLE_TOURIST, TERRIBLE_TOURIST, False, CS, 248, 5, 1961, 11, 7, 1960, 467),
    ComicBookInfo(Titles.THRIFT_GIFT_A, THRIFT_GIFT_A, False, US, 32, 12, 1960, 18, 7, 1960, 468),
    ComicBookInfo(Titles.LOST_FRONTIER, LOST_FRONTIER, False, CS, 246, 3, 1961, 18, 7, 1960, 469),
    ComicBookInfo(Titles.YOU_CANT_WIN, YOU_CANT_WIN, False, US, 33, 3, 1961, 15, 8, 1960, 470),
    ComicBookInfo(Titles.BILLIONS_IN_THE_HOLE, BILLIONS_IN_THE_HOLE, False, US, 33, 3, 1961, 3, 9, 1960, 471),
    ComicBookInfo(Titles.BONGO_ON_THE_CONGO, BONGO_ON_THE_CONGO, False, US, 33, 3, 1961, 12, 9, 1960, 472),
    ComicBookInfo(Titles.STRANGER_THAN_FICTION, STRANGER_THAN_FICTION, False, CS, 249, 6, 1961, 31, 10, 1960, 473),
    ComicBookInfo(Titles.BOXED_IN, BOXED_IN, False, CS, 250, 7, 1961, 12, 11, 1960, 474),
    ComicBookInfo(Titles.CHUGWAGON_DERBY, CHUGWAGON_DERBY, False, US, 34, 6, 1961, 16, 11, 1960, 475),
    ComicBookInfo(Titles.MYTHTIC_MYSTERY, MYTHTIC_MYSTERY, False, US, 34, 6, 1961, 10, 12, 1960, 476),
    ComicBookInfo(Titles.WILY_RIVAL, WILY_RIVAL, False, US, 34, 6, 1961, 10, 12, 1960, 477),
    ComicBookInfo(Titles.DUCK_LUCK, DUCK_LUCK, False, CS, 251, 8, 1961, 28, 12, 1960, 478),
    ComicBookInfo(Titles.MR_PRIVATE_EYE, MR_PRIVATE_EYE, False, CS, 252, 9, 1961, 10, 1, 1961, 479),
    ComicBookInfo(Titles.HOUND_HOUNDER, HOUND_HOUNDER, False, CS, 253, 10, 1961, 16, 1, 1961, 480),
    ComicBookInfo(Titles.GOLDEN_NUGGET_BOAT_THE, GOLDEN_NUGGET_BOAT_THE, False, US, 35, 9, 1961, 16, 2, 1961, 481),
    ComicBookInfo(Titles.FAST_AWAY_CASTAWAY, FAST_AWAY_CASTAWAY, False, US, 35, 9, 1961, 24, 2, 1961, 482),
    ComicBookInfo(Titles.GIFT_LION, GIFT_LION, False, US, 35, 9, 1961, 24, 2, 1961, 483),
    ComicBookInfo(Titles.JET_WITCH, JET_WITCH, False, CS, 254, 11, 1961, 13, 3, 1961, 484),
    ComicBookInfo(Titles.BOAT_BUSTER, BOAT_BUSTER, False, CS, 255, 12, 1961, 20, 3, 1961, 485),
    ComicBookInfo(Titles.MIDAS_TOUCH_THE, MIDAS_TOUCH_THE, False, US, 36, 12, 1961, 17, 4, 1961, 486),
    ComicBookInfo(Titles.MONEY_BAG_GOAT, MONEY_BAG_GOAT, False, US, 36, 12, 1961, 3, 5, 1961, 487),
    ComicBookInfo(Titles.DUCKBURGS_DAY_OF_PERIL, DUCKBURGS_DAY_OF_PERIL, False, US, 36, 12, 1961, 3, 5, 1961, 488),
    ComicBookInfo(Titles.NORTHEASTER_ON_CAPE_QUACK, NORTHEASTER_ON_CAPE_QUACK, False, CS, 256, 1, 1962, 17, 5, 1961, 489),
    ComicBookInfo(Titles.MOVIE_MAD, MOVIE_MAD, False, CS, 257, 2, 1962, 5, 6, 1961, 490),
    ComicBookInfo(Titles.TEN_CENT_VALENTINE, TEN_CENT_VALENTINE, False, CS, 258, 3, 1962, 14, 6, 1961, 491),
    ComicBookInfo(Titles.CAVE_OF_ALI_BABA, CAVE_OF_ALI_BABA, False, US, 37, 3, 1962, 7, 7, 1961, 492),
    ComicBookInfo(Titles.DEEP_DOWN_DOINGS, DEEP_DOWN_DOINGS, False, US, 37, 3, 1962, 13, 7, 1961, 493),
    ComicBookInfo(Titles.GREAT_POP_UP_THE, GREAT_POP_UP_THE, False, US, 37, 3, 1962, 22, 8, 1961, 494),
    ComicBookInfo(Titles.JUNGLE_BUNGLE, JUNGLE_BUNGLE, False, CS, 259, 4, 1962, 14, 9, 1961, 495),
    ComicBookInfo(Titles.MERRY_FERRY, MERRY_FERRY, False, CS, 260, 5, 1962, 19, 9, 1961, 496),
    ComicBookInfo(Titles.UNSAFE_SAFE_THE, UNSAFE_SAFE_THE, False, US, 38, 6, 1962, 11, 10, 1961, 497),
    ComicBookInfo(Titles.MUCH_LUCK_MCDUCK, MUCH_LUCK_MCDUCK, False, US, 38, 6, 1962, 16, 10, 1961, 498),
    ComicBookInfo(Titles.UNCLE_SCROOGE___MONKEY_BUSINESS, UNCLE_SCROOGE___MONKEY_BUSINESS, False, US, 38, 6, 1962, 1, 11, 1961, 499),
    ComicBookInfo(Titles.COLLECTION_DAY, COLLECTION_DAY, False, US, 38, 6, 1962, 1, 11, 1961, 500),
    ComicBookInfo(Titles.SEEING_IS_BELIEVING, SEEING_IS_BELIEVING, False, US, 38, 6, 1962, 1, 11, 1961, 501),
    ComicBookInfo(Titles.PLAYMATES, PLAYMATES, False, US, 38, 6, 1962, 1, 11, 1961, 502),
    ComicBookInfo(Titles.RAGS_TO_RICHES, RAGS_TO_RICHES, False, CS, 262, 7, 1962, 1, 11, 1961, 503),
    ComicBookInfo(Titles.ART_APPRECIATION, ART_APPRECIATION, False, US, 39, 9, 1962, 1, 11, 1961, 504),
    ComicBookInfo(Titles.FLOWERS_ARE_FLOWERS, FLOWERS_ARE_FLOWERS, False, US, 54, 12, 1964, 1, 11, 1961, 505),
    ComicBookInfo(Titles.MADCAP_INVENTORS, MADCAP_INVENTORS, False, US, 38, 6, 1962, 3, 11, 1961, 506),
    ComicBookInfo(Titles.MEDALING_AROUND, MEDALING_AROUND, False, CS, 261, 6, 1962, 16, 11, 1961, 507),
    ComicBookInfo(Titles.WAY_OUT_YONDER, WAY_OUT_YONDER, False, CS, 262, 7, 1962, 5, 12, 1961, 508),
    ComicBookInfo(Titles.CANDY_KID_THE, CANDY_KID_THE, False, CS, 263, 8, 1962, 13, 12, 1961, 509),
    ComicBookInfo(Titles.SPICY_TALE_A, SPICY_TALE_A, False, US, 39, 9, 1962, 15, 1, 1962, 510),
    ComicBookInfo(Titles.FINNY_FUN, FINNY_FUN, False, US, 39, 9, 1962, 15, 1, 1962, 511),
    ComicBookInfo(Titles.GETTING_THE_BIRD, GETTING_THE_BIRD, False, US, 39, 9, 1962, 15, 1, 1962, 512),
    ComicBookInfo(Titles.NEST_EGG_COLLECTOR, NEST_EGG_COLLECTOR, False, US, 39, 9, 1962, 15, 1, 1962, 513),
    ComicBookInfo(Titles.MILLION_DOLLAR_SHOWER, MILLION_DOLLAR_SHOWER, False, CS, 297, 6, 1965, 15, 1, 1962, 514),
    ComicBookInfo(Titles.TRICKY_EXPERIMENT, TRICKY_EXPERIMENT, False, US, 39, 9, 1962, 5, 2, 1962, 515),
    ComicBookInfo(Titles.MASTER_WRECKER, MASTER_WRECKER, False, CS, 264, 9, 1962, 9, 2, 1962, 516),
    ComicBookInfo(Titles.RAVEN_MAD, RAVEN_MAD, False, CS, 265, 10, 1962, 17, 2, 1962, 517),
    ComicBookInfo(Titles.STALWART_RANGER, STALWART_RANGER, False, CS, 266, 11, 1962, 5, 3, 1962, 518),
    ComicBookInfo(Titles.LOG_JOCKEY, LOG_JOCKEY, False, CS, 267, 12, 1962, 15, 3, 1962, 519),
    ComicBookInfo(Titles.SNOW_DUSTER, SNOW_DUSTER, False, US, 41, 3, 1963, 19, 3, 1962, 520),
    ComicBookInfo(Titles.ODDBALL_ODYSSEY, ODDBALL_ODYSSEY, False, US, 40, 1, 1963, 12, 4, 1962, 521),
    ComicBookInfo(Titles.POSTHASTY_POSTMAN, POSTHASTY_POSTMAN, False, US, 40, 1, 1963, 18, 4, 1962, 522),
    ComicBookInfo(Titles.STATUS_SEEKER_THE, STATUS_SEEKER_THE, False, US, 41, 3, 1963, 16, 5, 1962, 523),
    ComicBookInfo(Titles.MATTER_OF_FACTORY_A, MATTER_OF_FACTORY_A, False, CS, 269, 2, 1963, -1, 6, 1962, 524),
    ComicBookInfo(Titles.CHRISTMAS_CHEERS, CHRISTMAS_CHEERS, False, CS, 268, 1, 1963, 4, 6, 1962, 525),
    ComicBookInfo(Titles.JINXED_JALOPY_RACE_THE, JINXED_JALOPY_RACE_THE, False, CS, 270, 3, 1963, 25, 6, 1962, 526),
    ComicBookInfo(Titles.FOR_OLD_DIMES_SAKE, FOR_OLD_DIMES_SAKE, False, US, 43, 7, 1963, 16, 7, 1962, 527),
    ComicBookInfo(Titles.STONES_THROW_FROM_GHOST_TOWN_A, STONES_THROW_FROM_GHOST_TOWN_A, False, CS, 271, 4, 1963, 11, 8, 1962, 528),
    ComicBookInfo(Titles.SPARE_THAT_HAIR, SPARE_THAT_HAIR, False, CS, 272, 5, 1963, 15, 8, 1962, 529),
    ComicBookInfo(Titles.DUCKS_EYE_VIEW_OF_EUROPE_A, DUCKS_EYE_VIEW_OF_EUROPE_A, False, CS, 273, 6, 1963, 27, 8, 1962, 530),
    ComicBookInfo(Titles.CASE_OF_THE_STICKY_MONEY_THE, CASE_OF_THE_STICKY_MONEY_THE, False, US, 42, 5, 1963, 17, 9, 1962, 531),
    ComicBookInfo(Titles.DUELING_TYCOONS, DUELING_TYCOONS, False, US, 42, 5, 1963, 24, 9, 1962, 532),
    ComicBookInfo(Titles.WISHFUL_EXCESS, WISHFUL_EXCESS, False, US, 42, 5, 1963, 24, 9, 1962, 533),
    ComicBookInfo(Titles.SIDEWALK_OF_THE_MIND, SIDEWALK_OF_THE_MIND, False, US, 42, 5, 1963, 24, 9, 1962, 534),
    ComicBookInfo(Titles.NO_BARGAIN, NO_BARGAIN, False, US, 47, 2, 1964, 24, 9, 1962, 535),
    ComicBookInfo(Titles.UP_AND_AT_IT, UP_AND_AT_IT, False, US, 47, 2, 1964, 24, 9, 1962, 536),
    ComicBookInfo(Titles.GALL_OF_THE_WILD, GALL_OF_THE_WILD, False, CS, 274, 7, 1963, 10, 10, 1962, 537),
    ComicBookInfo(Titles.ZERO_HERO, ZERO_HERO, False, CS, 275, 8, 1963, 29, 10, 1962, 538),
    ComicBookInfo(Titles.BEACH_BOY, BEACH_BOY, False, CS, 276, 9, 1963, 13, 11, 1962, 539),
    ComicBookInfo(Titles.CROWN_OF_THE_MAYAS, CROWN_OF_THE_MAYAS, False, US, 44, 8, 1963, 10, 12, 1962, 540),
    ComicBookInfo(Titles.INVISIBLE_INTRUDER_THE, INVISIBLE_INTRUDER_THE, False, US, 44, 8, 1963, 26, 12, 1962, 541),
    ComicBookInfo(Titles.ISLE_OF_GOLDEN_GEESE, ISLE_OF_GOLDEN_GEESE, False, US, 45, 10, 1963, 28, 1, 1963, 542),
    ComicBookInfo(Titles.TRAVEL_TIGHTWAD_THE, TRAVEL_TIGHTWAD_THE, False, US, 45, 10, 1963, 7, 2, 1963, 543),
    ComicBookInfo(Titles.DUCKBURG_PET_PARADE_THE, DUCKBURG_PET_PARADE_THE, False, CS, 277, 10, 1963, 7, 3, 1963, 544),
    ComicBookInfo(Titles.HELPERS_HELPING_HAND_A, HELPERS_HELPING_HAND_A, False, US, 46, 12, 1963, 19, 3, 1963, 545),
    ComicBookInfo(Titles.HAVE_GUN_WILL_DANCE, HAVE_GUN_WILL_DANCE, False, CS, 278, 11, 1963, 11, 4, 1963, 546),
    ComicBookInfo(Titles.LOST_BENEATH_THE_SEA, LOST_BENEATH_THE_SEA, False, US, 46, 12, 1963, 27, 5, 1963, 547),
    ComicBookInfo(Titles.LEMONADE_FLING_THE, LEMONADE_FLING_THE, False, US, 46, 12, 1963, 4, 6, 1963, 548),
    ComicBookInfo(Titles.FIREMAN_SCROOGE, FIREMAN_SCROOGE, False, US, 46, 12, 1963, 7, 6, 1963, 549),
    ComicBookInfo(Titles.SAVED_BY_THE_BAG, SAVED_BY_THE_BAG, False, US, 54, 12, 1964, 7, 6, 1963, 550),
    ComicBookInfo(Titles.ONCE_UPON_A_CARNIVAL, ONCE_UPON_A_CARNIVAL, False, CS, 279, 12, 1963, 1, 7, 1963, 551),
    ComicBookInfo(Titles.DOUBLE_MASQUERADE, DOUBLE_MASQUERADE, False, CS, 280, 1, 1964, 15, 7, 1963, 552),
    ComicBookInfo(Titles.MAN_VERSUS_MACHINE, MAN_VERSUS_MACHINE, False, US, 47, 2, 1964, 22, 7, 1963, 553),
    ComicBookInfo(Titles.TICKING_DETECTOR, TICKING_DETECTOR, False, US, 55, 2, 1965, 3, 8, 1963, 554),
    ComicBookInfo(Titles.IT_HAPPENED_ONE_WINTER, IT_HAPPENED_ONE_WINTER, False, US, 61, 1, 1966, 3, 8, 1963, 555),
    ComicBookInfo(Titles.THRIFTY_SPENDTHRIFT_THE, THRIFTY_SPENDTHRIFT_THE, False, US, 47, 2, 1964, 14, 8, 1963, 556),
    ComicBookInfo(Titles.FEUD_AND_FAR_BETWEEN, FEUD_AND_FAR_BETWEEN, False, CS, 281, 2, 1964, 26, 8, 1963, 557),
    ComicBookInfo(Titles.BUBBLEWEIGHT_CHAMP, BUBBLEWEIGHT_CHAMP, False, CS, 282, 3, 1964, 9, 9, 1963, 558),
    ComicBookInfo(Titles.JONAH_GYRO, JONAH_GYRO, False, US, 48, 3, 1964, 16, 9, 1963, 559),
    ComicBookInfo(Titles.MANY_FACES_OF_MAGICA_DE_SPELL_THE, MANY_FACES_OF_MAGICA_DE_SPELL_THE, False, US, 48, 3, 1964, 5, 10, 1963, 560),
    ComicBookInfo(Titles.CAPN_BLIGHTS_MYSTERY_SHIP, CAPN_BLIGHTS_MYSTERY_SHIP, False, CS, 283, 4, 1964, 29, 10, 1963, 561),
    ComicBookInfo(Titles.LOONY_LUNAR_GOLD_RUSH_THE, LOONY_LUNAR_GOLD_RUSH_THE, False, US, 49, 5, 1964, 12, 11, 1963, 562),
    ComicBookInfo(Titles.OLYMPIAN_TORCH_BEARER_THE, OLYMPIAN_TORCH_BEARER_THE, False, CS, 286, 7, 1964, 3, 12, 1963, 563),
    ComicBookInfo(Titles.RUG_RIDERS_IN_THE_SKY, RUG_RIDERS_IN_THE_SKY, False, US, 50, 7, 1964, 26, 12, 1963, 564),
    ComicBookInfo(Titles.HOW_GREEN_WAS_MY_LETTUCE, HOW_GREEN_WAS_MY_LETTUCE, False, US, 51, 8, 1964, 18, 1, 1964, 565),
    ComicBookInfo(Titles.GREAT_WIG_MYSTERY_THE, GREAT_WIG_MYSTERY_THE, False, US, 52, 9, 1964, 19, 2, 1964, 566),
    ComicBookInfo(Titles.HERO_OF_THE_DIKE, HERO_OF_THE_DIKE, False, CS, 288, 9, 1964, 6, 3, 1964, 567),
    ComicBookInfo(Titles.INTERPLANETARY_POSTMAN, INTERPLANETARY_POSTMAN, False, US, 53, 10, 1964, 27, 3, 1964, 568),
    ComicBookInfo(Titles.UNFRIENDLY_ENEMIES, UNFRIENDLY_ENEMIES, False, CS, 289, 10, 1964, 6, 4, 1964, 569),
    ComicBookInfo(Titles.BILLION_DOLLAR_SAFARI_THE, BILLION_DOLLAR_SAFARI_THE, False, US, 54, 12, 1964, 11, 5, 1964, 570),
    ComicBookInfo(Titles.DELIVERY_DILEMMA, DELIVERY_DILEMMA, False, CS, 291, 12, 1964, 25, 5, 1964, 571),
    ComicBookInfo(Titles.INSTANT_HERCULES, INSTANT_HERCULES, False, CS, 292, 1, 1965, 11, 6, 1964, 572),
    ComicBookInfo(Titles.MCDUCK_OF_ARABIA, MCDUCK_OF_ARABIA, False, US, 55, 2, 1965, 13, 7, 1964, 573),
    ComicBookInfo(Titles.MYSTERY_OF_THE_GHOST_TOWN_RAILROAD, MYSTERY_OF_THE_GHOST_TOWN_RAILROAD, False, US, 56, 3, 1965, 31, 8, 1964, 574),
    ComicBookInfo(Titles.DUCK_OUT_OF_LUCK, DUCK_OUT_OF_LUCK, False, CS, 294, 3, 1965, 17, 9, 1964, 575),
    ComicBookInfo(Titles.LOCK_OUT_THE, LOCK_OUT_THE, False, US, 57, 5, 1965, 19, 9, 1964, 576),
    ComicBookInfo(Titles.BIGGER_THE_BEGGAR_THE, BIGGER_THE_BEGGAR_THE, False, US, 57, 5, 1965, 28, 9, 1964, 577),
    ComicBookInfo(Titles.PLUMMETING_WITH_PRECISION, PLUMMETING_WITH_PRECISION, False, US, 57, 5, 1965, 28, 9, 1964, 578),
    ComicBookInfo(Titles.SNAKE_TAKE, SNAKE_TAKE, False, US, 57, 5, 1965, 28, 9, 1964, 579),
    ComicBookInfo(Titles.SWAMP_OF_NO_RETURN_THE, SWAMP_OF_NO_RETURN_THE, False, US, 57, 5, 1965, 30, 10, 1964, 580),
    ComicBookInfo(Titles.MONKEY_BUSINESS, MONKEY_BUSINESS, False, CS, 297, 6, 1965, 16, 11, 1964, 581),
    ComicBookInfo(Titles.GIANT_ROBOT_ROBBERS_THE, GIANT_ROBOT_ROBBERS_THE, False, US, 58, 7, 1965, 13, 12, 1964, 582),
    ComicBookInfo(Titles.LAUNDRY_FOR_LESS, LAUNDRY_FOR_LESS, False, US, 58, 7, 1965, 21, 12, 1964, 583),
    ComicBookInfo(Titles.LONG_DISTANCE_COLLISION, LONG_DISTANCE_COLLISION, False, US, 58, 7, 1965, 21, 12, 1964, 584),
    ComicBookInfo(Titles.TOP_WAGES, TOP_WAGES, False, US, 61, 1, 1966, 21, 12, 1964, 585),
    ComicBookInfo(Titles.NORTH_OF_THE_YUKON, NORTH_OF_THE_YUKON, False, US, 59, 9, 1965, 25, 1, 1965, 586),
    ComicBookInfo(Titles.DOWN_FOR_THE_COUNT, DOWN_FOR_THE_COUNT, False, US, 61, 1, 1966, 1, 2, 1965, 587),
    ComicBookInfo(Titles.WASTED_WORDS, WASTED_WORDS, False, US, 61, 1, 1966, 8, 2, 1965, 588),
    ComicBookInfo(Titles.PHANTOM_OF_NOTRE_DUCK_THE, PHANTOM_OF_NOTRE_DUCK_THE, False, US, 60, 11, 1965, 4, 3, 1965, 589),
    ComicBookInfo(Titles.SO_FAR_AND_NO_SAFARI, SO_FAR_AND_NO_SAFARI, False, US, 61, 1, 1966, 1, 4, 1965, 590),
    ComicBookInfo(Titles.QUEEN_OF_THE_WILD_DOG_PACK_THE, QUEEN_OF_THE_WILD_DOG_PACK_THE, False, US, 62, 3, 1966, 12, 5, 1965, 591),
    ComicBookInfo(Titles.HOUSE_OF_HAUNTS, HOUSE_OF_HAUNTS, False, US, 63, 5, 1966, 3, 8, 1965, 592),
    ComicBookInfo(Titles.TREASURE_OF_MARCO_POLO, TREASURE_OF_MARCO_POLO, False, US, 64, 7, 1966, 13, 10, 1965, 593),
    ComicBookInfo(Titles.BEAUTY_BUSINESS_THE, BEAUTY_BUSINESS_THE, False, CS, 308, 5, 1966, 16, 11, 1965, 594),
    ComicBookInfo(Titles.MICRO_DUCKS_FROM_OUTER_SPACE, MICRO_DUCKS_FROM_OUTER_SPACE, False, US, 65, 9, 1966, 7, 12, 1965, 595),
    ComicBookInfo(Titles.NOT_SO_ANCIENT_MARINER_THE, NOT_SO_ANCIENT_MARINER_THE, False, CS, 312, 9, 1966, 5, 1, 1966, 596),
    ComicBookInfo(Titles.HEEDLESS_HORSEMAN_THE, HEEDLESS_HORSEMAN_THE, False, US, 66, 11, 1966, 15, 2, 1966, 597),
    ComicBookInfo(Titles.HALL_OF_THE_MERMAID_QUEEN, HALL_OF_THE_MERMAID_QUEEN, False, US, 68, 3, 1967, 13, 4, 1966, 598),
    ComicBookInfo(Titles.DOOM_DIAMOND_THE, DOOM_DIAMOND_THE, False, US, 70, 7, 1967, 19, 5, 1966, 599),
    ComicBookInfo(Titles.CATTLE_KING_THE, CATTLE_KING_THE, False, US, 69, 5, 1967, 27, 5, 1966, 600),
    ComicBookInfo(Titles.KING_SCROOGE_THE_FIRST, KING_SCROOGE_THE_FIRST, False, US, 71, 10, 1967, 22, 6, 1966, 601),
]
# fmt: on


assert NUM_TITLES == len(BARKS_TITLE_INFO)


def check_story_submitted_order(title_list: List[ComicBookInfo]):
    prev_chronological_number = 0
    prev_title = ""
    prev_submitted_date = date(1940, 1, 1)
    for title in title_list:
        if not 1 <= title.submitted_month <= 12:
            raise Exception(f'"{title}": Invalid submission month: {title.submitted_month}.')
        submitted_day = 1 if title.submitted_day == -1 else title.submitted_day
        submitted_date = date(
            title.submitted_year,
            title.submitted_month,
            submitted_day,
        )
        if prev_submitted_date > submitted_date:
            raise Exception(
                f'"{title}": Out of order submitted date {submitted_date}.'
                f' Previous entry: "{prev_title}" - {prev_submitted_date}.'
            )
        chronological_number = title.chronological_number
        if prev_chronological_number >= chronological_number:
            raise Exception(
                f'"{title}": Out of order chronological number {chronological_number}.'
                f' Previous title: "{prev_title}"'
                f" with chronological number {prev_chronological_number}."
            )
        prev_title = title
        prev_submitted_date = submitted_date
        prev_chronological_number = chronological_number
