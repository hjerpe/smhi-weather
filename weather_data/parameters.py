from typing import Dict, NamedTuple


# Define a named tuple type with types
class Parameter(NamedTuple):
    id: str
    title: str
    summary: str
    unit: str


# List of parameters as named tuples
parameters_list = [
    Parameter("21", "Byvind", "max, 1 gång/tim", "meter per sekund"),
    Parameter("39", "Daggpunktstemperatur", "momentanvärde, 1 gång/tim", "celsius"),
    Parameter(
        "11",
        "Global Irradians (svenska stationer)",
        "medelvärde 1 timme, 1 gång/tim",
        "watt per kvadratmeter",
    ),
    Parameter("22", "Lufttemperatur", "medel, 1 gång per månad", "celsius"),
    Parameter(
        "26", "Lufttemperatur", "min, 2 gånger per dygn, kl 06 och 18", "celsius"
    ),
    Parameter(
        "27", "Lufttemperatur", "max, 2 gånger per dygn, kl 06 och 18", "celsius"
    ),
    Parameter("19", "Lufttemperatur", "min, 1 gång per dygn", "celsius"),
    Parameter("1", "Lufttemperatur", "momentanvärde, 1 gång/tim", "celsius"),
    Parameter(
        "2", "Lufttemperatur", "medelvärde 1 dygn, 1 gång/dygn, kl 00", "celsius"
    ),
    Parameter("20", "Lufttemperatur", "max, 1 gång per dygn", "celsius"),
    Parameter(
        "9",
        "Lufttryck reducerat havsytans nivå",
        "vid havsytans nivå, momentanvärde, 1 gång/tim",
        "hektopascal",
    ),
    Parameter(
        "24",
        "Långvågs-Irradians",
        "Långvågsstrålning, medel 1 timme, varje timme",
        "watt per kvadratmeter",
    ),
    Parameter("40", "Markens tillstånd", "momentanvärde, 1 gång/dygn, kl 06", "kod"),
    Parameter(
        "25",
        "Max av MedelVindhastighet",
        "maximum av medelvärde 10 min, under 3 timmar, 1 gång/tim",
        "meter per sekund",
    ),
    Parameter("28", "Molnbas", "lägsta molnlager, momentanvärde, 1 gång/tim", "meter"),
    Parameter("30", "Molnbas", "andra molnlager, momentanvärde, 1 gång/tim", "meter"),
    Parameter("32", "Molnbas", "tredje molnlager, momentanvärde, 1 gång/tim", "meter"),
    Parameter("34", "Molnbas", "fjärde molnlager, momentanvärde, 1 gång/tim", "meter"),
    Parameter("36", "Molnbas", "lägsta molnbas, momentanvärde, 1 gång/tim", "meter"),
    Parameter("37", "Molnbas", "lägsta molnbas, min under 15 min, 1 gång/tim", "meter"),
    Parameter("29", "Molnmängd", "lägsta molnlager, momentanvärde, 1 gång/tim", "kod"),
    Parameter("31", "Molnmängd", "andra molnlager, momentanvärde, 1 gång/tim", "kod"),
    Parameter("33", "Molnmängd", "tredje molnlager, momentanvärde, 1 gång/tim", "kod"),
    Parameter("35", "Molnmängd", "fjärde molnlager, momentanvärde, 1 gång/tim", "kod"),
    Parameter("17", "Nederbörd", "2 gånger/dygn, kl 06 och 18", "kod"),
    Parameter("18", "Nederbörd", "1 gång/dygn, kl 18", "kod"),
    Parameter(
        "15",
        "Nederbördsintensitet",
        "max under 15 min, 4 gånger/tim",
        "millimeter per sekund",
    ),
    Parameter(
        "38",
        "Nederbördsintensitet",
        "max av medel under 15 min, 4 gånger/tim",
        "millimeter per sekund",
    ),
    Parameter("23", "Nederbördsmängd", "summa, 1 gång per månad", "millimeter"),
    Parameter("14", "Nederbördsmängd", "summa 15 min, 4 gånger/tim", "millimeter"),
    Parameter("5", "Nederbördsmängd", "summa 1 dygn, 1 gång/dygn, kl 06", "millimeter"),
    Parameter("7", "Nederbördsmängd", "summa 1 timme, 1 gång/tim", "millimeter"),
    Parameter("6", "Relativ Luftfuktighet", "momentanvärde, 1 gång/tim", "procent"),
    Parameter(
        "13", "Rådande väder", "momentanvärde, 1 gång/tim resp 8 gånger/dygn", "kod"
    ),
    Parameter("12", "Sikt", "momentanvärde, 1 gång/tim", "meter"),
    Parameter("8", "Snödjup", "momentanvärde, 1 gång/dygn, kl 06", "meter"),
    Parameter("10", "Solskenstid", "summa 1 timme, 1 gång/tim", "sekund"),
    Parameter("16", "Total molnmängd", "momentanvärde, 1 gång/tim", "procent"),
    Parameter(
        "4", "Vindhastighet", "medelvärde 10 min, 1 gång/tim", "meter per sekund"
    ),
    Parameter("3", "Vindriktning", "medelvärde 10 min, 1 gång/tim", "grader"),
]

# Creating a dictionary with titles as keys
parameters: Dict[str, Parameter] = {param.id: param for param in parameters_list}
