#!/usr/bin/env python
from __future__ import nested_scopes
__version__="2.0"
import re
import MontyUtils

class MontyLemmatiser(object):
    path_prefix=''
    xtag_morph_english_corpus=path_prefix+'xtag_morph_english.txt'
    exceptions_file="LEMMAEXCEPTIONS.MDF"
    regular_any=[]
    regular_verb=[]
    regular_noun=[]
    irregular_re_any=[]
    irregular_re_verbs=[]
    irregular_re_nouns=[]
    irregular_verbs=[]
    irregular_nouns=[]
    irregular_nouns +=[('vegas','vegas',''),('tomatoes','tomato','s'),\
	('potatoes','potato','s'),('Asia','Asia',''),('asia','asia',''),\
	('media','media',''),('Media','Media',''),('California','California',''),\
	('california','california',''),('leaves','leaf','s'),('acme','acme',''),\
	('gloria','gloria',''),('mini','mini',''),('doggies','doggy','s'),\
	('Chianti','Chianti',''),('briefs','brief','s'),('wives','wife','s'),\
	('johannes','johannes',''),('tops','top','s'),('deadeyes','deadeye','s'),\
	('eyes','eye','s'),('alumnae','alumnus','s'),('acropolis','acropolis',''),\
	('metropolis','metropolis',''),('stamens','stamen','s'),]
    irregular_verbs +=[('leaves','leave',''),('does','do',''),('alibiing',\
	'alibii','ing'),('snorkeling','snorkel','ing'),('gaping','gape','ing'),\
	('siting','site','ing'),('chequering','chequer','ing'),('restring','restring','')]

    def __init__(self):
        filename_str=[self.regular_any,self.regular_verb,self.regular_noun,\
		self.irregular_re_any,self.irregular_re_verbs,self.irregular_re_nouns]
        self.regular_any,self.regular_verb,self.regular_noun,\
		self.irregular_re_any,self.irregular_re_verbs,self.irregular_re_nouns=\
		map(lambda the_tokenizers:map(lambda the_tokenizer_str:[\
		re.compile('^'+the_tokenizer_str[0].lower()+'$')]+the_tokenizer_str[1:],\
		the_tokenizers),filename_str)
        self.exceptions_db={}
        hostname_cleaned=self.exceptions_db
        c=self.setitem
        buffers=MontyUtils.MontyUtils().find_file(self.exceptions_file)
        pathname_str=open(buffers,'r')
        cd_cleaned=map(lambda the_tokenizer_str:the_tokenizer_str.split(),\
		pathname_str.read().split('\n'))
        pathname_str.close()
        map(lambda the_tokenizer_str:c(hostname_cleaned,the_tokenizer_str[0]+\
		'/'+the_tokenizer_str[1],the_tokenizer_str[2]),cd_cleaned)
        print "Lemmatiser OK!"
        return

    def lemmatise_untagged_sentence(self,untagged):
        the_parser_dict=' '.join(map(lambda the_tokenizer_str:the_tokenizer_str+\
		'/UNK',untagged.split()))
        return self.lemmatise_tagged_sentence(the_parser_dict)

    def lemmatise_tagged_sentence(self,tagged):
        cmp=self.lemmatise_word
        domain_str=map(lambda the_tokenizer_str:the_tokenizer_str.split('/'),tagged.split())

        for popds in range(len(domain_str)):
            j,cksum_str=domain_str[popds]
            _hugo_cleaned=""

            if cksum_str in['NN','NNS','NNP','NNPS']:
                _hugo_cleaned='noun'
            elif cksum_str in['VB','VBD','VBZ','VBG','VBP','VBN']:
                _hugo_cleaned='verb'

            if _hugo_cleaned=='':
                command1=j
            else :
                command1=cmp(j,_hugo_cleaned)
            domain_str[popds]=[j,cksum_str,command1]
        domain_str=map(lambda the_tokenizer_str:'/'.join(the_tokenizer_str),domain_str)
        cal=' '.join(domain_str)
        return cal

    def lemmatise_word(self,word,pos=""):
        the_parser=self.fix_case

        if word[-2:]=="'s":
            word=word[:-2]
        elif word[-2:]=="s'":
            word=word[:-1]
        cron_dictr=self.check_dictionary_exceptions(word,pos)

        if cron_dictr!=None:
            chown,cd_cleanedo=cron_dictr
            chown=the_parser(word,chown)
            return chown
        cron_dictr=self.find_irregular_morph(word,pos)

        if cron_dictr!=None:
            chown,cd_cleanedo=cron_dictr
            chown=the_parser(word,chown)
            return chown
        cron_dictr=self.find_regular_morph(word,pos)

        if cron_dictr!=None:
            chown,cd_cleanedo=cron_dictr
            chown=the_parser(word,chown)
            return chown
        return word

    def verify_lemmatiser(self):
        arg_cleaned=[]
        print "LOADING verification corpus"
        dict=self.make_verification_dictionary()
        print 'verifying against',len(dict),'entries'
        built_in_dict=0

        for chmod_pq in dict:
            j,command1,chmod_cleaned=chmod_pq

            if chmod_cleaned in['PropN']:
                chmod_cleaned='noun'
            elif chmod_cleaned in['V']:
                chmod_cleaned='verb'
            else :
                continue
            file_cleaned=self.lemmatise_word(j,chmod_cleaned)

            if file_cleaned!=command1:
                built_in_dict += 1
                print 'WRONG! WORD: '+j+' GUESSED: '+file_cleaned+' ACTUAL: '+command1
                arg_cleaned.append([j,chmod_cleaned,command1])

                if j!=j.lower():
                    arg_cleaned.append([j.lower(),chmod_cleaned,command1.lower()])
            else :
                pass
        print 'Results: got',built_in_dict,'out of',len(dict),'wrong (',\
		built_in_dict*1.0/len(dict),'% error)'
        pathname_str=open(self.exceptions_file,'w')
        pathname_str.write('\n'.join(map(lambda the_tokenizer_str:' '.join(\
		the_tokenizer_str),arg_cleaned)))
        pathname_str.close()
        return arg_cleaned

    def make_verification_dictionary(self):
        pathname_str=open(self.xtag_morph_english_corpus,'r')
        output=pathname_str.read()
        factor=output.split('\n')
        factor=filter(lambda the_tokenizer_str:the_tokenizer_str[:3]!=';;;',factor)
        factor=map(lambda the_tokenizer_str:the_tokenizer_str.split(),factor)
        factor=filter(lambda the_tokenizer_str:len(the_tokenizer_str)>=3,factor)
        factor=map(lambda the_tokenizer_str:[the_tokenizer_str[0],\
		the_tokenizer_str[1],the_tokenizer_str[2]],factor)
        factor=filter(lambda the_tokenizer_str:the_tokenizer_str[1][-3:]!=\
		'ize' and the_tokenizer_str[1][-7:]!='ization' \
		and the_tokenizer_str[1][4:]!='izer' and '-' not in the_tokenizer_str[1],factor)
        return factor

    def fix_case(self,word1,word2):

        if word1.lower()==word1:
            return word2.lower()
        elif word1.capitalize()==word1:
            return word2.capitalize()
        elif word1.upper()==word1:
            return word2.upper()
        else :
            return word2

    def _re_match_helper(self,re_kb,word):

        for popds in range(len(re_kb)):
            buf1,file_str,buffer1,cd_cleanedo=re_kb[popds]
            pairs_cleaned=buf1.search(word.lower())

            if pairs_cleaned!=None:
                chown=word[:len(word)-file_str]+buffer1
                return[chown,cd_cleanedo]
        return None

    def find_irregular_morph(self,word,pos=""):
        a1=self._re_match_helper
        groupnames1=self.find_irregular_morph
        cron_dictr=a1(self.irregular_re_any,word)

        if cron_dictr!=None:
            return cron_dictr

        if pos=='verb':
            cron_dictr=a1(self.irregular_re_verbs,word)

            if cron_dictr!=None:
                return cron_dictr
        elif pos=='noun':
            cron_dictr=a1(self.irregular_re_nouns,word)

            if cron_dictr!=None:
                return cron_dictr
        else :
            cron_dictr=groupnames1(word,'verb')

            if cron_dictr!=None:
                return cron_dictr
            cron_dictr=groupnames1(word,'noun')
            return cron_dictr
        return None

    def find_regular_morph(self,word,pos=""):
        a1=self._re_match_helper
        history1=self.find_regular_morph
        info_arr=word.lower()

        if pos=='verb':
            cron_dictr=a1(self.regular_verb,info_arr)

            if cron_dictr!=None:
                return cron_dictr
        elif pos=='noun':
            cron_dictr=a1(self.regular_noun,info_arr)

            if cron_dictr!=None:
                return cron_dictr
        else :
            cron_dictr=history1(word,'verb')

            if cron_dictr!=None:
                return cron_dictr
            cron_dictr=history1(word,'noun')
            return cron_dictr
        cron_dictr=a1(self.regular_any,info_arr)

        if cron_dictr!=None:
            return cron_dictr
        return None

    def check_dictionary_exceptions(self,word,pos=""):
        hostname_cleaned=self.exceptions_db
        contents_str=self.check_dictionary_exceptions
        info_arr=word.lower()

        if pos=="verb":
            built_in_cleaned=map(lambda the_tokenizer_str:the_tokenizer_str[0],\
			self.irregular_verbs)

            if info_arr in built_in_cleaned:
                hostname_arr=built_in_cleaned.index(info_arr)
                chown_p=self.irregular_verbs[hostname_arr]
                return chown_p[1:3]
            elif hostname_cleaned.get(word+'/verb',''):
                return[hostname_cleaned[word+'/verb'],'']
            else :
                return None
        elif pos=="noun":
            pairs_dict=map(lambda the_tokenizer_str:the_tokenizer_str[0],\
			self.irregular_nouns)

            if info_arr in pairs_dict:
                hostname_arr=pairs_dict.index(info_arr)
                chown_p=self.irregular_nouns[hostname_arr]
                return chown_p[1:3]
            elif hostname_cleaned.get(word+'/noun',''):
                return[hostname_cleaned[word+'/noun'],'']
            else :
                return None
        else :
            cron_dictr=contents_str(word,'verb')

            if cron_dictr==None:
                cron_dictr=contents_str(word,'noun')
            return cron_dictr
    V='[aeiou]'
    VI='[aeiouy]'
    C='[bcdfghjklmnpqrstvwxyz]'
    CX='[bcdfghjklmnpqrstvwxz]'
    CX2='(bb|cc|dd|ff|gg|hh|jj|kk|ll|mm|nn|pp|qq|rr|ss|tt|vv|ww|xx|zz)'
    CX2S='(ff|ss|zz)'
    S='([sx]|([cs]h))'
    A='[^ \n_]'
    SKIP='[ \n]'
    EDING='ed|ing'
    ESEDING='es|ed|ing'
    regular_any +=[[A+'+'+CX2S+'es',2,'','s'],[A+'+'+'thes',1,'','s'],\
	[A+'+'+CX+'[cglsv]'+'es',1,'','s'],[A+'+'+CX+CX+'es',2,'','s'],\
	[A+'+'+VI+VI+'es',2,'','s'],[A+'+'+'xes',2,'','s'],[A+'+'+S+'es',1,'','s'],\
	[A+'+'+C+'ies',3,'y','s'],[A+'+'+'s',1,'','s']]
    regular_verb +=[[A+'+'+'vened',1,'','ed'],[CX+'ed',0,'',''],[C+V+\
	'nged',2,'','ed'],[A+'+'+'icked',2,'','ed'],[A+'+'+CX2S+'ed',2,'','ed'],\
	[C+'+'+V+'lled',2,'','ed'],[A+'*'+C+'ined',1,'','ed'],[A+'*'+C+V+'[npwx]'+\
	'ed',2,'','ed'],[A+'*'+C+V+CX2+'ed',3,'','ed'],[A+'+'+C+'ied',3,'y','ed'],\
	[A+'*'+'qu'+V+C+'ed',1,'','ed'],[A+'+'+'u'+V+'ded',1,'','ed'],\
	[A+'+'+'[ei]'+'ted',2,'','ed'],[A+'+'+'[eo]'+'ated',2,'','ed'],\
	[A+'+'+V+'ated',1,'','ed'],[A+'*'+V+V+'[cgsvz]'+'ed',1,'','ed'],\
	[A+'*'+V+V+C+'ed',2,'','ed'],[A+'+'+'[rw]'+'led',2,'','ed'],\
	[A+'+'+'thed',1,'','ed'],[A+'+'+CX+'[cglsv]'+'ed',1,'','ed'],\
	[A+'+'+CX+CX+'ed',2,'','ed'],[A+'+'+VI+VI+'ed',2,'','ed'],\
	[A+'*'+C+'[clt]'+'ored',1,'','ed'],[A+'+'+'[eo]'+'red',2,'','ed'],\
	[A+'+'+'ed',1,'','ed'],[CX+'+'+'ing',0,'',''],[C+V+'nging',3,'','ing'],\
	[A+'+'+'icking',3,'','ing'],[A+'+'+CX2S+'ing',3,'','ing'],\
	[C+'+'+V+'lling',3,'','ing'],[A+'*'+C+'ining',3,'e','ing'],[A+'*'+C+V+'[npwx]'\
	+'ing',3,'','ing'],[A+'*'+C+V+CX2+'ing',4,'','ing'],[A+'*'+'qu'+V+C+'ing',\
	3,'e','ing'],[A+'+'+'u'+V+'ding',3,'e','ing'],[A+'+'+'[ei]'+'ting',3,'','ing'],\
	[A+'+'+'[eo]'+'ating',3,'','ing'],[A+'+'+V+'ating',3,'e','ing'],[A+'*'+V+V+\
	'[cgsvz]'+'ing',3,'e','ing'],[A+'*'+V+V+C+'ing',3,'','ing'],[A+'+'+'[rw]'+\
	'ling',3,'','ing'],[A+'+'+'thing',3,'e','ing'],[A+'+'+CX+'[cglsv]'+'ing',3,\
	'e','ing'],[A+'+'+CX+CX+'ing',3,'','ing'],[A+'+'+VI+VI+'ing',3,'','ing'],\
	[C+'ying',4,'ie','ing'],[A+'+'+'ying',3,'','ing'],[A+'*'+CX+'oing',3,'','ing'],\
	[A+'*'+C+'[clt]'+'oring',3,'e','ing'],[A+'+'+'[eo]'+'ring',3,'','ing'],\
	[A+'+'+'(el)'+'ing',3,'','ing'],[A+'+'+'ing',3,'e','ing']]
    regular_verb +=[[A+'+'+'uses',2,'','s'],[A+'+'+'used',2,'','ed'],[A+'+'+'using',3,\
	'','ing']]
    regular_noun +=[[A+'+'+'uses',2,'','s']]
    regular_noun +=[[A+'*'+'men',2,'an','s'],[A+'*'+'wives',3,'fe','s'],\
	[A+'+'+'zoa',1,'on','s'],[A+'+'+'iia',2,'um','s'],[A+'+'+'la',1,'um','s'],\
	[A+'+'+'ae',1,'','s'],[A+'+'+'ata',2,'','s']]
    irregular_re_any +=[['(his|hers|theirs|ours|yours|as|its|this|during|something|\
	nothing|anything|everything|('+A+'+(us|ss|sis|eed)))',0,'','']]
    irregular_re_verbs +=[['bias',0,'',''],['canvas',0,'',''],['canvas'+'(es)',2,'','s'],\
	['canvas'+'(ing)',3,'','ing'],['canvas'+'(ed)',2,'','ed'],['cryed',2,'','ed'],\
	['embed',0,'',''],['focuss'+'(es)',3,'','s'],['focuss'+'(ing)',4,'','ing'],\
	['focuss'+'(ed)',3,'','ed'],['forted',2,'e','ed'],['forteing',3,'','ing'],\
	['gas',0,'',''],['picknicks',2,'','s'],['picknick'+'(ing)',4,'','ing'],\
	['picknick'+'(ed)',3,'','ed'],['resold',3,'ell','ed'],['retold',3,'ell','ed'],\
	['retying',4,'ie','ing'],['singed',2,'e','ed'],['singeing',3,'','ing'],\
	['trecked',4,'k','ed'],['trecking',5,'k','ing'],['(adher|ador|attun|bast|bor|\
	bronz|can|centr|cit|compet|complet|concret|condon|contraven|conven|cran|delet|\
	delineat|dop|drap|dron|escap|excit|fort|gazett|grop|hon|ignit|ignor|incit|\
	interven|inton|invit|landscap|manoeuvr|nauseat|normalis|outmanoeuvr|overaw|\
	permeat|persever|por|postpon|prun|recit|reshap|rop|shap|shor|snor|ston|wip)'\
	+'(es)',2,'e','s'],['(adher|ador|attun|bast|bor|bronz|can|centr|cit|compet|\
	complet|concret|condon|contraven|conven|cran|delet|delineat|dop|drap|dron|\
	escap|excit|fort|gazett|grop|hon|ignit|ignor|incit|interven|inton|invit|\
	landscap|manoeuvr|nauseat|normalis|outmanoeuvr|overaw|permeat|persever|por|\
	postpon|prun|recit|reshap|rop|shap|shor|snor|ston|wip)'+'(ed)',2,'e','ed'],\
	['(adher|ador|attun|bast|bor|bronz|can|centr|cit|compet|complet|concret|\
	condon|contraven|conven|cran|delet|delineat|dop|drap|dron|escap|excit|\
	fort|gazett|grop|hon|ignit|ignor|incit|interven|inton|invit|landscap|\
	manoeuvr|nauseat|normalis|outmanoeuvr|overaw|permeat|persever|por|\
	postpon|prun|recit|reshap|rop|shap|shor|snor|ston|wip)'+'(ing)',3,'e','ing'],\
	['(ape|appall|augur|belong|berth|burr|conquer|egg|enroll|enthrall|forestall|\
	froth|fulfill|install|instill|lacquer|martyr|mouth|murmur|pivot|preceed|prolong\
	|purr|quell|recall|refill|remill|resell|retell|smooth|throng|twang|unearth)'\
	+'(ed)',2,'','ed'],['(ape|appall|augur|belong|berth|burr|conquer|egg|enroll|\
	enthrall|forestall|froth|fulfill|install|instill|lacquer|martyr|mouth|murmur|\
	pivot|preceed|prolong|purr|quell|recall|refill|remill|resell|retell|smooth|\
	throng|twang|unearth)'+'(ing)',3,'','ing']]
    irregular_re_nouns +=[['canvases',2,'','s'],['carcases',2,'','s'],['lenses',2,'','s'],\
	['schizophrenia',0,'',''],['(('+A+'*'+'metre'+')|('+A+'*'+'litre'+')|('+A+'+'+'ette'+')|\
	'+'acre|Aussie|bronze|budgie|burnurn|canoe|carriageway|catastrophe|centre|cill|cliche|\
	commie|coolie|curie|demesne|employee|evacuee|fibre|foe|headache|horde|magpie|manoeuvre|\
	moggie|moustache|movie|nightie|oboe|programme|queue|sabre|shoe|sloe|sortie|taste|\
	theatre|timbre|titre|umbrella|utopia|wiseacre|woe)'+'(s)',1,'','s'],[\
	'(('+A+'+'+'itis'+')|'+'abdomen|achimenes|acumen|Afrikaans|alibi|alkali|\
	amnesia|anaesthesia|aphis|aria|asbestos|asphyxia|atlas|axis|bedclothes|\
	begonia|bias|bikini|calyptopis|cannula|cantharides|canvas|caries|chas|\
	chamois|chaos|chili|chinchilla|Christmas|confetti|contretemps|cornucopia|\
	corps|cosmos|cupola|cyclamen|dais|debris|diabetes|diphtheria|dysphagia|\
	encyclopaedia|ennui|escallonia|ethos|extremis|fella|ferris|flotilla|\
	formula|forsythia|gallows|ganglia|gardenia|gas|gasworks|gondola|grata|\
	guerrilla|haemophilia|hors|hovis|hustings|hysteria|inertia|innards|iris|\
	isosceles|khaki|koala|lens|macaroni|manilla|mania|mantis|maquis|martini|\
	matins|memorabilia|metropolis|minutiae|molasses|morphia|mortis|neurasthenia|\
	normoglycaemia|nostalgia|omen|pantometria|parabola|paraphernalia|pastis|patella|\
	patens|pathos|patois|pectoris|pelvis|peninsula|phantasmagoria|pharos|plumbites\
	|pneumonia|polyuria|portcullis|pyrexia|regalia|rhinoceros|safari|salami|\
	sari|saturnalia|series|spaghetti|specimen|species|submatrices|subtopia|\
	suburbia|syphilis|tares|taxi|tennis|toccata|trellis|tripos|turps|tutti|\
	umbrella|utopia|villa'+')',0,'',''],['('+'accoutrements|aerodynamics|\
	aeronautics|aesthetics|algae|amends|ammonia|ancients|annals|antics|\
	arrears|assizes|auspices|backwoods|bacteria|banns|barracks|baths|\
	battlements|bellows|belongings|billiards|binoculars|bitters|blandishments|\
	bleachers|blinkers|blues|breeches|brussels|clothes|clutches|commons|confines|\
	contents|credentials|crossbones|crossroads|curia|damages|dealings|dentures|\
	depths|devotions|diggings|doings|downs|droppings|dues|dynamics|earnings|\
	eatables|eaves|economics|electrodynamics|electronics|entrails|environs|\
	equities|ethics|eugenics|filings|finances|folks|footlights|fumes|\
	furnishings|genitals|genitalia|goggles|goods|grits|groceries|grounds|\
	handcuffs|headquarters|histrionics|hostilities|humanities|hydraulics|\
	hysterics|illuminations|innings|italics|jeans|jitters|kinetics|knickers|\
	kudos|latitudes|leggings|likes|linguistics|lodgings|loggerheads|mains|\
	manners|mathematics|means|measles|media|memoirs|metaphysics|mews|mockers|\
	morals|motions|munitions|news|nutria|nylons|oats|odds|oils|oilskins|optics|\
	orthodontics|outskirts|overalls|overtones|pants|pantaloons|papers|paras|\
	paratroops|particulars|pediatrics|phonemics|phonetics|physics|pincers|\
	plastics|politics|proceeds|proceedings|prospects|provinces|provisions|\
	pyjamas|races|rations|ravages|refreshments|regards|reinforcements|remains|\
	respects|returns|riches|rights|savings|schizophrenia|scissors|seconds|\
	semantics|senses|shades|shallows|shambles|shares|shivers|shorts|singles|\
	skittles|slacks|soundings|specifics|spectacles|spoils|stamens|statics|\
	statistics|stratums|summons|supplies|surroundings|suspenders|takings|\
	teens|telecommunications|tenterhooks|thanks|theatricals|thermos|\
	thermodynamics|tights|toils|tops|trades|trappings|travels|troops|\
	tropics|trousers|tweeds|underpants|vapours|vicissitudes|vitals|volumes|\
	wages|wanderings|wares|waters|whereabouts|whites|winnings|withers|woollens|\
	workings|writings|yes'+')',0,'',''],['('+'boatie|bonhomie|clippie|creepie|\
	dearie|droppie|gendarmerie|girlie|goalie|haddie|kookie|kyrie|lambie|lassie|\
	marie|menagerie|pettie|reverie|snottie|sweetie'+')'+'(s)',1,'','s']]
    irregular_re_verbs +=[['(buffett|plummett)'+'es',3,'','s'],['(buffett|plummett)'+\
	'ed',3,'','ed'],['(buffett|plummett)'+'ing',4,'','ing'],\
	['buffetts',2,'','s'],['plummetts',2,'','s'],['gunsling',0,'',''],\
	['gunslung',3,'ing','ed'],['gunslinging',3,'','ing'],\
	['hamstring',0,'',''],['shred',0,'',''],['unfocuss'+'es',3,'','s'],\
	['unfocuss'+'ed',3,'','ed'],['unfocuss'+'ing',4,'','ing'],\
	['(accret|clon|deplet|dethron|dup|excret|expedit|extradit|fet|\
	finetun|gor|hing|massacr|obsolet|reconven|recreat|recus|reignit|\
	swip|videotap|zon)'+'(es)',2,'e','s'],['(accret|clon|deplet|dethron|\
	dup|excret|expedit|extradit|fet|finetun|gor|hing|massacr|obsolet|\
	reconven|recreat|recus|reignit|swip|videotap|zon)'+'(ed)',2,'e','ed'],\
	['(accret|clon|deplet|dethron|dup|excret|expedit|extradit|fet|finetun|\
	gor|hing|massacr|obsolet|reconven|recreat|recus|reignit|swip|videotap|\
	zon)'+'(ing)',3,'e','ing'],\
	['(backpedal|bankroll|bequeath|blackball|bottom|clang|debut|doctor|eyeball|\
	factor|imperil|landfill|margin|occur|overbill|pilot|prong|pyramid|reinstall|\
	relabel|remodel|squirrel|stonewall|wrong)'+'(ed)',2,'','ed'],\
	['(backpedal|bankroll|bequeath|blackball|bottom|clang|debut|doctor|\
	eyeball|factor|imperil|landfill|margin|occur|overbill|pilot|prong|\
	pyramid|reinstall|relabel|remodel|squirrel|stonewall|wrong)'+'(ed)',3,'','ing']]
    irregular_re_nouns +=[['biases',2,'','s'],['biscotti',1,'o','s'],\
	['bookshelves',3,'f','s'],['palazzi',1,'o','s'],['(beastie|brownie|cache|cadre|\
	calorie|champagne|cologne|cookie|druggie|eaterie|emigre|emigree|employee|\
	freebie|genre|kiddie|massacre|moonie|necktie|niche|prairie|softie|toothpaste|willie)'\
	+'(s)',1,'','s'],['(('+A+'*'+'phobia'+')|'+'academia|accompli|aegis|anemia|anorexia|\
	anti|artemisia|ataxia|beatlemania|blini|cafeteria|capita|cognoscenti|coli|deli|\
	dementia|downstairs|dyslexia|dystopia|encyclopedia|estancia|euphoria|\
	euthanasia|fracas|fuss|gala|gorilla|gravitas|GI|habeas|haemophilia|\
	hemophilia|hoopla|hubris|hula|hypoglycemia|ides|impatiens|informatics|\
	intelligentsia|jacuzzi|kiwi|leukaemia|leukemia|mafia|magnolia|malaria|\
	maquila|marginalia|megalomania|mercedes|militia|miniseries|mips|mufti|muni|\
	olympics|pancreas|paranoia|pastoris|pastrami|pepperoni|pepsi|piroghi|pizzeria|\
	plainclothes|pneumocystis|potpourri|proboscis|rabies|reggae|regimen|rigatoni|\
	salmonella|samurai|sarsaparilla|semen|ski|sonata|spatula|stats|subtilis|sushi|\
	tachyarrhythmia|tachycardia|tequila|tetris|thrips|throes|timpani|tsunami|vaccinia|vanilla)'\
	,0,'',''],\
	['(acrobatics|alias|athletics|basics|betters|bifocals|bowels|briefs|checkers|\
	denims|doldrums|dramatics|dungarees|ergonomics|genetics|gymnastics|hackles|haves|\
	incidentals|ironworks|jinks|leavings|leftovers|logistics|makings|microelectronics|\
	mores|oodles|pajamas|pampas|panties|payola|pickings|pliers|pi|ravings|reparations|\
	rudiments|scads|splits|stays|subtitles|sunglasss|sweepstakes|tatters|toiletries|\
	tongs|trivia|tweezers|vibes|waterworks|woolens)',0,'',''],\
	['(biggie|bourgeoisie|brie|camaraderie|chinoiserie|coterie|doggie|genie|hippie|\
	junkie|lingerie|moxie|preppie|rookie|yuppie)'+'(s)',1,'','s']]
    irregular_re_verbs +=[['(chor|sepulchr|silhouett|telescop)'+'(es)',2,'e','s'],\
	['(chor|sepulchr|silhouett|telescop)'+'(ed)',2,'e','ed'],\
	['(chor|sepulchr|silhouett|telescop)'+'(ing)',3,'e','ing'],\
	['(subpena|suds|fresco)'+'(es)',2,'','s'],\
	['(subpena|suds|fresco)'+'(ed)',2,'','ed'],\
	['(subpena|suds|fresco)'+'(ing)',3,'','ing'],\
	['daises',2,'','s'],['reguli',1,'o','s'],\
	['steppes',1,'','s'],\
	['(('+A+'+'+'philia'+')|'+'fantasia|Feis|Gras|Mardi|OS|pleura|tularemia|vasa)',0,'',''],\
	['(calisthenics|heroics|rheumatics|victuals|wiles)',0,'',''],\
	['(auntie|anomie|coosie|quickie)'+'(s)',1,'','s']]
    irregular_re_nouns +=[['(absentia|bourgeois|pecunia|Syntaxis|uncia)',0,'',''],\
	['(apologetics|goings|outdoors)',0,'',''],['collies',1,'','s']]
    irregular_re_verbs +=[['bob-sled',0,'',''],['imbed',0,'',''],\
	['precis',0,'',''],['precis'+'(es)',2,'','s'],['precis'+'(ed)',2,'','ed'],\
	['precis'+'(ing)',3,'','ing']]
    irregular_re_nouns +=[['obsequies',3,'y','s'],['superficies',1,'','s'],\
	['(acacia|albumen|alms|alopecia|ambergris|ambrosia|anaemia|analgesia|\
	anopheles|aphasia|arras|assagai|assegai|astrophysics|aubrietia|avoirdupois|\
	bathos|beriberi|biceps|bitumen|borzoi|broccoli|cadi|calends|callisthenics|\
	calla|camellia|campanula|cantata|caravanserai|cedilla|chilli|chrysalis|\
	clematis|clitoris|cognomen|collywobbles|copula|corolla|cybernetics|cyclops|\
	cyclopaedia|cyclopedia|dahlia|dhoti|dickens|dietetics|dipsomania|dolmen|\
	dyspepsia|effendi|elevenses|epidermis|epiglottis|erysipelas|eurhythmics|\
	faeces|fascia|fibula|finis|fistula|fives|fleur-de-lis|forceps|freesia|\
	fuchsia|geophysics|geriatrics|glottis|guerilla|hadji|haggis|hara-kiri|\
	hernia|herpes|hoop-la|houri|hymen|hyperbola|hypochondria|ibis|inamorata|\
	insignia|insomnia|jackanapes|jimjams|jodhpurs|kepi|kleptomania|kohlrabi|\
	kris|kukri|kumis|litchi|litotes|loggia|magnesia|man-at-arms|manila|\
	mantilla|marquis|master-at-arms|mattins|melancholia|menses|minutia|\
	monomania|muggins|mumps|mi|myopia|nebula|necropolis|neuralgia|nibs|\
	numismatics|nymphomania|obstetrics|okapi|onomatopoeia|ophthalmia|paraplegia|\
	patchouli|paterfamilias|penis|pergola|petunia|pharmacopoeia|phi|piccalilli|\
	poinsettia|praxis|precis|primula|prophylaxis|pyrites|rabbi|raffia|reredos|\
	revers|rickets|rounders|rubella|saki|salvia|sassafras|sawbones|scabies|\
	scapula|schnapps|scintilla|scrofula|secateurs|sepia|septicaemia|sequoia|\
	shears|smithereens|spermaceti|stamen|suds|sundae|si|swami|tarantella|\
	tarantula|testis|therapeutics|thews|tibia|tiddlywinks|tombola|topi|\
	tortilla|trews|triceps|underclothes|undies|uvula|verdigris|vermicelli|\
	viola|wadi|wapiti|wisteria|yaws|yogi|zinnia)',0,'',''],\
	['(aerie|birdie|bogie|caddie|cock-a-leekie|collie|corrie|cowrie|dixie|\
	eyrie|faerie|gaucherie|gillie|knobkerrie|laddie|mashie|mealie|menagerie|\
	organdie|patisserie|pinkie|pixie|stymie|talkie)'+'(s)',1,'','s']]
    irregular_re_nouns +=[['(ablutions|adenoids|aerobatics|afters|astronautics|\
	atmospherics|bagpipes|ballistics|bell-bottoms|belles-lettres|blinders|\
	bloomers|butterfingers|buttocks|bygones|cahoots|cannabis|castanets|\
	clappers|corgi|cross-purposes|dodgems|dregs|duckboards|edibles|envoi|\
	eurythmics|externals|extortions|falsies|fisticuffs|fleshings|fleur-de-lys|\
	fours|gentleman-at-arms|geopolitics|giblets|glassworks|gleanings|handlebars|\
	heartstrings|hi-fi|homiletics|housetops|hunkers|hydroponics|impala|kalends|\
	knickerbockers|kwela|lees|lei|lexis|lieder|literati|loins|meanderings|meths|\
	muesli|muniments|necessaries|nines|ninepins|nippers|nuptials|orthopaedics|\
	paediatrics|phonics|polemics|pontificals|prelims|pyrotechnics|ravioli|rompers|\
	ructions|scampi|scrapings|serjeant-at-arms|sheila|shires|smalls|steelworks|\
	sweepings|toxaemia|ti|vespers|virginals|waxworks|yeti|zucchini)',0,'',''],\
	['(mountie|brasserie|cup-tie|grannie|koppie|rotisserie|walkie-talkie)'+'(s)'\
	,1,'','s']]
    irregular_re_verbs +=[['busses',3,'','s'],['bussed',3,'','ed'],\
	['bussing',4,'','ing'],['hocus-pocusses',3,'','s'],['hocusses',3,'','s'],\
	['(('+A+'*'+'-us'+')|'+'abus|accus|amus|arous|bemus|carous|contus|disabus|\
	disus|dous|enthus|excus|grous|misus|mus|overus|perus|reus|rous|sous|us|\
	('+A+'*'+'[hlmp]ous)|('+A+'*'+'[af]us))'+'(es)',2,'e','s'],\
	['(('+A+'*'+'-us'+')|'+'abus|accus|amus|arous|bemus|carous|contus|\
	disabus|disus|dous|enthus|excus|grous|misus|mus|overus|perus|reus|\
	rous|sous|us|('+A+'*'+'[hlmp]ous)|('+A+'*'+'[af]us))'+'(ed)',2,'e','ed'],\
	['(('+A+'*'+'-us'+')|'+'abus|accus|amus|arous|bemus|carous|contus|disabus|\
	disus|dous|enthus|excus|grous|misus|mus|overus|perus|reus|rous|sous|us|\
	('+A+'*'+'[hlmp]ous)|('+A+'*'+'[af]us))'+'(ing)',3,'e','ing']]
    irregular_re_nouns +=[['(('+A+'*-abus)|('+A+'*-us)|abus|burnous|cayus|\
	chanteus|chartreus|chauffeus|crus|disus|excus|grous|hypotenus|masseus|\
	misus|mus|Ous|overus|poseus|reclus|reus|rus|us|('+A+'*[hlmp]ous)|\
	('+A+'*[af]us))'+'(es)',1,'','s']]
    irregular_verbs +=[['ached','ache','ed'],['aching','ache','ing'],\
	['being','be','ing'],['accustomed','accustom','ed'],\
	['accustoming','accustom','ing'],['blossomed','blossom','ed'],\
	['blossoming','blossom','ing'],['boycotted','boycott','ed'],\
	['boycotting','boycott','ing'],['cataloged','catalog','ed'],\
	['cataloging','catalog','ing'],['created','create','ed'],\
	['creating','create','ing'],['finesses','finesse','s'],\
	['finessed','finesse','ed'],['finessing','finesse','ing'],\
	['interfered','interfere','ed'],['interfering','interfere','ing'],\
	['tastes','taste','s'],['tasted','taste','ed'],\
	['tasting','taste','ing'],['torpedoed','torpedo','ed'],\
	['torpedoing','torpedo','ing'],['wastes','waste','s'],\
	['wasted','waste','ed'],['wasting','waste','ing'],['routed','route','ed'],\
	['routing','route','ing'],['rerouted','reroute','ed'],\
	['rerouting','reroute','ing']]

    def irregular_verbs_wordnet(self):
        return[('abode','abide','ed'),('abought','aby','ed'),('abye','aby',''),\
		('abyes','aby','s'),('acquitted','acquit','ed'),('acquitting','acquit','ing'),\
		('addrest','address','ed'),('ageing','age','ing'),('agreed','agree','ed'),\
		('am','be',''),('anted','ante','ed'),('anteed','ante','ed'),\
		('anteing','ante','ing'),('antes','ante','s'),('arced','arc','ed'),\
		('arcing','arc','ing'),('arcked','arc','ed'),('arcking','arc','ing'),\
		('are','be',''),('arisen','arise','en'),('arose','arise','ed'),\
		('ate','eat','ed'),('awoke','awake','ed'),('awoken','awake','en'),\
		('baby-sat','baby-sit','ed'),('back-pedaled','back-pedal','ed'),\
		('back-pedaling','back-pedal','ing'),('backbit','backbite','ed'),\
		('backbiting','backbite','ing'),('backbitten','backbite','en'),\
		('backslid','backslide','ed'),('backslidden','backslide','en'),\
		('bade','bid','ed'),('bandieds','bandy','s'),('banqueted','banquet','ed'),\
		('banqueting','banquet','ing'),('barreled','barrel','ed'),\
		('barreling','barrel','ing'),('bastinadoed','bastinado','ed'),\
		('beaten','beat','en'),('became','become','ed'),('bedeviled','bedevil','ed'),\
		('bedeviling','bedevil','ing'),('been','be','en'),('befallen','befall','en'),\
		('befalling','befall','ing'),('befell','befall','ed'),('began','begin','ed'),\
		('begat','beget','ed'),('begirt','begird','ed'),('begot','beget','ed'),\
		('begotten','beget','en'),('beguiled','beguile','ed'),('beguiling','beguile','ing'),\
		('begun','begin','en'),('beheld','behold','ed'),('beholden','behold','en'),\
		('bejeweled','bejewel','ed'),('bejeweling','bejewel','ing'),\
		('belied','belie','ed'),('belies','belie','s'),('belying','belie','ing'),\
		('benempt','bename','ed'),('bent','bend','ed'),('besought','beseech','ed'),\
		('bespoke','bespeak','ed'),('bespoken','bespeak','en'),('bestrewn','bestrew','en'),\
		('bestrid','bestride','ed'),('bestridden','bestride','en'),\
		('bestrode','bestride','ed'),('betaken','betake','en'),('bethought','bethink','ed'),\
		('betook','betake','ed'),('beveled','bevel','ed'),
		('beveling','bevel','ing'),
		('biased','bias','ed'),
		('biases','bias','s'),
		('biasing','bias','ing'),
		('biassed','bias','ed'),
		('biassing','bias','ing'),
		('bidden','bid','en'),
		('bit','bite','ed'),
		('biting','bite','ing'),
		('bitten','bite','en'),
		('bivouacked','bivouac','ed'),
		('bivouacking','bivouac','ing'),
		('bled','bleed','ed'),
		('blest','bless','ed'),
		('blew','blow','ed'),
		('blown','blow','en'),
		('blue-pencils','blue-pencil','s'),
		('bogged-down','bog-down','ed'),
		('bogging-down','bog-down','ing'),
		('bogs-down','bog-down','s'),
		('boogied','boogie','ed'),
		('boogies','boogie','s'),
		('bore','bear','ed'),
		('born','bear','en'),
		('borne','bear','en'),
		('bottle-fed','bottle-feed','ed'),
		('bought','buy','ed'),
		('bound','bind','ed'),
		('breast-fed','breast-feed','ed'),
		('bred','breed','ed'),
		('breid','brei','ed'),
		('bringing','bring','ing'),
		('broke','break','ed'),
		('broken','break','en'),
		('brought','bring','ed'),
		('browbeaten','browbeat','en'),
		('buckramed','buckram','ed'),
		('buckraming','buckram','ing'),
		('built','build','ed'),
		('buncoed','bunco','ed'),
		('bunkoed','bunko','ed'),
		('burnt','burn','ed'),
		('busheled','bushel','ed'),
		('busheling','bushel','ing'),
		('bypast','bypass','ed'),
		('came','come','ed'),
		('canaled','canal','ed'),
		('canaling','canal','ing'),
		('canceled','cancel','ed'),
		('canceling','cancel','ing'),
		('carbonadoed','carbonado','ed'),
		('caroled','carol','ed'),
		('caroling','carol','ing'),
		('caught','catch','ed'),
		('caviled','cavil','ed'),
		('caviling','cavil','ing'),
		('cbeled','cbel','ed'),
		('cbeling','cbel','ing'),
		('cbelled','cbel','ed'),
		('cbelling','cbel','ing'),
		('channeled','channel','ed'),
		('channeling','channel','ing'),
		('chassed','chasse','ed'),
		('chasseing','chasse','ing'),
		('chasses','chasse','s'),
		('chevied','chivy','ed'),
		('chevies','chivy','s'),
		('chevying','chivy','ing'),
		('chid','chide','ed'),
		('chidden','chide','en'),
		('chiseled','chisel','ed'),
		('chiseling','chisel','ing'),
		('chivvied','chivy','ed'),
		('chivvies','chivy','s'),
		('chivvying','chivy','ing'),
		('chose','choose','ed'),
		('chosen','choose','en'),
		('clad','clothe','ed'),
		('cleft','cleave','ed'),
		('cleped','clepe','ed'),
		('cleping','clepe','ing'),
		('clept','clepe','ed'),
		('clinging','cling','ing'),
		('clothed','clothe','ed'),
		('clothes','clothe','s'),
		('clothing','clothe','ing'),
		('clove','cleave','ed'),
		('cloven','cleave','en'),
		('clung','cling','ed'),
		('co-opted','coopt','ed'),
		('co-opting','coopt','ing'),
		('co-opts','coopts','s'),
		('co-ordinate','coordinate',''),
		('co-ordinated','coordinate','ed'),
		('co-ordinates','coordinate','s'),
		('co-ordinating','coordinate','ing'),
		('coiffed','coif','ed'),
		('coiffing','coif','ing'),
		('combated','combat','ed'),
		('combating','combat','ing'),
		('concertinaed','concertina','ed'),
		('concertinaing','concertina','ing'),
		('congaed','conga','ed'),
		('congaing','conga','ing'),
		('contangoed','contango','ed'),
		('cooeed','cooee','ed'),
		('cooees','cooee','s'),
		('coquetted','coquet','ed'),
		('coquetting','coquet','ing'),
		('counseled','counsel','ed'),
		('counseling','counsel','ing'),
		('countersank','countersink','ed'),
		('countersunk','countersink','en'),
		('court-martialled','court-martial','ed'),
		('court-martialling','court-martial','ing'),
		('crept','creep','ed'),
		('crescendoed','crescendo','ed'),
		('croqueted','croquet','ed'),
		('croqueting','croquet','ing'),
		('crossbred','crossbreed','ed'),
		('cudgeled','cudgel','ed'),
		('cudgeling','cudgel','ing'),
		('cupeled','cupel','ed'),
		('cupeling','cupel','ing'),
		('curettes','curet','s'),
		('curst','curse','ed'),
		('dealt','deal','ed'),
		('debussed','debus','ed'),
		('debusses','debus','s'),
		('debussing','debus','ing'),
		('decreed','decree','ed'),
		('deep-freeze','deepfreeze',''),
		('deep-freezed','deepfreeze','ed'),
		('deep-freezes','deepfreeze','s'),
		('deep-frozen','deepfreeze','en'),
		('degases','degas','s'),
		('degassed','degas','ed'),
		('degasses','degas','s'),
		('degassing','degas','ing'),
		('deleing','dele','ing'),
		('deviled','devil','ed'),
		('deviling','devil','ing'),
		('diagramed','diagram','ed'),
		('diagraming','diagram','ing'),
		('dialled','dial','ed'),
		('dialling','dial','ing'),
		('did','do','ed'),
		('disagreed','disagree','ed'),
		('disemboweled','disembowel','ed'),
		('disemboweling','disembowel','ing'),
		('disenthralls','disenthral','s'),
		('disenthrals','disenthrall','s'),
		('disheveled','dishevel','ed'),
		('disheveling','dishevel','ing'),
		('dittoed','ditto','ed'),
		('done','do','en'),
		('dought','dow','ed'),
		('dove','dive','ed'),
		('drank','drink','ed'),
		('drawn','draw','en'),
		('dreamt','dream','ed'),
		('dreed','dree','ed'),
		('drew','draw','ed'),
		('driveled','drivel','ed'),
		('driveling','drivel','ing'),
		('driven','drive','en'),
		('drove','drive','ed'),
		('drunk','drink','en'),
		('duelled','duel','ed'),
		('duelling','duel','ing'),
		('dug','dig','ed'),
		('dwelt','dwell','ed'),
		('eaten','eat','en'),
		('echoed','echo','ed'),
		('embargoed','embargo','ed'),
		('embussed','embus','ed'),
		('embusses','embus','s'),
		('embussing','embus','ing'),
		('emceed','emcee','ed'),
		('empaneled','empanel','ed'),
		('empaneling','empanel','ing'),
		('enameled','enamel','ed'),
		('enameling','enamel','ing'),
		('enwound','enwind','ed'),
		('equaled','equal','ed'),
		('equaling','equal','ing'),
		('equalled','equal','ed'),
		('equalling','equal','ing'),
		('equipped','equip','ed'),
		('equipping','equip','ing'),
		('eying','eye','ing'),
		('facsimileing','facsimile','ing'),
		('fallen','fall','en'),
		('fed','feed','ed'),
		('fell','fall','ed'),
		('felt','feel','ed'),
		('filagreed','filagree','ed'),
		('filigreed','filigree','ed'),
		('fillagreed','fillagree','ed'),
		('fine-drawn','fine-draw','en'),
		('fine-drew','fine-draw','ed'),
		('flanneled','flannel','ed'),
		('flanneling','flannel','ing'),
		('fled','flee','ed'),
		('flew','fly','ed'),
		('flinging','fling','ing'),
		('floodlit','floodlight','ed'),
		('flown','fly','en'),
		('flung','fling','ed'),
		('flyblew','flyblow','ed'),
		('flyblown','flyblow','en'),
		('forbad','forbid','ed'),
		('forbade','forbid','ed'),
		('forbidden','forbid','en'),
		('forbore','forbear','ed'),
		('forborne','forbear','en'),
		('force-fed','force-feed','ed'),
		('fordid','fordo','ed'),
		('fordone','fordo','en'),
		('foredid','foredo','ed'),
		('foredone','foredo','en'),
		('foregone','forego','en'),
		('foreknew','foreknow','ed'),
		('foreknown','foreknow','en'),
		('foreran','forerun','ed'),
		('foresaw','foresee','ed'),
		('foreseen','foresee','en'),
		('foreshown','foreshow','en'),
		('forespoke','forespeak','ed'),
		('forespoken','forespeak','en'),
		('foretelling','foretell','ing'),
		('foretold','foretell','ed'),
		('forewent','forego','ed'),
		('forgave','forgive','ed'),
		('forgiven','forgive','en'),
		('forgone','forgo','en'),
		('forgot','forget','ed'),
		('forgotten','forget','en'),
		('forsaken','forsake','en'),
		('forsook','forsake','ed'),
		('forspoke','forspeak','ed'),
		('forspoken','forspeak','en'),
		('forswore','forswear','ed'),
		('forsworn','forswear','en'),
		('forwent','forgo','ed'),
		('fought','fight','ed'),
		('found','find','ed'),
		('freed','free','ed'),
		('fricasseed','fricassee','ed'),
		('frivoled','frivol','ed'),
		('frivoling','frivol','ing'),
		('frolicked','frolic','ed'),
		('frolicking','frolic','ing'),
		('froze','freeze','ed'),
		('frozen','freeze','en'),
		('fuelled','fuel','ed'),
		('fuelling','fuel','ing'),
		('funneled','funnel','ed'),
		('funneling','funnel','ing'),
		('gainsaid','gainsay','ed'),
		('gamboled','gambol','ed'),
		('gamboling','gambol','ing'),
		('gan','gin','en'),
		('garnisheed','garnishee','ed'),
		('gases','gas','s'),
		('gassed','gas','ed'),
		('gasses','gas','s'),
		('gassing','gas','ing'),
		('gave','give','ed'),
		('geed','gee','ed'),
		('gelled','gel','ed'),
		('gelling','gel','ing'),
		('gelt','geld','ed'),
		('genned-up','gen-up','ed'),
		('genning-up','gen-up','ing'),
		('gens-up','gen-up','s'),
		('ghostwriting','ghostwrite','ing'),
		('ghostwritten','ghostwrite','en'),
		('ghostwrote','ghostwrite','ed'),
		('gilt','gild','ed'),
		('girt','gird','ed'),
		('given','give','en'),
		('glaceed','glace','ed'),
		('glaceing','glace','ing'),
		('gnawn','gnaw','en'),
		('gone','go','en'),
		('got','get','ed'),
		('gotten','get','en'),
		('graveled','gravel','ed'),
		('graveling','gravel','ing'),
		('graven','grave','en'),
		('greed','gree','ed'),
		('grew','grow','ed'),
		('gript','grip','ed'),
		('ground','grind','ed'),
		('groveled','grovel','ed'),
		('groveling','grovel','ing'),
		('grown','grow','en'),
		('guaranteed','guarantee','ed'),
		('gumshoes','gumshoe','s'),
		('gypped','gyp','ed'),
		('gypping','gyp','ing'),
		('hacksawn','hacksaw','en'),
		('had','have','ed'),
		('halloed','hallo','ed'),
		('haloed','halo','ed'),
		('hamstringing','hamstring','ing'),
		('hamstrung','hamstring','ed'),
		('handfed','handfeed','ed'),
		('hanseled','hansel','ed'),
		('hanseling','hansel','ing'),
		('has','have','s'),
		('hatcheled','hatchel','ed'),
		('hatcheling','hatchel','ing'),
		('heard','hear','ed'),
		('held','hold','ed'),
		('hewn','hew','en'),
		('hid','hide','ed'),
		('hidden','hide','en'),
		('hocus-pocussed','hocus-pocus','ed'),
		('hocus-pocussing','hocus-pocus','ing'),
		('hocussed','hocus','ed'),
		('hocussing','hocus','ing'),
		('hoes','hoe','s'),
		('hogtied','hogtie','ed'),
		('hogties','hogtie','s'),
		('hogtying','hogtie','ing'),
		('honied','honey','ed'),
		('horseshoes','horseshoe','s'),
		('houseled','housel','ed'),
		('houseling','housel','ing'),
		('hove','heave','ed'),
		('hoveled','hovel','ed'),
		('hoveling','hovel','ing'),
		('hung','hang','ed'),
		('impaneled','impanel','ed'),
		('impaneling','impanel','ing'),
		('impanells','impanel','s'),
		('inbred','inbreed','ed'),
		('indwelling','indwell','ing'),
		('indwelt','indwell','ed'),
		('initialled','initial','ed'),
		('initialling','initial','ing'),
		('inlaid','inlay','ed'),
		('interbred','interbreed','ed'),
		('interlaid','interlay','ed'),
		('interpled','interplead','ed'),
		('interwove','interweave','ed'),
		('interwoven','interweave','en'),
		('inwove','inweave','ed'),
		('inwoven','inweave','en'),
		('is','be','s'),
		('jerry-built','jerry-build','ed'),
		('jeweled','jewel','ed'),
		('jeweling','jewel','ing'),
		('joint','join','ed'),
		('joy-ridden','joy-ride','en'),
		('joy-rode','joy-ride','ed'),
		('kenneled','kennel','ed'),
		('kenneling','kennel','ing'),
		('kent','ken','ed'),
		('kept','keep','ed'),
		('kerneled','kernel','ed'),
		('kerneling','kernel','ing'),
		('kneed','knee','ed'),
		('knelt','kneel','ed'),
		('knew','know','ed'),
		('known','know','en'),
		("ko'd",'ko','ed'),
		("ko'ing",'ko','ing'),
		("ko's",'ko','s'),
		('labeled','label','ed'),
		('labeling','label','ing'),
		('laden','lade','en'),
		('ladyfied','ladify','ed'),
		('ladyfies','ladify','s'),
		('ladyfying','ladify','ing'),
		('laid','lay','ed'),
		('lain','lie','en'),
		('lassoed','lasso','ed'),
		('laureled','laurel','ed'),
		('laureling','laurel','ing'),
		('leant','lean','ed'),
		('leapt','leap','ed'),
		('learnt','learn','ed'),
		('led','lead','ed'),
		('left','leave','ed'),
		('lent','lend','ed'),
		('leveled','level','ed'),
		('leveling','level','ing'),
		('libeled','libel','ed'),
		('libeling','libel','ing'),
		('lit','light','ed'),
		('lost','lose','ed'),
		('made','make','ed'),
		('marshaled','marshal','ed'),
		('marshaling','marshal','ing'),
		('marveled','marvel','ed'),
		('marveling','marvel','ing'),
		('meant','mean','ed'),
		('medaled','medal','ed'),
		('medaling','medal','ing'),
		('met','meet','ed'),
		('metaled','metal','ed'),
		('metaling','metal','ing'),
		('might','may',''),
		('mimicked','mimic','ed'),
		('mimicking','mimic','ing'),
		('misbecame','misbecome','ed'),
		('misdealt','misdeal','ed'),
		('misgave','misgive','ed'),
		('misgiven','misgive','en'),
		('misheard','mishear','ed'),
		('mislaid','mislay','ed'),
		('misled','mislead','ed'),
		('mispled','misplead','ed'),
		('misspelled','misspell','ed'),
		('misspelling','misspell','ing'),
		('misspelt','misspell','ed'),
		('misspent','misspend','ed'),
		('mistaken','mistake','en'),
		('mistook','mistake','ed'),
		('misunderstood','misunderstand','ed'),
		('modeled','model','ed'),
		('modeling','model','ing'),
		('molten','melt','en'),
		('mown','mow','en'),
		('nickeled','nickel','ed'),
		('nickeling','nickel','ing'),
		('nielloed','niello','ed'),
		('non-prossed','non-pros','ed'),
		('non-prosses','non-pros','s'),
		('non-prossing','non-pros','ing'),
		('nonplussed','nonplus','ed'),
		('nonplusses','nonplus','s'),
		('nonplussing','nonplus','ing'),
		('outbidden','outbid','en'),
		('outbred','outbreed','ed'),
		('outdid','outdo','ed'),
		('outdone','outdo','en'),
		('outgassed','outgas','ed'),
		('outgasses','outgas','s'),
		('outgassing','outgas','ing'),
		('outgeneraled','outgeneral','ed'),
		('outgeneraling','outgeneral','ing'),
		('outgone','outgo','en'),
		('outgrew','outgrow','ed'),
		('outgrown','outgrow','en'),
		('outlaid','outlay','ed'),
		('outran','outrun','ed'),
		('outridden','outride','en'),
		('outrode','outride','ed'),
		('outselling','outsell','ing'),
		('outshone','outshine','ed'),
		('outshot','outshoot','ed'),
		('outsold','outsell','ed'),
		('outstood','outstand','ed'),
		('outthought','outthink','ed'),
		('outwent','outgo','ed'),
		('outwore','outwear','ed'),
		('outworn','outwear','en'),
		('overbidden','overbid','en'),
		('overblew','overblow','ed'),
		('overblown','overblow','en'),
		('overbore','overbear','ed'),
		('overborne','overbear','en'),
		('overbuilt','overbuild','ed'),
		('overcame','overcome','ed'),
		('overdid','overdo','ed'),
		('overdone','overdo','en'),
		('overdrawn','overdraw','en'),
		('overdrew','overdraw','ed'),
		('overdriven','overdrive','en'),
		('overdrove','overdrive','ed'),
		('overflew','overfly','ed'),
		('overgrew','overgrow','ed'),
		('overgrown','overgrow','en'),
		('overhanging','overhang','ing'),
		('overheard','overhear','ed'),
		('overhung','overhang','ed'),
		('overlaid','overlay','ed'),
		('overlain','overlie','en'),
		('overlies','overlie','s'),
		('overlying','overlie','ing'),
		('overpaid','overpay','ed'),
		('overpast','overpass','ed'),
		('overran','overrun','ed'),
		('overridden','override','en'),
		('overrode','override','ed'),
		('oversaw','oversee','ed'),
		('overseen','oversee','en'),
		('overselling','oversell','ing'),
		('oversewn','oversew','en'),
		('overshot','overshoot','ed'),
		('overslept','oversleep','ed'),
		('oversold','oversell','ed'),
		('overspent','overspend','ed'),
		('overspilled','overspill','ed'),
		('overspilling','overspill','ing'),
		('overspilt','overspill','ed'),
		('overtaken','overtake','en'),
		('overthrew','overthrow','ed'),
		('overthrown','overthrow','en'),
		('overtook','overtake','ed'),
		('overwound','overwind','ed'),
		('overwriting','overwrite','ing'),
		('overwritten','overwrite','en'),
		('overwrote','overwrite','ed'),
		('paid','pay','ed'),
		('palled','pal','ed'),
		('palling','pal','ing'),
		('paneled','panel','ed'),
		('paneling','panel','ing'),
		('panicked','panic','ed'),
		('panicking','panic','ing'),
		('paralleled','parallel','ed'),
		('paralleling','parallel','ing'),
		('parceled','parcel','ed'),
		('parceling','parcel','ing'),
		('partaken','partake','en'),
		('partook','partake','ed'),
		('pasquil','pasquinade',''),
		('pasquilled','pasquinade','ed'),
		('pasquilling','pasquinade','ing'),
		('pasquils','pasquinade','s'),
		('pedaled','pedal','ed'),
		('pedaling','pedal','ing'),
		('peed','pee','ed'),
		('penciled','pencil','ed'),
		('penciling','pencil','ing'),
		('pent','pen','ed'),
		('physicked','physic','ed'),
		('physicking','physic','ing'),
		('picnicked','picnic','ed'),
		('picnicking','picnic','ing'),
		('pistoled','pistol','ed'),
		('pistoling','pistol','ing'),
		('pled','plead','ed'),
		('polkaed','polka','ed'),
		('polkaing','polka','ing'),
		('pommeled','pommel','ed'),
		('pommeling','pommel','ing'),
		('precanceled','precancel','ed'),
		('precanceling','precancel','ing'),
		('prepaid','prepay','ed'),
		('programmes','program','s'),
		('prologed','prologue','ed'),
		('prologing','prologue','ing'),
		('prologs','prologue','s'),
		('proven','prove','en'),
		('pummeled','pummel','ed'),
		('pummeling','pummel','ing'),
		('pureed','puree','ed'),
		('quarreled','quarrel','ed'),
		('quarreling','quarrel','ing'),
		('quartersawn','quartersaw','en'),
		('queued','queue','ed'),
		('queues','queue','s'),
		('queuing','queue','ing'),
		('quick-froze','quick-freeze','ed'),
		('quick-frozen','quick-freeze','en'),
		('quipped','quip','ed'),
		('quipping','quip','ing'),
		('quitted','quit','ed'),
		('quitting','quit','ing'),
		('quizzed','quiz','ed'),
		('quizzes','quiz','s'),
		('quizzing','quiz','ing'),
		('ran','run','ed'),
		('rang','ring','ed'),
		('raoed','radio','ed'),
		('rarefied','rarefy','ed'),
		('rarefies','rarefy','s'),
		('rarefying','rarefy','ing'),
		('raveled','ravel','ed'),
		('raveling','ravel','ing'),
		('razeed','razee','ed'),
		('re-trod','re-tread','ed'),
		('re-trodden','re-tread','en'),
		('rebuilt','rebuild','ed'),
		('recced','recce','ed'),
		('recceed','recce','ed'),
		('recceing','recce','ing'),
		('red','red','ed'),
		('red-penciled','red-pencil','ed'),
		('red-penciling','red-pencil','ing'),
		('red-pencils','red-pencil','s'),
		('redid','redo','ed'),
		('redone','redo','en'),
		('refereed','referee','ed'),
		('reft','reave','ed'),
		('refuelled','refuel','ed'),
		('refuelling','refuel','ing'),
		('remade','remake','ed'),
		('rent','rend','ed'),
		('repaid','repay','ed'),
		('reran','rerun','ed'),
		('resat','resit','ed'),
		('retaken','retake','en'),
		('rethought','rethink','ed'),
		('retook','retake','ed'),
		('reveled','revel','ed'),
		('reveling','revel','ing'),
		('rewound','rewind','ed'),
		('rewriting','rewrite','ing'),
		('rewritten','rewrite','en'),
		('rewrote','rewrite','ed'),
		('ridden','ride','en'),
		('risen','rise','en'),
		('rivaled','rival','ed'),
		('rivaling','rival','ing'),
		('riven','rive','en'),
		('rode','ride','ed'),
		('roqueted','roquet','ed'),
		('roqueting','roquet','ing'),
		('rose','rise','ed'),
		('rough-hewn','rough-hew','en'),
		('rove','reeve','ed'),
		('roweled','rowel','ed'),
		('roweling','rowel','ing'),
		('rung','ring','ing'),
		('said','say','ed'),
		('sambaed','samba','ed'),
		('sambaing','samba','ing'),
		('sang','sing','ed'),
		('sank','sink','ed'),
		('sat','sit','ed'),
		('sauteed','saute','ed'),
		('sauteing','saute','ing'),
		('saw','see','ed'),
		('sawn','saw','en'),
		('seen','see','en'),
		('sent','send','ed'),
		('sewn','sew','en'),
		('shaken','shake','en'),
		('shaven','shave','en'),
		('shed','shed','ed'),
		('shellacked','shellac','ed'),
		('shellacking','shellac','ing'),
		('shent','shend','ed'),
		('shewn','shew','en'),
		('shod','shoe','ed'),
		('shoes','shoe','s'),
		('shone','shine','ed'),
		('shook','shake','ed'),
		('shot','shoot','ed'),
		('shoveled','shovel','ed'),
		('shoveling','shovel','ing'),
		('shown','show','en'),
		('shrank','shrink','ed'),
		('shriveled','shrivel','ed'),
		('shriveling','shrivel','ing'),
		('shriven','shrive','en'),
		('shrove','shrive','ed'),
		('shrunk','shrink','en'),
		('shrunken','shrink','en'),
		('sicked','sic','ed'),
		('sicking','sic','ing'),
		('sightsaw','sightsee','ed'),
		('sightseen','sightsee','en'),
		('signaled','signal','ed'),
		('signaling','signal','ing'),
		("ski'd",'ski','ed'),
		('skied','ski','ed'),
		('skiing','ski','ing'),
		('skydove','skydive','ed'),
		('slain','slay','en'),
		('slept','sleep','ed'),
		('slew','slay','ed'),
		('slid','slide','ed'),
		('slidden','slide','en'),
		('slinging','sling','ing'),
		('slung','sling','ed'),
		('slunk','slink','ed'),
		('smelt','smell','ed'),
		('smit','smite','ed'),
		('smiting','smite','ing'),
		('smitten','smite','en'),
		('smote','smite','ed'),
		('snafued','snafu','ed'),
		('snafues','snafu','s'),
		('snafuing','snafu','ing'),
		('sniveled','snivel','ed'),
		('sniveling','snivel','ing'),
		('snowshoes','snowshoe','s'),
		('soft-pedaled','soft-pedal','ed'),
		('soft-pedaling','soft-pedal','ing'),
		('sol-faed','sol-fa','ed'),
		('sol-faing','sol-fa','ing'),
		('sold','sell','ed'),
		('soothsaid','soothsay','ed'),
		('sortied','sortie','ed'),
		('sorties','sortie','s'),
		('sought','seek','ed'),
		('sown','sow','en'),
		('spanceled','spancel','ed'),
		('spanceling','spancel','ing'),
		('spat','spit','ed'),
		('sped','speed','ed'),
		('spellbound','spellbind','ed'),
		('spelt','spell','ed'),
		('spent','spend','ed'),
		('spilt','spill','ed'),
		('spiraled','spiral','ed'),
		('spiraling','spiral','ing'),
		('spoilt','spoil','ed'),
		('spoke','speak','ed'),
		('spoken','speak','en'),
		('spoon-fed','spoon-feed','ed'),
		('spotlit','spotlight','ed'),
		('sprang','spring','ed'),
		('springing','spring','ing'),
		('sprung','spring','en'),
		('spun','spin','ed'),
		('squatted','squat','ed'),
		('squatting','squat','ing'),
		('squeegeed','squeegee','ed'),
		('squibbed','squib','ed'),
		('squibbing','squib','ing'),
		('squidded','squid','ed'),
		('squidding','squid','ing'),
		('squilgee','squeegee',''),
		('stall-fed','stall-feed','ed'),
		('stank','stink','ed'),
		('stenciled','stencil','ed'),
		('stenciling','stencil','ing'),
		('stilettoed','stiletto','ed'),
		('stilettoeing','stiletto','ing'),
		('stinging','sting','ing'),
		('stole','steal','ed'),
		('stolen','steal','en'),
		('stood','stand','ed'),
		('stove','stave','ed'),
		('strewn','strew','en'),
		('stridden','stride','en'),
		('stringing','string','ing'),
		('striven','strive','en'),
		('strode','stride','ed'),
		('strove','strive','ed'),
		('strown','strow','en'),
		('struck','strike','ed'),
		('strung','string','ed'),
		('stuccoed','stucco','ed'),
		('stuck','stick','ed'),
		('stung','sting','ed'),
		('stunk','stink','en'),
		('stymied','stymie','ed'),
		('stymies','stymie','s'),
		('stymying','stymie','ing'),
		('subpoenaed','subpoena','ed'),
		('subpoenaing','subpoena','ing'),
		('subtotaled','subtotal','ed'),
		('subtotaling','subtotal','ing'),
		('sung','sing','en'),
		('sunk','sink','en'),
		('sunken','sink','en'),
		('swam','swim','ed'),
		('swept','sweep','ed'),
		('swinging','swing','ing'),
		('swiveled','swivel','ed'),
		('swiveling','swivel','ing'),
		('swollen','swell','en'),
		('swopped','swap','ed'),
		('swopping','swap','ing'),
		('swops','swap','s'),
		('swore','swear','ed'),
		('sworn','swear','en'),
		('swum','swim','en'),
		('swung','swing','ed'),
		('symboled','symbol','ed'),
		('symboling','symbol','ing'),
		('symbolled','symbol','ed'),
		('symbolling','symbol','ing'),
		('taken','take','en'),
		('talced','talc','ed'),
		('talcing','talc','ing'),
		('talcked','talc','ed'),
		('talcking','talc','ing'),
		("tally-ho'd",'tally-ho','ed'),
		('tally-hoed','tally-ho','ed'),
		('tangoed','tango','ed'),
		('tasseled','tassel','ed'),
		('tasseling','tassel','ing'),
		('taught','teach','ed'),
		('taxied','taxi','ed'),
		('taxies','taxi','s'),
		('taxiing','taxi','ing'),
		('taxying','taxi','ing'),
		('te-heed','te-hee','ed'),
		('teed','tee','ed'),
		('thought','think','ed'),
		('threw','throw','ed'),
		('thriven','thrive','en'),
		('throve','thrive','ed'),
		('thrown','throw','en'),
		('tinged','tinge','ed'),
		('tingeing','tinge','ing'),
		('tinging','tinge','ing'),
		('tinseled','tinsel','ed'),
		('tinseling','tinsel','ing'),
		('tiptoes','tiptoe','s'),
		('toes','toe','s'),
		('told','tell','ed'),
		('took','take','ed'),
		('tore','tear','ed'),
		('torn','tear','en'),
		('torrify','torrefy',''),
		('totaled','total','ed'),
		('totaling','total','ing'),
		('toweled','towel','ed'),
		('toweling','towel','ing'),
		('trafficked','traffic','ed'),
		('trafficking','traffic','ing'),
		('trameled','trammel','ed'),
		('trameling','trammel','ing'),
		('tramelled','trammel','ed'),
		('tramelling','trammel','ing'),
		('tramels','trammel','s'),
		('transfixt','transfix','ed'),
		('tranship','transship','ed'),
		('traveled','travel','ed'),
		('traveling','travel','ing'),
		('trod','tread','ed'),
		('trodden','tread','en'),
		('troweled','trowel','ed'),
		('troweling','trowel','ing'),
		('tunneled','tunnel','ed'),
		('tunneling','tunnel','ing'),
		('typewriting','typewrite','ing'),
		('typewritten','typewrite','en'),
		('typewrote','typewrite','ed'),
		('unbent','unbend','ed'),
		('unbound','unbind','ed'),
		('unclad','unclothe','ed'),
		('unclothed','unclothe','ed'),
		('unclothes','unclothe','s'),
		('unclothing','unclothe','ing'),
		('underbought','underbuy','ed'),
		('underfed','underfeed','ed'),
		('undergirt','undergird','ed'),
		('undergone','undergo','en'),
		('underlaid','underlay','ed'),
		('underlain','underlie','en'),
		('underlies','underlie','s'),
		('underlying','underlie','ing'),
		('underpaid','underpay','ed'),
		('underselling','undersell','ing'),
		('undershot','undershoot','ed'),
		('undersold','undersell','ed'),
		('understood','understand','ed'),
		('undertaken','undertake','en'),
		('undertook','undertake','ed'),
		('underwent','undergo','ed'),
		('underwriting','underwrite','ing'),
		('underwritten','underwrite','en'),
		('underwrote','underwrite','ed'),
		('undid','undo','ed'),
		('undone','undo','en'),
		('unfroze','unfreeze','ed'),
		('unfrozen','unfreeze','en'),
		('unkenneled','unkennel','ed'),
		('unkenneling','unkennel','ing'),
		('unlaid','unlay','ed'),
		('unlearnt','unlearn','ed'),
		('unmade','unmake','ed'),
		('unraveled','unravel','ed'),
		('unraveling','unravel','ing'),
		('unrove','unreeve','ed'),
		('unsaid','unsay','ed'),
		('unslinging','unsling','ing'),
		('unslung','unsling','ed'),
		('unspoke','unspeak','ed'),
		('unspoken','unspeak','en'),
		('unstringing','unstring','ing'),
		('unstrung','unstring','ed'),
		('unstuck','unstick','ed'),
		('unswore','unswear','ed'),
		('unsworn','unswear','en'),
		('untaught','unteach','ed'),
		('unthought','unthink','ed'),
		('untied','untie','ed'),
		('unties','untie','s'),
		('untying','untie','ing'),
		('untrod','untread','ed'),
		('untrodden','untread','en'),
		('unwound','unwind','ed'),
		('upbuilt','upbuild','ed'),
		('upheld','uphold','ed'),
		('uphove','upheave','ed'),
		('upped','up','ed'),
		('upping','up','ing'),
		('uprisen','uprise','en'),
		('uprose','uprise','ed'),
		('upsprang','upspring','ed'),
		('upspringing','upspring','ing'),
		('upsprung','upspring','en'),
		('upswelled','upswell','ed'),
		('upswelling','upswell','ing'),
		('upswept','upsweep','ed'),
		('upswinging','upswing','ing'),
		('upswollen','upswell','en'),
		('upswung','upswing','ed'),
		('vetoed','veto','ed'),
		('victualled','victual','ed'),
		('victualling','victual','ing'),
		('visaed','visa','ed'),
		('visaing','visa','ing'),
		('vitriolled','vitriol','ed'),
		('vitriolling','vitriol','ing'),
		('vivaed','viva','ed'),
		('vivaing','viva','ing'),
		('was','be','ed'),
		("water-ski'd",'water-ski','ed'),
		('water-skied','water-ski','ed'),
		('water-skiing','water-ski','ing'),
		('waylaid','waylay','ed'),
		('waylain','waylay','en'),
		('went','go','ed'),
		('wept','weep','ed'),
		('were','be','ed'),
		('whipsawn','whipsaw','en'),
		('whizzed','whiz','ed'),
		('whizzes','whiz','s'),
		('whizzing','whiz','ing'),
		('winterfed','winterfeed','ed'),
		('wiredrawn','wiredraw','en'),
		('wiredrew','wiredraw','ed'),
		('withdrawn','withdraw','en'),
		('withdrew','withdraw','ed'),
		('withheld','withhold','ed'),
		('withstood','withstand','ed'),
		('woke','wake','ed'),
		('woken','wake','en'),
		('won','win','ed'),
		('wore','wear','ed'),
		('worn','wear','en'),
		('wound','wind','ed'),
		('wove','weave','ed'),
		('woven','weave','en'),
		('wringing','wring','ing'),
		('writing','write','ing'),
		('written','write','en'),
		('wrote','write','ed'),
		('wrung','wring','ed'),
		('ycleped','clepe','ed'),
		('yclept','clepe','ed'),
		('yodeled','yodel','ed'),
		('yodeling','yodel','ing'),
		('zeroed','zero','ed')]

    def irregular_nouns_wordnet(self):
        return[
		('addenda','addendum','s'),
		('adieux','adieu','s'),
		('aides-de-camp','aide-de-camp','s'),
		('aliases','alias','s'),
		('alkalies','alkali','s'),
		('aloes','aloe','s'),
		('amanuenses','amanuensis','s'),
		('analyses','analysis','s'),
		('anastomoses','anastomosis','s'),
		('anthraces','anthrax','s'),
		('antitheses','antithesis','s'),
		('aphides','aphis','s'),
		('apices','apex','s'),
		('apotheoses','apotheosis','s'),
		('appendices','appendix','s'),
		('arboreta','arboretum','s'),
		('areg','erg','s'),
		('arterioscleroses','arteriosclerosis','s'),
		('atlantes','atlas','s'),
		('automata','automaton','s'),
		('axises','axis','s'),
		('bambini','bambino','s'),
		('bandeaux','bandeau','s'),
		('banditti','bandit','s'),
		('bassi','basso','s'),
		('beaux','beau','s'),
		('beeves','beef','s'),
		('bicepses','biceps','s'),
		('bijoux','bijou','s'),
		('billets-doux','billet-doux','s'),
		('boraces','borax','s'),
		('bossies','boss','s'),
		('brainchildren','brainchild','s'),
		('brethren','brother','s'),
		('brothers-in-law','brother-in-law','s'),
		('buckteeth','bucktooth','s'),
		('bunde','bund','s'),
		('bureaux','bureau','s'),
		('busses','bus','s'),
		('calves','calf','s'),
		('calyces','calyx','s'),
		('candelabra','candelabrum','s'),
		('capricci','capriccio','s'),
		('caribous','caribou','s'),
		('carides','caryatid','s'),
		('catalyses','catalysis','s'),
		('cerebra','cerebrum','s'),
		('cervices','cervix','s'),
		('chateaux','chateau','s'),
		('cherubim','cherub','s'),
		('children','child','s'),
		('chillies','chilli','s'),
		('chrysalides','chrysalis','s'),
		('chrysalises','chrysalis','s'),
		('ciceroni','cicerone','s'),
		('cloverleaves','cloverleaf','s'),
		('coccyges','coccyx','s'),
		('codices','codex','s'),
		('cola','colon','s'),
		('colloquies','colloquy','s'),
		('colones','colon','s'),
		('concertanti','concertante','s'),
		('concerti','concerto','s'),
		('concertini','concertino','s'),
		('conquistadores','conquistador','s'),
		('contralti','contralto','s'),
		('corpora','corpus','s'),
		('corrigenda','corrigendum','s'),
		('cortices','cortex','s'),
		('cosmoses','cosmos','s'),
		('crescendi','crescendo','s'),
		('crises','crisis','s'),
		('criteria','criterion','s'),
		('cruces','crux','s'),
		('culs-de-sac','cul-de-sac','s'),
		('cyclopes','cyclops','s'),
		('cyclopses','cyclops','s'),
		('data','datum','s'),
		('daughters-in-law','daughter-in-law','s'),
		('desiderata','desideratum','s'),
		('diaereses','diaeresis','s'),
		('diaerses','diaeresis','s'),
		('diagnoses','diagnosis','s'),
		('dialyses','dialysis','s'),
		('diathses','diathesis','s'),
		('dicta','dictum','s'),
		('diereses','dieresis','s'),
		('dilettantes','dilettante','s'),
		('dilettanti','dilettante','s'),
		('divertimenti','divertimento','s'),
		('dogteeth','dogtooth','s'),
		('dormice','dormouse','s'),
		('dryades','dryad','s'),
		('dui','duo','s'),
		('duona','duodenum','s'),
		('duonas','duodenum','s'),
		('dwarves','dwarf','s'),
		('eisteddfodau','eisteddfod','s'),
		('ellipses','ellipsis','s'),
		('elves','elf','s'),
		('emphases','emphasis','s'),
		('epicentres','epicentre','s'),
		('epiglottides','epiglottis','s'),
		('epiglottises','epiglottis','s'),
		('errata','erratum','s'),
		('exegeses','exegesis','s'),
		('eyeteeth','eyetooth','s'),
		('fathers-in-law','father-in-law','s'),
		('feet','foot','s'),
		('fellaheen','fellah','s'),
		('fellahin','fellah','s'),
		('femora','femur','s'),
		('fezzes','fez','s'),
		('flagstaves','flagstaff','s'),
		('flambeaux','flambeau','s'),
		('flatfeet','flatfoot','s'),
		('fleurs-de-lis','fleur-de-lis','s'),
		('fleurs-de-lys','fleur-de-lys','s'),
		('flyleaves','flyleaf','s'),
		('fora','forum','s'),
		('forcipes','forceps','s'),
		('forefeet','forefoot','s'),
		('fulcra','fulcrum','s'),
		('gallowses','gallows','s'),
		('gases','gas','s'),
		('gasses','gas','s'),
		('gateaux','gateau','s'),
		('geese','goose','s'),
		('gemboks','gemsbok','s'),
		('genera','genus','s'),
		('geneses','genesis','s'),
		('gentlemen-at-arms','gentleman-at-arms','s'),
		('gestalten','gestalt','s'),
		('giraffes','giraffe','s'),
		('glissandi','glissando','s'),
		('glottides','glottis','s'),
		('glottises','glottis','s'),
		('godchildren','godchild','s'),
		('goings-over','going-over','s'),
		('grandchildren','grandchild','s'),
		('halves','half','s'),
		('hangers-on','hanger-on','s'),
		('helices','helix','s'),
		('hooves','hoof','s'),
		('hosen','hose','s'),
		('hypnoses','hypnosis','s'),
		('hypotheses','hypothesis','s'),
		('iambi','iamb','s'),
		('ibices','ibex','s'),
		('ibises','ibis','s'),
		('impedimenta','impediment','s'),
		('indices','index','s'),
		('intagli','intaglio','s'),
		('intermezzi','intermezzo','s'),
		('interregna','interregnum','s'),
		('irides','iris','s'),
		('irises','iris','s'),
		('is','is','s'),
		('jacks-in-the-box','jack-in-the-box','s'),
		('kibbutzim','kibbutz','s'),
		('knives','knife','s'),
		('kohlrabies','kohlrabi','s'),
		('kronen','krone','s'),
		('kroner','krone','s'),
		('kronur','krona','s'),
		('kylikes','kylix','s'),
		('ladies-in-waiting','lady-in-waiting','s'),
		('larynges','larynx','s'),
		('latices','latex','s'),
		('leges','lex','s'),
		('libretti','libretto','s'),
		('lire','lira','s'),
		('lives','life','s'),
		('loaves','loaf','s'),
		('loggie','loggia','s'),
		('lustra','lustre','s'),
		('lyings-in','lying-in','s'),
		('macaronies','macaroni','s'),
		('maestri','maestro','s'),
		('mantes','mantis','s'),
		('mantises','mantis','s'),
		('markkaa','markka','s'),
		('marquises','marquis','s'),
		('masters-at-arms','master-at-arms','s'),
		('matrices','matrix','s'),
		('matzoth','matzo','s'),
		('mausolea','mausoleum','s'),
		('maxima','maximum','s'),
		('meioses','meiosis','s'),
		('memoranda','memorandum','s'),
		('men-at-arms','man-at-arms','s'),
		("men-o'-war",'man-of-war','s'),
		('men-of-war','man-of-war','s'),
		('menservants','manservant','s'),
		('mesdemoiselles','mademoiselle','s'),
		('messieurs','monsieur','s'),
		('metamorphoses','metamorphosis','s'),
		('metatheses','metathesis','s'),
		('metempsychoses','metempsychosis','s'),
		('metropolises','metropolis','s'),
		('mice','mouse','s'),
		('milieux','milieu','s'),
		('minima','minimum','s'),
		('momenta','momentum','s'),
		('monies','money','s'),
		('monsignori','monsignor','s'),
		('mooncalves','mooncalf','s'),
		('mothers-in-law','mother-in-law','s'),
		('naiades','naiad','s'),
		('necropoleis','necropolis','s'),
		('necropolises','necropolis','s'),
		('nemeses','nemesis','s'),
		('neuroses','neurosis','s'),
		('novelle','novella','s'),
		('oases','oasis','s'),
		('obloquies','obloquy','s'),
		('octahedra','octahedron','s'),
		('optima','optimum','s'),
		('ora','os','s'),
		('osar','os','s'),
		('ossa','os','s'),
		('ova','ovum','s'),
		('oxen','ox','s'),
		('paralyses','paralysis','s'),
		('parentheses','parenthesis','s'),
		('paris-mutuels','pari-mutuel','s'),
		('pastorali','pastorale','s'),
		('patresfamilias','paterfamilias','s'),
		('pease','pea','s'),
		('pekingese','pekinese','s'),
		('pelves','pelvis','s'),
		('pelvises','pelvis','s'),
		('pence','penny','s'),
		('penes','penis','s'),
		('penises','penis','s'),
		('penknives','penknife','s'),
		('perihelia','perihelion','s'),
		('pfennige','pfennig','s'),
		('pharynges','pharynx','s'),
		('phenomena','phenomenon','s'),
		('philodendra','philodendron','s'),
		('pieds-a-terre','pied-a-terre','s'),
		('pineta','pinetum','s'),
		('plateaux','plateau','s'),
		('plena','plenum','s'),
		('pocketknives','pocketknife','s'),
		('portmanteaux','portmanteau','s'),
		('potlies','potbelly','s'),
		('praxes','praxis','s'),
		('praxises','praxis','s'),
		('proboscides','proboscis','s'),
		('proboscises','proboscis','s'),
		('prostheses','prosthesis','s'),
		('protozoa','protozoan','s'),
		('pudenda','pudendum','s'),
		('putti','putto','s'),
		('quanta','quantum','s'),
		('quarterstaves','quarterstaff','s'),
		('quizzes','quiz','s'),
		('reales','real','s'),
		('recta','rectum','s'),
		('referenda','referendum','s'),
		('reis','real','s'),
		('rhinoceroses','rhinoceros','s'),
		('roes','roe','s'),
		('rondeaux','rondeau','s'),
		('rostra','rostrum','s'),
		('runners-up','runner-up','s'),
		('sancta','sanctum','s'),
		('sawboneses','sawbones','s'),
		('scarves','scarf','s'),
		('scherzi','scherzo','s'),
		('scleroses','sclerosis','s'),
		('scrota','scrotum','s'),
		('secretaries-general','secretary-general','s'),
		('selves','self','s'),
		('sera','serum','s'),
		('seraphim','seraph','s'),
		('sheaves','sheaf','s'),
		('shelves','shelf','s'),
		('simulacra','simulacrum','s'),
		('sisters-in-law','sister-in-law','s'),
		('soli','solo','s'),
		('soliloquies','soliloquy','s'),
		('sons-in-law','son-in-law','s'),
		('spectra','spectrum','s'),
		('sphinges','sphinx','s'),
		('splayfeet','splayfoot','s'),
		('sputa','sputum','s'),
		('stamina','stamen','s'),
		('stelae','stele','s'),
		('stepchildren','stepchild','s'),
		('sterna','sternum','s'),
		('strata','stratum','s'),
		('stretti','stretto','s'),
		('summonses','summons','s'),
		('swamies','swami','s'),
		('swathes','swathe','s'),
		('synopses','synopsis','s'),
		('syntheses','synthesis','s'),
		('tableaux','tableau','s'),
		('taxies','taxi','s'),
		('teeth','tooth','s'),
		('tempi','tempo','s'),
		('tenderfeet','tenderfoot','s'),
		('testes','testis','s'),
		('theses','thesis','s'),
		('thieves','thief','s'),
		('thoraces','thorax','s'),
		('titmice','titmouse','s'),
		('tootses','toots','s'),
		('torsi','torso','s'),
		('tricepses','triceps','s'),
		('triumviri','triumvir','s'),
		('trousseaux','trousseau','s'),
		('turves','turf','s'),
		('tympana','tympanum','s'),
		('ultimata','ultimatum','s'),
		('vacua','vacuum','s'),
		('vertices','vertex','s'),
		('vertigines','vertigo','s'),
		('virtuosi','virtuoso','s'),
		('vortices','vortex','s'),
		('wagons-lits','wagon-lit','s'),
		('weirdies','weirdie','s'),
		('werewolves','werewolf','s'),
		('wharves','wharf','s'),
		('whippers-in','whipper-in','s'),
		('wolves','wolf','s'),
		('woodlice','woodlouse','s'),
		('yogin','yogi','s'),
		('zombies','zombie','s')]
    irregular_verbs += irregular_verbs_wordnet(None)
    irregular_nouns += irregular_nouns_wordnet(None)

    def setitem(self,dict,key,value):
        dict[key]=value

if __name__=='__main__':
    import sys
    p=MontyLemmatiser()
    test_string='i bought a thousand pickles at supermarketing'
    print map(lambda the_tokenizer_str:p.lemmatise_word(the_tokenizer_str,)\
	,test_string.split())
