from collections import OrderedDict
from dataclasses import dataclass
from datetime import date

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


@dataclass
class ComicBookInfo:
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


ComicBookInfoDict = OrderedDict[str, ComicBookInfo]


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

# fmt: off
# noinspection LongLine
BARKS_TITLE_INFO: ComicBookInfoDict = OrderedDict([
    (DONALD_DUCK_FINDS_PIRATE_GOLD, ComicBookInfo(True, FC, 9, 10, 1942, -1, 5, 1942, 1)),
    (VICTORY_GARDEN_THE, ComicBookInfo(False, CS, 31, 4, 1943, -1, 12, 1942, 2)),
    (RABBITS_FOOT_THE, ComicBookInfo(False, CS, 32, 5, 1943, 23, 12, 1942, 3)),
    (LIFEGUARD_DAZE, ComicBookInfo(False, CS, 33, 6, 1943, 29, 1, 1943, 4)),
    (GOOD_DEEDS, ComicBookInfo(False, CS, 34, 7, 1943, 24, 2, 1943, 5)),
    (LIMBER_W_GUEST_RANCH_THE, ComicBookInfo(False, CS, 35, 8, 1943, 17, 3, 1943, 6)),
    (MIGHTY_TRAPPER_THE, ComicBookInfo(True, CS, 36, 9, 1943, 20, 4, 1943, 7)),
    (DONALD_DUCK_AND_THE_MUMMYS_RING, ComicBookInfo(True, FC, 29, 9, 1943, 10, 5, 1943, 8)),
    (HARD_LOSER_THE, ComicBookInfo(True, FC, 29, 9, 1943, 10, 5, 1943, 9)),
    (TOO_MANY_PETS, ComicBookInfo(True, FC, 29, 9, 1943, 29, 5, 1943, 10)),
    (GOOD_NEIGHBORS, ComicBookInfo(True, CS, 38, 11, 1943, 22, 6, 1943, 11)),
    (SALESMAN_DONALD, ComicBookInfo(True, CS, 39, 12, 1943, 23, 7, 1943, 12)),
    (SNOW_FUN, ComicBookInfo(True, CS, 40, 1, 1944, 28, 8, 1943, 13)),
    (DUCK_IN_THE_IRON_PANTS_THE, ComicBookInfo(True, CS, 41, 2, 1944, 22, 9, 1943, 14)),
    (KITE_WEATHER, ComicBookInfo(True, CS, 42, 3, 1944, 20, 10, 1943, 15)),
    (THREE_DIRTY_LITTLE_DUCKS, ComicBookInfo(True, CS, 43, 4, 1944, 27, 11, 1943, 16)),
    (MAD_CHEMIST_THE, ComicBookInfo(True, CS, 44, 5, 1944, 30, 12, 1943, 17)),
    (RIVAL_BOATMEN, ComicBookInfo(True, CS, 45, 6, 1944, 19, 1, 1944, 18)),
    (CAMERA_CRAZY, ComicBookInfo(True, CS, 46, 7, 1944, 29, 2, 1944, 19)),
    (FARRAGUT_THE_FALCON, ComicBookInfo(False, CS, 47, 8, 1944, 1, 4, 1944, 20)),
    (PURLOINED_PUTTY_THE, ComicBookInfo(False, CS, 48, 9, 1944, 26, 4, 1944, 21)),
    (HIGH_WIRE_DAREDEVILS, ComicBookInfo(False, CS, 49, 10, 1944, 26, 5, 1944, 22)),
    (TEN_CENTS_WORTH_OF_TROUBLE, ComicBookInfo(False, CS, 50, 11, 1944, 22, 6, 1944, 23)),
    (DONALDS_BAY_LOT, ComicBookInfo(False, CS, 51, 12, 1944, 27, 7, 1944, 24)),
    (FROZEN_GOLD, ComicBookInfo(True, FC, 62, 1, 1945, 9, 8, 1944, 25)),
    (THIEVERY_AFOOT, ComicBookInfo(False, CS, 52, 1, 1945, 26, 8, 1944, 26)),
    (MYSTERY_OF_THE_SWAMP, ComicBookInfo(True, FC, 62, 1, 1945, 23, 9, 1944, 27)),
    (TRAMP_STEAMER_THE, ComicBookInfo(False, CS, 53, 2, 1945, 6, 10, 1944, 28)),
    (LONG_RACE_TO_PUMPKINBURG_THE, ComicBookInfo(False, CS, 54, 3, 1945, 27, 10, 1944, 29)),
    (WEBFOOTED_WRANGLER, ComicBookInfo(False, CS, 55, 4, 1945, 1, 12, 1944, 30)),
    (ICEBOX_ROBBER_THE, ComicBookInfo(False, CS, 56, 5, 1945, -1, 1, 1945, 31)),
    (PECKING_ORDER, ComicBookInfo(False, CS, 57, 6, 1945, 2, 2, 1945, 32)),
    (TAMING_THE_RAPIDS, ComicBookInfo(False, CS, 58, 7, 1945, 9, 3, 1945, 33)),
    (EYES_IN_THE_DARK, ComicBookInfo(False, CS, 60, 9, 1945, 12, 3, 1945, 34)),
    (DAYS_AT_THE_LAZY_K, ComicBookInfo(False, CS, 59, 8, 1945, 3, 4, 1945, 35)),
    (RIDDLE_OF_THE_RED_HAT_THE, ComicBookInfo(True, FC, 79, 8, 1945, 27, 4, 1945, 36)),
    (THUG_BUSTERS, ComicBookInfo(False, CS, 61, 10, 1945, 31, 5, 1945, 37)),
    (GREAT_SKI_RACE_THE, ComicBookInfo(False, CS, 62, 11, 1945, 27, 6, 1945, 38)),
    (FIREBUG_THE, ComicBookInfo(True, FC, 108, 1, 1946, 19, 7, 1945, 39)),
    (TEN_DOLLAR_DITHER, ComicBookInfo(False, CS, 63, 12, 1945, 2, 8, 1945, 40)),
    (DONALD_DUCKS_BEST_CHRISTMAS, ComicBookInfo(True, FG, 45, 12, 1945, 31, 8, 1945, 41)),
    (SILENT_NIGHT, ComicBookInfo(False, CS, 64, 1, 1946, 31, 8, 1945, 42)),
    (DONALD_TAMES_HIS_TEMPER, ComicBookInfo(False, CS, 64, 1, 1946, 19, 9, 1945, 43)),
    (SINGAPORE_JOE, ComicBookInfo(False, CS, 65, 2, 1946, 4, 10, 1945, 44)),
    (MASTER_ICE_FISHER, ComicBookInfo(False, CS, 66, 3, 1946, 27, 10, 1945, 45)),
    (JET_RESCUE, ComicBookInfo(False, CS, 67, 4, 1946, 23, 11, 1945, 46)),
    (DONALDS_MONSTER_KITE, ComicBookInfo(False, CS, 68, 5, 1946, 4, 1, 1946, 47)),
    (TERROR_OF_THE_RIVER_THE, ComicBookInfo(True, FC, 108, 1, 1946, 25, 1, 1946, 48)),
    (SEALS_ARE_SO_SMART, ComicBookInfo(True, FC, 108, 1, 1946, 25, 1, 1946, 49)),
    (BICEPS_BLUES, ComicBookInfo(False, CS, 69, 6, 1946, 1, 2, 1946, 50)),
    (SMUGSNORKLE_SQUATTIE_THE, ComicBookInfo(False, CS, 70, 7, 1946, 28, 2, 1946, 51)),
    (SANTAS_STORMY_VISIT, ComicBookInfo(True, FG, 46, 12, 1946, 8, 3, 1946, 52)),
    (SWIMMING_SWINDLERS, ComicBookInfo(False, CS, 71, 8, 1946, 26, 3, 1946, 53)),
    (PLAYIN_HOOKEY, ComicBookInfo(False, CS, 72, 9, 1946, 25, 4, 1946, 54)),
    (GOLD_FINDER_THE, ComicBookInfo(False, CS, 73, 10, 1946, 27, 5, 1946, 55)),
    (BILL_COLLECTORS_THE, ComicBookInfo(False, CS, 74, 11, 1946, 14, 6, 1946, 56)),
    (TURKEY_RAFFLE, ComicBookInfo(False, CS, 75, 12, 1946, 8, 7, 1946, 57)),
    (MAHARAJAH_DONALD, ComicBookInfo(True, MC, 4, -1, 1947, 13, 8, 1946, 58)),
    (CANTANKEROUS_CAT_THE, ComicBookInfo(False, CS, 76, 1, 1947, 29, 8, 1946, 59)),
    (DONALD_DUCKS_ATOM_BOMB, ComicBookInfo(True, CH, 1, -1, 1947, 9, 9, 1946, 60)),
    (GOING_BUGGY, ComicBookInfo(False, CS, 77, 2, 1947, 25, 9, 1946, 61)),
    (PEACEFUL_HILLS_THE, ComicBookInfo(True, MC, 4, -1, 1947, 4, 10, 1946, 62)),
    (JAM_ROBBERS, ComicBookInfo(False, CS, 78, 3, 1947, 28, 10, 1946, 63)),
    (PICNIC_TRICKS, ComicBookInfo(False, CS, 79, 4, 1947, 18, 11, 1946, 64)),
    (VOLCANO_VALLEY, ComicBookInfo(True, FC, 147, 5, 1947, 9, 12, 1946, 65)),
    (IF_THE_HAT_FITS, ComicBookInfo(False, FC, 147, 5, 1947, 30, 12, 1946, 66)),
    (DONALDS_POSY_PATCH, ComicBookInfo(False, CS, 80, 5, 1947, 10, 1, 1947, 67)),
    (DONALD_MINES_HIS_OWN_BUSINESS, ComicBookInfo(False, CS, 81, 6, 1947, 28, 1, 1947, 68)),
    (MAGICAL_MISERY, ComicBookInfo(False, CS, 82, 7, 1947, 19, 2, 1947, 69)),
    (THREE_GOOD_LITTLE_DUCKS, ComicBookInfo(True, FG, 47, 12, 1947, 28, 2, 1947, 70)),
    (VACATION_MISERY, ComicBookInfo(False, CS, 83, 8, 1947, 19, 3, 1947, 71)),
    (ADVENTURE_DOWN_UNDER, ComicBookInfo(True, FC, 159, 8, 1947, 4, 4, 1947, 72)),
    (GHOST_OF_THE_GROTTO_THE, ComicBookInfo(True, FC, 159, 8, 1947, 15, 4, 1947, 73)),
    (WALTZ_KING_THE, ComicBookInfo(False, CS, 84, 9, 1947, 1, 5, 1947, 74)),
    (MASTERS_OF_MELODY_THE, ComicBookInfo(False, CS, 85, 10, 1947, 5, 5, 1947, 75)),
    (FIREMAN_DONALD, ComicBookInfo(False, CS, 86, 11, 1947, 23, 6, 1947, 76)),
    (CHRISTMAS_ON_BEAR_MOUNTAIN, ComicBookInfo(True, FC, 178, 12, 1947, 22, 7, 1947, 77)),
    (FASHION_IN_FLIGHT, ComicBookInfo(False, FC, 178, 12, 1947, 22, 7, 1947, 78)),
    (TURN_FOR_THE_WORSE, ComicBookInfo(False, FC, 178, 12, 1947, 22, 7, 1947, 79)),
    (MACHINE_MIX_UP, ComicBookInfo(False, FC, 178, 12, 1947, 22, 7, 1947, 80)),
    (TERRIBLE_TURKEY_THE, ComicBookInfo(False, CS, 87, 12, 1947, 31, 7, 1947, 81)),
    (WINTERTIME_WAGER, ComicBookInfo(False, CS, 88, 1, 1948, 15, 8, 1947, 82)),
    (WATCHING_THE_WATCHMAN, ComicBookInfo(False, CS, 89, 2, 1948, 4, 9, 1947, 83)),
    (DARKEST_AFRICA, ComicBookInfo(True, MC, 20, -1, 1948, 26, 9, 1947, 84)),
    (WIRED, ComicBookInfo(False, CS, 90, 3, 1948, 9, 10, 1947, 85)),
    (GOING_APE, ComicBookInfo(False, CS, 91, 4, 1948, 28, 10, 1947, 86)),
    (OLD_CASTLES_SECRET_THE, ComicBookInfo(True, FC, 189, 6, 1948, 3, 12, 1947, 87)),
    (SPOIL_THE_ROD, ComicBookInfo(False, CS, 92, 5, 1948, 30, 12, 1947, 88)),
    (BIRD_WATCHING, ComicBookInfo(False, FC, 189, 6, 1948, 6, 1, 1948, 89)),
    (HORSESHOE_LUCK, ComicBookInfo(False, FC, 189, 6, 1948, 6, 1, 1948, 90)),
    (BEAN_TAKEN, ComicBookInfo(False, FC, 189, 6, 1948, 6, 1, 1948, 91)),
    (ROCKET_RACE_TO_THE_MOON, ComicBookInfo(False, CS, 93, 6, 1948, 16, 1, 1948, 92)),
    (DONALD_OF_THE_COAST_GUARD, ComicBookInfo(False, CS, 94, 7, 1948, 3, 2, 1948, 93)),
    (GLADSTONE_RETURNS, ComicBookInfo(False, CS, 95, 8, 1948, 19, 2, 1948, 94)),
    (SHERIFF_OF_BULLET_VALLEY, ComicBookInfo(True, FC, 199, 10, 1948, 16, 3, 1948, 95)),
    (LINKS_HIJINKS, ComicBookInfo(False, CS, 96, 9, 1948, 25, 3, 1948, 96)),
    (SORRY_TO_BE_SAFE, ComicBookInfo(False, FC, 199, 10, 1948, 22, 4, 1948, 97)),
    (BEST_LAID_PLANS, ComicBookInfo(False, FC, 199, 10, 1948, 22, 4, 1948, 98)),
    (GENUINE_ARTICLE_THE, ComicBookInfo(False, FC, 199, 10, 1948, 22, 4, 1948, 99)),
    (PEARLS_OF_WISDOM, ComicBookInfo(False, CS, 97, 10, 1948, 29, 4, 1948, 100)),
    (FOXY_RELATIONS, ComicBookInfo(False, CS, 98, 11, 1948, 28, 5, 1948, 101)),
    (CRAZY_QUIZ_SHOW_THE, ComicBookInfo(False, CS, 99, 12, 1948, 10, 6, 1948, 102)),
    (GOLDEN_CHRISTMAS_TREE_THE, ComicBookInfo(True, FC, 203, 12, 1948, 30, 6, 1948, 103)),
    (TOYLAND, ComicBookInfo(True, FG, 48, 12, 1948, 8, 7, 1948, 104)),
    (JUMPING_TO_CONCLUSIONS, ComicBookInfo(False, FC, 203, 12, 1948, 22, 7, 1948, 105)),
    (TRUE_TEST_THE, ComicBookInfo(False, FC, 203, 12, 1948, 22, 7, 1948, 106)),
    (ORNAMENTS_ON_THE_WAY, ComicBookInfo(False, FC, 203, 12, 1948, 22, 7, 1948, 107)),
    (TRUANT_OFFICER_DONALD, ComicBookInfo(False, CS, 100, 1, 1949, 29, 7, 1948, 108)),
    (DONALD_DUCKS_WORST_NIGHTMARE, ComicBookInfo(False, CS, 101, 2, 1949, 26, 8, 1948, 109)),
    (PIZEN_SPRING_DUDE_RANCH, ComicBookInfo(False, CS, 102, 3, 1949, 9, 9, 1948, 110)),
    (RIVAL_BEACHCOMBERS, ComicBookInfo(False, CS, 103, 4, 1949, 23, 9, 1948, 111)),
    (LOST_IN_THE_ANDES, ComicBookInfo(True, FC, 223, 4, 1949, 21, 10, 1948, 112)),
    (TOO_FIT_TO_FIT, ComicBookInfo(False, FC, 223, 4, 1949, 24, 11, 1948, 113)),
    (TUNNEL_VISION, ComicBookInfo(False, FC, 223, 4, 1949, 24, 11, 1948, 114)),
    (SLEEPY_SITTERS, ComicBookInfo(False, FC, 223, 4, 1949, 24, 11, 1948, 115)),
    (SUNKEN_YACHT_THE, ComicBookInfo(False, CS, 104, 5, 1949, 24, 11, 1948, 116)),
    (RACE_TO_THE_SOUTH_SEAS, ComicBookInfo(True, MC, 41, -1, 1949, 15, 12, 1948, 117)),
    (MANAGING_THE_ECHO_SYSTEM, ComicBookInfo(False, CS, 105, 6, 1949, 13, 1, 1949, 118)),
    (PLENTY_OF_PETS, ComicBookInfo(False, CS, 106, 7, 1949, 27, 1, 1949, 119)),
    (VOODOO_HOODOO, ComicBookInfo(True, FC, 238, 8, 1949, 3, 3, 1949, 120)),
    (SLIPPERY_SHINE, ComicBookInfo(False, FC, 238, 8, 1949, 17, 3, 1949, 121)),
    (FRACTIOUS_FUN, ComicBookInfo(False, FC, 238, 8, 1949, 17, 3, 1949, 122)),
    (KING_SIZE_CONE, ComicBookInfo(False, FC, 238, 8, 1949, 17, 3, 1949, 123)),
    (SUPER_SNOOPER, ComicBookInfo(False, CS, 107, 8, 1949, 22, 3, 1949, 124)),
    (GREAT_DUCKBURG_FROG_JUMPING_CONTEST_THE, ComicBookInfo(False, CS, 108, 9, 1949, 14, 4, 1949, 125)),
    (DOWSING_DUCKS, ComicBookInfo(False, CS, 109, 10, 1949, 28, 4, 1949, 126)),
    (GOLDILOCKS_GAMBIT_THE, ComicBookInfo(False, CS, 110, 11, 1949, 12, 5, 1949, 127)),
    (LETTER_TO_SANTA, ComicBookInfo(True, CP, 1, 11, 1949, 1, 6, 1949, 128)),
    (NO_NOISE_IS_GOOD_NOISE, ComicBookInfo(False, CP, 1, 11, 1949, 1, 6, 1949, 129)),
    (LUCK_OF_THE_NORTH, ComicBookInfo(True, FC, 256, 12, 1949, 29, 6, 1949, 130)),
    (NEW_TOYS, ComicBookInfo(True, FG, 49, 12, 1949, 7, 7, 1949, 131)),
    (TOASTY_TOYS, ComicBookInfo(False, FC, 256, 12, 1949, 21, 7, 1949, 132)),
    (NO_PLACE_TO_HIDE, ComicBookInfo(False, FC, 256, 12, 1949, 21, 7, 1949, 133)),
    (TIED_DOWN_TOOLS, ComicBookInfo(False, FC, 256, 12, 1949, 21, 7, 1949, 134)),
    (DONALDS_LOVE_LETTERS, ComicBookInfo(False, CS, 111, 12, 1949, 4, 8, 1949, 135)),
    (RIP_VAN_DONALD, ComicBookInfo(False, CS, 112, 1, 1950, 24, 8, 1949, 136)),
    (TRAIL_OF_THE_UNICORN, ComicBookInfo(True, FC, 263, 2, 1950, 8, 9, 1949, 137)),
    (LAND_OF_THE_TOTEM_POLES, ComicBookInfo(True, FC, 263, 2, 1950, 29, 9, 1949, 138)),
    (NOISE_NULLIFIER, ComicBookInfo(False, FC, 263, 2, 1950, 6, 10, 1949, 139)),
    (MATINEE_MADNESS, ComicBookInfo(False, FC, 263, 2, 1950, 6, 10, 1949, 140)),
    (FETCHING_PRICE_A, ComicBookInfo(False, FC, 263, 2, 1950, 6, 10, 1949, 141)),
    (SERUM_TO_CODFISH_COVE, ComicBookInfo(False, CS, 114, 3, 1950, 13, 10, 1949, 142)),
    (WILD_ABOUT_FLOWERS, ComicBookInfo(False, CS, 117, 6, 1950, 27, 10, 1949, 143)),
    (IN_ANCIENT_PERSIA, ComicBookInfo(True, FC, 275, 5, 1950, 23, 11, 1949, 144)),
    (VACATION_TIME, ComicBookInfo(True, VP, 1, 7, 1950, 5, 1, 1950, 145)),
    (DONALDS_GRANDMA_DUCK, ComicBookInfo(True, VP, 1, 7, 1950, 19, 1, 1950, 146)),
    (CAMP_COUNSELOR, ComicBookInfo(True, VP, 1, 7, 1950, 27, 1, 1950, 147)),
    (PIXILATED_PARROT_THE, ComicBookInfo(True, FC, 282, 7, 1950, 23, 2, 1950, 148)),
    (MAGIC_HOURGLASS_THE, ComicBookInfo(True, FC, 291, 9, 1950, 16, 3, 1950, 149)),
    (BIG_TOP_BEDLAM, ComicBookInfo(True, FC, 300, 11, 1950, 20, 4, 1950, 150)),
    (YOU_CANT_GUESS, ComicBookInfo(True, CP, 2, 11, 1950, 24, 5, 1950, 151)),
    (DANGEROUS_DISGUISE, ComicBookInfo(True, FC, 308, 1, 1951, 29, 6, 1950, 152)),
    (NO_SUCH_VARMINT, ComicBookInfo(True, FC, 318, 3, 1951, 27, 7, 1950, 153)),
    (BILLIONS_TO_SNEEZE_AT, ComicBookInfo(False, CS, 124, 1, 1951, 10, 8, 1950, 154)),
    (OPERATION_ST_BERNARD, ComicBookInfo(False, CS, 125, 2, 1951, 31, 8, 1950, 155)),
    (FINANCIAL_FABLE_A, ComicBookInfo(False, CS, 126, 3, 1951, 14, 9, 1950, 156)),
    (APRIL_FOOLERS_THE, ComicBookInfo(False, CS, 127, 4, 1951, 28, 9, 1950, 157)),
    (IN_OLD_CALIFORNIA, ComicBookInfo(True, FC, 328, 5, 1951, 2, 11, 1950, 158)),
    (KNIGHTLY_RIVALS, ComicBookInfo(False, CS, 128, 5, 1951, 30, 11, 1950, 159)),
    (POOL_SHARKS, ComicBookInfo(False, CS, 129, 6, 1951, 7, 12, 1950, 160)),
    (TROUBLE_WITH_DIMES_THE, ComicBookInfo(False, CS, 130, 7, 1951, 28, 12, 1950, 161)),
    (GLADSTONES_LUCK, ComicBookInfo(False, CS, 131, 8, 1951, 11, 1, 1951, 162)),
    (TEN_STAR_GENERALS, ComicBookInfo(False, CS, 132, 9, 1951, 25, 1, 1951, 163)),
    (CHRISTMAS_FOR_SHACKTOWN_A, ComicBookInfo(True, FC, 367, 1, 1952, 15, 3, 1951, 164)),
    (ATTIC_ANTICS, ComicBookInfo(False, CS, 132, 9, 1951, 29, 3, 1951, 165)),
    (TRUANT_NEPHEWS_THE, ComicBookInfo(False, CS, 133, 10, 1951, 12, 4, 1951, 166)),
    (TERROR_OF_THE_BEAGLE_BOYS, ComicBookInfo(False, CS, 134, 11, 1951, 5, 5, 1951, 167)),
    (TALKING_PARROT, ComicBookInfo(False, FC, 356, 11, 1951, 24, 5, 1951, 168)),
    (TREEING_OFF, ComicBookInfo(False, FC, 367, 1, 1952, 24, 5, 1951, 169)),
    (CHRISTMAS_KISS, ComicBookInfo(False, FC, 367, 1, 1952, 24, 5, 1951, 170)),
    (PROJECTING_DESIRES, ComicBookInfo(False, FC, 367, 1, 1952, 24, 5, 1951, 171)),
    (BIG_BIN_ON_KILLMOTOR_HILL_THE, ComicBookInfo(False, CS, 135, 12, 1951, 31, 5, 1951, 172)),
    (GLADSTONES_USUAL_VERY_GOOD_YEAR, ComicBookInfo(False, CS, 136, 1, 1952, 7, 6, 1951, 173)),
    (SCREAMING_COWBOY_THE, ComicBookInfo(False, CS, 137, 2, 1952, 21, 6, 1951, 174)),
    (STATUESQUE_SPENDTHRIFTS, ComicBookInfo(False, CS, 138, 3, 1952, 12, 7, 1951, 175)),
    (ROCKET_WING_SAVES_THE_DAY, ComicBookInfo(False, CS, 139, 4, 1952, 26, 7, 1951, 176)),
    (GLADSTONES_TERRIBLE_SECRET, ComicBookInfo(False, CS, 140, 5, 1952, 23, 8, 1951, 177)),
    (ONLY_A_POOR_OLD_MAN, ComicBookInfo(True, FC, 386, 3, 1952, 27, 9, 1951, 178)),
    (OSOGOOD_SILVER_POLISH, ComicBookInfo(False, FC, 386, 3, 1952, 27, 9, 1951, 179)),
    (COFFEE_FOR_TWO, ComicBookInfo(False, FC, 386, 3, 1952, 27, 9, 1951, 180)),
    (SOUPLINE_EIGHT, ComicBookInfo(False, FC, 386, 3, 1952, 27, 9, 1951, 181)),
    (THINK_BOX_BOLLIX_THE, ComicBookInfo(False, CS, 141, 6, 1952, 18, 10, 1951, 182)),
    (GOLDEN_HELMET_THE, ComicBookInfo(True, FC, 408, 7, 1952, 3, 12, 1951, 183)),
    (FULL_SERVICE_WINDOWS, ComicBookInfo(False, FC, 408, 7, 1952, 3, 1, 1952, 184)),
    (RIGGED_UP_ROLLER, ComicBookInfo(False, FC, 408, 7, 1952, 3, 1, 1952, 185)),
    (AWASH_IN_SUCCESS, ComicBookInfo(False, FC, 408, 7, 1952, 3, 1, 1952, 186)),
    (HOUSEBOAT_HOLIDAY, ComicBookInfo(False, CS, 142, 7, 1952, 10, 1, 1952, 187)),
    (GEMSTONE_HUNTERS, ComicBookInfo(False, CS, 143, 8, 1952, 10, 1, 1952, 188)),
    (GILDED_MAN_THE, ComicBookInfo(True, FC, 422, 9, 1952, 31, 1, 1952, 189)),
    (STABLE_PRICES, ComicBookInfo(False, FC, 422, 9, 1952, 31, 1, 1952, 190)),
    (ARMORED_RESCUE, ComicBookInfo(False, FC, 422, 9, 1952, 31, 1, 1952, 191)),
    (CRAFTY_CORNER, ComicBookInfo(False, FC, 422, 9, 1952, 31, 1, 1952, 192)),
    (SPENDING_MONEY, ComicBookInfo(False, CS, 144, 9, 1952, 21, 2, 1952, 193)),
    (HYPNO_GUN_THE, ComicBookInfo(False, CS, 145, 10, 1952, 6, 3, 1952, 194)),
    (TRICK_OR_TREAT, ComicBookInfo(True, DD, 26, 11, 1952, 31, 3, 1952, 195)),
    (PRANK_ABOVE_A, ComicBookInfo(False, DD, 26, 11, 1952, 10, 4, 1952, 196)),
    (FRIGHTFUL_FACE, ComicBookInfo(False, DD, 26, 11, 1952, 10, 4, 1952, 197)),
    (HOBBLIN_GOBLINS, ComicBookInfo(True, DD, 26, 11, 1952, 8, 5, 1952, 198)),
    (OMELET, ComicBookInfo(False, CS, 146, 11, 1952, 15, 5, 1952, 199)),
    (CHARITABLE_CHORE_A, ComicBookInfo(False, CS, 147, 12, 1952, 29, 5, 1952, 200)),
    (TURKEY_WITH_ALL_THE_SCHEMINGS, ComicBookInfo(False, CS, 148, 1, 1953, 12, 6, 1952, 201)),
    (FLIP_DECISION, ComicBookInfo(False, CS, 149, 2, 1953, 30, 6, 1952, 202)),
    (MY_LUCKY_VALENTINE, ComicBookInfo(False, CS, 150, 3, 1953, 30, 6, 1952, 203)),
    (FARE_DELAY, ComicBookInfo(False, FC, 456, 3, 1953, 28, 8, 1952, 204)),
    (SOMETHIN_FISHY_HERE, ComicBookInfo(True, FC, 456, 3, 1953, -1, 9, 1952, 205)),
    (BACK_TO_THE_KLONDIKE, ComicBookInfo(True, FC, 456, 3, 1953, 18, 9, 1952, 206)),
    (MONEY_LADDER_THE, ComicBookInfo(False, FC, 456, 3, 1953, 16, 10, 1952, 207)),
    (CHECKER_GAME_THE, ComicBookInfo(False, FC, 456, 3, 1953, 16, 10, 1952, 208)),
    (EASTER_ELECTION_THE, ComicBookInfo(False, CS, 151, 4, 1953, 23, 10, 1952, 209)),
    (TALKING_DOG_THE, ComicBookInfo(False, CS, 152, 5, 1953, 30, 10, 1952, 210)),
    (WORM_WEARY, ComicBookInfo(False, CS, 153, 6, 1953, 27, 11, 1952, 211)),
    (MUCH_ADO_ABOUT_QUACKLY_HALL, ComicBookInfo(False, CS, 154, 7, 1953, 27, 11, 1952, 212)),
    (SOME_HEIR_OVER_THE_RAINBOW, ComicBookInfo(False, CS, 155, 8, 1953, 24, 12, 1952, 213)),
    (MASTER_RAINMAKER_THE, ComicBookInfo(False, CS, 156, 9, 1953, 31, 12, 1952, 214)),
    (MONEY_STAIRS_THE, ComicBookInfo(False, CS, 157, 10, 1953, 15, 1, 1953, 215)),
    (MILLION_DOLLAR_PIGEON, ComicBookInfo(False, US, 7, 9, 1954, 25, 2, 1953, 216)),
    (TEMPER_TAMPERING, ComicBookInfo(False, US, 7, 9, 1954, 25, 2, 1953, 217)),
    (DINER_DILEMMA, ComicBookInfo(False, US, 7, 9, 1954, 25, 2, 1953, 218)),
    (HORSERADISH_STORY_THE, ComicBookInfo(False, FC, 495, 9, 1953, 26, 2, 1953, 219)),
    (ROUND_MONEY_BIN_THE, ComicBookInfo(False, FC, 495, 9, 1953, 26, 2, 1953, 220)),
    (BARBER_COLLEGE, ComicBookInfo(False, FC, 495, 9, 1953, 26, 2, 1953, 221)),
    (FOLLOW_THE_RAINBOW, ComicBookInfo(False, FC, 495, 9, 1953, 26, 2, 1953, 222)),
    (ITCHING_TO_SHARE, ComicBookInfo(False, FC, 495, 9, 1953, 26, 2, 1953, 223)),
    (WISPY_WILLIE, ComicBookInfo(False, CS, 159, 12, 1953, 6, 4, 1953, 224)),
    (HAMMY_CAMEL_THE, ComicBookInfo(False, CS, 160, 1, 1954, 23, 4, 1953, 225)),
    (BALLET_EVASIONS, ComicBookInfo(False, US, 4, 12, 1953, 21, 5, 1953, 226)),
    (CHEAPEST_WEIGH_THE, ComicBookInfo(False, US, 4, 12, 1953, 21, 5, 1953, 227)),
    (BUM_STEER, ComicBookInfo(False, US, 4, 12, 1953, 21, 5, 1953, 228)),
    (BEE_BUMBLES, ComicBookInfo(False, CS, 158, 11, 1953, 26, 5, 1953, 229)),
    (MENEHUNE_MYSTERY_THE, ComicBookInfo(False, US, 4, 12, 1953, 28, 5, 1953, 230)),
    (TURKEY_TROT_AT_ONE_WHISTLE, ComicBookInfo(False, CS, 162, 3, 1954, 25, 6, 1953, 231)),
    (RAFFLE_REVERSAL, ComicBookInfo(False, CS, 163, 4, 1954, 2, 7, 1953, 232)),
    (FIX_UP_MIX_UP, ComicBookInfo(False, CS, 161, 2, 1954, 9, 7, 1953, 233)),
    (SECRET_OF_ATLANTIS_THE, ComicBookInfo(False, US, 5, 3, 1954, 30, 7, 1953, 234)),
    (HOSPITALITY_WEEK, ComicBookInfo(False, US, 5, 3, 1954, 30, 7, 1953, 235)),
    (MCDUCK_TAKES_A_DIVE, ComicBookInfo(False, US, 5, 3, 1954, 30, 7, 1953, 236)),
    (SLIPPERY_SIPPER, ComicBookInfo(False, US, 5, 3, 1954, 30, 7, 1953, 237)),
    (FLOUR_FOLLIES, ComicBookInfo(False, CS, 164, 5, 1954, 27, 8, 1953, 238)),
    (PRICE_OF_FAME_THE, ComicBookInfo(False, CS, 165, 6, 1954, 27, 8, 1953, 239)),
    (MIDGETS_MADNESS, ComicBookInfo(False, CS, 166, 7, 1954, 17, 9, 1953, 240)),
    (SALMON_DERBY, ComicBookInfo(False, CS, 167, 8, 1954, 1, 10, 1953, 241)),
    (TRALLA_LA, ComicBookInfo(False, US, 6, 6, 1954, 29, 10, 1953, 242)),
    (OIL_THE_NEWS, ComicBookInfo(False, US, 6, 6, 1954, 29, 10, 1953, 243)),
    (DIG_IT, ComicBookInfo(False, US, 6, 6, 1954, 29, 10, 1953, 244)),
    (MENTAL_FEE, ComicBookInfo(False, US, 6, 6, 1954, 29, 10, 1953, 245)),
    (OUTFOXED_FOX, ComicBookInfo(False, US, 6, 6, 1954, 26, 11, 1953, 246)),
    (CHELTENHAMS_CHOICE, ComicBookInfo(False, CS, 168, 9, 1954, 3, 12, 1953, 247)),
    (TRAVELLING_TRUANTS, ComicBookInfo(False, CS, 169, 10, 1954, 7, 1, 1954, 248)),
    (RANTS_ABOUT_ANTS, ComicBookInfo(False, CS, 170, 11, 1954, 7, 1, 1954, 249)),
    (SEVEN_CITIES_OF_CIBOLA_THE, ComicBookInfo(False, US, 7, 9, 1954, 28, 1, 1954, 250)),
    (WRONG_NUMBER, ComicBookInfo(False, US, 7, 9, 1954, 25, 2, 1954, 251)),
    (TOO_SAFE_SAFE, ComicBookInfo(False, CS, 171, 12, 1954, 4, 3, 1954, 252)),
    (SEARCH_FOR_THE_CUSPIDORIA, ComicBookInfo(False, CS, 172, 1, 1955, 18, 3, 1954, 253)),
    (NEW_YEARS_REVOLUTIONS, ComicBookInfo(False, CS, 173, 2, 1955, 25, 3, 1954, 254)),
    (ICEBOAT_TO_BEAVER_ISLAND, ComicBookInfo(False, CS, 174, 3, 1955, 22, 4, 1954, 255)),
    (MYSTERIOUS_STONE_RAY_THE, ComicBookInfo(False, US, 8, 12, 1954, 20, 5, 1954, 256)),
    (CAMPAIGN_OF_NOTE_A, ComicBookInfo(False, US, 8, 12, 1954, 10, 6, 1954, 257)),
    (CASH_ON_THE_BRAIN, ComicBookInfo(False, US, 8, 12, 1954, 10, 6, 1954, 258)),
    (CLASSY_TAXI, ComicBookInfo(False, US, 8, 12, 1954, 10, 6, 1954, 259)),
    (BLANKET_INVESTMENT, ComicBookInfo(False, US, 8, 12, 1954, 10, 6, 1954, 260)),
    (DAFFY_TAFFY_PULL_THE, ComicBookInfo(False, CS, 175, 4, 1955, 17, 6, 1954, 261)),
    (TUCKERED_TIGER_THE, ComicBookInfo(True, US, 9, 3, 1955, 24, 6, 1954, 262)),
    (DONALD_DUCK_TELLS_ABOUT_KITES, ComicBookInfo(True, KI, 2, 11, 1954, 8, 7, 1954, 263)),
    (LEMMING_WITH_THE_LOCKET_THE, ComicBookInfo(True, US, 9, 3, 1955, 15, 7, 1954, 264)),
    (EASY_MOWING, ComicBookInfo(False, US, 9, 3, 1955, 22, 7, 1954, 265)),
    (SKI_LIFT_LETDOWN, ComicBookInfo(False, US, 9, 3, 1955, 22, 7, 1954, 266)),
    (CAST_OF_THOUSANDS, ComicBookInfo(False, US, 9, 3, 1955, 22, 7, 1954, 267)),
    (GHOST_SHERIFF_OF_LAST_GASP_THE, ComicBookInfo(False, CS, 176, 5, 1955, 22, 7, 1954, 268)),
    (DESCENT_INTERVAL_A, ComicBookInfo(False, CS, 177, 6, 1955, 29, 7, 1954, 269)),
    (SECRET_OF_HONDORICA, ComicBookInfo(True, DD, 46, 3, 1956, 30, 9, 1954, 270)),
    (DOGCATCHER_DUCK, ComicBookInfo(False, DD, 45, 1, 1956, 14, 10, 1954, 271)),
    (COURTSIDE_HEATING, ComicBookInfo(False, DD, 45, 1, 1956, 14, 10, 1954, 272)),
    (POWER_PLOWING, ComicBookInfo(False, DD, 45, 1, 1956, 14, 10, 1954, 273)),
    (REMEMBER_THIS, ComicBookInfo(False, DD, 45, 1, 1956, 17, 10, 1954, 274)),
    (FABULOUS_PHILOSOPHERS_STONE_THE, ComicBookInfo(True, US, 10, 6, 1955, 28, 10, 1954, 275)),
    (HEIRLOOM_WATCH, ComicBookInfo(True, US, 10, 6, 1955, 11, 11, 1954, 276)),
    (DONALDS_RAUCOUS_ROLE, ComicBookInfo(False, CS, 178, 7, 1955, 26, 11, 1954, 277)),
    (GOOD_CANOES_AND_BAD_CANOES, ComicBookInfo(False, CS, 179, 8, 1955, 26, 11, 1954, 278)),
    (DEEP_DECISION, ComicBookInfo(False, US, 10, 6, 1955, 9, 12, 1954, 279)),
    (SMASH_SUCCESS, ComicBookInfo(False, US, 10, 6, 1955, 9, 12, 1954, 280)),
    (TROUBLE_INDEMNITY, ComicBookInfo(False, CS, 180, 9, 1955, 6, 1, 1955, 281)),
    (CHICKADEE_CHALLENGE_THE, ComicBookInfo(False, CS, 181, 10, 1955, 6, 1, 1955, 282)),
    (UNORTHODOX_OX_THE, ComicBookInfo(False, CS, 182, 11, 1955, 6, 1, 1955, 283)),
    (GREAT_STEAMBOAT_RACE_THE, ComicBookInfo(True, US, 11, 9, 1955, 3, 2, 1955, 284)),
    (COME_AS_YOU_ARE, ComicBookInfo(False, US, 11, 9, 1955, 24, 2, 1955, 285)),
    (ROUNDABOUT_HANDOUT, ComicBookInfo(False, US, 11, 9, 1955, 24, 2, 1955, 286)),
    (FAULTY_FORTUNE, ComicBookInfo(False, US, 14, 6, 1956, 24, 2, 1955, 287)),
    (RICHES_RICHES_EVERYWHERE, ComicBookInfo(True, US, 11, 9, 1955, 10, 3, 1955, 288)),
    (CUSTARD_GUN_THE, ComicBookInfo(False, CS, 183, 12, 1955, 17, 3, 1955, 289)),
    (THREE_UN_DUCKS, ComicBookInfo(False, CS, 184, 1, 1956, 31, 3, 1955, 290)),
    (SECRET_RESOLUTIONS, ComicBookInfo(False, CS, 185, 2, 1956, 21, 4, 1955, 291)),
    (ICE_TAXIS_THE, ComicBookInfo(False, CS, 186, 3, 1956, 21, 4, 1955, 292)),
    (SEARCHING_FOR_A_SUCCESSOR, ComicBookInfo(False, CS, 187, 4, 1956, 28, 4, 1955, 293)),
    (OLYMPIC_HOPEFUL_THE, ComicBookInfo(False, CS, 188, 5, 1956, 28, 4, 1955, 294)),
    (GOLDEN_FLEECING_THE, ComicBookInfo(True, US, 12, 12, 1955, 2, 6, 1955, 295)),
    (WATT_AN_OCCASION, ComicBookInfo(False, US, 12, 12, 1955, 2, 6, 1955, 296)),
    (DOUGHNUT_DARE, ComicBookInfo(False, US, 12, 12, 1955, 2, 6, 1955, 297)),
    (SWEAT_DEAL_A, ComicBookInfo(False, US, 12, 12, 1955, 2, 6, 1955, 298)),
    (GOPHER_GOOF_UPS, ComicBookInfo(False, CS, 189, 6, 1956, 30, 6, 1955, 299)),
    (IN_THE_SWIM, ComicBookInfo(False, CS, 190, 7, 1956, 14, 7, 1955, 300)),
    (LAND_BENEATH_THE_GROUND, ComicBookInfo(True, US, 13, 3, 1956, 18, 8, 1955, 301)),
    (TRAPPED_LIGHTNING, ComicBookInfo(False, US, 13, 3, 1956, 1, 9, 1955, 302)),
    (ART_OF_SECURITY_THE, ComicBookInfo(False, US, 13, 3, 1956, 1, 9, 1955, 303)),
    (FASHION_FORECAST, ComicBookInfo(False, US, 13, 3, 1956, 1, 9, 1955, 304)),
    (MUSH, ComicBookInfo(False, US, 13, 3, 1956, 1, 9, 1955, 305)),
    (CAMPING_CONFUSION, ComicBookInfo(False, CS, 191, 8, 1956, 1, 9, 1955, 306)),
    (MASTER_THE, ComicBookInfo(False, CS, 192, 9, 1956, 22, 9, 1955, 307)),
    (WHALE_OF_A_STORY_A, ComicBookInfo(False, CS, 193, 10, 1956, 29, 9, 1955, 308)),
    (SMOKE_WRITER_IN_THE_SKY, ComicBookInfo(False, CS, 194, 11, 1956, 29, 9, 1955, 309)),
    (INVENTOR_OF_ANYTHING, ComicBookInfo(True, US, 14, 6, 1956, 1, 10, 1955, 310)),
    (LOST_CROWN_OF_GENGHIS_KHAN_THE, ComicBookInfo(True, US, 14, 6, 1956, 3, 11, 1955, 311)),
    (LUNCHEON_LAMENT, ComicBookInfo(False, US, 14, 6, 1956, 17, 11, 1955, 312)),
    (RUNAWAY_TRAIN_THE, ComicBookInfo(False, CS, 195, 12, 1956, 23, 11, 1955, 313)),
    (GOLD_RUSH, ComicBookInfo(False, US, 14, 6, 1956, 8, 12, 1955, 314)),
    (FIREFLIES_ARE_FREE, ComicBookInfo(False, US, 14, 6, 1956, 8, 12, 1955, 315)),
    (EARLY_TO_BUILD, ComicBookInfo(False, US, 17, 3, 1957, 8, 12, 1955, 316)),
    (STATUES_OF_LIMITATIONS, ComicBookInfo(False, CS, 196, 1, 1957, 22, 12, 1955, 317)),
    (BORDERLINE_HERO, ComicBookInfo(False, CS, 197, 2, 1957, 5, 1, 1956, 318)),
    (SECOND_RICHEST_DUCK_THE, ComicBookInfo(True, US, 15, 9, 1956, 2, 2, 1956, 319)),
    (MIGRATING_MILLIONS, ComicBookInfo(False, US, 15, 9, 1956, 9, 2, 1956, 320)),
    (CAT_BOX_THE, ComicBookInfo(False, US, 15, 9, 1956, 9, 2, 1956, 321)),
    (CHINA_SHOP_SHAKEUP, ComicBookInfo(False, US, 17, 3, 1957, 13, 2, 1956, 322)),
    (BUFFO_OR_BUST, ComicBookInfo(False, US, 15, 9, 1956, 23, 2, 1956, 323)),
    (POUND_FOR_SOUND, ComicBookInfo(False, US, 15, 9, 1956, 23, 2, 1956, 324)),
    (FERTILE_ASSETS, ComicBookInfo(False, US, 16, 12, 1956, 23, 2, 1956, 325)),
    (GRANDMAS_PRESENT, ComicBookInfo(True, CP, 8, 12, 1956, 1, 3, 1956, 326)),
    (KNIGHT_IN_SHINING_ARMOR, ComicBookInfo(False, CS, 198, 3, 1957, 15, 3, 1956, 327)),
    (FEARSOME_FLOWERS, ComicBookInfo(False, CS, 214, 7, 1958, 15, 3, 1956, 328)),
    (DONALDS_PET_SERVICE, ComicBookInfo(False, CS, 200, 5, 1957, 5, 4, 1956, 329)),
    (BACK_TO_LONG_AGO, ComicBookInfo(True, US, 16, 12, 1956, 26, 4, 1956, 330)),
    (COLOSSALEST_SURPRISE_QUIZ_SHOW_THE, ComicBookInfo(False, US, 16, 12, 1956, 17, 5, 1956, 331)),
    (FORECASTING_FOLLIES, ComicBookInfo(False, US, 16, 12, 1956, 17, 5, 1956, 332)),
    (BACKYARD_BONANZA, ComicBookInfo(False, US, 16, 12, 1956, 24, 5, 1956, 333)),
    (ALL_SEASON_HAT, ComicBookInfo(False, DD, 51, 1, 1957, 24, 5, 1956, 334)),
    (EYES_HAVE_IT_THE, ComicBookInfo(False, US, 17, 3, 1957, 24, 5, 1956, 335)),
    (RELATIVE_REACTION, ComicBookInfo(False, US, 18, 6, 1957, 24, 5, 1956, 336)),
    (SECRET_BOOK_THE, ComicBookInfo(False, US, 31, 9, 1960, 24, 5, 1956, 337)),
    (TREE_TRICK, ComicBookInfo(False, US, 33, 3, 1961, 24, 5, 1956, 338)),
    (IN_KAKIMAW_COUNTRY, ComicBookInfo(False, CS, 202, 7, 1957, 31, 5, 1956, 339)),
    (LOST_PEG_LEG_MINE_THE, ComicBookInfo(True, DD, 52, 3, 1957, 14, 6, 1956, 340)),
    (LOSING_FACE, ComicBookInfo(False, CS, 204, 9, 1957, 21, 6, 1956, 341)),
    (DAY_DUCKBURG_GOT_DYED_THE, ComicBookInfo(False, CS, 201, 6, 1957, 5, 7, 1956, 342)),
    (PICNIC, ComicBookInfo(True, VP, 8, 7, 1957, 12, 7, 1956, 343)),
    (FISHING_MYSTERY, ComicBookInfo(False, US, 17, 3, 1957, -1, 8, 1956, 344)),
    (COLD_BARGAIN_A, ComicBookInfo(True, US, 17, 3, 1957, 2, 8, 1956, 345)),
    (GYROS_IMAGINATION_INVENTION, ComicBookInfo(False, CS, 199, 4, 1957, 20, 9, 1956, 346)),
    (RED_APPLE_SAP, ComicBookInfo(False, CS, 205, 10, 1957, 25, 9, 1956, 347)),
    (SURE_FIRE_GOLD_FINDER_THE, ComicBookInfo(False, US, 18, 6, 1957, 11, 10, 1956, 348)),
    (SPECIAL_DELIVERY, ComicBookInfo(False, CS, 203, 8, 1957, 11, 10, 1956, 349)),
    (CODE_OF_DUCKBURG_THE, ComicBookInfo(False, CS, 208, 1, 1958, 18, 10, 1956, 350)),
    (LAND_OF_THE_PYGMY_INDIANS, ComicBookInfo(True, US, 18, 6, 1957, 15, 11, 1956, 351)),
    (NET_WORTH, ComicBookInfo(False, US, 18, 6, 1957, 15, 11, 1956, 352)),
    (FORBIDDEN_VALLEY, ComicBookInfo(True, DD, 54, 7, 1957, 13, 12, 1956, 353)),
    (FANTASTIC_RIVER_RACE_THE, ComicBookInfo(False, USGTD, 1, 8, 1957, 10, 1, 1957, 354)),
    (SAGMORE_SPRINGS_HOTEL, ComicBookInfo(False, CS, 206, 11, 1957, 17, 1, 1957, 355)),
    (TENDERFOOT_TRAP_THE, ComicBookInfo(False, CS, 207, 12, 1957, 17, 1, 1957, 356)),
    (MINES_OF_KING_SOLOMON_THE, ComicBookInfo(True, US, 19, 9, 1957, 15, 2, 1957, 357)),
    (GYRO_BUILDS_A_BETTER_HOUSE, ComicBookInfo(False, US, 19, 9, 1957, 28, 2, 1957, 358)),
    (HISTORY_TOSSED, ComicBookInfo(False, US, 19, 9, 1957, 28, 2, 1957, 359)),
    (BLACK_PEARLS_OF_TABU_YAMA_THE, ComicBookInfo(False, CID, 1, 10, 1957, 14, 3, 1957, 360)),
    (AUGUST_ACCIDENT, ComicBookInfo(True, MMA, 1, 12, 1957, 21, 3, 1957, 361)),
    (SEPTEMBER_SCRIMMAGE, ComicBookInfo(True, MMA, 1, 12, 1957, 21, 3, 1957, 362)),
    (WISHING_STONE_ISLAND, ComicBookInfo(False, CS, 211, 4, 1958, 18, 4, 1957, 363)),
    (ROCKET_RACE_AROUND_THE_WORLD, ComicBookInfo(False, CS, 212, 5, 1958, 18, 4, 1957, 364)),
    (ROSCOE_THE_ROBOT, ComicBookInfo(False, US, 20, 12, 1957, 25, 4, 1957, 365)),
    (CITY_OF_GOLDEN_ROOFS, ComicBookInfo(True, US, 20, 12, 1957, 23, 5, 1957, 366)),
    (GETTING_THOR, ComicBookInfo(False, US, 21, 3, 1958, 6, 6, 1957, 367)),
    (DOGGED_DETERMINATION, ComicBookInfo(False, US, 21, 3, 1958, 6, 6, 1957, 368)),
    (FORGOTTEN_PRECAUTION, ComicBookInfo(False, US, 21, 3, 1958, 6, 6, 1957, 369)),
    (BIG_BOBBER_THE, ComicBookInfo(False, US, 33, 3, 1961, 6, 6, 1957, 370)),
    (WINDFALL_OF_THE_MIND, ComicBookInfo(False, US, 21, 3, 1958, 20, 6, 1957, 371)),
    (TITANIC_ANTS_THE, ComicBookInfo(True, DD, 60, 7, 1958, 20, 6, 1957, 372)),
    (RESCUE_ENHANCEMENT, ComicBookInfo(False, US, 20, 12, 1957, 25, 7, 1957, 373)),
    (PERSISTENT_POSTMAN_THE, ComicBookInfo(False, CS, 209, 2, 1958, 25, 7, 1957, 374)),
    (HALF_BAKED_BAKER_THE, ComicBookInfo(False, CS, 210, 3, 1958, 25, 7, 1957, 375)),
    (DODGING_MISS_DAISY, ComicBookInfo(False, CS, 213, 6, 1958, 25, 7, 1957, 376)),
    (MONEY_WELL_THE, ComicBookInfo(True, US, 21, 3, 1958, 22, 8, 1957, 377)),
    (MILKMAN_THE, ComicBookInfo(False, CS, 215, 8, 1958, 19, 9, 1957, 378)),
    (MOCKING_BIRD_RIDGE, ComicBookInfo(False, CS, 215, 8, 1958, 19, 9, 1957, 379)),
    (OLD_FROGGIE_CATAPULT, ComicBookInfo(False, CS, 216, 9, 1958, 1, 10, 1957, 380)),
    (GOING_TO_PIECES, ComicBookInfo(False, US, 22, 6, 1958, 31, 10, 1957, 381)),
    (HIGH_RIDER, ComicBookInfo(False, US, 22, 6, 1958, 31, 10, 1957, 382)),
    (THAT_SINKING_FEELING, ComicBookInfo(False, US, 22, 6, 1958, 31, 10, 1957, 383)),
    (WATER_SKI_RACE, ComicBookInfo(False, DD, 60, 7, 1958, 31, 10, 1957, 384)),
    (BALMY_SWAMI_THE, ComicBookInfo(False, US, 31, 9, 1960, 31, 10, 1957, 385)),
    (WINDY_STORY_THE, ComicBookInfo(False, US, 37, 3, 1962, 31, 10, 1957, 386)),
    (GOLDEN_RIVER_THE, ComicBookInfo(True, US, 22, 6, 1958, 21, 11, 1957, 387)),
    (MOOLA_ON_THE_MOVE, ComicBookInfo(False, US, 23, 9, 1958, 5, 12, 1957, 388)),
    (THUMBS_UP, ComicBookInfo(False, US, 33, 3, 1961, 5, 12, 1957, 389)),
    (KNOW_IT_ALL_MACHINE_THE, ComicBookInfo(False, US, 22, 3, 1958, 12, 12, 1957, 390)),
    (STRANGE_SHIPWRECKS_THE, ComicBookInfo(False, US, 23, 9, 1958, 31, 12, 1957, 391)),
    (FABULOUS_TYCOON_THE, ComicBookInfo(False, US, 23, 9, 1958, 9, 1, 1958, 392)),
    (GYRO_GOES_FOR_A_DIP, ComicBookInfo(False, US, 23, 9, 1958, 9, 1, 1958, 393)),
    (BILL_WIND, ComicBookInfo(False, US, 25, 3, 1959, 10, 1, 1958, 394)),
    (TWENTY_FOUR_CARAT_MOON_THE, ComicBookInfo(False, US, 24, 12, 1958, 20, 1, 1958, 395)),
    (HOUSE_ON_CYCLONE_HILL_THE, ComicBookInfo(False, US, 24, 12, 1958, 20, 1, 1958, 396)),
    (NOBLE_PORPOISES, ComicBookInfo(False, CS, 218, 11, 1958, 14, 2, 1958, 397)),
    (MAGIC_INK_THE, ComicBookInfo(False, US, 24, 12, 1958, 17, 2, 1958, 398)),
    (SLEEPIES_THE, ComicBookInfo(False, DD, 81, 1, 1962, 17, 2, 1958, 399)),
    (TRACKING_SANDY, ComicBookInfo(False, CS, 221, 2, 1959, 5, 3, 1958, 400)),
    (LITTLEST_CHICKEN_THIEF_THE, ComicBookInfo(False, CS, 219, 12, 1958, 12, 3, 1958, 401)),
    (BEACHCOMBERS_PICNIC_THE, ComicBookInfo(False, CS, 224, 5, 1959, 19, 3, 1958, 402)),
    (LIGHTS_OUT, ComicBookInfo(False, US, 23, 9, 1958, 25, 3, 1958, 403)),
    (DRAMATIC_DONALD, ComicBookInfo(False, CS, 217, 10, 1958, 4, 4, 1958, 404)),
    (CHRISTMAS_IN_DUCKBURG, ComicBookInfo(True, CP, 9, 12, 1958, 6, 4, 1958, 405)),
    (ROCKET_ROASTED_CHRISTMAS_TURKEY, ComicBookInfo(False, CS, 220, 1, 1959, 14, 4, 1958, 406)),
    (MASTER_MOVER_THE, ComicBookInfo(False, CS, 222, 3, 1959, 14, 4, 1958, 407)),
    (SPRING_FEVER, ComicBookInfo(False, CS, 223, 4, 1959, 18, 4, 1958, 408)),
    (FLYING_DUTCHMAN_THE, ComicBookInfo(False, US, 25, 3, 1959, 20, 4, 1958, 409)),
    (PYRAMID_SCHEME, ComicBookInfo(False, US, 25, 3, 1959, 20, 4, 1958, 410)),
    (WISHING_WELL_THE, ComicBookInfo(False, US, 25, 3, 1959, 9, 6, 1958, 411)),
    (IMMOVABLE_MISER, ComicBookInfo(False, US, 25, 3, 1959, 9, 6, 1958, 412)),
    (RETURN_TO_PIZEN_BLUFF, ComicBookInfo(False, US, 26, 6, 1959, 16, 6, 1958, 413)),
    (KRANKENSTEIN_GYRO, ComicBookInfo(False, US, 26, 6, 1959, 16, 6, 1958, 414)),
    (MONEY_CHAMP_THE, ComicBookInfo(False, US, 27, 9, 1959, 12, 7, 1958, 415)),
    (HIS_HANDY_ANDY, ComicBookInfo(False, US, 27, 9, 1959, 12, 7, 1958, 416)),
    (FIREFLY_TRACKER_THE, ComicBookInfo(False, US, 27, 9, 1959, 15, 7, 1958, 417)),
    (PRIZE_OF_PIZARRO_THE, ComicBookInfo(False, US, 26, 6, 1959, 11, 8, 1958, 418)),
    (LOVELORN_FIREMAN_THE, ComicBookInfo(False, CS, 225, 6, 1959, 15, 8, 1958, 419)),
    (KITTY_GO_ROUND, ComicBookInfo(False, US, 25, 3, 1959, 9, 9, 1958, 420)),
    (POOR_LOSER, ComicBookInfo(False, DD, 79, 9, 1961, 9, 9, 1958, 421)),
    (FLOATING_ISLAND_THE, ComicBookInfo(False, CS, 226, 7, 1959, 16, 9, 1958, 422)),
    (CRAWLS_FOR_CASH, ComicBookInfo(False, US, 27, 9, 1959, 1, 10, 1958, 423)),
    (BLACK_FOREST_RESCUE_THE, ComicBookInfo(False, CS, 227, 8, 1959, 10, 10, 1958, 424)),
    (GOOD_DEEDS_THE, ComicBookInfo(False, CS, 229, 10, 1959, 15, 10, 1958, 425)),
    (BLACK_WEDNESDAY, ComicBookInfo(False, CS, 230, 11, 1959, 30, 10, 1958, 426)),
    (ALL_CHOKED_UP, ComicBookInfo(False, US, 23, 9, 1958, 31, 10, 1958, 427)),
    (WATCHFUL_PARENTS_THE, ComicBookInfo(False, CS, 228, 9, 1959, 10, 11, 1958, 428)),
    (WAX_MUSEUM_THE, ComicBookInfo(False, CS, 231, 12, 1959, 17, 11, 1958, 429)),
    (PAUL_BUNYAN_MACHINE_THE, ComicBookInfo(False, US, 28, 12, 1959, 15, 12, 1958, 430)),
    (KNIGHTS_OF_THE_FLYING_SLEDS, ComicBookInfo(False, CS, 233, 2, 1960, 2, 1, 1959, 431)),
    (WITCHING_STICK_THE, ComicBookInfo(False, US, 28, 12, 1959, 16, 1, 1959, 432)),
    (INVENTORS_CONTEST_THE, ComicBookInfo(False, US, 28, 12, 1959, 16, 1, 1959, 433)),
    (JUNGLE_HI_JINKS, ComicBookInfo(True, SF, 2, 8, 1959, 30, 1, 1959, 434)),
    (FLYING_FARMHAND_THE, ComicBookInfo(True, FC, 1010, 7, 1959, 6, 3, 1959, 435)),
    (HONEY_OF_A_HEN_A, ComicBookInfo(True, FC, 1010, 7, 1959, 6, 3, 1959, 436)),
    (WEATHER_WATCHERS_THE, ComicBookInfo(True, FC, 1010, 7, 1959, 6, 3, 1959, 437)),
    (SHEEPISH_COWBOYS_THE, ComicBookInfo(True, FC, 1010, 7, 1959, 6, 3, 1959, 438)),
    (OODLES_OF_OOMPH, ComicBookInfo(False, US, 29, 3, 1960, 20, 4, 1959, 439)),
    (MASTER_GLASSER_THE, ComicBookInfo(False, DD, 68, 11, 1959, 20, 5, 1959, 440)),
    (MONEY_HAT_THE, ComicBookInfo(False, US, 28, 12, 1959, 20, 5, 1959, 441)),
    (ISLAND_IN_THE_SKY, ComicBookInfo(False, US, 29, 3, 1960, 15, 6, 1959, 442)),
    (UNDER_THE_POLAR_ICE, ComicBookInfo(False, CS, 232, 1, 1960, 11, 7, 1959, 443)),
    (HOUND_OF_THE_WHISKERVILLES, ComicBookInfo(False, US, 29, 3, 1960, 11, 7, 1959, 444)),
    (RIDING_THE_PONY_EXPRESS, ComicBookInfo(False, CS, 234, 3, 1960, 17, 8, 1959, 445)),
    (WANT_TO_BUY_AN_ISLAND, ComicBookInfo(False, CS, 235, 4, 1960, 28, 9, 1959, 446)),
    (FROGGY_FARMER, ComicBookInfo(False, CS, 236, 5, 1960, 14, 10, 1959, 447)),
    (PIPELINE_TO_DANGER, ComicBookInfo(False, US, 30, 6, 1960, 13, 11, 1959, 448)),
    (YOICKS_THE_FOX, ComicBookInfo(False, US, 30, 6, 1960, 9, 12, 1959, 449)),
    (WAR_PAINT, ComicBookInfo(False, US, 30, 6, 1960, 9, 12, 1959, 450)),
    (DOG_SITTER_THE, ComicBookInfo(False, CS, 238, 7, 1960, 7, 1, 1960, 451)),
    (MYSTERY_OF_THE_LOCH, ComicBookInfo(False, CS, 237, 6, 1960, 15, 1, 1960, 452)),
    (VILLAGE_BLACKSMITH_THE, ComicBookInfo(False, CS, 239, 8, 1960, 15, 1, 1960, 453)),
    (FRAIDY_FALCON_THE, ComicBookInfo(False, CS, 240, 9, 1960, 15, 1, 1960, 454)),
    (ALL_AT_SEA, ComicBookInfo(False, US, 31, 9, 1960, 12, 2, 1960, 455)),
    (FISHY_WARDEN, ComicBookInfo(False, US, 31, 9, 1960, 16, 2, 1960, 456)),
    (TWO_WAY_LUCK, ComicBookInfo(False, US, 31, 9, 1960, 26, 2, 1960, 457)),
    (BALLOONATICS, ComicBookInfo(False, CS, 242, 11, 1960, 11, 3, 1960, 458)),
    (TURKEY_TROUBLE, ComicBookInfo(False, CS, 243, 12, 1960, 11, 4, 1960, 459)),
    (MISSILE_FIZZLE, ComicBookInfo(False, CS, 244, 1, 1961, 11, 4, 1960, 460)),
    (ROCKS_TO_RICHES, ComicBookInfo(False, CS, 241, 10, 1960, 18, 4, 1960, 461)),
    (SITTING_HIGH, ComicBookInfo(False, CS, 245, 2, 1961, 18, 4, 1960, 462)),
    (THATS_NO_FABLE, ComicBookInfo(False, US, 32, 12, 1960, 12, 5, 1960, 463)),
    (CLOTHES_MAKE_THE_DUCK, ComicBookInfo(False, US, 32, 12, 1960, 17, 5, 1960, 464)),
    (THAT_SMALL_FEELING, ComicBookInfo(False, US, 32, 12, 1960, 13, 6, 1960, 465)),
    (MADCAP_MARINER_THE, ComicBookInfo(False, CS, 247, 4, 1961, 11, 7, 1960, 466)),
    (TERRIBLE_TOURIST, ComicBookInfo(False, CS, 248, 5, 1961, 11, 7, 1960, 467)),
    (THRIFT_GIFT_A, ComicBookInfo(False, US, 32, 12, 1960, 18, 7, 1960, 468)),
    (LOST_FRONTIER, ComicBookInfo(False, CS, 246, 3, 1961, 18, 7, 1960, 469)),
    (YOU_CANT_WIN, ComicBookInfo(False, US, 33, 3, 1961, 15, 8, 1960, 470)),
    (BILLIONS_IN_THE_HOLE, ComicBookInfo(False, US, 33, 3, 1961, 3, 9, 1960, 471)),
    (BONGO_ON_THE_CONGO, ComicBookInfo(False, US, 33, 3, 1961, 12, 9, 1960, 472)),
    (STRANGER_THAN_FICTION, ComicBookInfo(False, CS, 249, 6, 1961, 31, 10, 1960, 473)),
    (BOXED_IN, ComicBookInfo(False, CS, 250, 7, 1961, 12, 11, 1960, 474)),
    (CHUGWAGON_DERBY, ComicBookInfo(False, US, 34, 6, 1961, 16, 11, 1960, 475)),
    (MYTHTIC_MYSTERY, ComicBookInfo(False, US, 34, 6, 1961, 10, 12, 1960, 476)),
    (WILY_RIVAL, ComicBookInfo(False, US, 34, 6, 1961, 10, 12, 1960, 477)),
    (DUCK_LUCK, ComicBookInfo(False, CS, 251, 8, 1961, 28, 12, 1960, 478)),
    (MR_PRIVATE_EYE, ComicBookInfo(False, CS, 252, 9, 1961, 10, 1, 1961, 479)),
    (HOUND_HOUNDER, ComicBookInfo(False, CS, 253, 10, 1961, 16, 1, 1961, 480)),
    (GOLDEN_NUGGET_BOAT_THE, ComicBookInfo(False, US, 35, 9, 1961, 16, 2, 1961, 481)),
    (FAST_AWAY_CASTAWAY, ComicBookInfo(False, US, 35, 9, 1961, 24, 2, 1961, 482)),
    (GIFT_LION, ComicBookInfo(False, US, 35, 9, 1961, 24, 2, 1961, 483)),
    (JET_WITCH, ComicBookInfo(False, CS, 254, 11, 1961, 13, 3, 1961, 484)),
    (BOAT_BUSTER, ComicBookInfo(False, CS, 255, 12, 1961, 20, 3, 1961, 485)),
    (MIDAS_TOUCH_THE, ComicBookInfo(False, US, 36, 12, 1961, 17, 4, 1961, 486)),
    (MONEY_BAG_GOAT, ComicBookInfo(False, US, 36, 12, 1961, 3, 5, 1961, 487)),
    (DUCKBURGS_DAY_OF_PERIL, ComicBookInfo(False, US, 36, 12, 1961, 3, 5, 1961, 488)),
    (NORTHEASTER_ON_CAPE_QUACK, ComicBookInfo(False, CS, 256, 1, 1962, 17, 5, 1961, 489)),
    (MOVIE_MAD, ComicBookInfo(False, CS, 257, 2, 1962, 5, 6, 1961, 490)),
    (TEN_CENT_VALENTINE, ComicBookInfo(False, CS, 258, 3, 1962, 14, 6, 1961, 491)),
    (CAVE_OF_ALI_BABA, ComicBookInfo(False, US, 37, 3, 1962, 7, 7, 1961, 492)),
    (DEEP_DOWN_DOINGS, ComicBookInfo(False, US, 37, 3, 1962, 13, 7, 1961, 493)),
    (GREAT_POP_UP_THE, ComicBookInfo(False, US, 37, 3, 1962, 22, 8, 1961, 494)),
    (JUNGLE_BUNGLE, ComicBookInfo(False, CS, 259, 4, 1962, 14, 9, 1961, 495)),
    (MERRY_FERRY, ComicBookInfo(False, CS, 260, 5, 1962, 19, 9, 1961, 496)),
    (UNSAFE_SAFE_THE, ComicBookInfo(False, US, 38, 6, 1962, 11, 10, 1961, 497)),
    (MUCH_LUCK_MCDUCK, ComicBookInfo(False, US, 38, 6, 1962, 16, 10, 1961, 498)),
    (UNCLE_SCROOGE___MONKEY_BUSINESS, ComicBookInfo(False, US, 38, 6, 1962, 1, 11, 1961, 499)),
    (COLLECTION_DAY, ComicBookInfo(False, US, 38, 6, 1962, 1, 11, 1961, 500)),
    (SEEING_IS_BELIEVING, ComicBookInfo(False, US, 38, 6, 1962, 1, 11, 1961, 501)),
    (PLAYMATES, ComicBookInfo(False, US, 38, 6, 1962, 1, 11, 1961, 502)),
    (RAGS_TO_RICHES, ComicBookInfo(False, CS, 262, 7, 1962, 1, 11, 1961, 503)),
    (ART_APPRECIATION, ComicBookInfo(False, US, 39, 9, 1962, 1, 11, 1961, 504)),
    (FLOWERS_ARE_FLOWERS, ComicBookInfo(False, US, 54, 12, 1964, 1, 11, 1961, 505)),
    (MADCAP_INVENTORS, ComicBookInfo(False, US, 38, 6, 1962, 3, 11, 1961, 506)),
    (MEDALING_AROUND, ComicBookInfo(False, CS, 261, 6, 1962, 16, 11, 1961, 507)),
    (WAY_OUT_YONDER, ComicBookInfo(False, CS, 262, 7, 1962, 5, 12, 1961, 508)),
    (CANDY_KID_THE, ComicBookInfo(False, CS, 263, 8, 1962, 13, 12, 1961, 509)),
    (SPICY_TALE_A, ComicBookInfo(False, US, 39, 9, 1962, 15, 1, 1962, 510)),
    (FINNY_FUN, ComicBookInfo(False, US, 39, 9, 1962, 15, 1, 1962, 511)),
    (GETTING_THE_BIRD, ComicBookInfo(False, US, 39, 9, 1962, 15, 1, 1962, 512)),
    (NEST_EGG_COLLECTOR, ComicBookInfo(False, US, 39, 9, 1962, 15, 1, 1962, 513)),
    (MILLION_DOLLAR_SHOWER, ComicBookInfo(False, CS, 297, 6, 1965, 15, 1, 1962, 514)),
    (TRICKY_EXPERIMENT, ComicBookInfo(False, US, 39, 9, 1962, 5, 2, 1962, 515)),
    (MASTER_WRECKER, ComicBookInfo(False, CS, 264, 9, 1962, 9, 2, 1962, 516)),
    (RAVEN_MAD, ComicBookInfo(False, CS, 265, 10, 1962, 17, 2, 1962, 517)),
    (STALWART_RANGER, ComicBookInfo(False, CS, 266, 11, 1962, 5, 3, 1962, 518)),
    (LOG_JOCKEY, ComicBookInfo(False, CS, 267, 12, 1962, 15, 3, 1962, 519)),
    (SNOW_DUSTER, ComicBookInfo(False, US, 41, 3, 1963, 19, 3, 1962, 520)),
    (ODDBALL_ODYSSEY, ComicBookInfo(False, US, 40, 1, 1963, 12, 4, 1962, 521)),
    (POSTHASTY_POSTMAN, ComicBookInfo(False, US, 40, 1, 1963, 18, 4, 1962, 522)),
    (STATUS_SEEKER_THE, ComicBookInfo(False, US, 41, 3, 1963, 16, 5, 1962, 523)),
    (MATTER_OF_FACTORY_A, ComicBookInfo(False, CS, 269, 2, 1963, -1, 6, 1962, 524)),
    (CHRISTMAS_CHEERS, ComicBookInfo(False, CS, 268, 1, 1963, 4, 6, 1962, 525)),
    (JINXED_JALOPY_RACE_THE, ComicBookInfo(False, CS, 270, 3, 1963, 25, 6, 1962, 526)),
    (FOR_OLD_DIMES_SAKE, ComicBookInfo(False, US, 43, 7, 1963, 16, 7, 1962, 527)),
    (STONES_THROW_FROM_GHOST_TOWN_A, ComicBookInfo(False, CS, 271, 4, 1963, 11, 8, 1962, 528)),
    (SPARE_THAT_HAIR, ComicBookInfo(False, CS, 272, 5, 1963, 15, 8, 1962, 529)),
    (DUCKS_EYE_VIEW_OF_EUROPE_A, ComicBookInfo(False, CS, 273, 6, 1963, 27, 8, 1962, 530)),
    (CASE_OF_THE_STICKY_MONEY_THE, ComicBookInfo(False, US, 42, 5, 1963, 17, 9, 1962, 531)),
    (DUELING_TYCOONS, ComicBookInfo(False, US, 42, 5, 1963, 24, 9, 1962, 532)),
    (WISHFUL_EXCESS, ComicBookInfo(False, US, 42, 5, 1963, 24, 9, 1962, 533)),
    (SIDEWALK_OF_THE_MIND, ComicBookInfo(False, US, 42, 5, 1963, 24, 9, 1962, 534)),
    (NO_BARGAIN, ComicBookInfo(False, US, 47, 2, 1964, 24, 9, 1962, 535)),
    (UP_AND_AT_IT, ComicBookInfo(False, US, 47, 2, 1964, 24, 9, 1962, 536)),
    (GALL_OF_THE_WILD, ComicBookInfo(False, CS, 274, 7, 1963, 10, 10, 1962, 537)),
    (ZERO_HERO, ComicBookInfo(False, CS, 275, 8, 1963, 29, 10, 1962, 538)),
    (BEACH_BOY, ComicBookInfo(False, CS, 276, 9, 1963, 13, 11, 1962, 539)),
    (CROWN_OF_THE_MAYAS, ComicBookInfo(False, US, 44, 8, 1963, 10, 12, 1962, 540)),
    (INVISIBLE_INTRUDER_THE, ComicBookInfo(False, US, 44, 8, 1963, 26, 12, 1962, 541)),
    (ISLE_OF_GOLDEN_GEESE, ComicBookInfo(False, US, 45, 10, 1963, 28, 1, 1963, 542)),
    (TRAVEL_TIGHTWAD_THE, ComicBookInfo(False, US, 45, 10, 1963, 7, 2, 1963, 543)),
    (DUCKBURG_PET_PARADE_THE, ComicBookInfo(False, CS, 277, 10, 1963, 7, 3, 1963, 544)),
    (HELPERS_HELPING_HAND_A, ComicBookInfo(False, US, 46, 12, 1963, 19, 3, 1963, 545)),
    (HAVE_GUN_WILL_DANCE, ComicBookInfo(False, CS, 278, 11, 1963, 11, 4, 1963, 546)),
    (LOST_BENEATH_THE_SEA, ComicBookInfo(False, US, 46, 12, 1963, 27, 5, 1963, 547)),
    (LEMONADE_FLING_THE, ComicBookInfo(False, US, 46, 12, 1963, 4, 6, 1963, 548)),
    (FIREMAN_SCROOGE, ComicBookInfo(False, US, 46, 12, 1963, 7, 6, 1963, 549)),
    (SAVED_BY_THE_BAG, ComicBookInfo(False, US, 54, 12, 1964, 7, 6, 1963, 550)),
    (ONCE_UPON_A_CARNIVAL, ComicBookInfo(False, CS, 279, 12, 1963, 1, 7, 1963, 551)),
    (DOUBLE_MASQUERADE, ComicBookInfo(False, CS, 280, 1, 1964, 15, 7, 1963, 552)),
    (MAN_VERSUS_MACHINE, ComicBookInfo(False, US, 47, 2, 1964, 22, 7, 1963, 553)),
    (TICKING_DETECTOR, ComicBookInfo(False, US, 55, 2, 1965, 3, 8, 1963, 554)),
    (IT_HAPPENED_ONE_WINTER, ComicBookInfo(False, US, 61, 1, 1966, 3, 8, 1963, 555)),
    (THRIFTY_SPENDTHRIFT_THE, ComicBookInfo(False, US, 47, 2, 1964, 14, 8, 1963, 556)),
    (FEUD_AND_FAR_BETWEEN, ComicBookInfo(False, CS, 281, 2, 1964, 26, 8, 1963, 557)),
    (BUBBLEWEIGHT_CHAMP, ComicBookInfo(False, CS, 282, 3, 1964, 9, 9, 1963, 558)),
    (JONAH_GYRO, ComicBookInfo(False, US, 48, 3, 1964, 16, 9, 1963, 559)),
    (MANY_FACES_OF_MAGICA_DE_SPELL_THE, ComicBookInfo(False, US, 48, 3, 1964, 5, 10, 1963, 560)),
    (CAPN_BLIGHTS_MYSTERY_SHIP, ComicBookInfo(False, CS, 283, 4, 1964, 29, 10, 1963, 561)),
    (LOONY_LUNAR_GOLD_RUSH_THE, ComicBookInfo(False, US, 49, 5, 1964, 12, 11, 1963, 562)),
    (OLYMPIAN_TORCH_BEARER_THE, ComicBookInfo(False, CS, 286, 7, 1964, 3, 12, 1963, 563)),
    (RUG_RIDERS_IN_THE_SKY, ComicBookInfo(False, US, 50, 7, 1964, 26, 12, 1963, 564)),
    (HOW_GREEN_WAS_MY_LETTUCE, ComicBookInfo(False, US, 51, 8, 1964, 18, 1, 1964, 565)),
    (GREAT_WIG_MYSTERY_THE, ComicBookInfo(False, US, 52, 9, 1964, 19, 2, 1964, 566)),
    (HERO_OF_THE_DIKE, ComicBookInfo(False, CS, 288, 9, 1964, 6, 3, 1964, 567)),
    (INTERPLANETARY_POSTMAN, ComicBookInfo(False, US, 53, 10, 1964, 27, 3, 1964, 568)),
    (UNFRIENDLY_ENEMIES, ComicBookInfo(False, CS, 289, 10, 1964, 6, 4, 1964, 569)),
    (BILLION_DOLLAR_SAFARI_THE, ComicBookInfo(False, US, 54, 12, 1964, 11, 5, 1964, 570)),
    (DELIVERY_DILEMMA, ComicBookInfo(False, CS, 291, 12, 1964, 25, 5, 1964, 571)),
    (INSTANT_HERCULES, ComicBookInfo(False, CS, 292, 1, 1965, 11, 6, 1964, 572)),
    (MCDUCK_OF_ARABIA, ComicBookInfo(False, US, 55, 2, 1965, 13, 7, 1964, 573)),
    (MYSTERY_OF_THE_GHOST_TOWN_RAILROAD, ComicBookInfo(False, US, 56, 3, 1965, 31, 8, 1964, 574)),
    (DUCK_OUT_OF_LUCK, ComicBookInfo(False, CS, 294, 3, 1965, 17, 9, 1964, 575)),
    (LOCK_OUT_THE, ComicBookInfo(False, US, 57, 5, 1965, 19, 9, 1964, 576)),
    (BIGGER_THE_BEGGAR_THE, ComicBookInfo(False, US, 57, 5, 1965, 28, 9, 1964, 577)),
    (PLUMMETING_WITH_PRECISION, ComicBookInfo(False, US, 57, 5, 1965, 28, 9, 1964, 578)),
    (SNAKE_TAKE, ComicBookInfo(False, US, 57, 5, 1965, 28, 9, 1964, 579)),
    (SWAMP_OF_NO_RETURN_THE, ComicBookInfo(False, US, 57, 5, 1965, 30, 10, 1964, 580)),
    (MONKEY_BUSINESS, ComicBookInfo(False, CS, 297, 6, 1965, 16, 11, 1964, 581)),
    (GIANT_ROBOT_ROBBERS_THE, ComicBookInfo(False, US, 58, 7, 1965, 13, 12, 1964, 582)),
    (LAUNDRY_FOR_LESS, ComicBookInfo(False, US, 58, 7, 1965, 21, 12, 1964, 583)),
    (LONG_DISTANCE_COLLISION, ComicBookInfo(False, US, 58, 7, 1965, 21, 12, 1964, 584)),
    (TOP_WAGES, ComicBookInfo(False, US, 61, 1, 1966, 21, 12, 1964, 585)),
    (NORTH_OF_THE_YUKON, ComicBookInfo(False, US, 59, 9, 1965, 25, 1, 1965, 586)),
    (DOWN_FOR_THE_COUNT, ComicBookInfo(False, US, 61, 1, 1966, 1, 2, 1965, 587)),
    (WASTED_WORDS, ComicBookInfo(False, US, 61, 1, 1966, 8, 2, 1965, 588)),
    (PHANTOM_OF_NOTRE_DUCK_THE, ComicBookInfo(False, US, 60, 11, 1965, 4, 3, 1965, 589)),
    (SO_FAR_AND_NO_SAFARI, ComicBookInfo(False, US, 61, 1, 1966, 1, 4, 1965, 590)),
    (QUEEN_OF_THE_WILD_DOG_PACK_THE, ComicBookInfo(False, US, 62, 3, 1966, 12, 5, 1965, 591)),
    (HOUSE_OF_HAUNTS, ComicBookInfo(False, US, 63, 5, 1966, 3, 8, 1965, 592)),
    (TREASURE_OF_MARCO_POLO, ComicBookInfo(False, US, 64, 7, 1966, 13, 10, 1965, 593)),
    (BEAUTY_BUSINESS_THE, ComicBookInfo(False, CS, 308, 5, 1966, 16, 11, 1965, 594)),
    (MICRO_DUCKS_FROM_OUTER_SPACE, ComicBookInfo(False, US, 65, 9, 1966, 7, 12, 1965, 595)),
    (NOT_SO_ANCIENT_MARINER_THE, ComicBookInfo(False, CS, 312, 9, 1966, 5, 1, 1966, 596)),
    (HEEDLESS_HORSEMAN_THE, ComicBookInfo(False, US, 66, 11, 1966, 15, 2, 1966, 597)),
    (HALL_OF_THE_MERMAID_QUEEN, ComicBookInfo(False, US, 68, 3, 1967, 13, 4, 1966, 598)),
    (DOOM_DIAMOND_THE, ComicBookInfo(False, US, 70, 7, 1967, 19, 5, 1966, 599)),
    (CATTLE_KING_THE, ComicBookInfo(False, US, 69, 5, 1967, 27, 5, 1966, 600)),
    (KING_SCROOGE_THE_FIRST, ComicBookInfo(False, US, 71, 10, 1967, 22, 6, 1966, 601)),
])
# fmt: on


# NOTE: Returns OrderedDict sorted in order of submission date abd chronological number.
def get_all_comic_book_info() -> ComicBookInfoDict:
    return BARKS_TITLE_INFO


def check_story_submitted_order(all_titles: ComicBookInfoDict):
    prev_chronological_number = 0
    prev_title = ""
    prev_submitted_date = date(1940, 1, 1)
    for title in all_titles:
        if not 1 <= all_titles[title].submitted_month <= 12:
            raise Exception(
                f'"{title}": Invalid submission month: {all_titles[title].submitted_month}.'
            )
        submitted_day = (
            1 if all_titles[title].submitted_day == -1 else all_titles[title].submitted_day
        )
        submitted_date = date(
            all_titles[title].submitted_year,
            all_titles[title].submitted_month,
            submitted_day,
        )
        if prev_submitted_date > submitted_date:
            raise Exception(
                f'"{title}": Out of order submitted date {submitted_date}.'
                f' Previous entry: "{prev_title}" - {prev_submitted_date}.'
            )
        chronological_number = all_titles[title].chronological_number
        if prev_chronological_number >= chronological_number:
            raise Exception(
                f'"{title}": Out of order chronological number {chronological_number}.'
                f' Previous title: "{prev_title}"'
                f" with chronological number {prev_chronological_number}."
            )
        prev_title = title
        prev_submitted_date = submitted_date
        prev_chronological_number = chronological_number
