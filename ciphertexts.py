# ciphertexts.py
# Raw ciphertexts and helpers

from collections import namedtuple
from enum import Enum, auto
import itertools
import random

class Cipher(Enum):
    UNKNOWN = auto()
    MONO_SUBSTITUTION = auto()
    PLAYFAIR = auto()

CipherText = namedtuple("CipherText", ["cipher", "value"])

CIPHERTEXTS = [
    CipherText(cipher=Cipher.MONO_SUBSTITUTION, value="BSHBTSSLAXCXCTBMXRCEEBAZAQYGCXYLBTWCKRCEEBBKXBHHEFTSLBZADQMIATXCSGFSWLCMTSCPMZASLADQMIATUFMSABRLCQFTCJZCMRATBTOAXXCSWLYRCEEBTLARCEEBCJRCFQTARCEEBTBMXSLAXCXCRCEEBDCMKSMKPSCBHMRAWMSLCKAJMKPAQBKXSLAWLCHADBQSYBSCKRARQCWXAXQCFKXLAQRCEEBRBHHMKPCFSMKBRCKJFTAXWBYRCEEBDQMIATDQMIATBHMRALBXKCMXABWLBSSCXCRCEEBBKXMKXATDBMQTLADFSLAQLBKXMKLAQDCROASRCEEBBKXDFHHAXCFSBGCVCJRCEJMSTRCEEBHFROMHYSLATBHSWBSAQLBXKCSPCSMKSCMSRCEEBBKXLBKXAXSLAEQCFKXBTDQMIATXCSSLAQAWBTAVBRSHYCKABDMARABHHQCFKX"),
    CipherText(cipher=Cipher.PLAYFAIR, value="TMFTMHBCLGUBDEOFGETPGOGKLYPXBPYDAOFTMCTIUYXCRGGEZKPDAXSMZKPCGOIZUKZVGEUPSCSMYZYHPDTXXPUNAOGEFHTPZBQXVBWFDVEZWPSTIMPWPDAXSMZKPZUBYDAOFTXHHTZKOAPACXZKSQAGUNAOBCCWZKPDVGPWNZITYZUBLYPXBUHFOSPWPSGPAXSMRHZKPHSZOPGPAXSMZKCNTFPOMTVRHLAXSMBSGEMKUEIQPUQCAOGEUYUBKMZEIDAXSMDECWDVZOUBOXPNXQAXBCRSAXSMZKCZGTUPGOPOIGRMSMZKPZUBKZXGZUCUSXIGRMSMIGYQWDUPNVIZGESCTEWPFWOPTBCPAOVGQCIGRMSMBGBSPABCCDAXSMVXBUWPOSIQIZOPAPZSCXFEWECSYUIMCDAXSMKMSPVXHPAXSMBSGEZBAFXBDVZCAOHUGOPSPNZBIZPOXTXCDVBYHFIZYUPOVGAVUBFHGEGOVSUNTXOGNLBAYZAMCWIZFYAOFTFGFHXWYHSZUNRCBHHUPOUPAOPOBGHZEGSPZAAPXOHFIZOPNUXOWDDVWPPAZIXCYLOAVDRGZPAOWEOPAPDVFKUBZSETAEGXPWKUUBKUWPOGFGUPUBFHIZOPSMVRVCKZQWIQCNHPZKGFHPGVYHPGZKEFBCLZTXPOWGQCNVIZOFFTVRKRHPAXSMVXBUZVWPGPAXSMVZHSAXSMGVPQHYYHQCSPSPXVOPTBIGRMSMDVBYHFFWZKOFOAITKQKPZBKGUNBGVZXCYUYBQRWTYZOAIGRMSMVXUPAOFTVRKRBUABPOAMCDAXSMVXUPAOGIAXSMPOKMEMHNZKCUSXIAVTZUZGUNCFAXSCDVZCAOHUVFVTEZBAAMIMCDEQRYDVRLAXSMZKCUTPTFLGUPVTBZYUBSGEGEBUWTIUAGQCZKPNZBPTVRYRKGOGUNGEUYEDVTHDAXHPAXSMGKHCBFHYDVZGUNPAGZTHXCLZIGRMSMVCYWIGRMSMZKPCKZGPUBPZUBLYPXWTUNSORMFWPSOPYZGBSXIGRMSMDBPAMKUBPTGPUBPNZBZKAOUBMGEMHNLHSIZKCUHFTEZBYBKGSPIGRMSMMKPUZSMKMAUPTHOPVRNYABIZOAIGRMSMSPSPYZLYABHUGOSBMKZSXVLZIZOPBSCWSXTKPSTFBCKSDVEZBPXPPSIQIZOPAEMKGKVGKZIRIGZUOAPFUBHUSCLVZKPZUBBFDSFTFWYZIGRMSMCXHPVAUNAODVBYHFWDUPMABFTYZVDVFKVCPTWBXTFHIGRMSMVXUPAOVBTPZBRGGPAXSMWEZYBYHFBSGEHBTYZVCPAOGETEVRKGVRKCTKGEGOIZOPTBIGRMSMIZYZFTVRKCTKVTEHZVOFFTVRHLAXSMVXTFWGAPGZXIZIPTVRYHQCAOSOKHTKCKSVUPVTBDTBIGRMSMZKPCOAZIEDXTFLZBIGRMSMOAZIAOIZYZVTHQWFWFWBFLZBBAYZFTVRHLAXSMBSVRNVZBVXWTUNGETYXIGXLCWTZEFHCQTIYTIZLUSCLYBFWPWBXTFHGEWPOAVCSQHQPUFHCLAXSMZKPDKGCIUPBCKMIFYTGKDVRGZKPCIZZYGIAXSMVTBNWTKHTKIWBFUYMTCXZKPCDZGMBHPOWRHPAXSMQWXMPYAOFTCLAXSMZKPSBAYZZAWOSLZVVTZNAOGEHFHPAXSMVZHSAXSMGEGOKMPMOSMGKMSMLDZKKMNPAOGIAXSMVXHPAXSMVTHQWTKZLZHYIZOPVRVHYHIMPKZBXTFGBCPAUBVGLZWPZPTKCVVBUPAOZKPIAOFTXHHTZKOALCNPAOIGFWIGRMSMVZHSAXSMGEGOPWVZHZBGPFWGZPAOGESCOSYZZKEFSXTPGXHVEWWBXCLZIZFEZBWBTXPEZVPUMHTKZKPSVRHRAOBCCPAOXAYBIGRMSMVZHSAXSMZKIQIZYZYHOKWTYVGFGSWKWBBCUNVTZNAOITOFFTMCOGFGUPZVGOXGOFGEGODZSDLNVPLDFHMKUPOAGMZUIZOFGEBUGKXEFHUPPAXIZIVGAVDVZGPFHFBCQSAOUBQWOFFTFHPSREWPMKQWLGPAZUYUSUPOEGUBVCSLZKPQZNCNUPBSGEGEHFWQMKUBWGPZUBVGAVTXWBDVRLAXSMUBBAYZGEDVVAPFUBLYPXTFCVHGWPZAYUIAMTCGHYVHWTXQOSPZGIAXBWGSWMPFHFPOOADWLGTSKGPHEVBCSKHYRPBCSLUYUBGMOFAEXIGXGEFHWFDVEZWPKGFTFGUBQWQCHFUPSMLDAXSMGEBWKGYLTFUPIGFCPWIGRMSMGEHYSPYHIMCDTXXPKZUNGEBTYTLZMGYBHBFHZUPUQLXVKDYTPGVXVUEZGEWFXIZVCPAOGEWPOPVRNYWPKAMKIGFSYHFTGZOSLDAXSMOAZIAOLGTSFTXGYUTUXGPSFHCFTIUBPLTXGEBUABVCLZIZZOUBAEXOTVPMYHBAKZUNZVIGRMSMOAAMQCGEBYCVKGTHIGRMSMCIBFHPGHWPKAPOBRBGQMXGQCAOGETERHZKPHIUGSWAGMIZYBFGUBCXCWZBNCHFPMXGFASXTFAOSXHPAXSMTSCFBUUYCSYBNVIGRMSMMKPXGETEPTGMUPGETEXSRGOETPGVVGHBIQ"),
]

def generate_key(alphabet):
    """
    Helper that generates a permutation of the given alphabet.
    """
    key_builder = []
    choices = [c for c in alphabet]
    for i in range(len(alphabet)):
        choice_idx = random.choice(range(len(choices)))
        choice = choices.pop(choice_idx)
        key_builder.append(choice)
    return "".join(key_builder)

def step_key(key, seen=None):
    """
    Helper to make one swap in provided key.
    """
    if seen is None:
        seen = set()
    choices=list(itertools.product(range(len(key)), range(len(key))))
    seen.add(key)
    new_key = key
    while new_key in seen:
        if len(choices) == 0:
            return False
        result = list(key)
        choice_idx = random.choice(range(len(choices)))
        first_idx, second_idx = choices.pop(choice_idx)
        result[first_idx], result[second_idx] = result[second_idx], key[first_idx]
        new_key = "".join(result)
    return new_key

Coord = namedtuple("Coord", ["x", "y"])

def square_key(key):
    """
    Helper to make a playfair square key (moved here to avoid import overhead)
    """
    key_square = []
    key_mapping = {}
    for j in range(5):
        key_square.append([])
        for i in range(5):
            key_square[j].append(key[i+j*5])
            key_mapping[key[i+j*5]] = Coord(i, j)
    return key_square, key_mapping