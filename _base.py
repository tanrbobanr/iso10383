"""A wrapper around the data provided by the ISO 10383 specification.

:copyright: (c) 2024 Tanner Corcoran
:license: Apache 2.0, see LICENSE for more details.

"""

__author__ = "Tanner Corcoran"
__license__ = "Apache 2.0 License"
__copyright__ = "Copyright (c) 2024 Tanner Corcoran"


import sys
import enum
import pathlib
import datetime
import dataclasses
from typing import (
    Any,
    BinaryIO,
    TypeVar,
    Union,
)
from collections.abc import Callable
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


_T = TypeVar("_T")
_E = TypeVar("_E", bound=enum.Enum)


class MCC(enum.Enum):
    """Market Category Code (MCC)"""
    appa = 0
    atss = 1
    casp = 2
    dcms = 3
    idqs = 4
    mltf = 5
    nspd = 6
    otfs = 7
    othr = 8
    rmkt = 9
    rmos = 10
    sefs = 11
    sint = 12
    trfs = 13


class ISOCC(enum.Enum):
    """ISO Country Code"""
    ae = 0
    ag = 1
    al = 2
    am = 3
    ao = 4
    ar = 5
    at = 6
    au = 7
    az = 8
    ba = 9
    bb = 10
    bd = 11
    be = 12
    bg = 13
    bh = 14
    bm = 15
    bo = 16
    br = 17
    bs = 18
    bw = 19
    by = 20
    ca = 21
    ch = 22
    ci = 23
    cl = 24
    cm = 25
    cn = 26
    co = 27
    cr = 28
    cv = 29
    cw = 30
    cy = 31
    cz = 32
    de = 33
    dk = 34
    do = 35
    dz = 36
    ec = 37
    ee = 38
    eg = 39
    es = 40
    fi = 41
    fj = 42
    fo = 43
    fr = 44
    gb = 45
    ge = 46
    gg = 47
    gh = 48
    gi = 49
    gr = 50
    gt = 51
    gy = 52
    hk = 53
    hn = 54
    hr = 55
    hu = 56
    id = 57
    ie = 58
    il = 59
    in_ = 60
    iq = 61
    ir = 62
    is_ = 63
    it = 64
    jm = 65
    jo = 66
    jp = 67
    ke = 68
    kg = 69
    kh = 70
    kn = 71
    kr = 72
    kw = 73
    ky = 74
    kz = 75
    la = 76
    lb = 77
    li = 78
    lk = 79
    lt = 80
    lu = 81
    lv = 82
    ly = 83
    ma = 84
    md = 85
    me = 86
    mg = 87
    mk = 88
    mn = 89
    mt = 90
    mu = 91
    mv = 92
    mw = 93
    mx = 94
    my = 95
    mz = 96
    na = 97
    ng = 98
    ni = 99
    nl = 100
    no = 101
    np = 102
    nz = 103
    om = 104
    pa = 105
    pe = 106
    pg = 107
    ph = 108
    pk = 109
    pl = 110
    ps = 111
    pt = 112
    py = 113
    qa = 114
    ro = 115
    rs = 116
    ru = 117
    rw = 118
    sa = 119
    sc = 120
    sd = 121
    se = 122
    sg = 123
    si = 124
    sk = 125
    sv = 126
    sy = 127
    sz = 128
    th = 129
    tn = 130
    tr = 131
    tt = 132
    tw = 133
    tz = 134
    ua = 135
    ug = 136
    us = 137
    uy = 138
    uz = 139
    vc = 140
    ve = 141
    vn = 142
    vu = 143
    za = 144
    zm = 145
    zw = 146
    zz = 147


class _City(int):
    _name: str

    def __new__(cls, id: int, name: str) -> Self:
        inst = int.__new__(cls, id)
        inst._name = name
        return inst

    @property
    def name(self) -> str:
        return self._name


class City(enum.Enum):
    aabenraa                  = _City(0, "Aabenraa")
    aalborg                   = _City(1, "Aalborg")
    abidjan                   = _City(2, "Abidjan")
    abu_dhabi                 = _City(3, "Abu Dhabi")
    accra                     = _City(4, "Accra")
    ahmedabad                 = _City(5, "Ahmedabad")
    aichi                     = _City(6, "Aichi")
    alberta                   = _City(7, "Alberta")
    algiers                   = _City(8, "Algiers")
    almaty                    = _City(9, "Almaty")
    amman                     = _City(10, "Amman")
    amsterdam                 = _City(11, "Amsterdam")
    ankara                    = _City(12, "Ankara")
    antananarivo              = _City(13, "Antananarivo")
    antwerpen                 = _City(14, "Antwerpen")
    astana                    = _City(15, "Astana")
    asti                      = _City(16, "Asti")
    asuncion                  = _City(17, "Asuncion")
    athens                    = _City(18, "Athens")
    atlanta                   = _City(19, "Atlanta")
    auckland                  = _City(20, "Auckland")
    aylesbury                 = _City(21, "Aylesbury")
    baghdad                   = _City(22, "Baghdad")
    baku                      = _City(23, "Baku")
    bangalore                 = _City(24, "Bangalore")
    bangkok                   = _City(25, "Bangkok")
    banja_luka                = _City(26, "Banja Luka")
    barcelona                 = _City(27, "Barcelona")
    basseterre                = _City(28, "Basseterre")
    bedminster                = _City(29, "Bedminster")
    beijing                   = _City(30, "Beijing")
    beirut                    = _City(31, "Beirut")
    belgrade                  = _City(32, "Belgrade")
    bergamo                   = _City(33, "Bergamo")
    bergen                    = _City(34, "Bergen")
    berlin                    = _City(35, "Berlin")
    bermuda                   = _City(36, "Bermuda")
    berne                     = _City(37, "Berne")
    biella                    = _City(38, "Biella")
    bilbao                    = _City(39, "Bilbao")
    bishkek                   = _City(40, "Bishkek")
    blantyre                  = _City(41, "Blantyre")
    boca_raton                = _City(42, "Boca Raton")
    bogota                    = _City(43, "Bogota")
    bologna                   = _City(44, "Bologna")
    boston                    = _City(45, "Boston")
    bradford                  = _City(46, "Bradford")
    bratislava                = _City(47, "Bratislava")
    bremen                    = _City(48, "Bremen")
    bridgetown                = _City(49, "Bridgetown")
    brussels                  = _City(50, "Brussels")
    bryanston_sandton         = _City(51, "Bryanston - Sandton")
    bucharest                 = _City(52, "Bucharest")
    budaors                   = _City(53, "Budaors")
    budapest                  = _City(54, "Budapest")
    buenos_aires              = _City(55, "Buenos Aires")
    cairo                     = _City(56, "Cairo")
    calcutta                  = _City(57, "Calcutta")
    calgary                   = _City(58, "Calgary")
    caracas                   = _City(59, "Caracas")
    casablanca                = _City(60, "Casablanca")
    charlotte                 = _City(61, "Charlotte")
    chatham                   = _City(62, "Chatham")
    chicago                   = _City(63, "Chicago")
    chisinau                  = _City(64, "Chisinau")
    chittagong                = _City(65, "Chittagong")
    chiyoda_ku                = _City(66, "Chiyoda-Ku")
    cluj_napoca               = _City(67, "Cluj Napoca")
    colombo                   = _City(68, "Colombo")
    copenhagen                = _City(69, "Copenhagen")
    cordoba                   = _City(70, "Cordoba")
    corrientes                = _City(71, "Corrientes")
    curitiba                  = _City(72, "Curitiba")
    cybercity_ebene           = _City(73, "Cybercity, Ebene")
    dalian                    = _City(74, "Dalian")
    damascus                  = _City(75, "Damascus")
    dar_es_salaam             = _City(76, "Dar Es Salaam")
    delhi                     = _City(77, "Delhi")
    dhaka                     = _City(78, "Dhaka")
    dnipropetrovsk            = _City(79, "Dnipropetrovsk")
    doha                      = _City(80, "Doha")
    douala                    = _City(81, "Douala")
    dubai                     = _City(82, "Dubai")
    dublin                    = _City(83, "Dublin")
    duesseldorf               = _City(84, "Duesseldorf")
    ebene                     = _City(85, "Ebene")
    ebene_city                = _City(86, "Ebene City")
    eden_island               = _City(87, "Eden Island")
    edinburgh                 = _City(88, "Edinburgh")
    ekaterinburg              = _City(89, "Ekaterinburg")
    el_salvador               = _City(90, "El Salvador")
    esch_sur_alzette          = _City(91, "Esch-Sur-Alzette")
    eschborn                  = _City(92, "Eschborn")
    espirito_santo            = _City(93, "Espirito Santo")
    espoo                     = _City(94, "Espoo")
    fiac                      = _City(95, "Fiac")
    firenze                   = _City(96, "Firenze")
    florence                  = _City(97, "Florence")
    frankfurt                 = _City(98, "Frankfurt")
    frankfurt_am_main         = _City(99, "Frankfurt Am Main")
    fukuoka                   = _City(100, "Fukuoka")
    gaborone                  = _City(101, "Gaborone")
    gandhinagar               = _City(102, "Gandhinagar")
    geneva                    = _City(103, "Geneva")
    genova                    = _City(104, "Genova")
    georgetown                = _City(105, "Georgetown")
    gibraltar                 = _City(106, "Gibraltar")
    gift_city_gandhinagar     = _City(107, "Gift City, Gandhinagar")
    glenview                  = _City(108, "Glenview")
    great_neck                = _City(109, "Great Neck")
    greenwich                 = _City(110, "Greenwich")
    grindsted                 = _City(111, "Grindsted")
    guatemala                 = _City(112, "Guatemala")
    guayaquil                 = _City(113, "Guayaquil")
    guaynabo                  = _City(114, "Guaynabo")
    guildford                 = _City(115, "Guildford")
    hamburg                   = _City(116, "Hamburg")
    hamilton                  = _City(117, "Hamilton")
    hannover                  = _City(118, "Hannover")
    hanoi                     = _City(119, "Hanoi")
    harare                    = _City(120, "Harare")
    helsinki                  = _City(121, "Helsinki")
    hiroshima                 = _City(122, "Hiroshima")
    ho_chi_minh_city          = _City(123, "Ho Chi Minh City")
    hong_kong                 = _City(124, "Hong Kong")
    horsens                   = _City(125, "Horsens")
    hove                      = _City(126, "Hove")
    illinois                  = _City(127, "Illinois")
    indore_madhya_pradesh     = _City(128, "Indore Madhya Pradesh")
    islamabad                 = _City(129, "Islamabad")
    istanbul                  = _City(130, "Istanbul")
    izmir                     = _City(131, "Izmir")
    jaen                      = _City(132, "Jaen")
    jakarta                   = _City(133, "Jakarta")
    jersey_city               = _City(134, "Jersey City")
    johannesburg              = _City(135, "Johannesburg")
    kampala                   = _City(136, "Kampala")
    kansas_city               = _City(137, "Kansas City")
    karachi                   = _City(138, "Karachi")
    kathmandu                 = _City(139, "Kathmandu")
    kharkov                   = _City(140, "Kharkov")
    khartoum                  = _City(141, "Khartoum")
    kiel                      = _City(142, "Kiel")
    kiev                      = _City(143, "Kiev")
    kigali                    = _City(144, "Kigali")
    kingston                  = _City(145, "Kingston")
    kingstown                 = _City(146, "Kingstown")
    klagenfurt_am_woerthersee = _City(147, "Klagenfurt Am Woerthersee")
    kobe                      = _City(148, "Kobe")
    kongsvinger               = _City(149, "Kongsvinger")
    krakow                    = _City(150, "Krakow")
    kuala_lumpur              = _City(151, "Kuala Lumpur")
    kuwait                    = _City(152, "Kuwait")
    kyoto                     = _City(153, "Kyoto")
    la_paz                    = _City(154, "La Paz")
    labuan                    = _City(155, "Labuan")
    lagos                     = _City(156, "Lagos")
    lahore                    = _City(157, "Lahore")
    lane_cove                 = _City(158, "Lane Cove")
    lao                       = _City(159, "Lao")
    larnaca                   = _City(160, "Larnaca")
    leipzig                   = _City(161, "Leipzig")
    lenexa                    = _City(162, "Lenexa")
    leuven                    = _City(163, "Leuven")
    lima                      = _City(164, "Lima")
    limassol                  = _City(165, "Limassol")
    linz                      = _City(166, "Linz")
    lisbon                    = _City(167, "Lisbon")
    ljubljana                 = _City(168, "Ljubljana")
    london                    = _City(169, "London")
    los_angeles               = _City(170, "Los Angeles")
    luanda                    = _City(171, "Luanda")
    lusaka                    = _City(172, "Lusaka")
    luxembourg                = _City(173, "Luxembourg")
    luzern                    = _City(174, "Luzern")
    madras                    = _City(175, "Madras")
    madrid                    = _City(176, "Madrid")
    makati_city               = _City(177, "Makati City")
    male                      = _City(178, "Male")
    managua                   = _City(179, "Managua")
    manama                    = _City(180, "Manama")
    manila                    = _City(181, "Manila")
    maputo                    = _City(182, "Maputo")
    maringa                   = _City(183, "Maringa")
    mbabane                   = _City(184, "Mbabane")
    melbourne                 = _City(185, "Melbourne")
    mendoza                   = _City(186, "Mendoza")
    mexico                    = _City(187, "Mexico")
    miami                     = _City(188, "Miami")
    milan                     = _City(189, "Milan")
    minneapolis               = _City(190, "Minneapolis")
    minsk                     = _City(191, "Minsk")
    montevideo                = _City(192, "Montevideo")
    montreal                  = _City(193, "Montreal")
    moorpark                  = _City(194, "Moorpark")
    moscow                    = _City(195, "Moscow")
    mount_pleasant            = _City(196, "Mount Pleasant")
    muenchen                  = _City(197, "Muenchen")
    mumbai                    = _City(198, "Mumbai")
    munich                    = _City(199, "Munich")
    muscat                    = _City(200, "Muscat")
    nablus                    = _City(201, "Nablus")
    nacka                     = _City(202, "Nacka")
    nagoya                    = _City(203, "Nagoya")
    nairobi                   = _City(204, "Nairobi")
    narberth                  = _City(205, "Narberth")
    nasau                     = _City(206, "Nasau")
    new_jersey                = _City(207, "New Jersey")
    new_york                  = _City(208, "New York")
    new_york_ny               = _City(209, "New York, Ny")
    newcastle                 = _City(210, "Newcastle")
    nicosia                   = _City(211, "Nicosia")
    nicosia_lefkosia          = _City(212, "Nicosia (Lefkosia)")
    nigita                    = _City(213, "Nigita")
    nizhniy_novgorod          = _City(214, "Nizhniy Novgorod")
    north_bergen              = _City(215, "North Bergen")
    not_applicable            = _City(216, "Not Applicable")
    novosibirsk               = _City(217, "Novosibirsk")
    nyon                      = _City(218, "Nyon")
    odessa                    = _City(219, "Odessa")
    oldenburg                 = _City(220, "Oldenburg")
    osaka                     = _City(221, "Osaka")
    oslo                      = _City(222, "Oslo")
    oststeinbek               = _City(223, "Oststeinbek")
    padova                    = _City(224, "Padova")
    palma_de_mallorca         = _City(225, "Palma De Mallorca")
    panama                    = _City(226, "Panama")
    paris                     = _City(227, "Paris")
    pasig_city                = _City(228, "Pasig City")
    philadelphia              = _City(229, "Philadelphia")
    phnom_penh                = _City(230, "Phnom Penh")
    phoenix                   = _City(231, "Phoenix")
    podgorica                 = _City(232, "Podgorica")
    polokwane                 = _City(233, "Polokwane")
    port_louis                = _City(234, "Port Louis")
    port_moresby              = _City(235, "Port Moresby")
    port_of_spain             = _City(236, "Port Of Spain")
    port_vila                 = _City(237, "Port Vila")
    porto                     = _City(238, "Porto")
    prague                    = _City(239, "Prague")
    praia                     = _City(240, "Praia")
    princeton                 = _City(241, "Princeton")
    purchase                  = _City(242, "Purchase")
    quito                     = _City(243, "Quito")
    randers                   = _City(244, "Randers")
    red_bank                  = _City(245, "Red Bank")
    regensburg                = _City(246, "Regensburg")
    reggio_emilia             = _City(247, "Reggio Emilia")
    reykjavik                 = _City(248, "Reykjavik")
    riga                      = _City(249, "Riga")
    rio_de_janeiro            = _City(250, "Rio De Janeiro")
    riyadh                    = _City(251, "Riyadh")
    rodgau                    = _City(252, "Rodgau")
    rome                      = _City(253, "Rome")
    rosario                   = _City(254, "Rosario")
    rostov                    = _City(255, "Rostov")
    s_hertogenbosch           = _City(256, "S-Hertogenbosch")
    sabadell                  = _City(257, "Sabadell")
    saint_petersburg          = _City(258, "Saint-Petersburg")
    salzburg                  = _City(259, "Salzburg")
    samara                    = _City(260, "Samara")
    san_carlos                = _City(261, "San Carlos")
    san_francisco             = _City(262, "San Francisco")
    san_jose                  = _City(263, "San Jose")
    san_pedro_sula            = _City(264, "San Pedro Sula")
    santa_fe                  = _City(265, "Santa Fe")
    santander                 = _City(266, "Santander")
    santiago                  = _City(267, "Santiago")
    santo_domingo             = _City(268, "Santo Domingo")
    sao_paulo                 = _City(269, "Sao Paulo")
    sapporo                   = _City(270, "Sapporo")
    sarajevo                  = _City(271, "Sarajevo")
    schwerin                  = _City(272, "Schwerin")
    sea_girt                  = _City(273, "Sea Girt")
    seoul                     = _City(274, "Seoul")
    shanghai                  = _City(275, "Shanghai")
    shenzhen                  = _City(276, "Shenzhen")
    shimonoseki               = _City(277, "Shimonoseki")
    sibiu                     = _City(278, "Sibiu")
    silkeborg                 = _City(279, "Silkeborg")
    singapore                 = _City(280, "Singapore")
    skopje                    = _City(281, "Skopje")
    sliema                    = _City(282, "Sliema")
    sofia                     = _City(283, "Sofia")
    split                     = _City(284, "Split")
    st_albans                 = _City(285, "St Albans")
    st_john                   = _City(286, "St John")
    st_peter_port             = _City(287, "St. Peter Port")
    stamford                  = _City(288, "Stamford")
    stockholm                 = _City(289, "Stockholm")
    stuttgart                 = _City(290, "Stuttgart")
    surabaya                  = _City(291, "Surabaya")
    suva                      = _City(292, "Suva")
    sydney                    = _City(293, "Sydney")
    taipei                    = _City(294, "Taipei")
    taiwan                    = _City(295, "Taiwan")
    tallinn                   = _City(296, "Tallinn")
    tashkent                  = _City(297, "Tashkent")
    tbilisi                   = _City(298, "Tbilisi")
    tegucigalpa               = _City(299, "Tegucigalpa")
    tehran                    = _City(300, "Tehran")
    tel_aviv                  = _City(301, "Tel Aviv")
    the_hague                 = _City(302, "The Hague")
    the_woodlands             = _City(303, "The Woodlands")
    tirana                    = _City(304, "Tirana")
    tokyo                     = _City(305, "Tokyo")
    torino                    = _City(306, "Torino")
    toronto                   = _City(307, "Toronto")
    torshavn                  = _City(308, "Torshavn")
    tripoli                   = _City(309, "Tripoli")
    tromso                    = _City(310, "Tromso")
    trondheim                 = _City(311, "Trondheim")
    tucuman                   = _City(312, "Tucuman")
    tunis                     = _City(313, "Tunis")
    ulaan_baatar              = _City(314, "Ulaan Baatar")
    unterschleisshem          = _City(315, "Unterschleisshem")
    utrecht                   = _City(316, "Utrecht")
    vaduz                     = _City(317, "Vaduz")
    valencia                  = _City(318, "Valencia")
    valletta                  = _City(319, "Valletta")
    valparaiso                = _City(320, "Valparaiso")
    vancouver                 = _City(321, "Vancouver")
    varazdin                  = _City(322, "Varazdin")
    victoria                  = _City(323, "Victoria")
    victoria_falls            = _City(324, "Victoria Falls")
    vienna                    = _City(325, "Vienna")
    vila                      = _City(326, "Vila")
    vilnius                   = _City(327, "Vilnius")
    vladivostok               = _City(328, "Vladivostok")
    warsaw                    = _City(329, "Warsaw")
    washington                = _City(330, "Washington")
    washington_new_york       = _City(331, "Washington/New York")
    willemstad                = _City(332, "Willemstad")
    wilmington                = _City(333, "Wilmington")
    windhoek                  = _City(334, "Windhoek")
    winnipeg                  = _City(335, "Winnipeg")
    winter_park               = _City(336, "Winter Park")
    wroclaw                   = _City(337, "Wroclaw")
    wuxi                      = _City(338, "Wuxi")
    yerevan                   = _City(339, "Yerevan")
    zagreb                    = _City(340, "Zagreb")
    zaragoza                  = _City(341, "Zaragoza")
    zhengzhou                 = _City(342, "Zhengzhou")
    zilina                    = _City(343, "Zilina")
    zurich                    = _City(344, "Zurich")

    # added after initial package release
    milton_keynes             = _City(345, "Milton Keynes")
    hradec_kralove            = _City(346, "Hradec Kralove")

    value: _City

    def __new__(cls, value: _City) -> Self:
        member = object.__new__(cls)
        member._value_ = value

        if int(value) in cls._value2member_map_:
            raise ValueError(f"Duplicate value: {value!r}")
        if value.name in cls._value2member_map_:
            raise ValueError(f"Duplicate value: {value.name!r}")
        
        cls._value2member_map_[value] = member
        cls._value2member_map_[value.name] = member

        return member


class Status(enum.Enum):
    active = 0
    expired = 1
    updated = 2


@dataclasses.dataclass(frozen=True)
class MICEntry:
    """Represents a single MIC entry"""
    mic: str
    market_name: str
    market_category_code: MCC
    creation_date: datetime.date
    status: Status
    city: Union[City, None] = None
    operating_mic: Union["MICEntry", None] = None
    institution_description: Union[str, None] = None
    legel_entity_name: Union[str, None] = None
    legal_entity_identifier: Union[str, None] = None
    acronym: Union[str, None] = None
    iso_country_code: Union[ISOCC, None] = None
    website: Union[str, None] = None
    last_update_date: Union[datetime.date, None] = None
    last_validation_date: Union[datetime.date, None] = None
    expiry_date: Union[datetime.date, None] = None
    comments: Union[str, None] = None


class MIC(enum.Enum):
    value: MICEntry
