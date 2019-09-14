# -*- coding: utf-8 -*-

# from __future__ import print_function
# from __future__ import division
import re, codecs, sys#, enchant (tidak dijaga lagi; diganti dgn pyspellchecker)
from spellchecker import SpellChecker
from itertools import permutations
from pickle import load

# Penanggal enklitik naif
def NyahEnklitik(w):
    lapis1 = ["ku","mu","kau","nya","Nya"]
    lapis2 = ["lah","kah"]
    aff = []
    for item in lapis2:
        if w.endswith(item):
            aff.append("-"+item)
            w = w[:-3]
    if w.endswith("-Nya"):
        aff.append("-Nya")
        w = w[:-4]
    else:
        for item in lapis1:
            if w.endswith(item):
                aff.append("-"+item)
                w = w[:-len(item)]
    aff.reverse()
    return w, "+".join(aff)

# Penanggal proklitik naif
def NyahProklitik(w):
    lapis1 = ["ku","kau"]
    aff = []
    for item in lapis1:
        if w.startswith(item):
            aff.append(item+"-")
            w = w[len(item):]
    return w, "+".join(aff)

# Analisis serius
def start(w, Indo = False):
    """
    Kembalikan senarai rentetan permulaan yg mungkin.
    @param Indo: Jika benar, N- juga termasuk.
    """
    lapis0 = ["ku","kau", "ke", "se"] # proklitik, KGN yg salah dieja, KEberSE
    lapis1 = ["di", "ber", "ter", "menge", "meng", "menye", "meny", "mem", "men", "me"] # V, A
    if Indo:
        lapis1 = ["di", "ber", "ter", "menge", "meng", "menye", "meny", "mem", "men", "me", "%"] # V, A
    lapis1r = ["be", "te"] # V, A (terus diikuti dgn kada dasar yg bermula dgn "r")
    lapis2 = ["penge", "peng", "penye", "peny", "pem", "pen", "per", "pe", "ke", "se"] # N, A, per- kausatif
    startlist = set(lapis0 + lapis1 + lapis1r +lapis2 + \
        [item0+item1+item2 for item0 in lapis0 for item1 in lapis1 for item2 in lapis2] + \
        [item0+item2+item1 for item0 in lapis0 for item2 in lapis2 for item1 in lapis1] + \
        [item0+item1 for item0 in lapis0 for item1 in lapis1] + \
        [item0+item1 for item0 in lapis0 for item1 in lapis1r] + \
        [item0+item2 for item0 in lapis0 for item2 in lapis2] + \
        [item1+item2 for item1 in lapis1 for item2 in lapis2] + \
        [item2+item1 for item1 in lapis1 for item2 in lapis2] + \
        [item2+item1 for item1 in lapis1r for item2 in lapis2] + \
        [item0+item2+item1+item2 for item0 in lapis0 for item1 in lapis1 for item2 in lapis2] + \
        [item0+item1+item2+item1 for item0 in lapis0 for item1 in lapis1 for item2 in lapis2] + \
        [item0+item1+item2+item1r for item0 in lapis0 for item1 in lapis1 
                for item1r in lapis1r for item2 in lapis2] + \
        [item2+item1+item2 for item1 in lapis1 for item2 in lapis2] + \
        [item1+item2+item1 for item1 in lapis1 for item2 in lapis2] + \
        [item1+item2+item1r for item1 in lapis1 for item1r in lapis1r for item2 in lapis2]
        )
    beginning = set()
    for item in startlist:
        if w.lower().startswith(item):
            beginning.add(item)
    return beginning

def end(w, Indo = False):
    """
    Kembalikan senarai rentetan akhir yg mungkin.
    @param Indo: Jika benar, -in juga termasuk.
    """
    lapis0 = ["kan","i"]
    if Indo:
        lapis0 = ["kan","i", "in"]
    lapis1 = ["ku","mu","kau","nya","Nya"]
    lapis2 = ["lah","kah"]
    endlist = set(["an", "anan"] + lapis0 + lapis1 + lapis2 + \
        ["an"+item0+item1+item2 for item0 in lapis0 for item1 in lapis1 for item2 in lapis2] + \
        ["an"+item0+item1 for item0 in lapis0 for item1 in lapis1] + \
        ["an"+item0+item2 for item0 in lapis0 for item2 in lapis2] + \
        ["an"+item1+item2 for item1 in lapis1 for item2 in lapis2] + \
        ["an"+item0 for item0 in lapis0] + \
        ["an"+item1 for item1 in lapis1] + \
        ["an"+item2 for item2 in lapis2] + \
        [item0+item1+item2 for item0 in lapis0 for item1 in lapis1 for item2 in lapis2] + \
        [item0+item1 for item0 in lapis0 for item1 in lapis1] + \
        [item0+item2 for item0 in lapis0 for item2 in lapis2] + \
        [item1+item2 for item1 in lapis1 for item2 in lapis2] + \
        ["anan"+item0+item1+item2 for item0 in lapis0 for item1 in lapis1 for item2 in lapis2] + \
        ["anan"+item0+item1 for item0 in lapis0 for item1 in lapis1] + \
        ["anan"+item0+item2 for item0 in lapis0 for item2 in lapis2] + \
        ["anan"+item1+item2 for item1 in lapis1 for item2 in lapis2] + \
        ["anan"+item0 for item0 in lapis0] + \
        ["anan"+item1 for item1 in lapis1] + \
        ["anan"+item2 for item2 in lapis2]
        )
    ending = set()
    for item in endlist:
        if w.lower().endswith(item):
            ending.add(item)
    return ending

def SylCount(w, root = False, mono = False):
    """
    Kembelikan jumlah suku kata ("syllable count") bagi w.
    @param root: Jika benar, w dianggap sebagai akar, dan diftong ditangani dengan betul.
    @param mono: Jika benar, perkataan bersuku kata satu dianggap sebagai mempunyai 3.5 suku kata.
    """
    n = 0
    if root and (w.endswith("ai") or w.endswith("au") or w.endswith("oi")):
        w = w[:-1]
    p = len(re.findall(r"[aeiou]", w))
    if mono and p == 1:
        n = 3.5
    else:
        n = p
    return n

def ngopi(w, rootlist):
    """Menukar N kepada konsonan yang sesuai."""
    stem  = []
    if w.startswith("m"):
        if "p" + w[1:] in rootlist:
            stem.append("p" + w[1:])
        if "f" + w[1:] in rootlist:
            stem.append("f" + w[1:])
    if w.startswith("n"):
        if "t" + w[1:] in rootlist:
            stem.append("t" + w[1:])
        if w.startswith("ny"):
            if "s" + w[2:] in rootlist:
                stem.append("s" + w[2:])
            if "c" + w[2:] in rootlist:
                stem.append("c" + w[2:])
        if w.startswith("ng"):
            if "k" + w[2:] in rootlist:
                stem.append("k" + w[2:])
            if len(w) > 2 and w[2] in ["a", "e", "i", "o", "u"]  and w[2:] in rootlist:
                stem.append(w[2:])
            if w.startswith("nge") and SylCount(w[3:], root = True) == 1 and w[3:] in rootlist:
                stem.append(w[3:])
    return stem

# Pnegklasifikasi reduplikasi
def Ganda(w, rootlist):
    """
    Kembalikan dasar dan jenis reduplikasi (penuh, penuh+imbuhan, ritma, ritma_majmuk).
    w tidak boleh mengandungi klitik.
    """
    base = ""
    kind = ""
    nonbase = ""
    if w.count("-") == 1 and w.replace("-", "").isalpha():
        first, second = w.split("-")
        vowels = set(["a","e","i","o","u"])
        V1 = [x for x in first if x in vowels]
        V2 = [x for x in second if x in vowels]
        C1 = [x for x in first if x not in vowels]
        C2 = [x for x in second if x not in vowels]
        common = [x for x in first if x in second]
        # Penuh (cth. kecantikan-kecantikan, masalah-masalah)
        if first == second:
            base = first
            kind = "penuh"
            nonbase = second
        # Penuh + imbuhan (dasar = unsur 1)
        # (cth. pukul-memukul, adik-beradik, nengok-menengok, cinta-menyintai, buah-buahan)
        elif (second.startswith("me") or second.startswith("be") or second.endswith("an")) and first[1:] in second:
            kind = "penuh+imbuhan_1"
            nonbase = second
            if first not in rootlist:
                n = ngopi(first, rootlist)
                if n:
                    base = n[0]
            else:
                base = first
        # Penuh + imbuhan (dasar = unsur 2)
        # (cth. beramai-ramai, berkirim-kiriman, kemerah-merahan, memukul-mukul(kan/i), sepandai-pandai, dua-duanya)
        # ber--an, ke--an
        elif second.endswith("an") and (first.startswith("be") or first.startswith("ke")) and \
                first[3:] in second[:-2]:
            base = second[:-2]
            kind = "penuh+imbuhan_2"
            nonbase = first
        # memper--kan
        elif first.startswith("memper") and second.endswith("kan") and \
                (first[6:] in second or first[6:] in second[:-3]): # klausa kedua untuk akar pendek
            kind = "penuh+imbuhan_2"
            nonbase = first
            base = second[:-3]
        # memper--i
        elif first.startswith("memper") and second.endswith("i") and \
                (first[6:] in second or first[6:] in second[:-1]): # klausa kedua untuk akar pendek
            kind = "penuh+imbuhan_2"
            nonbase = first
            base = second[:-1]
        # meN--kan
        elif first.startswith("me") and second.endswith("kan") and \
                (first[4:] in second or first[3:] in second[:-3]): # klausa kedua untuk akar pendek
            kind = "penuh+imbuhan_2"
            nonbase = first
            second = second[:-3]
            if second not in rootlist:
                n = ngopi(second, rootlist)
                if n:
                    base = n[0]
            else:
                base = second
        # meN--i
        elif first.startswith("me") and second.endswith("i") and \
                (first[4:] in second or first[3:] in second[:-1]): # klausa kedua untuk akar pendek
            kind = "penuh+imbuhan_2"
            nonbase = first
            second = second[:-1]
            if second not in rootlist:
                n = ngopi(second, rootlist)
                if n:
                    base = n[0]
            else:
                base = second
        # ber-, meN-, ter-, se-
        elif (first.startswith("be") or first.startswith("me") or first.startswith("te") or first.startswith("se")) and \
                (first[4:] in second or first[3:] in second): # klausa kedua untuk akar pendek
            kind = "penuh+imbuhan_2"
            nonbase = first
            if second not in rootlist:
                n = ngopi(second, rootlist)
                if n:
                    base = n[0]
            else:
                base = second
        # -nya
        elif (second.endswith("nya")) and \
                (second[:-3] in first):
            kind = "penuh+imbuhan_2"
            nonbase = first
            base = second
        # Reduplikasi ritma (cth. lauk-pauk, caci-maki, gunung-ganang, tunggang-langgang)
        elif V1 == V2 or C1 == C2 or \
                (len(common)/len(first) >= .75 and len(common)/len(second) >= .75):
            if first in rootlist and second in rootlist:
                base = first
                kind = "ritma_mjmk"
                nonbase = second
            else:
                kind = "ritma"
                if second in rootlist:
                    base = second
                    nonbase = first
                else:
                    base = first
                    nonbase = second
    return base, kind, nonbase

# Pencari akar
def Akar(word, rootlist, Indo = False):
    """
    Kembalikan set calon akar dan imbuhan.
    @param Indo: Jika benar, awalan N- juga termasuk.
    """
    cand = []
    word = word.lower()
    s = start(word)
    e = end(word)
    if Indo:
        s = start(word, Indo = True)
        e = end(word, Indo = True)
    pair = set([(pre, suf) for pre in s for suf in e] + [(pre, "") for pre in s] + [("", suf) for suf in e])
    vowels = set(["a","e","i","o","u"])
    legit = re.compile(r"^((skl|skr|spl|spr|str|bl|br|dr|dw|fl|fr|gh|gl|gr|kh|kl|kr|ng|ny|pl|pr|ps|sf|sh|sk|sl|sm|sn|sp|sr|st|sy|sw|tr)|[^aeiou])?[aeiou]+.*(?<![^aeiougklnprs][^aeiouhstdgkbmny])$")
    # Reduplikasi, 1990-an(lah), ke-19(lah)
    if not word in rootlist and "-" in word:
        # Buang klitik
        pro = ""
        en = ""
        b, en = NyahEnklitik(word)
        if en:
            en = en[1:].replace("+-", "")
        # Penggunaan "-" secara tidak baku (cth. kata-kata-nya)
        if b.endswith("-"):
            b = b[:-1]
        if b not in rootlist:
            word, pro = NyahProklitik(b)
            if pro:
                pro = pro[:-1]
        else:
            word = b
        # Penggunaan "-" secara tidak baku (cth. ku-kata-kata)
        if word.startswith("-"):
            word = word[1:]
        # Reduplikasi
        base, kind, nonbase = Ganda(word, rootlist)
        # Penuh (cth. kecantikan-kecantikan, masalah-masalah)
        if kind == "penuh":
            for tpl in Akar(base, rootlist):
                cand.append((tpl[0], pro+tpl[1], tpl[2]+en, "R-"+kind))
        # Ritma (cth. lauk-pauk, caci-maki, gunung-ganang, tunggang-langgang)
        elif "ritma" in kind:
            cand.append((base, pro, en, "R-"+kind))
        else:
            # Penuh + imbuhan (dasar = unsur 2)
            # (cth. beramai-ramai, berkirim-kiriman, kemerah-merahan, memukul-mukul(kan/i))
            if kind == "penuh+imbuhan_2":
                # ber--an, ke--an
                if word.endswith("an") and (word.startswith("be") or word.startswith("ke")):
                    nonbase = nonbase + "an"
                # meN--kan
                elif word.startswith("me") and word.endswith("kan"):
                    nonbase = nonbase + "kan"
                # meN--i
                elif word.startswith("me") and word.endswith("i"):
                    nonbase = nonbase + "i"
            # Penuh + imbuhan (dasar = unsur 1) juga
            # (cth. pukul-memukul, adik-beradik, nengok-menengok, cinta-menyintai)
            if "penuh+imbuhan" in kind:
                for tpl in Akar(nonbase, rootlist):
                    if tpl[1] or tpl[2]:
                        cand.append((tpl[0], pro+tpl[1], tpl[2]+en, "R-"+kind))
            # Bukan reduplikasi
            nodash = word.replace("-", "")
            cuba = Akar(nodash, rootlist)
            if cuba:
                for tpl in cuba:
                    # Hyphenation (cth. ke-merahan), ke-19(lah), 1990-an(lah)
                    if tpl[0] in rootlist or (tpl[0].isdigit() and "ke" in tpl[1]) or \
                       (tpl[0].isdigit() and "an" in tpl[2]):
                        cand.append((tpl[0], pro+tpl[1], tpl[2]+en, "0"))
                    else:
                        cand.append((word, pro, en, "0"))
            else:
                cand.append((word, pro, en, "0"))
    elif not word in rootlist and pair:
        for (pre, suf) in pair:
            if suf:
                r = word[len(pre):-len(suf)]
            else:
                r = word[len(pre):]
            if not r:
                break
            # Pulihkan konsonan yang gugur disebabkan penggantian nasal 
            #(NOTA: memroses dsb. dalama bahasa Indonesia diabaikan)
            if pre.endswith("m") and r[0] in vowels: # mem-, pem-
                r = "p" + r
            elif pre.endswith("ny") and r[0] in vowels: # meny-, peny-
                r = "s" + r
            elif pre.endswith("n") and not pre.endswith("ng") and r[0] in vowels: # men-, pen-
                r = "t" + r
            elif pre.endswith("ng") and r[0] in vowels: # meng-, peng- (NOTA: meng-V = meN- + V or kV)
                r1 = "k" + r
                cand.append((r1, pre, suf, "0"))
            # Morfotaktik & Jangan pisahkan <ng> dan <ny> & be-/te- hanya sebelum akar yg bermula dgn "r"
            if not r.isalpha() or \
               (legit.match(r) and \
                not (pre.endswith("n") and (r.startswith("g") or r.startswith("y"))) and \
                not ((pre.endswith("be") or pre.endswith("te")) and not r.startswith("r"))):
                cand.append((r, pre, suf, "0"))
            else:
                cand.append((word, "", "", "0"))
    if not cand:
        cand.append((word, "", "", "0"))
    # N- dalam bahasa Indonesia (cth. ng-apa-kan)
    if Indo:
        for c in cand:
            if c[0].startswith("n") or c[0].startswith("m"):
                N1 = ngopi(c[0], rootlist)
                if N1:
                    for n in N1:
                        for tpl in Akar(c[1]+n+c[2], rootlist, Indo = True):
                            cand.append((tpl[0], tpl[1]+"%", tpl[2], tpl[3]))
                N2 = ngopi(c[0]+c[2], rootlist)
                if N2:
                    for n in N2:
                        for tpl in Akar(c[1]+n, rootlist, Indo = True):
                            cand.append((tpl[0], tpl[1]+"%", tpl[2], tpl[3]))
    # Choose analyses with existing roots, if any
    cand1 = [(r, pre, suf, red) for (r, pre, suf, red) in cand if r in rootlist]
    if cand1:
        cand = cand1
    return cand

# Penanggal apitan
# peN--an, pe--an, per--an
def NyahApitan_p(r, pre, suf, cir, p_pre, p_suf):
    """Kembalikan sekumpulan calon apitan dan imbuhan"""
    if "pe" in pre and "an" in suf:
        pre1 = pre.replace("pe", "", 1)
        suf1 = suf.replace("an", "", 1)
        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
            pre = pre1
            suf = suf1
            if r.startswith("r"):
                if cir:
                    cir += "+peN--an@pe--an@per--an"
                else:
                    cir += "peN--an@pe--an@per--an"
            else:
                if cir:
                    cir += "+peN--an@pe--an"
                else:
                    cir += "peN--an@pe--an"
        elif "pem" in pre and "an" in suf:
            pre1 = pre.replace("pem", "", 1)
            suf1 = suf.replace("an", "", 1)
            if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
                pre = pre1
                suf = suf1
                if cir:
                    cir += "+peN--an"
                else:
                    cir += "peN--an"
        elif "per" in pre and "an" in suf:
            pre1 = pre.replace("per", "", 1)
            suf1 = suf.replace("an", "", 1)
            if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
                pre = pre1
                suf = suf1
                if cir:
                    cir += "+per--an"
                else:
                    cir += "per--an"
        elif "pen" in pre and "an" in suf:
            pre1 = pre.replace("pen", "", 1)
            suf1 = suf.replace("an", "", 1)
            if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
                pre = pre1
                suf = suf1
                if cir:
                    cir += "+peN--an"
                else:
                    cir += "peN--an"
            elif "peny" in pre and "an" in suf:
                pre1 = pre.replace("peny", "", 1)
                suf1 = suf.replace("an", "", 1)
                if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
                    pre = pre1
                    suf = suf1
                    if cir:
                        cir += "+peN--an"
                    else:
                        cir += "peN--an"
                elif "penye" in pre and "an" in suf: # peN--an + se-
                    pre1 = pre.replace("penye", "se", 1)
                    suf1 = suf.replace("an", "", 1)
                    if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
                        pre = pre1
                        suf = suf1
                        if cir:
                            cir += "+peN--an"
                        else:
                            cir += "peN--an"
            elif "peng" in pre and "an" in suf:
                pre1 = pre.replace("peng", "", 1)
                suf1 = suf.replace("an", "", 1)
                if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
                    pre = pre1
                    suf = suf1
                    if cir:
                        cir += "+peN--an"
                    else:
                        cir += "peN--an"
                elif "penge" in pre and "an" in suf: # monosyllabic root or peN--an + ke-(an)
                    if SylCount(r, root = True) == 1:
                        pre1 = pre.replace("penge", "", 1)
                        suf1 = suf.replace("an", "", 1)
                        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
                            pre = pre1
                            suf = suf1
                            if cir:
                                cir += "+peN--an"
                            else:
                                cir += "peN--an"
                    else:
                        pre1 = pre.replace("penge", "ke", 1)
                        suf1 = suf.replace("an", "", 1)
                        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
                            pre = pre1
                            suf = suf1
                            if cir:
                                cir += "+peN--an"
                            else:
                                cir += "peN--an"
    return pre, suf, cir

# ke--an
def NyahApitan_k(r, pre, suf, cir, p_pre, p_suf):
    """Kembalikan sekumpulan calon apitan dan imbuhan"""
    if "ke" in pre and "an" in suf:
        pre1 = pre.replace("ke", "", 1)
        suf1 = suf.replace("an", "", 1)
        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
            pre = pre1
            suf = suf1
            if cir:
                cir += "+ke--an"
            else:
                cir += "ke--an"
    elif ("penge" in pre or "menge" in pre) and "an" in suf:
        pre1 = pre.replace("enge", "eng", 1)
        suf1 = suf.replace("an", "", 1)
        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
            pre = pre1
            suf = suf1
            if cir:
                cir += "+ke--an"
            else:
                cir += "ke--an"
    return pre, suf, cir

# ber--an, ber--kan
def NyahApitan_b(r, pre, suf, cir, p_pre, p_suf):
    """Kembalikan sekumpulan calon apitan dan imbuhan"""
    if "ber" in pre and "an" in suf:
        pre1 = pre.replace("ber", "", 1)
        suf1 = suf.replace("an", "", 1)
        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)) and (not r.startswith("r")):
            pre = pre1
            suf = suf1
            if cir:
                cir += "+ber--an"
            else:
                cir += "ber--an"
    elif "be" in pre and "an" in suf:
        pre1 = pre.replace("be", "", 1)
        suf1 = suf.replace("an", "", 1)
        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
            pre = pre1
            pre = pre1
            suf = suf1
            if cir:
                cir += "+ber--an"
            else:
                cir += "ber--an"
    if "ber" in pre and "kan" in suf:
        pre1 = pre.replace("ber", "", 1)
        suf1 = suf.replace("kan", "", 1)
        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)) and (not r.startswith("r")):
            pre = pre1
            suf = suf1
            if cir:
                cir += "+ber--kan"
            else:
                cir += "ber--kan"
    elif "be" in pre and "kan" in suf:
        pre1 = pre.replace("be", "", 1)
        suf1 = suf.replace("kan", "", 1)
        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
            pre = pre1
            suf = suf1
            if cir:
                cir += "+ber--kan"
            else:
                cir += "ber--kan"
    return pre, suf, cir

# se--nya
def NyahApitan_s(r, pre, suf, cir, p_pre, p_suf):
    """Kembalikan sekumpulan calon apitan dan imbuhan"""
    if "se" in pre and "nya" in suf:
        pre1 = pre.replace("se", "", 1)
        suf1 = suf.replace("nya", "", 1)
        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
            pre = pre1
            suf = suf1
            if cir:
                cir += "+se--nya"
            else:
                cir += "se--nya"
    elif ("penye" in pre or "menye" in pre) and "nya" in suf:
        pre1 = pre.replace("enye", "eny", 1)
        suf1 = suf.replace("nya", "", 1)
        if (not p_pre.sub("", pre1)) and (not p_suf.sub("", suf1)):
            pre = pre1
            suf = suf1
            if cir:
                cir += "+se--nya"
            else:
                cir += "se--nya"
    return pre, suf, cir

def NyahApitan(word, rootlist, Indo = False):
    """Kembalikan sekumpulan calon apitan dan imbuhan"""
    cand = set()
    roots = Akar(word, rootlist)
    p_pre = re.compile(r"(ku|kau|be(r)?|te(r)?|me(m|n(g(e)?|y)?)?|pe(m|r|n(g(e)?|y)?)?|ke|se|di)")
    p_suf = re.compile(r"(kan|i|ku|mu|kau|nya|\-Nya|lah|kah|an)")
    if Indo:
        roots = Akar(word, rootlist, Indo = True)
        p_pre = re.compile(r"(ku|kau|be(r)?|te(r)?|me(m|n(g(e)?|y)?)?|pe(m|r|n(g(e)?|y)?)?|ke|se|di|%)")
        p_suf = re.compile(r"(kan|i(n)?|ku|mu|kau|nya|\-Nya|lah|kah|an)")
    jenis = ["p", "b", "k", "s"]
    g = list(permutations(jenis, 4)) + list(permutations(jenis, 3)) + list(permutations(jenis, 2)) + \
        list(permutations(jenis, 1))
    for c in roots:
        for item in g:
            (r, pre, suf, red) = c
            cir = ""
            for letter in item:
                if letter == "p":
                    result = NyahApitan_p(r, pre, suf, cir, p_pre, p_suf)
                elif letter == "b":
                    result = NyahApitan_b(r, pre, suf, cir, p_pre, p_suf)
                elif letter == "k":
                    result = NyahApitan_k(r, pre, suf, cir, p_pre, p_suf)
                elif letter == "s":
                    result = NyahApitan_s(r, pre, suf, cir, p_pre, p_suf)
                if result[2] and cir !=  result[2]:
                    pre = result[0]
                    suf = result[1]
                    cir = result[2]
            # kesamaan (x+y = y+z)
            cir = "+".join(sorted(cir.split("+")))
            if cir == "":
                cir = "0"
            cand.add((c, r, pre, suf, cir, red))
    return cand

# Penanggal awalan
def NyahAwalan(word, rootlist, Indo = False):
    """
    Kembalikan sekumpulan calon awalan dan imbuhan.
    @param Indo: Jika benar, awalan N- juga termasuk.
    """
    cand = set()
    roots = Akar(word, rootlist)
    p_pre = re.compile(r"(ku|kau|be(r)?|te(r)?|me(m|n(g(e)?|y)?)?|pe(m|r|n(g(e)?|y)?)?|ke|se|di)")
    if Indo:
        roots = Akar(word, rootlist, Indo = True)
        p_pre = re.compile(r"(ku|kau|be(r)?|te(r)?|me(m|n(g(e)?|y)?)?|pe(m|r|n(g(e)?|y)?)?|ke|se|di|%)")
    for c in roots:
        (r, pre, suf, red) = c
        pfx = ""
        # ku-
        if "ku" in pre:
            pre1 = pre.replace("ku", "", 1)
            if (not p_pre.sub("", pre1)):
                pre = pre1
                if pfx:
                    pfx += "+ku-"
                else:
                    pfx += "ku-"
        # kau-
        if "kau" in pre:
            pre1 = pre.replace("kau", "", 1)
            if (not p_pre.sub("", pre1)):
                pre = pre1
                if pfx:
                    pfx += "+kau-"
                else:
                    pfx += "kau-"
        # di-
        if "di" in pre:
            pre1 = pre.replace("di", "", 1)
            if (not p_pre.sub("", pre1)):
                pre = pre1
                if pfx:
                    pfx += "+di-"
                else:
                    pfx += "di-"
        # ter-
        if "ter" in pre:
            pre1 = pre.replace("ter", "", 1)
            if (not p_pre.sub("", pre1)) and (not r.startswith("r")):
                pre = pre1
                if pfx:
                    pfx += "+ter-"
                else:
                    pfx += "ter-"
        elif "te" in pre:
            pre1 = pre.replace("te", "", 1)
            if (not p_pre.sub("", pre1)):
                pre = pre1
                if pfx:
                    pfx += "+ter-"
                else:
                    pfx += "ter-"
        # ber-
        if "ber" in pre:
            pre1 = pre.replace("ber", "", 1)
            if (not p_pre.sub("", pre1)) and (not r.startswith("r")):
                pre = pre1
                if pfx:
                    pfx += "+ber-"
                else:
                    pfx += "ber-"
        elif "be" in pre:
            pre1 = pre.replace("be", "", 1)
            if (not p_pre.sub("", pre1)):
                pre = pre1
                if pfx:
                    pfx += "+ber-"
                else:
                    pfx += "ber-"
        # meN-
        if "me" in pre:
            pre1 = pre.replace("me", "", 1)
            if not p_pre.sub("", pre1):
                pre = pre1
                if pfx:
                    pfx += "+meN-"
                else:
                    pfx += "meN-"
            elif "mem" in pre:
                pre1 = pre.replace("mem", "", 1)
                if not p_pre.sub("", pre1):
                    pre = pre1
                    if pfx:
                        pfx += "+meN-"
                    else:
                        pfx += "meN-"
            elif "men" in pre:
                pre1 = pre.replace("men", "", 1)
                if not p_pre.sub("", pre1):
                    pre = pre1
                    if pfx:
                        pfx += "+meN-"
                    else:
                        pfx += "meN-"
                elif "meny" in pre:
                    pre1 = pre.replace("meny", "", 1)
                    if not p_pre.sub("", pre1):
                        pre = pre1
                        if pfx:
                            pfx += "+meN-"
                        else:
                            pfx += "meN-"
                    elif "menye" in pre: # meN- + se-
                        pre1 = pre.replace("menye", "se", 1)
                        if not p_pre.sub("", pre1):
                            pre = pre1
                            if pfx:
                                pfx += "+meN-"
                            else:
                                pfx += "meN-"
                elif "meng" in pre:
                    pre1 = pre.replace("meng", "", 1)
                    if not p_pre.sub("", pre1):
                        pre = pre1
                        if pfx:
                            pfx += "+meN-"
                        else:
                            pfx += "meN-"
                    elif "menge" in pre: # monosyllabic root or meN- + ke-(an)
                        if SylCount(r, root = True) == 1:
                            pre1 = pre.replace("menge", "", 1)
                            if not p_pre.sub("", pre1):
                                pre = pre1
                                if pfx:
                                    pfx += "+meN-"
                                else:
                                    pfx += "meN-"
                        else:
                            pre1 = pre.replace("menge", "ke", 1)
                            if not p_pre.sub("", pre1):
                                pre = pre1
                                if pfx:
                                    pfx += "+meN-"
                                else:
                                    pfx += "meN-"
        # N-
        if Indo and "%" in pre:
            pre1 = pre.replace("%", "", 1)
            if not p_pre.sub("", pre1):
                pre = pre1
                if pfx:
                    pfx += "+N-"
                else:
                    pfx += "N-"
        # peN-, pe-, per-
        if "pe" in pre:
            pre1 = pre.replace("pe", "", 1)
            if not p_pre.sub("", pre1):
                pre = pre1
                if r.startswith("r"):
                    if pfx:
                        pfx += "+peN-@pe-@per-"
                    else:
                        pfx += "peN-@pe-@per-"
                else:
                    if pfx:
                        pfx += "+peN-@pe-"
                    else:
                        pfx += "peN-@pe-"
            elif "pem" in pre:
                pre1 = pre.replace("pem", "", 1)
                if not p_pre.sub("", pre1):
                    pre = pre1
                    if pfx:
                        pfx += "+peN-"
                    else:
                        pfx += "peN-"
            elif "per" in pre:
                pre1 = pre.replace("per", "", 1)
                if not p_pre.sub("", pre1):
                    pre = pre1
                    if pfx:
                        pfx += "+per-"
                    else:
                        pfx += "per-"
            elif "pen" in pre:
                pre1 = pre.replace("pen", "", 1)
                if not p_pre.sub("", pre1):
                    pre = pre1
                    if pfx:
                        pfx += "+peN-"
                    else:
                        pfx += "peN-"
                elif "peny" in pre:
                    pre1 = pre.replace("peny", "", 1)
                    if not p_pre.sub("", pre1):
                        pre = pre1
                        if pfx:
                            pfx += "+peN-"
                        else:
                            pfx += "peN-"
                    elif "penye" in pre: # peN- + se-
                        pre1 = pre.replace("penye", "se", 1)
                        if not p_pre.sub("", pre1):
                            pre = pre1
                            if pfx:
                                pfx += "+peN-"
                            else:
                                pfx += "peN-"
                elif "peng" in pre:
                    pre1 = pre.replace("peng", "", 1)
                    if not p_pre.sub("", pre1):
                        pre = pre1
                        if pfx:
                            pfx += "+peN-"
                        else:
                            pfx += "peN-"
                    elif "penge" in pre: # monosyllabic root or peN- + ke-(an)
                        if SylCount(r, root = True) == 1:
                            pre1 = pre.replace("penge", "", 1)
                            if not p_pre.sub("", pre1):
                                pre = pre1
                                if pfx:
                                    pfx += "+peN-"
                                else:
                                    pfx += "peN-"
                        else:
                            pre1 = pre.replace("penge", "ke", 1)
                            if not p_pre.sub("", pre1):
                                pre = pre1
                                if pfx:
                                    pfx += "+peN-"
                                else:
                                    pfx += "peN-"
        # ke-
        if "ke" in pre:
            pre1 = pre.replace("ke", "", 1)
            if not p_pre.sub("", pre1):
                pre = pre1
                if pfx:
                    pfx += "+ke-"
                else:
                    pfx += "ke-"
        elif "menge" in pre or "penge" in pre:
            pre1 = pre.replace("enge", "eng", 1)
            if not p_pre.sub("", pre1):
                pre = pre1
                if pfx:
                    pfx += "+ke-"
                else:
                    pfx += "ke-"
        # se-
        if "se" in pre:
            pre1 = pre.replace("se", "", 1)
            if (not p_pre.sub("", pre1)):
                pre = pre1
                if pfx:
                    pfx += "+se-"
                else:
                    pfx += "se-"
        elif "menye" in pre or "penye" in pre:
            pre1 = pre.replace("enye", "eny", 1)
            if (not p_pre.sub("", pre1)):
                pre = pre1
                if pfx:
                    pfx += "+se-"
                else:
                    pfx += "se-"
        # kesamaan (x+y = y+z)
        pfx = "+".join(sorted(pfx.split("+")))
        if pfx == "":
            pfx = "0"
        cand.add((c, r, pre, suf, pfx, red))
    return cand

# Penanggal akhiran
def NyahAkhiran(word, rootlist, Indo = False):
    """
    Kembalikan sekumpulan calon akhiran dan imbuhan.
    @param Indo: Jika benar, akhiran -in juga termasuk.
    """
    cand = set()
    roots = Akar(word, rootlist)
    p_suf = re.compile(r"(kan|i|ku|mu|kau|nya|\-Nya|lah|kah|an)")
    if Indo:
        roots = Akar(word, rootlist, Indo = True)
        p_suf = re.compile(r"(kan|i(n)?|ku|mu|kau|nya|\-Nya|lah|kah|an)")
    for c in roots:
        (r, pre, suf, red) = c
        sfx = ""
        # -an
        if "an" in suf:
            suf1 = suf.replace("an", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-an"
                else:
                    sfx += "-an"
        # -i
        if "i" in suf:
            suf1 = suf.replace("i", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-i"
                else:
                    sfx += "-i"
        # -kan
        if "kan" in suf:
            suf1 = suf.replace("kan", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-kan"
                else:
                    sfx += "-kan"
        # -in
        if Indo and "in" in suf:
            suf1 = suf.replace("in", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-in"
                else:
                    sfx += "-in"
        # -ku
        if "ku" in suf:
            suf1 = suf.replace("ku", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-ku"
                else:
                    sfx += "-ku"
        # -mu
        if "mu" in suf:
            suf1 = suf.replace("mu", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-mu"
                else:
                    sfx += "-mu"
        # -kau
        if "kau" in suf:
            suf1 = suf.replace("kau", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-kau"
                else:
                    sfx += "-kau"
        # -nya
        if "nya" in suf:
            suf1 = suf.replace("nya", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-nya"
                else:
                    sfx += "-nya"
        # -Nya
        if "Nya" in suf:
            suf1 = suf.replace("Nya", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-Nya"
                else:
                    sfx += "-Nya"
        # -lah
        if "lah" in suf:
            suf1 = suf.replace("lah", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-lah"
                else:
                    sfx += "-lah"
        # -kah
        if "kah" in suf:
            suf1 = suf.replace("kah", "", 1)
            if not p_suf.sub("", suf1):
                suf = suf1
                if sfx:
                    sfx += "+-kah"
                else:
                    sfx += "-kah"
        # kesamaan (x+y = y+z)
        sfx = "+".join(sorted(sfx.split("+")))
        if sfx == "":
            sfx = "0"
        cand.add((c, r, pre, suf, sfx, red))
    return cand

def morph(word, rootlist, Indo = False, n = 5):
    """
    Bagi sesuatu perkataan ("word"), kembalikan n analisis morphologi yang paling mungkin berdasarkan 
    senarai akar ("rootlist").
    Format output: akar, perkataan, proklitik/awalan, akhiran/enklitik, apitan, reduplikasi
    @param Indo: Jika benar, awalan N- dan akhiran -in juga termasuk dalam analisis.
    @param n: Bilangan calon yang dikembalikan.
    """
    cand = set()
    check = set()
    cand1 = NyahApitan(word, rootlist)
    cand2 = NyahAwalan(word, rootlist)
    cand3 = NyahAkhiran(word, rootlist)
    if Indo:
        cand1 = NyahApitan(word, rootlist, Indo = True)
        cand2 = NyahAwalan(word, rootlist, Indo = True)
        cand3 = NyahAkhiran(word, rootlist, Indo = True)

    # Tanpa imbuhan
    for (c1, c2, c3) in [(c1, c2, c3) for c1 in cand1 for c2 in cand2 for c3 in cand3]:
        if c1[0] == c2[0] == c3[0]  and (c1[4], c2[4], c3[4]) == ("0", "0", "0"):
                cand.add((c1[0], c1[1], "0", "0", "0", c1[5]))
    # Dengan imbuhan
    else:
        for c1 in cand1:
            # Tanpa awalan, tanpa akhiran
            if not c1[2] and not c1[3]:
                cand.add((c1[0], c1[1], "0", "0", c1[4], c1[5]))
            # Tanpa awalan
            elif not c1[2]:
                temp = c1[1] + c1[3] # bentuk tanpa huruf-huruf apitan
                cand3c = NyahAkhiran(temp, rootlist)
                if Indo:
                    cand3c = NyahAkhiran(temp, rootlist, Indo = True)
                for c3 in cand3c:
                    if c1[1] == c3[0][0] and c1[3] == c3[0][2] and not c3[3]:
                        cand.add((c1[0], c1[1], "0", c3[4], c1[4], c1[5]))
            # Tanpa akhiran
            elif not c1[3]:
                temp = c1[2] + c1[1] # bentuk tanpa huruf-huruf apitan
                cand2c = NyahAwalan(temp, rootlist)
                if Indo:
                    cand2c = NyahAwalan(temp, rootlist, Indo = True)
                for c2 in cand2c:
                    if c1[1] == c2[0][0] and c1[2] == c2[0][1] and not c2[2]:
                        cand.add((c1[0], c1[1], c2[4], "0", c1[4], c1[5]))
            # Dengan awalan dan akhiran
            else:
                temp = c1[2] + c1[1] + c1[3] # bentuk tanpa huruf-huruf apitan
                cand2c = NyahAwalan(temp, rootlist)
                cand3c = NyahAkhiran(temp, rootlist)
                if Indo:
                    cand2c = NyahAwalan(temp, rootlist, Indo = True)
                    cand3c = NyahAkhiran(temp, rootlist, Indo = True)
                for c2 in cand2c:
                    if c1[1] == c2[0][0] and c1[2] == c2[0][1] and not c2[2]:# and c1[3] == c2[0][2]:
                        for c3 in cand3c:
                            if c1[1] == c3[0][0] and c1[3] == c3[0][2] and not c3[3]:
                                cand.add((c1[0], c1[1], c2[4], c3[4], c1[4], c1[5]))
    # Utamakan akar yang sedia ada
    cand4 = set([c for c in cand if c[1] in rootlist])
    if cand4:
        cand = cand4
    # Jika tiada analisis ditemui, cuba dengan huruf kecil
    if not cand:
        if not word.islower():
            kecil = morph(word.lower(), rootlist)
            for k in kecil:
                check.add((k[0], word, k[2], k[3], k[4], k[5]))
        else:
            check.add((word, word, "0", "0", "0", c1[5]))
    # Susun mengikut jumlah suku kata (2 > 3 > 1 > 4 ...) dan panjang akar
    cand = sorted(cand, key = lambda x: SylCount(x[1], root = True, mono = True) + len(x[1])/100)
    # Tambah 5 hasil yang paling besar kemungkinannnya kepada senarai semak
    for c in cand[:n]:
        check.add((c[1], word, c[2], c[3], c[4], c[5]))
    return check

if __name__ == "__main__":
    print("Sedang memproses kamus dan senarai akar...")
#    with codecs.open("kamus.pkl", "r", "utf-8") as f:
    with open("kamus.pkl", "rb") as f:
        kamus = load(f)
#    with codecs.open("kamus_hyp.pkl", "r", "utf-8") as f:
    with open("kamus_hyp.pkl", "rb") as f:
        kamus_hyp = load(f)
#    with codecs.open("rootlist.pkl", "r", "utf-8") as f:
    with open("rootlist.pkl", "rb") as f:
        rootlist = load(f)

# Input dari sini
    # Senarai perkataan untuk dianalisis
    tokens = """
    ngopi
    ngapaan
    ngapain
    cas-cis-cus-nya
    cas-cis-cus-Nya
    yield
    teikyo
    seniri
    meman-dang
    Me
    Makanan
    Biaya-biaya
    Bid'ah
    Kupertahankan
    ST-12
    ke-12
    0%
    pengerarapanan
    penyerarapannya
    keberapaannya
    mempertahankan pertahankan mempertahankanlah kupertahankan kumempertahankan
    dipertahankan kupertahankanlah dipertahankan-Nya dipertahankan-Nyalah
    kuku kukuku kukukuku kukukukuku
    menyorong-nyorong kumemadamkan kumembaca kumenakutkan kumentafsirkan kumengonggong kumenggonggong kumengomel
    keberapakannya
    kebeapakannya
    keberaprapanankan
    penyearapanan
    pengerapanan
    berarapan
    berrarapan
    dipengarrapikannya
    dipengarrapikan
    berukurran
    berpembunttuanan
    keberkaitanan
    cas-cis-cus
    kausayang-menyayangi
    nyorong-menyorong
    memukul-mukulnya
    aanap-kaanap-nya
    aanap-kaanapnya
    pengearapanan
    kebersebelahanan
    Indonesia-Melanesia
    mobil-mobil-nya
    mobil-mobil-Nya
    1990-an
    90-an
    aanap-kaanap
    safwe-fdle
    caci-maki
    lauk-vauk
    lauki-vauki
    tunggang-danggang
    gunung-genang
    adik-beradik-nya
    """.split()

# Input dari fail
#    reload(sys)
#    sys.setdefaultencoding("utf-8")
#    #sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
#    #sys.stdin = codecs.getreader("utf-8")(sys.stdin)
#
#    # Senarai perkataan untuk dianalisis
#    tokens = set()
#    with codecs.open("./malindo_conc_corpus.freq2_diff/ind_freq2_7.txt") as fh:
##    with codecs.open("./malindo_conc_corpus.freq2_diff/fail_ind9.txt") as fh:
##    --- Failed because the XXfreq2 files were made based on an older version of morphdict
#        for l in fh:
#            t = l.strip()
#            tokens.add(t)

    # Bentuk sedia ada atau bentuk hipotetikal + klitik
    tambah = set() # nama set ini dulu adalah "add" (diubah 2/1/2018)
    # Bukan abjad, cth. 10.0%
    nonalph = set()
    # Perkataan bahasa Inggeris
    eng = set()
#    d = enchant.Dict("en_US")
    d = SpellChecker()
    # Lain-lain
    belum = set()
    p_nonalph = re.compile(r"^[0-9|\-|,|.|%|$|']+$")

    print("Sedang memproses kata...")
    for token in tokens:
#        print(token + ": ", end = "")
        # Bukan abjad
        if p_nonalph.match(token):
            nonalph.add((token, token, "0", "0", "0", "0"))
#            print("Bukan abjad")
        # Semak sama ada kata itu sudah ada dalam morphdic-core
        elif not token in kamus:
            lower = token.lower()
            if lower in kamus:
                for val in kamus[lower]:
                    tambah.add((val[0], token, val[1], val[2], val[3], val[4]))
#                    print("kamus")
            elif token in kamus_hyp:
                for val in kamus_hyp[token]:
                    tambah.add((val[0], token, val[1], val[2], val[3], val[4]))
#                    print("kamus_hyp")
            elif lower in kamus_hyp:
                for val in kamus_hyp[lower]:
                    tambah.add((val[0], token, val[1], val[2], val[3], val[4]))
#                    print("kamus_hyp")
            else:
                # Buang kedua-dua pro- dan enklitik (Andaian: Proklitik hanya dibubuh kepada bentuk asas ("basic").)
                (stem1, en) = NyahEnklitik(lower)
                (stem2, pro_en) = NyahProklitik(stem1)
                (stem3, pro) = NyahProklitik(lower)
                if en and pro_en and stem1 not in kamus and stem2 in kamus_hyp:
                    for val in kamus_hyp[stem2]:
                        if val[1] == "0" and val[2] == "0":
                            tambah.add((val[0], token, pro_en, en, val[3], val[4]))
                        elif val[1] == "0":
                            tambah.add((val[0], token, pro_en, val[2]+"+"+en, val[3], val[4]))
                        elif val[2] == "0":
                            tambah.add((val[0], token, pro_en+"+"+val[1], en, val[3], val[4]))
                        else:
                            tambah.add((val[0], token, pro_en+"+"+val[1], val[2]+"+"+en, val[3], val[4]))
#                        print("kamus_hyp + proklitik + enklitik")
                elif en:
                    if stem1 in kamus:
                        for val in kamus[stem1]:
                            if val[2] == "0":
                                tambah.add((val[0], token, val[1], en, val[3], val[4]))
                            else:
                                tambah.add((val[0], token, val[1], val[2]+"+"+en, val[3], val[4]))
#                            print("kamus + enklitik")
                    elif stem1 in kamus_hyp:
                        for val in kamus_hyp[stem1]:
                            if val[2] == "0":
                                tambah.add((val[0], token, val[1], en, val[3], val[4]))
                            else:
                                tambah.add((val[0], token, val[1], val[2]+"+"+en, val[3], val[4]))
#                            print("kamus_hyp + enklitik")
                    else:
                        belum.add(token)
#                        print("Buatlah analisis serius!")
                elif pro and stem3 in kamus_hyp:
                    for val in kamus_hyp[stem3]:
                        if val[1] == "0":
                            tambah.add((val[0], token, pro, val[2], val[3], val[4]))
                        else:
                            tambah.add((val[0], token, pro+"+"+val[1], val[2], val[3], val[4]))
#                        print("kamus_hyp + proklitik")
                # Perkataan bahasa Inggeris
#                elif d.check(token):
                elif d.unknown([token]):
                    eng.add((token, token, "0", "0", "0", "0"))
#                    print("Perkataan bahasa Inggeris")
                else:
                    belum.add(token)
#                    print("Buatlah analisis serius!")
#        else:
#                print("kamus")

# Output ke skrin
    print("Tambah:", tambah)
    print("Bukan abjad:", nonalph)
    print("Bahasa Inggeris:", eng)
    print("Belum:", belum)
    for word in belum:
        print(word)
        for (bil, i) in enumerate(morph(word, rootlist, Indo = True)):
            bil += 1
            print("{0:>2}.\t{1[0]:<15}{1[1]:<20}{1[2]:<15}{1[3]:<15}{1[4]:<15}{1[5]:<15}".format(bil, i))

# Output ke fail
#    # Bentuk sedia ada atau bentuk hipotetikal + klitik -> tidak perlu disemak manusia, tambah saja
#    with codecs.open("add.tsv", "w", "utf-8") as f:
#        for i in tambah:
#            print("\t".join([i[0], i[1], i[2], i[3], i[4], i[5]]), file = f)
#    # Bukan abjad, cth. 10.0% -> tidak perlu disemak manusia, tambah saja
#    with codecs.open("nonalph.tsv", "w", "utf-8") as f:
#        for i in nonalph:
#            print("\t".join([i[0], i[1], i[2], i[3], i[4], i[5]]), file = f)
#    # Perkataan bahasa Inggeris ->  tidak perlu disemak manusia, tambah saja
#    with codecs.open("eng.tsv", "w", "utf-8") as f:
#        for i in eng:
#            print("\t".join([i[0], i[1], i[2], i[3], i[4], i[5]]), file = f)
#    # Lain-lain -> perlu disemak manusia
#    check = set()
#    for word in belum:
##        print(word)
##        for i in morph(word, rootlist):
#        for i in morph(word, rootlist, Indo = True):
#            check.add("\t".join([i[0], i[1], i[2], i[3], i[4], i[5]]))
#    with codecs.open("check.tsv", "w", "utf-8") as f:
#        for i in check:
#            print(i, file = f)
#
#    print("Selesai!")
