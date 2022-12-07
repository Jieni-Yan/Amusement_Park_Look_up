from os import major
# from google.cloud import firestore
# from google.oauth2 import service_account

import streamlit as st
import json
import pandas as pd
import numpy as np
# from st_aggrid import AgGrid, GridOptionsBuilder
# from st_aggrid.shared import GridUpdateMode
from PIL import Image
import altair as alt

# import matplotlib.pyplot as plt
# import plotly.figure_factory as ff
# import plotly.graph_objects as go
# import plotly.express as px
#
#
# from constants import *
# from neo4j_controller import Neo4jController
# import graphviz

from neo4j import GraphDatabase

# key_dict = json.loads(st.secrets["textkey"])
# creds = service_account.Credentials.from_service_account_info(key_dict)
# db = firestore.Client(credentials=creds, project="college-return-on-investment")


navi = st.sidebar.radio("Navigation", ["Amusement Park Home Page", "Parks Searching", "Park Detail", "Contact Us"])
# def park_detail():
#     # cols = st.columns((2,4))
#     # fields = ["name", 'content']
#     # for col, field_name in zip(cols, fields):
#     #     col.write(field_name)
#     d = {'col1': [1, 2], 'link': ["https://www.kentuckykingdom.com/", "http://beachboardwalk.com/"]}
#     df = pd.DataFrame(data=d)
#
#     #st.dataframe(df)
#     st.markdown(df.to_html(render_links=True), unsafe_allow_html=True)


park_name = ['Sky Zone - Roswell', 'Winter Park Historical Museum', 'Sesame Place',
             'The Holocaust Memorial Resource and Education Center', 'The Void at San Francisco Centre',
             'WinterClub Indoor Ski & Snowboard', 'The Void at Battery Atlanta', 'Seattle Art Museum',
             'Universal Studios Islands of Adventure', 'Cypress Gardens', 'Six Flags Magic Mountain',
             'Elitch Gardens', 'Sky High Sports - Concord', 'Jumpstreet - Allen', 'The Wheel at ICON Park',
             'Planet Air Sports', 'ICON Orlando', 'Fly High', 'Sky Zone - Pompano Beach', 'The Slime Factory',
             'Valleyfair!', 'Hangar Trampoline Park', 'Airbound Trampoline Park - Greensboro',
             "Holiday World & Splashin' Safari", 'Smithsonian American Art Museum (With The Renwick Gallery)',
             'Little Jan Playground', 'Quarry Park', 'NinjAdventure Park', "Monkey Joe's - Copperfield Crossing",
             'Up Down Trampoline Park', 'Glenwood Caverns Adventure Park', 'Kapiolani Park', 'Zoombezi Bay',
             'Jazzland', 'MindQuest Escape Games', 'Urban Air - South Hackensack', 'Sky Zone - Columbus',
             'AirHeads Trampoline Arena - Pinellas', 'Schlitterbahn Kansas', 'Gizmos Fun Factory',
             'Sky Zone - Miami', 'Zero Latency Wisconsin Dells', "America's Escape Game",
             "Ripley's Believe It or Not! Orlando", 'AirHeads Trampoline Arena',
             "Rockin' Jump Trampoline Park Fort Lauderdale", "Speedy's Fast Track", 'Escapology',
             'Hannibal Square Heritage Center', 'Northern Air',
             'National Museum Of African American History And Culture', 'The Wheel at Steel Pier',
             'SEA LIFE Charlotte-Concord', 'Iolani Palace', 'Aquatica San Antonio Waterpark', 'Ravine Waterpark',
             '2 Xtreme Arena', 'Disney California Adventure Park', 'iRise Trampoline & Fun Park',
             'Detroit Institute of Arts', 'Coco Key Water Resort', 'National Portrait Gallery/SAAM',
             'Galvenston Island Historic Pleasure Pier', 'Craigs Cruisers', 'Altimate Air',
             'Congo River Golf East Orlando', 'Foster Botanical Gardens', 'Arcade City',
             'Adventuredome At Circus Circus', 'High Roller', 'Wild Adventures', 'Lake Compounce',
             'SEA LIFE California USA', 'Launch Trampoline Park - Warwick',
             'Wet &#039;N Wild Emerald Pointe- Greensboro', 'Urban Air - Coppell', 'Creepy Hollow Ticket Booth',
             'Sky High Sports - Naperville', 'Riverside Park', 'Kings Island', "Wet 'N Wild Las Vegas",
             'The Park at OWA', 'Elevation Station', 'Sky Zone - Kennesaw', 'The Escape Ventures',
             'Jumpstreet - Lawrenceville', 'Urban Air - Overland Park', 'Six Flags-White Water', 'Texas Star',
             'Six Flags America', 'i-Trampoline Hawaii', 'Max Air Trampoline Park',
             'Sky High Sports - Orange County', 'Na Pali Coast State Park', 'Jumpstreet - Greenwood Village',
             'Majors Motors', 'Big Rivers Waterpark', "California's Great America", 'Worlds of Fun',
             'Metropolitan Museum of Arts', 'Jump Time - Idaho', 'Six Flags Great America', 'Zero Latency Woburn',
             'Sleuths Mystery Dinner Shows', 'Madame Tussauds Orlando', 'National Memorial Cemetery of the Pacific',
             'BALAXI - Play Party (Formerly Glowzone Willowbrook)', 'Kennywood',
             'American Museum Of Natural History', 'Pearl Harbor / WW II Valor in the Pacific National Monument',
             "Rockin' Jump - New Hartford", "Rockin' Jump - East Haven", 'Get Air - Orem',
             "Dolly Parton's Stampede", 'AZ Air Time - Scottsdale', 'Te Moana Nui, Tales of the Pacific',
             "Wet 'N Wild Splashtown", 'Snap! Space', 'Six Flags Marine World- Vallejo', 'Just Jump',
             "Martin's Fantasy Island", 'Six Flags Over Georgia', 'Lanai Cat Sanctuary', 'Drive Shack Orlando',
             'Fort DeRussy Beach Park', 'Six Flags Astroworld', 'Hawaii Tropical Botanical Garden', 'Jump America',
             'Slidewaters', "Rockin' Jump Westerville", "Morgan's Wonderland",
             'Charles Hosmer Morse Museum of American Art', 'Frontier City', 'The Woods Laser Tag', 'Puyallup Fair',
             'Get Air - Surf City', 'Beech Bend', 'Zero Gravity', 'Houston Zoo', 'Branson Ferris Wheel',
             'Waldameer Park & Water World', 'SEA LIFE Minnesota USA', "Rockin' Jump - Dublin",
             'Virtual Adventures Orlando', 'GameTime', 'Sling Shot', 'Field Museum Of Natural History',
             'The Bureau Adventure Games', 'Six Flags Discovery Kingdom', 'Indianapolis Zoo',
             'LEGOLAND Water Park California', 'The Holy Land Experience', 'Dollywood', 'The VOID Santa Monica',
             'Waianapanapa State Park', 'I-Drive NASCAR Indoor Kart Racing', 'Putting Edge', 'Adventure Park USA',
             'Nona Adventure Park', 'Strawberry Park', 'Sesame Street', 'Sun-N-Fun Lagoon', 'iXescape',
             'Jumpin Fun Sports', 'Houston Aquarium & Animal Adventure', "Rockin' Jump - Brentwood",
             'Kahuna Laguna', 'Shangri La', 'Sky Zone - Buffalo', 'Six Flags St. Louis',
             'Wycliffe Discovery Center', 'Splish-Splash', "Rockin' Jump - Fremont", 'Orlando Eye',
             'Six Flags Fiesta Texas', "Rockin' Jump - San Dimas", 'Trampoline Nation',
             "Rockin' Jump - Williamstown", 'National Gallery of Art', 'Six Flags Hurricane Harbor- Valencia',
             "Rockin' Jump - Las Vegas", 'Air Time Trampoline Park - Westland', 'American Escape Rooms', 'Aulani',
             'Rugrat Play Zone', 'Paradise Cove Luau', "Santa's Village", 'SEA LIFE Michigan',
             'Whales Tale Waterpark', 'NRH2O Family Water Park', "Mariner'S Landing", 'VR Territory',
             'Six Flags Hurricane Harbor Phoenix', 'Six Flags Hurricane Harbor- Jackson', "Knott's Berry Farm",
             'Museum of Fine Arts', "Gillian's Wonderland Pier", 'Battle Field Orlando',
             'National Vietnam War Museum', "Rockin' Jump - Myrtle Beach",
             'Airbound Trampoline Park - Winston/Salem', 'Magic Springs & Crystal Falls',
             'Chocolate Kingdom Factory Adventure Tour', "Rockin' Jump - Montgomery", 'Legoland California',
             "Rockin' Jump - Madison", 'Santa Cruz Beach Boardwalk', 'The NBA Experience', 'Aquatica',
             'Area 21 Laser Tag Arena', 'Fun Spot America', 'The Void Utah', 'Sky High Sports - Niles',
             "Rockin' Jump - Vacaville", 'The Great Escape', 'Sky Zone - Fort Wayne', 'Magic of Polynesia Show',
             'Magical Midway', "Wells' Built Museum of African American History", 'Enchanted Forest Water Safari',
             'Jumpstreet - Cedar Park', 'Urban Air - Downingtown', 'Action City Family Fun Center',
             'Air Trampoline Sports', 'Meijer Gardens and Sculpture Park', 'AirHeads Trampoline Arena - Tampa',
             'Airtime - Novi', 'California Science Center', 'Plex Indoor Sports, LLC', 'Grand Texas',
             'The VOID at Glendale Galleria', "Wet 'N Wild Orlando", 'Honolulu Museum of Art',
             'Hollywood Drive-in Golf', 'Minneapolis Institute of Arts', 'Three Point Bowling Alley',
             'Zero Latency Tulsa', 'Jumpstreet - Murfreesboro', 'Airtime - Grand Rapids', 'Wake Station Cable Park',
             "Trimper's Rides", 'Jump Highway Sports', 'Wonderland Amusement Park', 'Fun Spot Action Park',
             'Wheeling Park', 'LEGOLAND Florida Water Park', 'Old Lahaina Luau Maui', 'Huntington Library',
             'Wild Rivers', 'Jumpstreet - Plano', 'Jumpstreet - Dallas', 'Cool de Sac', 'Aloma Bowling Center',
             'Orlando Paintball', 'SeaWorld San Diego', "Rockin' Jump - San Carlos", 'Sevier Air',
             'Museum of Modern Art', 'Sky High Sports - Nashville', 'Maui Ocean Center', 'Rebounderz - Edison',
             'Houston Museum Of Natural Science', 'King Kamehameha Statue', 'Launching Pad Trampoline Park',
             'Canobie Lake Park', 'Extreme Trampoline Park', "Stumpy's Hatchet House", 'Typhoon Lagoon',
             'The Orange County Regional History Center', 'Sky High Sports - Santa Clara',
             'Paintball World Sports Complex', 'iFLY Indoor Skydiving - Orlando', 'Congo River Golf',
             'Sky Zone - Milwaukee', "Flip N' Fun Trampoline Park", 'Sky Mania Trampolines', 'Hersheypark',
             'Jumpstreet - Littleton', 'Vertical Jump Park II', 'Breakout Escape Rooms Orlando',
             'Altitude Trampoline Park - Billerica', 'Kentucky Kingdom', 'Guggenheim Museum',
             'Gator Baou Adventure Park', 'WhirlyDome', 'The Byodo-In Temple', 'Six Flags New Orleans',
             "Morey's Piers", 'Busch Gardens Tampa', 'EPCOT at Walt Disney World',
             'Sea Life Park Hawaii (Waimanalo)', 'Six Flags Wild Safari Animal Park, Jackson',
             'Knuckleheads Trampoline Park', 'Museum Of Science', 'Hanauma Bay Nature Preserve', 'Kualoa',
             'The Escape Company', 'EZ Air Trampoline Park', 'Casino Pier', 'Splitsville Luxury Lanes',
             'Madame Tussauds Washington DC', "World's Largest Entertainment McDonald's & PlayPlace", 'Escape Key',
             'Jumpstreet - Goodlettsville', 'Universal Studios Florida', 'Idlewild & SoakZone', 'AMF Sky Lanes',
             'Hawaiian Rumble Adventure Golf', 'Xtreme Air', 'Adventure Air Sports', 'Dole Plantation',
             'US Army Museum of Hawaii', 'Knoebels Amusement Park & Resort', "Rockin' Jump - O'Fallon",
             'Great Wolf Lodge', 'Seattle Great Wheel', 'Dolphins and You', 'Kings Dominion',
             'Sky High Sports - Ontario', 'Titanic: The Artifact Exhibition (Orlando)', 'The VOID West Plano',
             'RiverPark Splash Pad', 'SEA LIFE Arizona', 'Haleakala Crater(Haleakala National Park )',
             'Clementon Park', 'House of Air', 'Zero Latency Scottsdale', 'Rebounderz - Sterling',
             'Adventure Island', 'Opryland', '7D Dark Ride Adventure', 'Jumpstreet - Colleyville',
             "Pirate's Cove Adventure Golf", "Doldrick's Escape Room", 'Ark Encounter', 'Jumpstreet - Lakewood',
             'Sky Zone - Van Nuys', 'Downtown Aquarium', 'Flight Trampoline Park', 'Art Institute of Chicago',
             'Six Flags Elitch Gardens', 'Motor World', 'Galaxy Fun Park', 'Gilroy Gardens Family Theme Park',
             "Rockin' Jump - Gaithersburg", 'Sky High Sports - Burlingame', 'Main Event', 'Zero Latency Pocono',
             'The VOID at Disney Springs', 'Busch Gardens Williamsburg', 'Lagoon', 'Warrior Sports Park',
             'Jolly Roger Amusement Park', 'The Factory - Gulf Shores', 'Aerosports Trampoline Park',
             'My Little Town Kids Orlando', 'The Wairhouse Trampoline Park', "Buffalo Bill's Resort & Casino",
             'Rare Air Trampoline Park', 'Velocity Air Sports - Jacksonville', 'Defy Gravity - Lincoln', 'LACMA',
             'Sky Zone - Suwanee', "Rockin' Jump - Buffalo Grove", 'AZ Air Time - Tucson', 'Kemah Waterfront',
             'Castle Amusement Park', "Walt Disney World - Disney's Hollywood Studios",
             'Puuhonua o Honaunau National Historical Park', 'Jumpstreet - Katy', "Wet 'N Wild Phoenix",
             'Capital Wheel', 'Get Air - Roy', 'Firkin and Kegler Family Entertainment Center', 'WonderWorks',
             'Diamond Head Luau', 'Orlando Fire Museum', 'Alabama Adventure', 'Typhoon Texas Waterpark',
             'Astro Skating Center Orlando', "Rockin' Jump - Elk Grove", 'Typhoon Texas', 'Fourever Fab Show',
             'Outer Limitz Trampoline Arena', 'Steel Pier', 'Topgolf', 'Waikiki Aquarium', 'Seabreeze',
             'Akaka Falls State Park', 'Hale Koa Luau', 'Madame Tussauds Las Vegas',
             'The VOID at Grand Canal Shoppes', 'Hawaii Volcanoes National Park', 'Orlando Museum of Art',
             'Pacific Park Wheel', 'Get Out! Escape Room Orlando', "Morey's Piers and Beachfront Water Parks",
             'Air Time Trampoline Parks - Sterling Heights', 'Waldameer', 'Centennial Wheel', 'Orlando StarFlyer',
             'Lost Island Water Park', "DelGrosso's Amusement Park", 'Epic Axe Throwing', 'Wet n Wild Hawaii',
             'Urban Air - Waco', 'Off the Wall Trampoline Fun Center', 'The Void at Tysons Corner Center',
             'Sky Zone Trampoline Park - Orlando', 'Silver Dollar City', 'Orlando Science Center', 'Scene75',
             'Hangtime Trampoline Park', 'Cloud 10 Jump Club', 'The Escape Game Orlando', 'Defy Gravity',
             'Pirates Bay Waterpark', 'NASCAR SpeedPark', "Noah's Ark", "Deno's Wonder Wheel",
             'Sky High Sports - Pineville', 'Houston Funplex', 'The San Francisco Dungeon', 'Kemah Boardwalk',
             'Mennello Museum of American Art', 'FAMSF', 'Puu Ualakaa State Park', 'Tupperware Confidence Center',
             'Sky High Sports - Woodland Hills', 'Madame Tussauds San Francisco', 'DisneyQuest',
             'Cool Springz Trampoline Park', 'Six Flags New England', 'Zero Latency Las Vegas',
             'Andretti Indoor Karting and Games', 'Keansburg Amusement Park',
             'Splash Lagoon Indoor Water Park Resort', 'Casa Feliz Historic Home Museum',
             'Holiday World Santa Claus Land', 'Bronze Kingdom', 'SAAM/Renwick Gallery',
             'Six Flags Great Adventure', 'Defy', 'Nickelodeon Universe', 'Fun Spot USA',
             'USS Arizona Memorial (Honolulu)', 'The Factory - Gadsden', 'Jumpstreet - Chandler',
             'Jumpstreet - Franklin', 'Adrenaline City', 'Bishop Museum', "Monkey Joe's - Westheimer",
             'Mauna Kea Summit Adventures', 'Conneaut Lake Park', 'Universal&#039;s Volcano Bay',
             'Madame Tussauds Hollywood', 'National Air And Space Museum', 'Tomball Corn Maze',
             "Rockin' Jump - Modesto", 'SEA LIFE Kansas USA', 'Denver Museum Of Nature & Science', 'BATL',
             'Battleground Orlando', 'Rebounderz - Newport News', 'Museum Of Science And Industry', 'Playland Park',
             'SeaWorld San Antonio', 'Hyland Hills Water World', 'Hirshhorn Museum', "Dollywood's Splash Country",
             'Six Flags-Hurricane Harbor', 'Lakeside Amusement Park White City', 'Volcano Island Mini Golf',
             'Adventureland', 'Schlitterbahn-Galveston', 'Crayola Experience', 'Carowinds',
             'Miami Watersports Complex', 'Walt Disney World - Magic Kingdom',
             'Albin Polasek Museum & Sculpture Gardens', 'Adventure City', 'Water Country',
             'Zip City - Indianapolis', "Rockin' Jump Eagan", 'ClubLife SportZone', 'RDV Sportsplex Ice Den',
             'Waimea Canyon State Park', 'California Academy Of Sciences', "Michigan's Adventure",
             'USS Bowfin Submarine Museum & Park', 'Flight Trampoline', 'AirMaxx Trampoline Park - Eden Praire',
             'The Great Escape Room Orlando', 'Madame Tussauds New York', 'Schlitterbahn-New Braunfels',
             'Mt. Olympus Water & Theme Park', 'Lockbusters Escape Game', 'Calypso Cove',
             'Musical Instrument Museum', 'Escape Goat', 'Dallas Museum of Art',
             'Wildlife World Zoo, Aquarium & Safari', 'Vertical Jump Park', 'Silverwood Theme Park',
             'Shipwreck Island Waterpark', 'Rock-A-Hula', 'Altitude Trampoline Park', 'Lost Caverns Adventure Golf',
             'Statue of Duke Kahanamoku', 'Sky Zone - Sacramento', 'Orlando Watersports Complex', 'TopJump',
             'National Museum Of American History', 'Discovery Cove', 'Splashway Water Park', 'Cedar Point',
             "Flip'z Trampoline Park", 'Hermann Park Railroad', 'Anonymous Games', 'Sky Zone',
             'Zero Latency Orlando', 'Jumpstreet - Glendale', "Walt Disney World - Disney's Animal Kingdom",
             'Air Time Trampoline', 'Urban Air - Wichita Falls', 'The Escape Effect', 'Axe On Axe Off',
             'The Big Kahuna Luau', 'Lyon Arboretum', 'Flight Factory', 'SEA LIFE Dallas Fort Worth USA',
             'Panaewa Rainforest Zoo, Big Island', 'Funtown Splashtown U.S.A.', 'Hermann Park',
             'The VOID Downtown Disney', "Rockin' Jump - San Jose", 'Extreme Dinosaurs',
             'Philadelphia Museum of Art', 'Disneyland', "Hukoo's Family Fun", 'National Museum Of Natural History',
             'The Outta Control Magic Comedy Dinner Show', 'Get Air - Poway', 'Sky Sports Trampoline Park Houston',
             "Dixie Landin' Family Theme Park", 'Cedar Point Shores', 'Water Country USA',
             'The J. Paul Getty Center', "Rockin' Jump - Roseville", 'SeaWorld Orlando',
             'Six Flags Hurricane Harbor Splashtown', 'Universal Studios Hollywood', 'Wilderness Territory',
             'Knott&#039;s Soak City', "Rockin' Jump - Mt. Kisco", 'Sky High Sports - Houston', 'Flip Dunk Sports',
             'Polynesian Cultural Center', 'Funtania Orlando', 'Battleship Missouri Memorial',
             'Urban Air Adventure Park', 'Sky Zone - Toledo', 'Get Air - Temecula', 'Jumping World',
             'AirHeads Trampoine Arena - Orlando', 'Zora Neale Hurston National Museum of Fine Arts',
             'Raging Waters- San Dimas', 'Zero Latency Marlborough',
             'Air U Trampoline Park & Party Center of Greenville NC',
             'NASKART Indoor Kart Racing and Trampoline Park', 'Lucky Land', 'Six Flags Over Texas',
             'Lego Discovery Center', "Monkey Joe's", 'The Void at Mall of America', 'Stratosphere Tower',
             'Helium Trampoline & Climbing Park', 'State Fair of Texas', 'Galaxy Bowl', 'SEA LIFE Orlando',
             'Sky Zone - Newnan', 'Dorney Park & Wildwater Kingdom', "Rockin' Jump - Carol Stream",
             'Blizzard Beach', 'Honolulu Zoo', 'U.S. Holocaust Memorial Museum', 'Legoland Florida', 'Geauga Lake',
             'PanIQ Escape Room Houston', 'Six Flags Worlds Of Adventure', 'Diamond Head State Monument',
             'Sky High Sports - Ranco Cordova', 'Freer and Sackler Galleries', 'Darien Lake', 'Sky Zone - Fenton',
             'Camelbeach', 'Boardwalk Bowl Entertainment Center', 'Hapuna Beach State Park', 'Dutch Wonderland',
             'AirMaxx Trampoline Park - St. Cloud']
us_states = ['All','Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
             'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
             'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
             'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
             'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
             'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
             'West Virginia', 'Wisconsin', 'Wyoming']
park_types = ['All', 'Adventure Park', 'Religious/Spiritual', 'Watersports', 'Escape Room', 'Golf', 'Aquarium', 'Resort',
              'Indoor Park', 'Karting', 'Show', 'Waterpark', 'VR', 'Marine Attraction', 'Attraction - Other',
              'Theme Park', 'Nature/Wildlife', 'FEC', 'Closed', 'Wheel', 'Snow/Ski', 'Trampoline Park',
              'Museum/Historical', 'Botanic Gardens', 'Cultural Attraction', 'Bowling']
popularity_level = ['All','High', 'middle', 'Low']
brands = ['', 'Topgolf', 'Great Wolf Lodge', 'Disney', 'Sky Zone', 'Madame Tussauds', 'SeaWorld', 'Urban Air', 'Six Flags', "Wet 'N Wild", 'Schlitterbahn', 'Sea Life', 'Eye', 'Lego', 'Dungeons', 'Main Event', 'Universal Studios', 'Cedar Fair', 'Cool de Sac']

if navi == "Amusement Park Home Page":
    # st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
    # st.title("🎓 Diploma PDF Generator")
    # with open('choice.txt', 'w') as f:
    #     f.write('None')
    
    # image = Image.open('UNIROI.png')
    # st.image(image)
   
    st.subheader("What is Amusement Park Look Up?")
    st.write("UNIROI is a webpage platform where you can search for your interested colleges and/or majors to see the financial aspect around them. "
             "The main purpose of this platform is to provide financial information that could help you make decision on which college to go to and/or which major to pursue, "
             "in another terms, whether your decision is worth it in terms of financial investment.")

    st.write("-------------------------------------------------------------------------------------------------------")
    
    st.subheader("What is the motivation behind UNIROI?")
    st.write("When it comes to pursuing a college degree, many prospective students don’t know exactly where to start."
             " There are a lot of factors such as passion, strength, personality, tuition fee, debt after graduation, "
             "etc,... to take into account when choosing a major and which college to go to.")
    st.write("Many prospective students don’t have the privilege of having family members or someone they know that had such experiences to help "
             "guide them. These students often fall into the groups of first generation college students and "
             "underrepresented minorities.")
    st.write("Additionally, American college graduates have an average of $30000 loan debt. "
             "Some graduates may end up being in more debt due to the college they pick and/or the major they choose.")
    st.write("We want to build a website that provides prospective college students an understanding of the finance "
             "factor when it comes to getting a college degree, especially for helping first generation college students "
             "and underrepresented minorities who don’t have much resources around them.")
    st.write("-------------------------------------------------------------------------------------------------------")

    st.subheader("How to use UNIROI?")
    st.write("Two main uses of UNIROI are:" )
    st.write("- Searching for colleges/majors for finances information, which can be further explored by clicking 'University/Major Search' on the navigation bar.")
    st.write("- Calculate the total time and money for repaying loan debt, which can be further explored by clicking 'Loan Repayment Calculator' on the navigation bar.")
    st.write("-------------------------------------------------------------------------------------------------------")

    st.write("This webpage platform were built by Duyen Nguyen, Kaiyin Chan and Jieni Yan.")

park_detail_in_page = False
park_name = ""
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "dsci558"))

if navi == "Parks Searching":

    st.title("Amusement Park KG")
    st.write("In this page, you can select the amusement park you want to know, and we will show you the top 10 Amusement parks information.")
    # st.image(Image.open("images/uk-charts.png"))

    # state_option = st.multiselect(
    #     'Park Name',
    #     park_name)
    state, park_type, popularity = st.columns(3)
    # po1, po2, po3 = st.columns((4,1,4))
    with state:
        state_option = st.selectbox(
            'State',
            us_states)
    with park_type:
        type_option = st.selectbox(
            'Park Type',
            park_types)
    with popularity:
        popularity_option = st.selectbox(
            'Popularity',
            popularity_level)
    # with po2:
    #     finished = st.button("Search")
    # st.session_state
    # # if finished:
    # #st.write(state_option)
    # # if state_option not in st.session_state:
    # st.session_state['state'] = state_option
    # # if type_option not in st.session_state:
    # st.session_state['type'] = type_option
    # # if popularity_option not in st.session_state:
    # st.session_state['popularity'] = popularity_option

    with driver.session() as session:
        st.subheader("Parks")
        st.write("The top 10 amusement parks as you prefer.")
        # result = session.run("""
        # MATCH (chart:Chart)<-[inChart:IN_CHART {position: 1}]-(song)-[:ARTIST]->(artist)
        # WITH chart, song, collect(artist.name) AS artists
        # RETURN toString(chart.end) AS date, song.title AS song, artists
        # ORDER BY chart.end
        # """)

        query_state = f"MATCH (park:Park) - [:in_state] -> (state:State {{name: '{state_option}'}}), "
        if state_option == 'All':
            query_state = "MATCH (park:Park) - [:in_state] -> (state:State), "

        query_type = f"(park) - [:has_type] -> (type:Type {{name:'{type_option}'}}),"
        if type_option == 'All':
            query_type = "(park) - [:has_type] -> (type:Type),"

        query_popularity = f"(park) - [:has_popularity  ] -> (popularity:Popularity {{rank:'{popularity_option}'}})"
        if popularity_option == 'All':
            query_popularity = "(park) - [:has_popularity  ] -> (popularity:Popularity) "

        query_return = "RETURN park.name as Name, park.link as URL, popularity.rank as Popularity ORDER BY park.popularity_score DESC LIMIT 10"
        # result = session.run("""MATCH (park:Park) - [:in_state] -> (state:State {name: 'California'}),
        # (park) - [:has_type] -> (type:Type{name:"Theme Park"}),
        # (park) - [:has_popularity  ] -> (popularity:Popularity{rank:"Moderate"})
        # RETURN park.name as Name, park.link as URL, park.popularity_score as Popularity
        # ORDER BY park.popularity_score LIMIT 10 """)
        query = query_state + query_type + query_popularity + query_return
        result = session.run(query)
        # st.write(type(result.data()))
        length = len(result.data())
        result = session.run(query)
        if length == 0:
            st.write("There is no such a park as you prefer. Please change your preference and search again.")
        else:
            df = pd.DataFrame(result.data())
            # st.dataframe(df.style.hide_index())
            cols = st.columns((2,2,2,1))
            fields = ["Name", 'URL', 'Popularity Score', 'More Infor']
            for col, field_name in zip(cols, fields):
                col.write(field_name)
            button_flag = False
            park_name = ""
            for x, name in enumerate(df['Name']):
                col1, col2, col3, col4 = st.columns((2,2,2,1))
                # col1.write(x)  # index
                col1.write(df['Name'][x])  # email
                col2.write(df['URL'][x])  # unique ID
                col3.write(df['Popularity'][x])
                # col4.write(df['verified'][x])  # email status
                # disable_status = df['disabled'][x]  # flexible type of button
                # button_type = "Unblock" if disable_status else "Block"

                button_hold = col4.empty()  # create a placeholder
                do_action = button_hold.button("More", key=x)
                if do_action:
                    # button_flag = True
                    park_detail_in_page = True
                    park_name = df['Name'][x]

                    #st.session_state['park'] = park_name
                    navi = "Park Detail"

                # if button_flag is True:
                #     st.subheader(f"Park Detail for {park_name}")
        # def make_clickable(link):
        #     # target _blank to open new window
        #     # extract clickable text to display for your link
        #     # text = link.split('=')[1]
        #     return f'<a target="_blank" href="{link}"></a>'
        #
        # d = {'col1': [1, 2], 'link': ["https://www.kentuckykingdom.com/", "http://beachboardwalk.com/"]}
        # df = pd.DataFrame(data=d)
        # # link is the column with hyperlinks
        # # df['link'] = df['link'].apply(make_clickable)
        # # df = df.to_html(escape=False)
        # #st.write(df, unsafe_allow_html=True)
        # colms = st.columns((1,3,1))
        # fields = ["col1", 'link', 'more']
        # for col, field_name in zip(colms, fields):
        #     col.write(field_name)
        # # st.write(df[''])
        # for x, email in enumerate(df['col1']):
        #     col1, col2, col3= st.columns((1,3,1))
        #     #col1.write(x)  # index
        #     col1.write(df['col1'][x])  # email
        #     col2.write(df['link'][x])  # unique ID
        #     # col4.write(df['verified'][x])  # email status
        #     # disable_status = df['disabled'][x]  # flexible type of button
        #     # button_type = "Unblock" if disable_status else "Block"
        #     button_flag = False
        #     button_hold = col3.empty()  # create a placeholder
        #     do_action = button_hold.button("more", key=x)
        #     if do_action & (button_flag is False):
        #         button_flag = True
        #         navi = "Park Detail"
                # d = {'col1': [1, 2], 'link': ["https://www.kentuckykingdom.com/", "http://beachboardwalk.com/"]}
                # df = pd.DataFrame(data=d)
                #
                # # st.dataframe(df)
                # st.markdown(df.to_html(render_links=True), unsafe_allow_html=True)

            # if do_action & (button_flag is True):
            #     button_flag = False

                  # do some action with a row's data



        #button_hold = col3.empty()
        #do_action = button_hold.button("More", key=x)

        # page_names_to_funcs = {
        #     "": amusement_park_home_page,
        #     "Plotting Demo": plotting_demo,
        #     "Mapping Demo": mapping_demo,
        #     "DataFrame Demo": data_frame_demo
        # }
        #
        # demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
        # page_names_to_funcs[demo_name]()

        # st.dataframe(df)
        # st.markdown(df.to_html(render_links=True), unsafe_allow_html=True)
        #st.write(df)

park_name = ['Sky Zone - Roswell', 'Winter Park Historical Museum', 'Sesame Place',
             'The Holocaust Memorial Resource and Education Center', 'The Void at San Francisco Centre',
             'WinterClub Indoor Ski & Snowboard', 'The Void at Battery Atlanta', 'Seattle Art Museum',
             'Universal Studios Islands of Adventure', 'Cypress Gardens', 'Six Flags Magic Mountain',
             'Elitch Gardens', 'Sky High Sports - Concord', 'Jumpstreet - Allen', 'The Wheel at ICON Park',
             'Planet Air Sports', 'ICON Orlando', 'Fly High', 'Sky Zone - Pompano Beach', 'The Slime Factory',
             'Valleyfair!', 'Hangar Trampoline Park', 'Airbound Trampoline Park - Greensboro',
             "Holiday World & Splashin' Safari", 'Smithsonian American Art Museum (With The Renwick Gallery)',
             'Little Jan Playground', 'Quarry Park', 'NinjAdventure Park', "Monkey Joe's - Copperfield Crossing",
             'Up Down Trampoline Park', 'Glenwood Caverns Adventure Park', 'Kapiolani Park', 'Zoombezi Bay',
             'Jazzland', 'MindQuest Escape Games', 'Urban Air - South Hackensack', 'Sky Zone - Columbus',
             'AirHeads Trampoline Arena - Pinellas', 'Schlitterbahn Kansas', 'Gizmos Fun Factory',
             'Sky Zone - Miami', 'Zero Latency Wisconsin Dells', "America's Escape Game",
             "Ripley's Believe It or Not! Orlando", 'AirHeads Trampoline Arena',
             "Rockin' Jump Trampoline Park Fort Lauderdale", "Speedy's Fast Track", 'Escapology',
             'Hannibal Square Heritage Center', 'Northern Air',
             'National Museum Of African American History And Culture', 'The Wheel at Steel Pier',
             'SEA LIFE Charlotte-Concord', 'Iolani Palace', 'Aquatica San Antonio Waterpark', 'Ravine Waterpark',
             '2 Xtreme Arena', 'Disney California Adventure Park', 'iRise Trampoline & Fun Park',
             'Detroit Institute of Arts', 'Coco Key Water Resort', 'National Portrait Gallery/SAAM',
             'Galvenston Island Historic Pleasure Pier', 'Craigs Cruisers', 'Altimate Air',
             'Congo River Golf East Orlando', 'Foster Botanical Gardens', 'Arcade City',
             'Adventuredome At Circus Circus', 'High Roller', 'Wild Adventures', 'Lake Compounce',
             'SEA LIFE California USA', 'Launch Trampoline Park - Warwick',
             'Wet &#039;N Wild Emerald Pointe- Greensboro', 'Urban Air - Coppell', 'Creepy Hollow Ticket Booth',
             'Sky High Sports - Naperville', 'Riverside Park', 'Kings Island', "Wet 'N Wild Las Vegas",
             'The Park at OWA', 'Elevation Station', 'Sky Zone - Kennesaw', 'The Escape Ventures',
             'Jumpstreet - Lawrenceville', 'Urban Air - Overland Park', 'Six Flags-White Water', 'Texas Star',
             'Six Flags America', 'i-Trampoline Hawaii', 'Max Air Trampoline Park',
             'Sky High Sports - Orange County', 'Na Pali Coast State Park', 'Jumpstreet - Greenwood Village',
             'Majors Motors', 'Big Rivers Waterpark', "California's Great America", 'Worlds of Fun',
             'Metropolitan Museum of Arts', 'Jump Time - Idaho', 'Six Flags Great America', 'Zero Latency Woburn',
             'Sleuths Mystery Dinner Shows', 'Madame Tussauds Orlando', 'National Memorial Cemetery of the Pacific',
             'BALAXI - Play Party (Formerly Glowzone Willowbrook)', 'Kennywood',
             'American Museum Of Natural History', 'Pearl Harbor / WW II Valor in the Pacific National Monument',
             "Rockin' Jump - New Hartford", "Rockin' Jump - East Haven", 'Get Air - Orem',
             "Dolly Parton's Stampede", 'AZ Air Time - Scottsdale', 'Te Moana Nui, Tales of the Pacific',
             "Wet 'N Wild Splashtown", 'Snap! Space', 'Six Flags Marine World- Vallejo', 'Just Jump',
             "Martin's Fantasy Island", 'Six Flags Over Georgia', 'Lanai Cat Sanctuary', 'Drive Shack Orlando',
             'Fort DeRussy Beach Park', 'Six Flags Astroworld', 'Hawaii Tropical Botanical Garden', 'Jump America',
             'Slidewaters', "Rockin' Jump Westerville", "Morgan's Wonderland",
             'Charles Hosmer Morse Museum of American Art', 'Frontier City', 'The Woods Laser Tag', 'Puyallup Fair',
             'Get Air - Surf City', 'Beech Bend', 'Zero Gravity', 'Houston Zoo', 'Branson Ferris Wheel',
             'Waldameer Park & Water World', 'SEA LIFE Minnesota USA', "Rockin' Jump - Dublin",
             'Virtual Adventures Orlando', 'GameTime', 'Sling Shot', 'Field Museum Of Natural History',
             'The Bureau Adventure Games', 'Six Flags Discovery Kingdom', 'Indianapolis Zoo',
             'LEGOLAND Water Park California', 'The Holy Land Experience', 'Dollywood', 'The VOID Santa Monica',
             'Waianapanapa State Park', 'I-Drive NASCAR Indoor Kart Racing', 'Putting Edge', 'Adventure Park USA',
             'Nona Adventure Park', 'Strawberry Park', 'Sesame Street', 'Sun-N-Fun Lagoon', 'iXescape',
             'Jumpin Fun Sports', 'Houston Aquarium & Animal Adventure', "Rockin' Jump - Brentwood",
             'Kahuna Laguna', 'Shangri La', 'Sky Zone - Buffalo', 'Six Flags St. Louis',
             'Wycliffe Discovery Center', 'Splish-Splash', "Rockin' Jump - Fremont", 'Orlando Eye',
             'Six Flags Fiesta Texas', "Rockin' Jump - San Dimas", 'Trampoline Nation',
             "Rockin' Jump - Williamstown", 'National Gallery of Art', 'Six Flags Hurricane Harbor- Valencia',
             "Rockin' Jump - Las Vegas", 'Air Time Trampoline Park - Westland', 'American Escape Rooms', 'Aulani',
             'Rugrat Play Zone', 'Paradise Cove Luau', "Santa's Village", 'SEA LIFE Michigan',
             'Whales Tale Waterpark', 'NRH2O Family Water Park', "Mariner'S Landing", 'VR Territory',
             'Six Flags Hurricane Harbor Phoenix', 'Six Flags Hurricane Harbor- Jackson', "Knott's Berry Farm",
             'Museum of Fine Arts', "Gillian's Wonderland Pier", 'Battle Field Orlando',
             'National Vietnam War Museum', "Rockin' Jump - Myrtle Beach",
             'Airbound Trampoline Park - Winston/Salem', 'Magic Springs & Crystal Falls',
             'Chocolate Kingdom Factory Adventure Tour', "Rockin' Jump - Montgomery", 'Legoland California',
             "Rockin' Jump - Madison", 'Santa Cruz Beach Boardwalk', 'The NBA Experience', 'Aquatica',
             'Area 21 Laser Tag Arena', 'Fun Spot America', 'The Void Utah', 'Sky High Sports - Niles',
             "Rockin' Jump - Vacaville", 'The Great Escape', 'Sky Zone - Fort Wayne', 'Magic of Polynesia Show',
             'Magical Midway', "Wells' Built Museum of African American History", 'Enchanted Forest Water Safari',
             'Jumpstreet - Cedar Park', 'Urban Air - Downingtown', 'Action City Family Fun Center',
             'Air Trampoline Sports', 'Meijer Gardens and Sculpture Park', 'AirHeads Trampoline Arena - Tampa',
             'Airtime - Novi', 'California Science Center', 'Plex Indoor Sports, LLC', 'Grand Texas',
             'The VOID at Glendale Galleria', "Wet 'N Wild Orlando", 'Honolulu Museum of Art',
             'Hollywood Drive-in Golf', 'Minneapolis Institute of Arts', 'Three Point Bowling Alley',
             'Zero Latency Tulsa', 'Jumpstreet - Murfreesboro', 'Airtime - Grand Rapids', 'Wake Station Cable Park',
             "Trimper's Rides", 'Jump Highway Sports', 'Wonderland Amusement Park', 'Fun Spot Action Park',
             'Wheeling Park', 'LEGOLAND Florida Water Park', 'Old Lahaina Luau Maui', 'Huntington Library',
             'Wild Rivers', 'Jumpstreet - Plano', 'Jumpstreet - Dallas', 'Cool de Sac', 'Aloma Bowling Center',
             'Orlando Paintball', 'SeaWorld San Diego', "Rockin' Jump - San Carlos", 'Sevier Air',
             'Museum of Modern Art', 'Sky High Sports - Nashville', 'Maui Ocean Center', 'Rebounderz - Edison',
             'Houston Museum Of Natural Science', 'King Kamehameha Statue', 'Launching Pad Trampoline Park',
             'Canobie Lake Park', 'Extreme Trampoline Park', "Stumpy's Hatchet House", 'Typhoon Lagoon',
             'The Orange County Regional History Center', 'Sky High Sports - Santa Clara',
             'Paintball World Sports Complex', 'iFLY Indoor Skydiving - Orlando', 'Congo River Golf',
             'Sky Zone - Milwaukee', "Flip N' Fun Trampoline Park", 'Sky Mania Trampolines', 'Hersheypark',
             'Jumpstreet - Littleton', 'Vertical Jump Park II', 'Breakout Escape Rooms Orlando',
             'Altitude Trampoline Park - Billerica', 'Kentucky Kingdom', 'Guggenheim Museum',
             'Gator Baou Adventure Park', 'WhirlyDome', 'The Byodo-In Temple', 'Six Flags New Orleans',
             "Morey's Piers", 'Busch Gardens Tampa', 'EPCOT at Walt Disney World',
             'Sea Life Park Hawaii (Waimanalo)', 'Six Flags Wild Safari Animal Park, Jackson',
             'Knuckleheads Trampoline Park', 'Museum Of Science', 'Hanauma Bay Nature Preserve', 'Kualoa',
             'The Escape Company', 'EZ Air Trampoline Park', 'Casino Pier', 'Splitsville Luxury Lanes',
             'Madame Tussauds Washington DC', "World's Largest Entertainment McDonald's & PlayPlace", 'Escape Key',
             'Jumpstreet - Goodlettsville', 'Universal Studios Florida', 'Idlewild & SoakZone', 'AMF Sky Lanes',
             'Hawaiian Rumble Adventure Golf', 'Xtreme Air', 'Adventure Air Sports', 'Dole Plantation',
             'US Army Museum of Hawaii', 'Knoebels Amusement Park & Resort', "Rockin' Jump - O'Fallon",
             'Great Wolf Lodge', 'Seattle Great Wheel', 'Dolphins and You', 'Kings Dominion',
             'Sky High Sports - Ontario', 'Titanic: The Artifact Exhibition (Orlando)', 'The VOID West Plano',
             'RiverPark Splash Pad', 'SEA LIFE Arizona', 'Haleakala Crater(Haleakala National Park )',
             'Clementon Park', 'House of Air', 'Zero Latency Scottsdale', 'Rebounderz - Sterling',
             'Adventure Island', 'Opryland', '7D Dark Ride Adventure', 'Jumpstreet - Colleyville',
             "Pirate's Cove Adventure Golf", "Doldrick's Escape Room", 'Ark Encounter', 'Jumpstreet - Lakewood',
             'Sky Zone - Van Nuys', 'Downtown Aquarium', 'Flight Trampoline Park', 'Art Institute of Chicago',
             'Six Flags Elitch Gardens', 'Motor World', 'Galaxy Fun Park', 'Gilroy Gardens Family Theme Park',
             "Rockin' Jump - Gaithersburg", 'Sky High Sports - Burlingame', 'Main Event', 'Zero Latency Pocono',
             'The VOID at Disney Springs', 'Busch Gardens Williamsburg', 'Lagoon', 'Warrior Sports Park',
             'Jolly Roger Amusement Park', 'The Factory - Gulf Shores', 'Aerosports Trampoline Park',
             'My Little Town Kids Orlando', 'The Wairhouse Trampoline Park', "Buffalo Bill's Resort & Casino",
             'Rare Air Trampoline Park', 'Velocity Air Sports - Jacksonville', 'Defy Gravity - Lincoln', 'LACMA',
             'Sky Zone - Suwanee', "Rockin' Jump - Buffalo Grove", 'AZ Air Time - Tucson', 'Kemah Waterfront',
             'Castle Amusement Park', "Walt Disney World - Disney's Hollywood Studios",
             'Puuhonua o Honaunau National Historical Park', 'Jumpstreet - Katy', "Wet 'N Wild Phoenix",
             'Capital Wheel', 'Get Air - Roy', 'Firkin and Kegler Family Entertainment Center', 'WonderWorks',
             'Diamond Head Luau', 'Orlando Fire Museum', 'Alabama Adventure', 'Typhoon Texas Waterpark',
             'Astro Skating Center Orlando', "Rockin' Jump - Elk Grove", 'Typhoon Texas', 'Fourever Fab Show',
             'Outer Limitz Trampoline Arena', 'Steel Pier', 'Topgolf', 'Waikiki Aquarium', 'Seabreeze',
             'Akaka Falls State Park', 'Hale Koa Luau', 'Madame Tussauds Las Vegas',
             'The VOID at Grand Canal Shoppes', 'Hawaii Volcanoes National Park', 'Orlando Museum of Art',
             'Pacific Park Wheel', 'Get Out! Escape Room Orlando', "Morey's Piers and Beachfront Water Parks",
             'Air Time Trampoline Parks - Sterling Heights', 'Waldameer', 'Centennial Wheel', 'Orlando StarFlyer',
             'Lost Island Water Park', "DelGrosso's Amusement Park", 'Epic Axe Throwing', 'Wet n Wild Hawaii',
             'Urban Air - Waco', 'Off the Wall Trampoline Fun Center', 'The Void at Tysons Corner Center',
             'Sky Zone Trampoline Park - Orlando', 'Silver Dollar City', 'Orlando Science Center', 'Scene75',
             'Hangtime Trampoline Park', 'Cloud 10 Jump Club', 'The Escape Game Orlando', 'Defy Gravity',
             'Pirates Bay Waterpark', 'NASCAR SpeedPark', "Noah's Ark", "Deno's Wonder Wheel",
             'Sky High Sports - Pineville', 'Houston Funplex', 'The San Francisco Dungeon', 'Kemah Boardwalk',
             'Mennello Museum of American Art', 'FAMSF', 'Puu Ualakaa State Park', 'Tupperware Confidence Center',
             'Sky High Sports - Woodland Hills', 'Madame Tussauds San Francisco', 'DisneyQuest',
             'Cool Springz Trampoline Park', 'Six Flags New England', 'Zero Latency Las Vegas',
             'Andretti Indoor Karting and Games', 'Keansburg Amusement Park',
             'Splash Lagoon Indoor Water Park Resort', 'Casa Feliz Historic Home Museum',
             'Holiday World Santa Claus Land', 'Bronze Kingdom', 'SAAM/Renwick Gallery',
             'Six Flags Great Adventure', 'Defy', 'Nickelodeon Universe', 'Fun Spot USA',
             'USS Arizona Memorial (Honolulu)', 'The Factory - Gadsden', 'Jumpstreet - Chandler',
             'Jumpstreet - Franklin', 'Adrenaline City', 'Bishop Museum', "Monkey Joe's - Westheimer",
             'Mauna Kea Summit Adventures', 'Conneaut Lake Park', 'Universal&#039;s Volcano Bay',
             'Madame Tussauds Hollywood', 'National Air And Space Museum', 'Tomball Corn Maze',
             "Rockin' Jump - Modesto", 'SEA LIFE Kansas USA', 'Denver Museum Of Nature & Science', 'BATL',
             'Battleground Orlando', 'Rebounderz - Newport News', 'Museum Of Science And Industry', 'Playland Park',
             'SeaWorld San Antonio', 'Hyland Hills Water World', 'Hirshhorn Museum', "Dollywood's Splash Country",
             'Six Flags-Hurricane Harbor', 'Lakeside Amusement Park White City', 'Volcano Island Mini Golf',
             'Adventureland', 'Schlitterbahn-Galveston', 'Crayola Experience', 'Carowinds',
             'Miami Watersports Complex', 'Walt Disney World - Magic Kingdom',
             'Albin Polasek Museum & Sculpture Gardens', 'Adventure City', 'Water Country',
             'Zip City - Indianapolis', "Rockin' Jump Eagan", 'ClubLife SportZone', 'RDV Sportsplex Ice Den',
             'Waimea Canyon State Park', 'California Academy Of Sciences', "Michigan's Adventure",
             'USS Bowfin Submarine Museum & Park', 'Flight Trampoline', 'AirMaxx Trampoline Park - Eden Praire',
             'The Great Escape Room Orlando', 'Madame Tussauds New York', 'Schlitterbahn-New Braunfels',
             'Mt. Olympus Water & Theme Park', 'Lockbusters Escape Game', 'Calypso Cove',
             'Musical Instrument Museum', 'Escape Goat', 'Dallas Museum of Art',
             'Wildlife World Zoo, Aquarium & Safari', 'Vertical Jump Park', 'Silverwood Theme Park',
             'Shipwreck Island Waterpark', 'Rock-A-Hula', 'Altitude Trampoline Park', 'Lost Caverns Adventure Golf',
             'Statue of Duke Kahanamoku', 'Sky Zone - Sacramento', 'Orlando Watersports Complex', 'TopJump',
             'National Museum Of American History', 'Discovery Cove', 'Splashway Water Park', 'Cedar Point',
             "Flip'z Trampoline Park", 'Hermann Park Railroad', 'Anonymous Games', 'Sky Zone',
             'Zero Latency Orlando', 'Jumpstreet - Glendale', "Walt Disney World - Disney's Animal Kingdom",
             'Air Time Trampoline', 'Urban Air - Wichita Falls', 'The Escape Effect', 'Axe On Axe Off',
             'The Big Kahuna Luau', 'Lyon Arboretum', 'Flight Factory', 'SEA LIFE Dallas Fort Worth USA',
             'Panaewa Rainforest Zoo, Big Island', 'Funtown Splashtown U.S.A.', 'Hermann Park',
             'The VOID Downtown Disney', "Rockin' Jump - San Jose", 'Extreme Dinosaurs',
             'Philadelphia Museum of Art', 'Disneyland', "Hukoo's Family Fun", 'National Museum Of Natural History',
             'The Outta Control Magic Comedy Dinner Show', 'Get Air - Poway', 'Sky Sports Trampoline Park Houston',
             "Dixie Landin' Family Theme Park", 'Cedar Point Shores', 'Water Country USA',
             'The J. Paul Getty Center', "Rockin' Jump - Roseville", 'SeaWorld Orlando',
             'Six Flags Hurricane Harbor Splashtown', 'Universal Studios Hollywood', 'Wilderness Territory',
             'Knott&#039;s Soak City', "Rockin' Jump - Mt. Kisco", 'Sky High Sports - Houston', 'Flip Dunk Sports',
             'Polynesian Cultural Center', 'Funtania Orlando', 'Battleship Missouri Memorial',
             'Urban Air Adventure Park', 'Sky Zone - Toledo', 'Get Air - Temecula', 'Jumping World',
             'AirHeads Trampoine Arena - Orlando', 'Zora Neale Hurston National Museum of Fine Arts',
             'Raging Waters- San Dimas', 'Zero Latency Marlborough',
             'Air U Trampoline Park & Party Center of Greenville NC',
             'NASKART Indoor Kart Racing and Trampoline Park', 'Lucky Land', 'Six Flags Over Texas',
             'Lego Discovery Center', "Monkey Joe's", 'The Void at Mall of America', 'Stratosphere Tower',
             'Helium Trampoline & Climbing Park', 'State Fair of Texas', 'Galaxy Bowl', 'SEA LIFE Orlando',
             'Sky Zone - Newnan', 'Dorney Park & Wildwater Kingdom', "Rockin' Jump - Carol Stream",
             'Blizzard Beach', 'Honolulu Zoo', 'U.S. Holocaust Memorial Museum', 'Legoland Florida', 'Geauga Lake',
             'PanIQ Escape Room Houston', 'Six Flags Worlds Of Adventure', 'Diamond Head State Monument',
             'Sky High Sports - Ranco Cordova', 'Freer and Sackler Galleries', 'Darien Lake', 'Sky Zone - Fenton',
             'Camelbeach', 'Boardwalk Bowl Entertainment Center', 'Hapuna Beach State Park', 'Dutch Wonderland',
             'AirMaxx Trampoline Park - St. Cloud']
if navi == "Park Detail":
    if park_detail_in_page:
        st.subheader(f"Park Detail for {park_name}")
        with driver.session() as session:

            # query_return = "RETURN park.name as Name, park.link as URL, popularity.rank as Popularity ORDER BY park.popularity_score DESC LIMIT 10"
            park_result = session.run(f'''MATCH (park:Park{{name:"{park_name}"}}) - [:in_state] -> (state:State), (park) - [:has_type] -> (type:Type) 
                        RETURN park.name as Name, park.popularity_score as Popularity, park.adult as Adult_Price, park.child as Child, state.name as State, type.name as Type''')
            park_df = pd.DataFrame(park_result.data())
            brand_result = session.run(
                f'''MATCH (park:Park{{name:"{park_name}"}}) - [:has_brand] -> (brand:Brand) RETURN park.name as Name, brand.name as Brand''')
            brand_df = pd.DataFrame(brand_result.data())
            county_result = session.run(
                f'''MATCH (park:Park{{name:"{park_name}"}}) - [:in_county] -> (county:County) RETURN park.name as Name, county.name as County''')
            # df1.merge(df2, left_on='lkey', right_on='rkey')
            county_df = pd.DataFrame(county_result.data())

            if brand_df.shape[0] != 0:
                park_df = park_df.merge(brand_df, on='Name')
            if brand_df.shape[0] != 0:
                park_df = park_df.merge(county_df, on='Name')
            park_df.index = ["Content"]
            park_df = park_df.transpose()

            # keys = list(park_df.keys())
            # for i in range(len(keys)):
            #     properties, value = st.columns((1,2))
            #     with properties:
            #         st.text(keys[i])
            #     with value:
            #         if keys[i] == "Popularity":
            #             popu = round(float(park_df[keys[i]][0]),4)
            #             st.text(popu)
            #         else:
            #             st.text(park_df[keys[i]][0])
            st.dataframe(park_df.style.hide_index())
    else:
        st.subheader("Park Detail")
        st.write("Display specific park information you choose")
        park, location = st.columns((2, 1))
        with park:
            park_option = st.selectbox(
                'Park Name',
                park_name)
        with location:
            location_option = st.selectbox(
                'State',
                us_states)
        # with po2:
        #     submitted = st.button("Search")

        # if submitted:
        #     st.write(location_option)
        with driver.session() as session:
            # query_return = "RETURN park.name as Name, park.link as URL, popularity.rank as Popularity ORDER BY park.popularity_score DESC LIMIT 10"
            park_result = session.run(f'''MATCH (park:Park{{name:"{park_option}"}}) - [:in_state] -> (state:State), (park) - [:has_type] -> (type:Type) 
                        RETURN park.name as Name, park.link as URL, park.popularity_score as Popularity, park.adult as Adult_Price, park.child as Child, state.name as State, type.name as Type''')
            park_df = pd.DataFrame(park_result.data())
            brand_result = session.run(
                f'''MATCH (park:Park{{name:"{park_option}"}}) - [:has_brand] -> (brand:Brand) RETURN park.name as Name, brand.name as Brand''')
            brand_df = pd.DataFrame(brand_result.data())
            county_result = session.run(
                f'''MATCH (park:Park{{name:"{park_option}"}}) - [:in_county] -> (county:County) RETURN park.name as Name, county.name as County''')
            # df1.merge(df2, left_on='lkey', right_on='rkey')
            county_df = pd.DataFrame(county_result.data())

            if brand_df.shape[0] != 0:
                park_df = park_df.merge(brand_df, on='Name')
            if brand_df.shape[0] != 0:
                park_df = park_df.merge(county_df, on='Name')
            # park_df.index = ["Content"]
            # park_df = park_df.transpose()

            keys = list(park_df.keys())
            for i in range(len(keys)):
                properties, value = st.columns((1,2))
                with properties:
                    st.text(keys[i]+":")
                with value:
                    if keys[i] == "Popularity":
                        popu = round(float(park_df[keys[i]][0]),4)
                        st.text(popu)

                    elif keys[i] == 'URL':
                        st.write(f"[Official Website]({park_df[keys[i]][0]})")
                    else:
                        st.text(park_df[keys[i]][0])

        # d = {'col1': [1, 2], 'link': ["https://www.kentuckykingdom.com/", "http://beachboardwalk.com/"]}
        # df = pd.DataFrame(data=d)

        # st.dataframe(df)
        # st.markdown(df.to_html(render_links=True), unsafe_allow_html=True)

if navi == "Contact Us":
    st.header('Contact Us')
    st.write("We appricate you for trying out UNIROI and we would love to hear your thoughts on what you love and/or any improvements we can make!")
    st.write("Submit the form below and we will take a look at it as soon as possible!")

    form = st.form(key="feedback", clear_on_submit=True)
    with form:
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        cols = st.columns(2)
        area = cols[0].text_input("Area Code")
        tel = cols[1].text_input("Phone Number")
        email = st.text_input("Email Address")
        cont = st.columns(2)
        contact1 = cont[0].checkbox("May we contact you?")
        contact2 = cont[1].selectbox("Contact By", ('Phone', 'Email'))
        feedback = st.text_area("Feedback")
        submitted = st.form_submit_button(label="Submit")

        if submitted:
            st.success("Submit Successfully!")
            doc_ref = db.collection("Feedback").document(f"{fname} {lname}")
            doc_ref.set({
                "Area Code": area,
                "Tel.Number": tel,
                "Email": email,
                "May we contact you": contact1,
                "Contact By": contact2,
                "Feedback": feedback
            })