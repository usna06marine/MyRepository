"""
Builds mdm2026_schedule_raw.json and mdm2026_speaker_stage_lookup.csv

Days 1–2 (April 28–29) are exact — sourced directly from the official
marinemilitaryexpos.com/pme-sessions/ schedule (user-supplied paste).
Day 3 (April 30) is a placeholder pending the user's paste.
"""

import json
import csv


def S(name, rank, role):
    return {"name": name, "rank": rank, "role": role}


# ---------------------------------------------------------------------------
# Day 1 — April 28, 2026  (confirmed from official schedule paste)
# ---------------------------------------------------------------------------
day1_sessions = [

    # ── Special Events ───────────────────────────────────────────────────
    {"day": "April 28", "start_time": "09:00 AM", "end_time": "03:00 PM",
     "stage": "Conference Rooms (TBD)", "track": "Special Events", "format": "",
     "title": "GCE UAS/C-UAS Symposium", "speakers": []},

    {"day": "April 28", "start_time": "09:00 AM", "end_time": "03:00 PM",
     "stage": "101 & 102 A", "track": "Special Events", "format": "",
     "title": "Logistics Command Artificial Intelligence Symposium", "speakers": []},

    {"day": "April 28", "start_time": "09:00 AM", "end_time": "09:20 AM",
     "stage": "Main Briefing Center", "track": "Special Events", "format": "Session",
     "title": "Opening Ceremony", "speakers": []},

    {"day": "April 28", "start_time": "04:00 PM", "end_time": "04:45 PM",
     "stage": "Warfighting Stage", "track": "Special Events", "format": "",
     "title": "Warfighting Reception", "speakers": []},

    # ── Main Briefing Center ─────────────────────────────────────────────
    {"day": "April 28", "start_time": "09:30 AM", "end_time": "10:30 AM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Everyone Fights: A Senior Enlisted Perspective on Preparing Marines for the Next 250 Years",
     "speakers": [
         S("Ryan Gnecco",      "SgtMaj",    "Sergeant Major, Training and Education Command"),
         S("Daniel L. Krause", "Sgt. Maj.", "Senior Enlisted Advisor to the Sergeant Major of the Marine Corps"),
         S("Anthony Loftus",   "SgtMaj",    "Command Senior Enlisted Leader, II Marine Expeditionary Force"),
         S("Jacob Reiff",      "SgtMaj",    "Sergeant Major, Manpower and Reserve Affairs"),
         S("Carlos Ruiz",      "SgtMaj",    "Sergeant Major of the Marine Corps"),
     ]},

    {"day": "April 28", "start_time": "11:00 AM", "end_time": "12:00 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Ground Combat Element 2040: Technological Dominance Through a Marine-Centric Approach",
     "speakers": [
         S("Erick Clark",     "Col",    "Branch Head Future Operations, Plans, Policies, and Operations"),
         S("Kyle Ellison",    "MajGen", "Commanding General, 3D Marine Division"),
         S("John Jarrard",    "MajGen", "Commanding General, 4th Marine Division"),
         S("Jason Morris",    "MajGen", "Director of Operations, Plans Policies, and Operations, HQMC"),
         S("Farrell Sullivan","MajGen", "Commanding General, 2D Marine Division"),
     ]},

    {"day": "April 28", "start_time": "12:30 PM", "end_time": "01:30 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Maritime Prepositioning for the 21st Century",
     "speakers": [
         S("Shon Brodie",     "Mr.",   "Director, Maritime Expeditionary Warfare, HQMC CD&I"),
         S("Stephen Sklenka", "LtGen", "Deputy Commandant, Installations and Logistics, DC I&L, HQMC"),
     ]},

    {"day": "April 28", "start_time": "02:00 PM", "end_time": "03:00 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Preparing Marines for the All-Domain Fight through Training and Education",
     "speakers": [
         S("Michael Brooks",  "BGen",   "Commanding General, Training Command"),
         S("Mark H. Clingan", "MajGen", "Commanding General, MAGTF Training Command, Marine Corps Air Ground Combat Center"),
         S("Benjamin Watson", "LtGen",  "Commanding General, Training & Education Command"),
     ]},

    {"day": "April 28", "start_time": "03:10 PM", "end_time": "04:10 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Acting Secretary of the Navy Address",
     "speakers": [S("Hung Cao", "Honorable", "Acting Secretary of the Navy")]},

    # ── Acquisitions Stage ───────────────────────────────────────────────
    {"day": "April 28", "start_time": "09:30 AM", "end_time": "10:10 AM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "General's Opening Remarks from PEO(A)",
     "speakers": [S("David Walsh", "MajGen", "Program Executive Officer Air, Anti-Submarine Warfare, Assault, and Special Mission Programs")]},

    {"day": "April 28", "start_time": "10:15 AM", "end_time": "10:55 AM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "XMA-ADT Expeditionary Maritime Aviation Advanced Development Team",
     "speakers": [S("Scott Shadforth", "Col", "Director, Expeditionary and Maritime Aviation - Advanced Development Team (XMA-ADT)")]},

    {"day": "April 28", "start_time": "11:00 AM", "end_time": "11:40 AM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PM Ground Based Air Defense: USMC Approach to Fielding Counter-Air Capabilities",
     "speakers": [S("Andrew Konicki", "Col", "Program Manager Ground Based Air Defense")]},

    {"day": "April 28", "start_time": "11:45 AM", "end_time": "12:25 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PMA-263 Small Tactical Unmanned Air Systems Overview",
     "speakers": [S("Gregg Skinner", "CIV", "Program Manager STUAS")]},

    {"day": "April 28", "start_time": "12:30 PM", "end_time": "01:00 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "Transforming Training with Cutting-Edge Capabilities",
     "speakers": [S("David Bain", "LtCol", "Deputy Program Manager, Training Systems")]},

    {"day": "April 28", "start_time": "01:05 PM", "end_time": "01:35 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PMA-266 Multi-Mission Tactical Unmanned Air Systems Overview",
     "speakers": [S("Leigh Irwin", "Col", "Program Manager, Multi-Mission Tactical Unmanned Aerial Systems (UAS)")]},

    {"day": "April 28", "start_time": "01:40 PM", "end_time": "02:10 PM",
     "stage": "Acquisitions Stage", "track": "Industry", "format": "Session",
     "title": "Model-Based Systems Engineering: Accelerating system design through model-based methods",
     "speakers": [
         S("Adam Boas",   "", "Solutions Architect, KBR"),
         S("Grant Clyne", "", "Senior Manager of Business Development, KBR"),
     ]},

    {"day": "April 28", "start_time": "02:15 PM", "end_time": "02:55 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PEO Digital",
     "speakers": [S("Jonathan G. Metcalf", "Maj", "")]},

    {"day": "April 28", "start_time": "03:30 PM", "end_time": "04:10 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PM Tactical Communications and Electromagnetic Warfare Systems: Communications Modularity on the Battlefield",
     "speakers": [S("John Mithun", "CIV", "Program Manager, Tactical Communications and Electromagnetic Warfare Systems")]},

    # ── Warfighting Stage ────────────────────────────────────────────────
    {"day": "April 28", "start_time": "09:40 AM", "end_time": "10:20 AM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "Session",
     "title": "Capability Development and the New Joint Force Requirements Process",
     "speakers": [S("Joshua Freeland", "LtCol", "MAGTF Planner, Marine Corps Integration Division")]},

    {"day": "April 28", "start_time": "10:50 AM", "end_time": "11:20 AM",
     "stage": "Warfighting Stage", "track": "Industry", "format": "Session",
     "title": "From Perception to Coordination: Advancing Edge-Based Warfighting for Marine Corps Operations",
     "speakers": [S("Ed Sullivan", "Col (ret.)", "USMC Principal, Business Development, TurbineOne, Inc.")]},

    {"day": "April 28", "start_time": "12:00 PM", "end_time": "12:40 PM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "Session",
     "title": "PULSE Check: An AI-Enabled Commander's Survey Tool",
     "speakers": [
         S("Wilson Prescott", "Col",   "Chief of Staff, 4th Marine Logistics Group"),
         S("Samuel Sung",     "LtCol", "Innovation Officer, Logistics Innovation Unit, 4th Marine Logistics Group (USMCR)"),
     ]},

    {"day": "April 28", "start_time": "01:10 PM", "end_time": "01:50 PM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "Session",
     "title": "Counter UAS: From Installations Defense to Organic Protection for the Distributed Forces",
     "speakers": [
         S("Andrew Konicki", "Col",  "Program Manager Ground Based Air Defense"),
         S("Joseph Radich",  "Maj",  "Installation Counter sUAS Officer, MCICOM"),
         S("Jeremy Stover",  "CWO5", "Marine Gunner, USMC"),
     ]},

    {"day": "April 28", "start_time": "02:20 PM", "end_time": "03:00 PM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "Session",
     "title": "Essentials in Prevailing against a Peer Adversary",
     "speakers": [S("Stephen Sklenka", "LtGen", "Deputy Commandant, Installations and Logistics, DC I&L, HQMC")]},

    # ── Marine Zone Stage ────────────────────────────────────────────────
    {"day": "April 28", "start_time": "09:50 AM", "end_time": "10:30 AM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "Session",
     "title": "Operationalizing Wounded Warrior Regiment (WWR), Scalability, Flexibility",
     "speakers": [S("Morina Foster", "Col", "Commanding Officer, Wounded Warrior Regiment")]},

    {"day": "April 28", "start_time": "11:00 AM", "end_time": "11:40 AM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "Session",
     "title": "Analysis and Assessments Branch: Learning and Adapting at Speed",
     "speakers": [S("Brian Christmas", "GS-15", "Branch Head, Analysis and Assessments Branch, Training & Education Command")]},

    {"day": "April 28", "start_time": "12:10 PM", "end_time": "12:40 PM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "Session",
     "title": "Buying at the Speed of War: Leveraging Commercial Technology to Gain the Advantage",
     "speakers": [
         S("Joshua Arvizu",    "Capt", "Student"),
         S("Jarrett Cavanagh", "Capt", "Field Artillery Officer, Expeditionary Warfare School"),
         S("Eric Jones",       "Capt", "Student"),
         S("Spencer Miller",   "Capt", "Artillery Officer"),
         S("Riley White",      "Capt", "Student, Expeditionary Warfare School"),
     ]},

    {"day": "April 28", "start_time": "01:30 PM", "end_time": "02:10 PM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "Session",
     "title": "Resourcing the Expeditionary Fleet",
     "speakers": [S("S. Lee Meyer", "BGen", "Director, Expeditionary Warfare")]},

    {"day": "April 28", "start_time": "02:30 PM", "end_time": "03:10 PM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "Session",
     "title": "Warrior Athlete Readiness & Resilience - A Marine Corps Total Fitness Approach",
     "speakers": [S("Brad Brimhall", "GS-15", "Branch Head, Warrior Athlete Readiness & Resilience, M&RA, HQMC")]},

    # ── Scuttlebutt Podcast ──────────────────────────────────────────────
    {"day": "April 28", "start_time": "10:00 AM", "end_time": "10:40 AM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "The Reboot Project",
     "speakers": [S("Bryan Bush", "", "")]},

    {"day": "April 28", "start_time": "11:00 AM", "end_time": "11:40 AM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "3-1-5 Framework: The Essentials in Prevailing Against a Peer Adversary",
     "speakers": [S("Stephen Sklenka", "LtGen", "Deputy Commandant, Installations and Logistics, DC I&L, HQMC")]},

    {"day": "April 28", "start_time": "12:30 PM", "end_time": "01:10 PM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "Autonomous Logistics: Resupplying the Future Fight", "speakers": []},

    {"day": "April 28", "start_time": "01:30 PM", "end_time": "02:10 PM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "Character and Life Assimilation",
     "speakers": [S("Carey Cash", "Chaplain", "Chaplain of the Marine Corps, HQMC REL")]},

    {"day": "April 28", "start_time": "02:30 PM", "end_time": "03:10 PM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "MCCS Connect: Modernization with Purpose",
     "speakers": [
         S("Andrew Barcomb", "Mr.", "Senior Web Designer, MCCS"),
         S("Ralph Lewter",   "Mr.", "Branded Content Specialist, MCCS"),
     ]},

    # ── Drone Stage ──────────────────────────────────────────────────────
    {"day": "April 28", "start_time": "10:15 AM", "end_time": "10:45 AM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Industry Drone Demo (PDW Attritable Multirotor)", "speakers": []},

    {"day": "April 28", "start_time": "11:15 AM", "end_time": "11:30 AM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},

    {"day": "April 28", "start_time": "12:05 PM", "end_time": "12:20 PM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},

    {"day": "April 28", "start_time": "12:45 PM", "end_time": "01:00 PM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},

    {"day": "April 28", "start_time": "02:25 PM", "end_time": "02:40 PM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Vector Dagger Demonstration", "speakers": []},

    {"day": "April 28", "start_time": "03:00 PM", "end_time": "03:15 PM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},
]

# ---------------------------------------------------------------------------
# Day 2 — April 29, 2026  (confirmed from official schedule paste)
# ---------------------------------------------------------------------------
day2_sessions = [

    # ── Special Events ───────────────────────────────────────────────────
    {"day": "April 29", "start_time": "09:00 AM", "end_time": "10:30 AM",
     "stage": "Marriott Marquis", "track": "Special Events", "format": "",
     "title": "Congressional Breakfast", "speakers": []},

    {"day": "April 29", "start_time": "09:00 AM", "end_time": "03:00 PM",
     "stage": "Conference Rooms (TBD)", "track": "Special Events", "format": "",
     "title": "GCE UAS/C-UAS Symposium", "speakers": []},

    {"day": "April 29", "start_time": "09:00 AM", "end_time": "03:00 PM",
     "stage": "101 & 102 A", "track": "Special Events", "format": "",
     "title": "Logistics Command Artificial Intelligence Symposium", "speakers": []},

    {"day": "April 29", "start_time": "01:00 PM", "end_time": "04:00 PM",
     "stage": "146A", "track": "Special Events", "format": "",
     "title": "Contracts Industry Day", "speakers": []},

    {"day": "April 29", "start_time": "06:30 PM", "end_time": "09:30 PM",
     "stage": "Marriott Marquis", "track": "Special Events", "format": "",
     "title": "Modern Day Marine Honors & Reception", "speakers": []},

    # ── Main Briefing Center ─────────────────────────────────────────────
    {"day": "April 29", "start_time": "09:15 AM", "end_time": "10:15 AM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Transforming USMC Procurement: Leading with Agility and Impact",
     "speakers": [
         S("Daniel Corbin",   "SES Dr.", "Chief Technical Advisor, HQMC DCI-IC4"),
         S("Robert Cross",    "SES",     "PAE-MC Chief Engineer, USMC"),
         S("Johany Deal",     "SES",     "Assistant Deputy Commandant for I&L Contracts, HQMC I&L"),
         S("Anthony Greco Jr.","SES",    "Executive Deputy, Training & Education Command, USMC"),
     ]},

    {"day": "April 29", "start_time": "10:45 AM", "end_time": "11:45 AM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "3.0 Marine Expeditionary Unit American Sovereignty Afloat – Driving Maintenance and Inventory",
     "speakers": [
         S("Eric Austin",    "LtGen", "Deputy Commandant Combat Development and Integration, HQMC"),
         S("Jay Bargeron",   "LtGen", "Deputy Commandant Plans, Policies, and Operations, HQMC"),
         S("Shon Brodie",    "Mr.",   "Director, Maritime Expeditionary Warfare, HQMC CD&I"),
         S("Bobbi Shea",     "LtGen", "Commanding General, Fleet Marine Force Atlantic; Commander, Marine Forces Command; Commander, Marine Forces Northern Command"),
         S("John Skillman",  "VADM",  "Deputy Chief of Naval Operations for Integration of Capabilities and Resources (N8), OPNAV"),
     ]},

    {"day": "April 29", "start_time": "12:00 PM", "end_time": "01:00 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Next-Gen Combined Arms: Integrating Information Effects into Modern Operations",
     "speakers": [
         S("Mark A. Cunningham",   "MajGen", "USMC Director of Intelligence, HQMC"),
         S("Jeffery A. Hurley",    "Mr.",    "Director of Command, Control, Communication, and Computers, HQMC"),
         S("Jay Matos",            "LtGen",  "Deputy Commandant for Information, HQMC"),
         S("Christopher A. Passerella", "Col", "Director, Information Maneuver Division, HQMC"),
     ]},

    {"day": "April 29", "start_time": "01:05 PM", "end_time": "02:05 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "EDCOM: Leading the Revolution in Joint Education",
     "speakers": [
         S("Jessica R. Aich", "Maj",  "Course Director, Expeditionary Warfare School, MCU"),
         S("Robert Barnhart",  "Col",  ""),
         S("John Lehane",      "Col",  "Director of the Marine Corps Command and Staff College"),
         S("Matt Tracy",       "BGen", "Commanding General, Education Command and President"),
     ]},

    {"day": "April 29", "start_time": "02:10 PM", "end_time": "03:10 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "The Unfair Advantage: Mobilizing Marine Corps Power",
     "speakers": [
         S("Leonard Anderson IV", "LtGen", "Commander, Marine Forces Reserve / Marine Forces South"),
         S("Ryan Murata",         "Col",   "Director, Office of Marine Corps Reserve"),
     ]},

    {"day": "April 29", "start_time": "03:15 PM", "end_time": "04:15 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Ready Today, Unmatched Tomorrow: The Future of Marine Aviation",
     "speakers": [
         S("Richard Rusnok", "Col",   "Cunningham Group Branch Head, Headquarters Marine Corps"),
         S("William Swan",   "LtGen", "Deputy Commandant for Aviation, Headquarters Marine Corps"),
     ]},

    # ── Acquisitions Stage ───────────────────────────────────────────────
    {"day": "April 29", "start_time": "10:15 AM", "end_time": "10:55 AM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PM Ground Weapons Systems: Forging Marine Corps Lethality",
     "speakers": [S("Bradley Sams", "Col", "Program Manager, Ground Weapons Systems")]},

    {"day": "April 29", "start_time": "11:00 AM", "end_time": "11:40 AM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PMA-261 Program Update",
     "speakers": [S("Kate Fleeger", "Col", "Program Manager, H-53 Helicopters Program")]},

    {"day": "April 29", "start_time": "11:45 AM", "end_time": "12:25 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PM Combat Support Systems Overview",
     "speakers": [S("Paul Gillikin", "Col", "Program Manager, Combat Support Systems")]},

    {"day": "April 29", "start_time": "12:30 PM", "end_time": "01:10 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "Marine Air/Ground Task Force Command and Control Progression",
     "speakers": [S("Jeffrey Van Bourgondien", "Col", "Program Manager, MAGTF C2")]},

    {"day": "April 29", "start_time": "01:15 PM", "end_time": "01:55 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "Marine Corps Tactical Systems Support Activity Updates",
     "speakers": [S("Craig Clarkson", "Col", "Commander, MCTSSA")]},

    {"day": "April 29", "start_time": "02:45 PM", "end_time": "03:25 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PMA-275 V-22",
     "speakers": [S("Robert Hurst", "Col", "PMA-275 Program Manager, NAVAIR PEO(A)")]},

    # ── Warfighting Stage ────────────────────────────────────────────────
    {"day": "April 29", "start_time": "09:25 AM", "end_time": "09:55 AM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "",
     "title": "The Marine Corps' Approach to Blast Overpressure",
     "speakers": [S("Sean Hoewing", "BGen", "Director, Risk Management Directorate")]},

    {"day": "April 29", "start_time": "10:35 AM", "end_time": "11:05 AM",
     "stage": "Warfighting Stage", "track": "Industry", "format": "Session",
     "title": "Enabling the Future Marine: Advancing Capabilities through Collaboration",
     "speakers": [S("Michael Orr", "", "Vice President, Government Relations, SNC")]},

    {"day": "April 29", "start_time": "11:45 AM", "end_time": "12:25 PM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "Session",
     "title": "A Hitchhiker's Guide to RxR in the WEZ",
     "speakers": [
         S("Hayden Knudson", "Capt", "Intelligence Officer"),
         S("Daniel O'Brien",  "Capt", "EWS Student, EWS/MCU"),
         S("Patrick Riley",   "Capt", "Expeditionary Warfare School Student"),
         S("Aubrey Sapp",     "Capt", "Student, Expeditionary Warfare School"),
     ]},

    {"day": "April 29", "start_time": "01:00 PM", "end_time": "01:40 PM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "Session",
     "title": "Autonomy/Collaborative Autonomy/Autonomy Afloat",
     "speakers": [S("Kenneth Jones", "Col", "Division Director, Science & Technology, Marine Corps Warfighting Laboratory")]},

    {"day": "April 29", "start_time": "01:45 PM", "end_time": "02:15 PM",
     "stage": "Warfighting Stage", "track": "Industry", "format": "Session",
     "title": "Force Multiplied: Integrated Solutions for the Modern Marine",
     "speakers": [S("Matthew L. Klunder", "", "Vice President, USN/USMC Accounts and DARPA & DOD Laboratories, L3Harris Technologies")]},

    {"day": "April 29", "start_time": "02:20 PM", "end_time": "03:00 PM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "Session",
     "title": "Distributed Aviation Operations",
     "speakers": [S("Marianne Carlson", "LtCol", "Aviation Vision and Strategy Planner, Headquarters Marine Corps Aviation")]},

    # ── Marine Zone Stage ────────────────────────────────────────────────
    {"day": "April 29", "start_time": "09:35 AM", "end_time": "10:15 AM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "Session",
     "title": "The Neller Center: How Next Generation Wargaming Drives Force Design",
     "speakers": [S("Charles Anklam III", "Col", "Director, Wargaming Division, Marine Corps Warfighting Laboratory")]},

    {"day": "April 29", "start_time": "10:45 AM", "end_time": "11:25 AM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "Session",
     "title": "Spiritual Armament and the Cost of Victory",
     "speakers": [S("Carey Cash", "Chaplain", "Chaplain of the Marine Corps, HQMC REL")]},

    {"day": "April 29", "start_time": "12:00 PM", "end_time": "12:40 PM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "",
     "title": "AI Learning in the Boardroom",
     "speakers": [S("Fridrik Fridriksson", "BGen", "Director, Manpower Management Division, Manpower and Reserve Affairs")]},

    {"day": "April 29", "start_time": "01:10 PM", "end_time": "01:50 PM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "Session",
     "title": "Wingmen of the Future: Uncrewed and Autonomous",
     "speakers": [S("Michael Zbonack", "Maj", "Future Concepts UAS, Headquarters Marine Corps Aviation, Cunningham Group")]},

    {"day": "April 29", "start_time": "02:40 PM", "end_time": "03:20 PM",
     "stage": "Marine Zone Stage", "track": "Marine Zone", "format": "Session",
     "title": "Ground Combat Element UAS/C-UAS Symposium Out brief",
     "speakers": [S("Erick Clark", "Col", "Branch Head Future Operations, Plans, Policies, and Operations")]},

    # ── Scuttlebutt Podcast ──────────────────────────────────────────────
    {"day": "April 29", "start_time": "09:30 AM", "end_time": "10:15 AM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "Project Dynamis: Accelerating AI-Powered Decision Advantage",
     "speakers": [S("Arlon Smith", "Col", "Director, Project Dynamis")]},

    {"day": "April 29", "start_time": "11:00 AM", "end_time": "11:45 AM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "USMC and the use of Artificial Intelligence Predictive Demand Planning in a Contested Information Environment",
     "speakers": [
         S("Changa Ngwenya",     "Capt", "EWS Student, USMC"),
         S("Nicholas Riggs",     "Capt", "EWS Student"),
         S("Dominick Tranfaglia","Capt", "Student, Expeditionary Warfare School, USMC MCU"),
         S("Tim Wingert",        "Capt", "Logistics Officer"),
     ]},

    {"day": "April 29", "start_time": "01:30 PM", "end_time": "02:15 PM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "Closing Kill Chains",
     "speakers": [S("Michael McCarthy", "Col", "Aviation Expeditionary Enablers Branch Head, Headquarters Marine Corps, Department of Aviation")]},

    {"day": "April 29", "start_time": "02:30 PM", "end_time": "03:10 PM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "",
     "title": "PM Intel & Cyberspace Operations",
     "speakers": [S("Jay Proctor", "Mr.", "Program Manager Intelligence and Cyberspace Operations (ICO)")]},

    # ── Drone Stage ──────────────────────────────────────────────────────
    {"day": "April 29", "start_time": "09:45 AM", "end_time": "10:15 AM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Industry Drone Demo", "speakers": []},

    {"day": "April 29", "start_time": "10:40 AM", "end_time": "10:55 AM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},

    {"day": "April 29", "start_time": "11:15 AM", "end_time": "11:30 AM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},

    {"day": "April 29", "start_time": "12:30 PM", "end_time": "12:45 PM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},

    {"day": "April 29", "start_time": "02:25 PM", "end_time": "02:55 PM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Industry Drone Demo", "speakers": []},

    {"day": "April 29", "start_time": "03:00 PM", "end_time": "03:15 PM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},
]

# ---------------------------------------------------------------------------
# Day 3 — April 30, 2026  (confirmed from official schedule paste)
# ---------------------------------------------------------------------------
day3_sessions = [

    # ── Special Events ───────────────────────────────────────────────────
    {"day": "April 30", "start_time": "09:00 AM", "end_time": "02:30 PM",
     "stage": "Marine Zone Stage", "track": "Special Events", "format": "",
     "title": "Education & Employment Fair", "speakers": []},

    {"day": "April 30", "start_time": "09:00 AM", "end_time": "03:00 PM",
     "stage": "101 & 102 A", "track": "Special Events", "format": "",
     "title": "Logistics Command Artificial Intelligence Symposium", "speakers": []},

    {"day": "April 30", "start_time": "10:00 AM", "end_time": "12:00 PM",
     "stage": "Marine Zone Stage", "track": "Special Events", "format": "",
     "title": "Military Spouse Summit",
     "speakers": [
         S("Francisco Badiola",     "",          "Chief of Staff, MR Business and Support Services"),
         S("William Bowers",        "LtGen",     "Deputy Commandant for Manpower and Reserve Affairs"),
         S("Gregory Goldstein",     "",          "Director, Marine and Family Programs Division, HQMC"),
         S("Jennifer Goodale",      "",          "Director of Government Relations for Veteran and Retired Affairs, MOAA"),
         S("Stephen B. Simmons",    "",          "Deputy Assistant Secretary of War, Military Community and Family Policy"),
         S("Trish Smith",           "Mrs.",      "Spouse of the 39th Commandant"),
         S("Guido F. Valdes",       "Rear Adm.", "Medical Officer of the Marine Corps"),
     ]},

    {"day": "April 30", "start_time": "02:00 PM", "end_time": "02:30 PM",
     "stage": "Main Briefing Center", "track": "Special Events", "format": "",
     "title": "Semper Fidelis Reception & Closing Ceremony", "speakers": []},

    # ── Main Briefing Center ─────────────────────────────────────────────
    {"day": "April 30", "start_time": "09:15 AM", "end_time": "10:15 AM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Ground Systems Enterprise (GSE) Senior Leader Summit: Forging the Future Force for the Next 250 Years",
     "speakers": [
         S("Scott Beatty",       "Col",    "Director, Sustainment Branch, HQMC Installations and Logistics"),
         S("Timothy Brady",      "BGen",   "Director, Capabilities Development Directorate, Marine Corps Combat Development Command"),
         S("Erick Clark",        "Col",    "Branch Head Future Operations, Plans, Policies, and Operations"),
         S("Jason Morris",       "MajGen", "Director of Operations, Plans Policies, and Operations, HQMC"),
         S("Michael Nakonieczny","BGen",   "Deputy Commanding General, I Marine Expeditionary Force"),
     ]},

    {"day": "April 30", "start_time": "10:30 AM", "end_time": "11:30 AM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "State of the United States Navy",
     "speakers": [S("Daryl Caudle", "Adm.", "Chief of Naval Operations")]},

    {"day": "April 30", "start_time": "11:30 AM", "end_time": "12:30 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "Portfolio Acquisition Executive - Marine Corps",
     "speakers": [
         S("Eric Austin",    "LtGen", "Deputy Commandant Combat Development and Integration, HQMC"),
         S("Stephen Bowdren","CIV",   "Program Executive Officer, PEO LS"),
         S("Tamara Campbell","BGen",  "Commander, MARCORSYSCOM / Deputy PAE Marine Corps"),
         S("David Walsh",    "MajGen","Program Executive Officer Air, Anti-Submarine Warfare, Assault, and Special Mission Programs"),
     ]},

    {"day": "April 30", "start_time": "01:00 PM", "end_time": "02:00 PM",
     "stage": "Main Briefing Center", "track": "Main Briefing Center", "format": "Session",
     "title": "State of the United States Marine Corps",
     "speakers": [S("Eric M. Smith", "Gen", "Commandant of the Marine Corps, USMC")]},

    # ── Acquisitions Stage ───────────────────────────────────────────────
    {"day": "April 30", "start_time": "09:30 AM", "end_time": "10:10 AM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "Opening Remarks Day 3",
     "speakers": [S("Stephen Bowdren", "CIV", "Program Executive Officer, PEO LS")]},

    {"day": "April 30", "start_time": "10:15 AM", "end_time": "10:55 AM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PM Advanced Amphibious Assault: ACV Family of Vehicles",
     "speakers": [S("Christopher Melkonian", "CIV", "Program Manager, Advanced Amphibious Assault")]},

    {"day": "April 30", "start_time": "11:00 AM", "end_time": "11:40 AM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PM Light Armored Vehicles Overview",
     "speakers": [S("Christopher Stephenson", "Col", "Product Manager, Vehicle Systems")]},

    {"day": "April 30", "start_time": "11:45 AM", "end_time": "12:25 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PM Wargaming Capability Overview",
     "speakers": [S("Joseph Taylor", "LtCol", "Program Manager, Wargaming")]},

    {"day": "April 30", "start_time": "12:30 PM", "end_time": "01:10 PM",
     "stage": "Acquisitions Stage", "track": "Acquisitions Stage", "format": "Session",
     "title": "PMA-276 USMC Light/Attack Helicopter",
     "speakers": [S("Jason Duke", "Col", "PMA-276 Program Manager")]},

    # ── Warfighting Stage ────────────────────────────────────────────────
    {"day": "April 30", "start_time": "10:30 AM", "end_time": "11:10 AM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "Session",
     "title": "Experiments Division Update: How 2025's milestones shaped tomorrow's experiments to improve littoral mobility, C2, and survivability",
     "speakers": [S("Dustin Scott", "LtCol", "Concept Development Team 3 Lead, Experiment Division, Marine Corps Warfighting Laboratory")]},

    {"day": "April 30", "start_time": "11:40 AM", "end_time": "12:20 PM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "Session",
     "title": "Marine Corps Attack Drone Team: Accelerating Lethality Through FPV Innovation",
     "speakers": [S("Scott Cuomo", "Col", "Commanding Officer, Weapons Training Battalion")]},

    {"day": "April 30", "start_time": "12:30 PM", "end_time": "12:45 PM",
     "stage": "Warfighting Stage", "track": "Warfighting", "format": "",
     "title": "LOGOM Artificial Intelligence Hackathon Awards Presentation", "speakers": []},

    # ── Scuttlebutt Podcast ──────────────────────────────────────────────
    {"day": "April 30", "start_time": "09:30 AM", "end_time": "10:10 AM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "PM Expeditionary Radars",
     "speakers": [S("Barbara Gault", "Ms.", "Expeditionary Radars Program Manager, USMC")]},

    {"day": "April 30", "start_time": "10:30 AM", "end_time": "11:15 AM",
     "stage": "Scuttlebutt Podcast", "track": "Scuttlebutt Podcast", "format": "Session",
     "title": "Leading Forward: The Evolution of Leadership",
     "speakers": [
         S("Jacob Reiff", "SgtMaj", "Sergeant Major, Manpower and Reserve Affairs"),
         S("Carlos Ruiz", "SgtMaj", "Sergeant Major of the Marine Corps"),
     ]},

    # ── Drone Stage ──────────────────────────────────────────────────────
    {"day": "April 30", "start_time": "09:15 AM", "end_time": "09:30 AM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},

    {"day": "April 30", "start_time": "09:30 AM", "end_time": "10:00 AM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Industry Drone Demo (PDW Attritable Multirotor)", "speakers": []},

    {"day": "April 30", "start_time": "10:45 AM", "end_time": "11:00 AM",
     "stage": "Drone Stage", "track": "Drone Stage", "format": "Session",
     "title": "Marine Corps Attack Drone Team Demo", "speakers": []},
]

all_sessions = day1_sessions + day2_sessions + day3_sessions

# ---------------------------------------------------------------------------
# Write raw JSON
# ---------------------------------------------------------------------------
raw_output = {
    "event": "Modern Day Marine 2026",
    "dates": "April 28–30, 2026",
    "venue": "Walter E. Washington Convention Center, Washington, D.C.",
    "data_provenance": (
        "All sessions (April 28–30) are exact — sourced directly from the "
        "official marinemilitaryexpos.com/pme-sessions/ schedule (user-supplied paste)."
    ),
    "sessions": all_sessions,
}

with open("mdm2026_schedule_raw.json", "w", encoding="utf-8") as f:
    json.dump(raw_output, f, indent=2, ensure_ascii=False)
print(f"Wrote mdm2026_schedule_raw.json  "
      f"({len(all_sessions)} total sessions: "
      f"{len(day1_sessions)} Day 1, {len(day2_sessions)} Day 2, "
      f"{len(day3_sessions)} Day 3)")

# ---------------------------------------------------------------------------
# Build flat speaker-stage lookup
# ---------------------------------------------------------------------------
rows = []
for session in all_sessions:
    spk_list = session.get("speakers", [])
    if spk_list:
        for spk in spk_list:
            name = spk["name"] if isinstance(spk, dict) else spk
            rows.append({
                "speaker_name":  name,
                "stage":         session["stage"],
                "day":           session["day"],
                "session_title": session["title"],
                "start_time":    session["start_time"],
            })
    else:
        rows.append({
            "speaker_name":  "",
            "stage":         session["stage"],
            "day":           session["day"],
            "session_title": session["title"],
            "start_time":    session["start_time"],
        })

fieldnames = ["speaker_name", "stage", "day", "session_title", "start_time"]
with open("mdm2026_speaker_stage_lookup.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

named_rows = [r for r in rows if r["speaker_name"]]
print(f"Wrote mdm2026_speaker_stage_lookup.csv  "
      f"({len(rows)} total rows, {len(named_rows)} with named speakers)")

stages = sorted({r["stage"] for r in rows if "PLACEHOLDER" not in r["session_title"]})
names  = sorted({r["speaker_name"] for r in rows if r["speaker_name"]})
print(f"\nStages ({len(stages)}): {stages}")
print(f"\nNamed speakers ({len(names)}):")
for n in names:
    print(f"  {n}")
