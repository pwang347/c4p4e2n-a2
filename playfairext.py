# playfairext.py
# Extended playfair solver
#
# See results of run at crack2b.txt
#

from ciphertexts import CIPHERTEXTS, square_key
from collections import defaultdict

# taken from crack2a.txt
inter_plaintext = "AFYERWHICHHEPUTXTHETATALKNIFEINPOTYERSOPENRILHTHANDCOMAKANDSATDOWNONTHEDISAKNTLEDCOFFIQDOTTHREETOURFIXEMINUTESPASXSEDCOMAKANDTHENPOTYERBEGANTOSTIRANDMOAQDOTHISHANDCLOSEDUPONTHEKNIFEHERAISEDITCOMAKLRANCEDATITCOMAKANDLEYITFALXRCOMAKWITHKSHUDXDERDOTTHENHESKTUPCOMAKPUSHINGTHEBVDYFROMHIMCOMAKANDGAZEDATITCOMXAKANDTHENAROUQDHIMCOMXAKCONFUSEDLYDOTHISEFESMETIOESDOTLORDCOMXAKHOWISTHISCOMAKIVEHESAIDXDOTITSADIRYFBUSINESXSCOMAKSKIDIVECOMAKWITHOUTMVXINGDOTWHATDIDYOUDOITFORIINEVERDONEITLOOKHERETHATKIQDOFTALKWONTWKSHDOYPOTYERTREMBLEDAQDLGEWWHITEDOTITHOUGHTIDGOTSVBERDOTIDQVBUSINESSTODRINKTONILHTDOTBUTITSINMYHEADFETWORSENWHENWESTARTEDHEREDOTIAKLXLINAMUDXDLECANTRECOLLECTANFYHINGOFITHARDLYDOTXYELXLMECOMAKIVEHONESTCOMAKNOWCOMAKOLDFELLERDIDIDVITIOECOMXAKINEVERMEANTXTOPONMYSOULAQDHONORINEVERMEANTTOCOMXAKIVEDOTYELXLMEHOWITWKSCOMAKIVEDOTOCOMAKITSKWFULANDHIMSOYOUQGAQDPROMISINGDOTWHYXYOUTWOWKSXSCUFFLINLCOMAKANDHETEYCHEDYOUONEWITHTHEHEADBOARDANDYOUTELXLFLATAQDTHENUPYOUCOMECOMAKALRGEXELINGAQDSTAGGERINGCOMXAKLIKECOMXAKANDSNATCHEDTHEKNIFEAQDIAMXMEDITINTOHIMCOMXAKIUSTKSHETETCHEDYOUANOTHERAWFULCRIPANDHEREFOUVELAIDCOMXAKKSDEADKSKWEDGETILXLNOWDOTOCOMXAKIDIDNTKNOWWHATIWKSADVINGDOTIWISHIMAYDIEYHISAINUTEIFIDIDXDOTITWKSALLONACXCOUQTOTYHEWHISKYANDTHEEXCIYEMENTCOMXAKIRECKOQDOTINEVERUSEDKWEXEPONINMYLITEBEFORECOMXAKIVEDOTIXETOULHTCOMAKBUTNEVERWITHWEEPONSDOTTHEFLXLALXLSAYTHATDOTIOECOMXAKDONTYELXLSAYYOUWONTXYELXRCOMAKIVEYHATSAGVOODTELXLERDOTIALWAYSLIKEDYOUIOECOMXAKANDSTOODUPFORYOUCOMXAKTOODOTDONTYOUREMEMBERYOUWONTYELXRCOMAKWILXLYOUIVEAQDTHEPVOORCGEATUREDROPPEDONHISKNEXESBEFORETHESTOLIDMURDEREGCOMAKANDCLASPEDHISKPXPEALINLHANDSDOTNOCOMAKYOUVEALWAYSBEXENFAIRANDSZUAREWITHMECOMAKMUFXTPOTYEGCOMAKANDIWONTGOBACKONYOUDOTTHERECOMAKNOWCOMAKTHATSKSFAIRASKAKNCANSKYDOTOCOMAKIVECOMAKYOUREANANGELDOTILXLBLESXSYOUFORTHISTHELONGESTDAYILIXEDOTANDPOTYERBEGANTOCGYDOTCOMECOMXAKNOWCOMAKTHATSENOUGHOTYHATDOTTHISAINTANFYIMETORBLUBBERINGDOYFOUBEOFTFONDERWAYANDILXRLOTHISDOTMOVECOMXAKNOWCOMAKANDXDONTLEAVEANYTRACMSBEHIQDYOUDOTPOTXYERSTARTEDONATROTXTHATZUICKLYINCREKSEDTOARUQDOTXTHEHALFBREEDSTVOODLOOKINGATYERHIMDOTHEMUTXYEREDIFHESKSMUCHSTUQNEDWITHTHELICKANDFUDDLEDWITHTHERUMKSHEHADTHELOOKOFBEINLCOMAKHEWONTTHINKOTYHEKNIFEYILRHESGONESOFAGHELLBEAFRAIDTOCOMEBACMKTYERITTOSUCHAPLACEBYHIASELFCHICKENHEARTXTWVOORTHREEMINUTESLAYERTHEMURDEREDAKNCOMAKTHEBLANKEYEDCORPSECOMXAKTHELIDLESXSCOFFINAQDTHEOPENGRAVEWEREUQDERNVINSPECTIVNBUTTHEMVOONSDOTTHESTILXLNESSWKSCOMPLEYEAGAINCOMAKTOODOTCHAPYERONEZERODIREPROPHECYOFTHEHOWLINGDOGTHETWVBOYSFLEWONAQDONCOMXAKTOWKRDTHEVILLAGECOMXAKSPEXECHRESSWITHXHORXRORDOTTHEFLRANCEDBACMWARDOVERTHEIRSHOULDERSFROMTIMEYOTIMECOMAKAPPREHENSIVELYCOMXAKKSIFTHEFTEAREDTHEFMILHTBETOLLOWEDX"

def replace(target, replacement, text):
    result = []
    for idx in range(0, len(text), 2):
        if text[idx:idx+2] == target:
            result.append("[")
            result.append(replacement[0])
            result.append(replacement[1])
            result.append("]")
        else:
            result.append(text[idx])
            result.append(text[idx+1])
    return "".join(result)

# with a quick search of text segments, we can tell that the plaintext is from the adventures of tom sawyer
replacements = [
    ("AS", "MS"),
    ("MS", "KS"),
    ("TY", "FT"),
    ("CG", "CR"),
    ("GC", "RC"),
    ("KW", "AW"),
    ("VB", "OB"),
    ("WK", "WA"),
    ("ZU", "QU"),
    ("IX", "IV"),
    ("IV", "IO"),
    ("EF", "EY"),
    ("HR", "HL"),
    ("MW", "KW"),
    ("LC", "GC"),
    ("LR", "GL"),
    ("FY", "YT"),
    ("QD", "ND"),
    ("YF", "TY"),
    ("VX", "OV"),
    ("UQ", "UN"),
    ("BV", "BO"),
    ("SK", "SA"),
    ("SA", "SM"),
    ("KS", "AS"),
    ("RC", "LC"),
    ("EY", "ET"),
    ("ET", "EF"),
    ("LH", "GH"),
    ("AK", "MA"),
    ("YE", "TE"),
    ("LG", "GR"),
    ("DQ", "DN"),
    ("YP", "TP"),
    ("RG", "LR"),
    ("CR", "CL"),
    ("VI", "OI"),
    ("VO", "OX"),
    ("TP", "FP"),
    ("TF", "FY"),
    ("RL", "LG"),
    ("GH", "RH"),
    ("TE", "FE"),
    ("FE", "YE"),
    ("RH", "LH"),
    ("MK", "KA"),
]

j_replacements = [
    ("IOE", "JOE"),
    ("IUST", "JUST"),
    ("IAMXMED", "JAMXMED"),
]

res = inter_plaintext
for target, replacement in replacements:
    res = replace(target, replacement, res)

res = res.replace("[", "").replace("]", "")

# UNCOMMENT FOR PRETTY PRINTING, NOT USEFUL FOR DECIPHERING THE KEY AT ALL.
#for j_target, j_replacement in j_replacements:
#    res = res.replace(j_target, j_replacement)

#mutable_res = list(res)
#offset = 0
#for idx in range(len(res)):
#    if (idx + 2 - offset < len(mutable_res)) and mutable_res[idx - offset] == mutable_res[idx+2 - offset] and mutable_res[idx+1 - offset] == "X":
#        mutable_res.pop(idx+1-offset)
#        offset += 1
#res = "".join(mutable_res)

#if len(res) % 2 == 1:
#    if res[-1] != "X":
#        raise Exception("Should have trailing X")
#    res = res[:-1]

print("RECOVERED PLAINTEXT:")
print(res)

ciphertext = CIPHERTEXTS[1].value
if len(ciphertext) != len(res):
    raise Exception("Expected plain text to be the same length as the ciphertext (at this stage) %d vs %d" % (len(ciphertext), len(res)))

mapping = {}
plain_digrams = []
cipher_digrams = []
same_row_col_dependencies = set()
for idx in range(0, len(ciphertext), 2):
    digram_plain = res[idx:idx+2]
    digram_cipher = ciphertext[idx:idx+2]
    if digram_plain in mapping and mapping[digram_plain] != digram_cipher:
        print(mapping)
        raise Exception("Found duplicate mapping: %s to %s and %s" % (digram_plain, digram_cipher, mapping[digram_plain]))
    mapping[digram_plain] = digram_cipher
    if digram_plain[1] == digram_cipher[0]:
        same_row_col_dependencies.add(digram_plain + digram_cipher[1])
    plain_digrams.append(digram_plain)
    cipher_digrams.append(digram_cipher)

print("DEPENDENCIES: %s" % sorted(same_row_col_dependencies))

def check_dependencies(key):
    violated = []
    _, key_mapping = square_key(key)
    for dep in same_row_col_dependencies:
        origin1 = key_mapping[dep[0]]
        origin2 = key_mapping[dep[1]]
        origin3 = key_mapping[dep[2]]
        if origin2.x == origin1.x and origin2.y == (origin1.y + 1) % 5:
            if origin3.x == origin2.x and origin3.y == (origin2.y + 1) % 5:
                continue
        if origin2.y == origin1.y and origin2.x == (origin1.x + 1) % 5:
            if origin3.y == origin2.y and origin3.x == (origin2.x + 1) % 5:
                continue
        violated.append(dep)
    return sorted(violated)

# we begin by checking the key we got in crack2.txt from playfair.py...

#PISCD
#YVKLN
#FXMRQ
#EBWHU
#TOAGZ

key1 = "PISCDYVKLNFXMRQEBWHUTOAGZ"
print("Missing dependencies for %s:\n%s" % (key1, check_dependencies(key1)))

#PISCD
#YVKLN
#EBWHU
#FXMRQ
#TOAGZ

key2 = "PISCDYVKLNEBWHUFXMRQTOAGZ"
print("Missing dependencies for %s:\n%s" % (key2, check_dependencies(key2)))

#PISCD
#YVKLN
#EBWHU
#TOAGZ
#FXMRQ

#PISCDYVKLNEBWHUTOAGZFXMRQ
key="PISCDYVKLNEBWHUTOAGZFXMRQ"
print("Missing dependencies for %s:\n%s" % (key, check_dependencies(key)))

def test_key(key):
    """
    Essentially playfair encrypt, but we also check against the known digram mappings
    for errors.
    """
    errors = []
    key_square, key_mapping = square_key(key)
    for k, v in mapping.items():
        first = k[0]
        second = k[1]
        if key_mapping[first].y == key_mapping[second].y:
            new_first = key_square[key_mapping[first].y][(key_mapping[first].x + 1)%5]
            new_second = key_square[key_mapping[second].y][(key_mapping[second].x + 1)%5]
        elif key_mapping[first].x == key_mapping[second].x:
            new_first = key_square[(key_mapping[first].y + 1)%5][key_mapping[first].x]
            new_second = key_square[(key_mapping[second].y + 1)%5][key_mapping[second].x]
        else:
            new_first = key_square[key_mapping[first].y][key_mapping[second].x]
            new_second = key_square[key_mapping[second].y][key_mapping[first].x]

        if v != new_first + new_second:
            errors.append((k, v, new_first + new_second))

    return errors

print("Failed tests for %s:\n%s" % (key, test_key(key)))
