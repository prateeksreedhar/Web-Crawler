import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.spiders import BaseSpider
from scrapy.http import FormRequest
from loginform import fill_login_form
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class ElementSpider(scrapy.Spider):
    name = 'simple'
    start_urls = ['http://forum.nafc.org/login/']
    # Getting URLs from "selspider" spider
    thread_urls = [u'topic/88/introductions---new-members-start-here/', u'topic/88/page/1/introductions---new-members-start-here/', u'topic/88/page/6/introductions---new-members-start-here/', u'topic/88/page/6/introductions---new-members-start-here/#148', u'topic/304/paid-survey-opportunity-for-caregivers/', u'topic/304/page/1/paid-survey-opportunity-for-caregivers/#11', u'topic/283/paid-survey-opportunity-re-oab/', u'topic/283/page/1/paid-survey-opportunity-re-oab/#5', u'topic/305/incontinence-survey/', u'topic/305/page/1/incontinence-survey/#7', u'topic/171/total-incontinence-and-hopeful-for-help/', u'topic/171/page/1/total-incontinence-and-hopeful-for-help/#13', u'topic/284/pelvic-floor/', u'topic/284/page/1/pelvic-floor/#6', u'topic/300/3-years-and-still-suffering-/', u'topic/300/page/1/3-years-and-still-suffering-/#9', u'topic/18/your-best-tips-and-advice/', u'topic/18/page/1/your-best-tips-and-advice/#10', u'topic/209/artificial-urinary-sphnichter/', u'topic/209/page/1/artificial-urinary-sphnichter/#12', u'topic/268/mail-order-contents-clearly-labeled/', u'topic/268/page/1/mail-order-contents-clearly-labeled/#14', u'topic/297/myrbetrig/', u'topic/297/page/1/myrbetrig/#5', u'topic/258/veterans/', u'topic/258/page/1/veterans/#16', u'topic/303/so-unhappy-in-this-hell/', u'topic/303/page/1/so-unhappy-in-this-hell/#9', u'topic/272/not-that-/', u'topic/272/page/1/not-that-/#28', u'topic/289/teen-enuresis-and-adult-bedwetting/', u'topic/289/page/1/teen-enuresis-and-adult-bedwetting/#7', u'topic/302/incontinence-while-being-active/', u'topic/302/page/1/incontinence-while-being-active/#9', u'topic/21/being-intimate-when-you-have-incontinence/', u'topic/21/page/1/being-intimate-when-you-have-incontinence/', u'topic/21/page/2/being-intimate-when-you-have-incontinence/', u'topic/21/page/2/being-intimate-when-you-have-incontinence/#37', u'topic/301/bathroom-locator-phone-app-idea/', u'topic/301/page/1/bathroom-locator-phone-app-idea/#3', u'topic/276/62-female-diagnosed-with-urinary-retention-l/', u'topic/276/page/1/62-female-diagnosed-with-urinary-retention-l/#3', u'topic/271/dr-visit/', u'topic/271/page/1/dr-visit/#16', u'topic/148/neurogenic-underactive-bladder/', u'topic/148/page/1/neurogenic-underactive-bladder/#11', u'topic/299/fsa/', u'topic/299/page/1/fsa/#3', u'topic/23/managing-the-emotional-aspect-of-incontinence/', u'topic/23/page/1/managing-the-emotional-aspect-of-incontinence/#27', u'topic/295/how-to-best-manage/', u'topic/295/page/1/how-to-best-manage/#24', u'topic/298/pessary-ring/', u'topic/298/page/1/pessary-ring/#1', u'topic/296/sling/', u'topic/296/page/1/sling/#4', u'topic/291/college-with-incontinence/', u'topic/291/page/1/college-with-incontinence/#9', u'topic/6/prostate-cancer/', u'topic/6/page/1/prostate-cancer/', u'topic/6/page/2/prostate-cancer/', u'topic/6/page/2/prostate-cancer/#40', u'topic/293/just-started-bed-wetting-in-my-20s/', u'topic/293/page/1/just-started-bed-wetting-in-my-20s/#5', u'topic/223/spiral-down-to-incontinence/', u'topic/223/page/1/spiral-down-to-incontinence/#17', u'topic/287/20-and-losing-control/', u'topic/287/page/1/20-and-losing-control/#20', u'topic/290/running-contributing-to-incontinence-symptom/', u'topic/290/page/1/running-contributing-to-incontinence-symptom/#5', u'topic/292/bedwetting-guest/', u'topic/292/page/1/bedwetting-guest/#5', u'topic/282/bowel-incontinence/', u'topic/282/page/1/bowel-incontinence/#3', u'topic/288/bedwetting-after-taking-tamsulosin-for-bph/', u'topic/288/page/1/bedwetting-after-taking-tamsulosin-for-bph/#13', u'topic/244/has-anyone-overcome-bedwetting/', u'topic/244/page/1/has-anyone-overcome-bedwetting/', u'topic/244/page/2/has-anyone-overcome-bedwetting/', u'topic/244/page/2/has-anyone-overcome-bedwetting/#36', u'topic/285/hip-operationbedwetting/', u'topic/285/page/1/hip-operationbedwetting/#8', u'topic/180/help-with-cloth-selection/', u'topic/180/page/1/help-with-cloth-selection/#8', u'topic/286/type-one-diabetic-with-fecal-incontinance/', u'topic/286/page/1/type-one-diabetic-with-fecal-incontinance/#2', u'topic/87/diaper-recommendation/', u'topic/87/page/1/diaper-recommendation/', u'topic/87/page/3/diaper-recommendation/', u'topic/87/page/3/diaper-recommendation/#57', u'topic/281/recommendation/', u'topic/281/page/1/recommendation/#5', u'topic/95/i-feel-awful/', u'topic/95/page/1/i-feel-awful/#28', u'topic/255/new-guy/', u'topic/255/page/1/new-guy/', u'topic/255/page/2/new-guy/', u'topic/255/page/2/new-guy/#33', u'topic/280/suggestions-please/', u'topic/280/page/1/suggestions-please/#11', u'topic/257/incontinence-and-utis/', u'topic/257/page/1/incontinence-and-utis/#5', u'topic/231/need-advice-willful-fecal-incontinence/', u'topic/231/page/1/need-advice-willful-fecal-incontinence/#19', u'topic/279/young-woman/', u'topic/279/page/1/young-woman/#8', u'topic/278/proton-radiation-u-of-f-jacksonvillefl/', u'topic/278/page/1/proton-radiation-u-of-f-jacksonvillefl/#4', u'topic/275/abx-and-oab/', u'topic/275/page/1/abx-and-oab/#6', u'topic/277/other-advice-on-self-managing/', u'topic/277/page/1/other-advice-on-self-managing/#1', u'topic/274/anyone-taking-duloxetine-for-stress-ui/', u'topic/274/page/1/anyone-taking-duloxetine-for-stress-ui/#8', u'topic/273/how-to-be-green--minimize-odor/', u'topic/273/page/1/how-to-be-green--minimize-odor/#3', u'topic/256/waking-up-dry/', u'topic/256/page/1/waking-up-dry/#8', u'topic/267/robotic-prostatectomy-and-diverticulotomy/', u'topic/267/page/1/robotic-prostatectomy-and-diverticulotomy/#5', u'topic/269/light-at-the-end-of-the-tunnel/', u'topic/269/page/1/light-at-the-end-of-the-tunnel/#3', u'topic/270/earn-100-in-new-at-home-research-for-sui/', u'topic/270/page/1/earn-100-in-new-at-home-research-for-sui/#1', u'topic/213/exhausted/', u'topic/213/page/1/exhausted/#10', u'topic/263/good-cloth-covered-diaper/', u'topic/263/page/1/good-cloth-covered-diaper/#11', u'topic/266/runners/', u'topic/266/page/1/runners/#2', u'topic/126/embarrassed-to-find-myself-here-bedwetting/', u'topic/126/page/1/embarrassed-to-find-myself-here-bedwetting/#20', u'topic/259/incontinent-underwear/', u'topic/259/page/1/incontinent-underwear/#13', u'topic/265/will-you-share-your-story-with-us/', u'topic/265/page/1/will-you-share-your-story-with-us/#1', u'topic/264/update/', u'topic/264/page/1/update/#5', u'topic/234/coloplast-peristeen-rectal-incontinence-plug/', u'topic/234/page/1/coloplast-peristeen-rectal-incontinence-plug/#4', u'topic/260/diaper-change/', u'topic/260/page/1/diaper-change/#4', u'topic/173/when-someone-knows-that-shouldnt/', u'topic/173/page/1/when-someone-knows-that-shouldnt/#21', u'topic/262/substituting-imodium-ad-for-lomotil/', u'topic/262/page/1/substituting-imodium-ad-for-lomotil/#1', u'topic/248/symptoms-returned-and-question/', u'topic/248/page/1/symptoms-returned-and-question/#11', u'topic/250/first-pee-of-the-day/', u'topic/250/page/1/first-pee-of-the-day/#4', u'topic/156/tibial-nerve-stimulation/', u'topic/156/page/1/tibial-nerve-stimulation/#7', u'topic/104/incontinence-after-radical-prostate-surgery/', u'topic/104/page/1/incontinence-after-radical-prostate-surgery/#12', u'topic/249/new-member/', u'topic/249/page/1/new-member/#24', u'topic/191/anyone-taking-desmopresin/', u'topic/191/page/1/anyone-taking-desmopresin/#8', u'topic/254/newbe/', u'topic/254/page/1/newbe/#9', u'topic/253/can-i-ask/', u'topic/253/page/1/can-i-ask/#4', u'topic/252/male-booster-pads/', u'topic/252/page/1/male-booster-pads/#4', u'topic/251/article-some-of-you-may-find-interesting/', u'topic/251/page/1/article-some-of-you-may-find-interesting/#5', u'topic/235/preventing-urinary-catheter-blockages/', u'topic/235/page/1/preventing-urinary-catheter-blockages/#4', u'topic/247/hello-folks/', u'topic/247/page/1/hello-folks/#4', u'topic/238/electric-blankets/', u'topic/238/page/1/electric-blankets/#6', u'topic/159/college-freshman-with-incontinence/', u'topic/159/page/1/college-freshman-with-incontinence/#13', u'topic/246/changing-products/', u'topic/246/page/1/changing-products/#4', u'topic/146/diaper-help/', u'topic/146/page/1/diaper-help/#14', u'topic/236/prostate-cancer/', u'topic/236/page/1/prostate-cancer/#12', u'topic/224/botox-injections/', u'topic/224/page/1/botox-injections/#7', u'topic/245/female-underware/', u'topic/245/page/1/female-underware/#9', u'topic/243/miniature-washing-machines--my-privacy/', u'topic/243/page/1/miniature-washing-machines--my-privacy/#1', u'topic/241/introducing-care-and-getting-the-word-out/', u'topic/241/page/1/introducing-care-and-getting-the-word-out/#9', u'topic/242/not-new-but-never-introduced-myself/', u'topic/242/page/1/not-new-but-never-introduced-myself/#4', u'topic/240/relationships-with-guys/', u'topic/240/page/1/relationships-with-guys/#13', u'topic/219/night-time-enuresis/', u'topic/219/page/1/night-time-enuresis/#9', u'topic/117/do-you-suffer-from-adult-bedwetting/', u'topic/117/page/1/do-you-suffer-from-adult-bedwetting/', u'topic/117/page/2/do-you-suffer-from-adult-bedwetting/', u'topic/117/page/2/do-you-suffer-from-adult-bedwetting/#49', u'topic/239/what-happened-to/', u'topic/239/page/1/what-happened-to/#2', u'topic/7/whats-your-best-solution-to-constipation/', u'topic/7/page/1/whats-your-best-solution-to-constipation/#11', u'topic/237/hi-i-am-new-here/', u'topic/237/page/1/hi-i-am-new-here/#6', u'topic/204/peyronies/', u'topic/204/page/1/peyronies/#5', u'topic/229/first-time/', u'topic/229/page/1/first-time/#7', u'topic/155/interstim-therapy/', u'topic/155/page/1/interstim-therapy/#10', u'topic/228/good-day-all/', u'topic/228/page/1/good-day-all/#5', u'topic/233/38-with-a-prolapse-bladder/', u'topic/233/page/1/38-with-a-prolapse-bladder/#2', u'topic/166/condom-catheter/', u'topic/166/page/1/condom-catheter/#26', u'topic/232/fecal-incontinence--russian-tens/', u'topic/232/page/1/fecal-incontinence--russian-tens/#1', u'topic/226/interstem/', u'topic/226/page/1/interstem/#2', u'topic/230/inquiry/', u'topic/230/page/1/inquiry/#2', u'topic/214/which-way-to-go/', u'topic/214/page/1/which-way-to-go/#17', u'topic/91/when-to-tell-others/', u'topic/91/page/1/when-to-tell-others/#16', u'topic/227/kentucky/', u'topic/227/page/1/kentucky/#1', u'topic/225/botox/', u'topic/225/page/1/botox/#2', u'topic/164/frustrated-by-lack-of-info/', u'topic/164/page/1/frustrated-by-lack-of-info/#20', u'topic/221/oxytrol-otc-for-women/', u'topic/221/page/1/oxytrol-otc-for-women/#5', u'topic/216/tub-bathing-yay-or-nay/', u'topic/216/page/1/tub-bathing-yay-or-nay/#6', u'topic/222/male-incontinence-canadian-start-up/', u'topic/222/page/1/male-incontinence-canadian-start-up/#3', u'topic/220/no-activity-on-here/', u'topic/220/page/1/no-activity-on-here/#5', u'topic/210/urinary-retention/', u'topic/210/page/1/urinary-retention/#4', u'topic/190/ages-15-30-please-help/', u'topic/190/page/1/ages-15-30-please-help/#17', u'topic/217/long-trip-solutions/', u'topic/217/page/1/long-trip-solutions/#7', u'topic/218/drip-restraint/', u'topic/218/page/1/drip-restraint/#4', u'topic/181/any-young-people-18-25-have-this/', u'topic/181/page/1/any-young-people-18-25-have-this/#21', u'topic/215/after-surgery-drink-more-or-less-water/', u'topic/215/page/1/after-surgery-drink-more-or-less-water/#6', u'topic/212/best-solution-when-being-active/', u'topic/212/page/1/best-solution-when-being-active/#7', u'topic/211/trus-biobsy/', u'topic/211/page/1/trus-biobsy/#2', u'topic/58/ms-bladder-health/', u'topic/58/page/1/ms-bladder-health/#11', u'topic/202/hypnosis-sketch-for-adults-with-bedwetting/', u'topic/202/page/1/hypnosis-sketch-for-adults-with-bedwetting/#4', u'topic/207/hello/', u'topic/207/page/1/hello/#3', u'topic/170/oxybutynin/', u'topic/170/page/1/oxybutynin/#9', u'topic/208/introduction-pain-for-a-year/', u'topic/208/page/1/introduction-pain-for-a-year/#1', u'topic/205/recurring-kidney-stones-and-incontinence/', u'topic/205/page/1/recurring-kidney-stones-and-incontinence/#17', u'topic/197/frustrated-buying-diapers/', u'topic/197/page/1/frustrated-buying-diapers/#8', u'topic/206/nafc-needs-your-help/', u'topic/206/page/1/nafc-needs-your-help/#1', u'topic/203/waking-up-stinky/', u'topic/203/page/1/waking-up-stinky/#7', u'topic/46/need-comfortable-plastic-pants/', u'topic/46/page/1/need-comfortable-plastic-pants/#12', u'topic/200/back-to-bedwetting-no-hope-to-improve/', u'topic/200/page/1/back-to-bedwetting-no-hope-to-improve/#5', u'topic/201/caregivers/', u'topic/201/page/1/caregivers/#3', u'topic/199/unique-problem/', u'topic/199/page/1/unique-problem/#1', u'topic/198/32-years-old/', u'topic/198/page/1/32-years-old/#3', u'topic/98/advice-to-help-a-parent/', u'topic/98/page/1/advice-to-help-a-parent/#15', u'topic/92/friends/', u'topic/92/page/1/friends/#9', u'topic/196/diapers-vs-indwelling-catheters/', u'topic/196/page/1/diapers-vs-indwelling-catheters/#2', u'topic/167/underwear/', u'topic/167/page/1/underwear/#22', u'topic/195/does-your-children--know-about-your-inco/', u'topic/195/page/1/does-your-children--know-about-your-inco/#10', u'topic/194/favorite-thing-about-the-nafc-message-boards/', u'topic/194/page/1/favorite-thing-about-the-nafc-message-boards/#13', u'topic/193/babykins-adult-diapers/', u'topic/193/page/1/babykins-adult-diapers/#3', u'topic/188/help-me/', u'topic/188/page/1/help-me/', u'topic/188/page/2/help-me/', u'topic/188/page/2/help-me/#34', u'topic/184/comfortable-with-diapers/', u'topic/184/page/1/comfortable-with-diapers/#18', u'topic/192/forget-to-put-on-diaper-for-the-night/', u'topic/192/page/1/forget-to-put-on-diaper-for-the-night/#4', u'topic/189/journalist-seeks-parents-of-bedwetting-kids/', u'topic/189/page/1/journalist-seeks-parents-of-bedwetting-kids/#2', u'topic/187/any-tips-of-removeing-stains/', u'topic/187/page/1/any-tips-of-removeing-stains/#7', u'topic/182/fed-up/', u'topic/182/page/1/fed-up/#9', u'topic/183/water-parks/', u'topic/183/page/1/water-parks/#4', u'topic/174/incontinent-after-back-surgery/', u'topic/174/page/1/incontinent-after-back-surgery/#10', u'topic/186/bladder-training/', u'topic/186/page/1/bladder-training/#7', u'topic/185/friends/', u'topic/185/page/1/friends/#2', u'topic/39/bedwetting-and-sleep-apnea/', u'topic/39/page/1/bedwetting-and-sleep-apnea/#4', u'topic/163/myrbetriq-report/', u'topic/163/page/1/myrbetriq-report/#7', u'topic/70/help-my-story-starting-to-self-cath/', u'topic/70/page/1/help-my-story-starting-to-self-cath/#9', u'topic/178/curious/', u'topic/178/page/1/curious/#11', u'topic/177/they-said-i-would-grow-out-of-it-27-years-on/', u'topic/177/page/1/they-said-i-would-grow-out-of-it-27-years-on/#5', u'topic/122/nafc-8-week-challenge---share-your-tips/', u'topic/122/page/1/nafc-8-week-challenge---share-your-tips/#4', u'topic/176/my-poor-husband/', u'topic/176/page/1/my-poor-husband/#11', u'topic/175/stuck-on-an-elevator-for-almost-four-hours/', u'topic/175/page/1/stuck-on-an-elevator-for-almost-four-hours/#4', u'topic/73/opps-again/', u'topic/73/page/1/opps-again/#20', u'topic/172/i-am-tired/', u'topic/172/page/1/i-am-tired/#14', u'topic/86/college-bedwetting/', u'topic/86/page/1/college-bedwetting/#10', u'topic/169/total-incontinence/', u'topic/169/page/1/total-incontinence/#3', u'topic/140/male-bedwetting/', u'topic/140/page/1/male-bedwetting/#21', u'topic/143/hotel-nightmare/', u'topic/143/page/1/hotel-nightmare/#17', u'topic/168/fustrated/', u'topic/168/page/1/fustrated/#4', u'topic/133/neurogenic-bladder-tired-out-bladder/', u'topic/133/page/1/neurogenic-bladder-tired-out-bladder/#9', u'topic/165/hospital--stay/', u'topic/165/page/1/hospital--stay/#14', u'topic/136/dating/', u'topic/136/page/1/dating/#5', u'topic/56/free-sample/', u'topic/56/page/1/free-sample/#13', u'topic/152/absorbent-diapers/', u'topic/152/page/1/absorbent-diapers/#17', u'topic/128/bedwetting-to-day-wetting-also/', u'topic/128/page/1/bedwetting-to-day-wetting-also/#8', u'topic/17/wondering---ptns/', u'topic/17/page/1/wondering---ptns/#5', u'topic/160/sudden-bedwetting-problem--new-here/', u'topic/160/page/1/sudden-bedwetting-problem--new-here/#12', u'topic/68/adult-diapers/', u'topic/68/page/1/adult-diapers/#7', u'topic/109/45-yr-old-bedwetter/', u'topic/109/page/1/45-yr-old-bedwetter/#8', u'topic/162/male-sterilization-when-incontinent/', u'topic/162/page/1/male-sterilization-when-incontinent/#1', u'topic/161/hi/', u'topic/161/page/1/hi/#1', u'topic/153/meeting-people/', u'topic/153/page/1/meeting-people/#7', u'topic/131/new-member/', u'topic/131/page/1/new-member/#7', u'topic/158/oab-patients---please-share-your-story/', u'topic/158/page/1/oab-patients---please-share-your-story/#2', u'topic/157/protection/', u'topic/157/page/1/protection/#7', u'topic/111/my-doctor-said-kegals-are-not-for-me/', u'topic/111/page/1/my-doctor-said-kegals-are-not-for-me/#8', u'topic/14/in-tone-pelvic-floor-exerciser/', u'topic/14/page/1/in-tone-pelvic-floor-exerciser/#6', u'topic/154/enterocutaneous-or-colocutaneous-fistula-occ/', u'topic/154/page/1/enterocutaneous-or-colocutaneous-fistula-occ/#4', u'topic/144/nocturnal-diuresis-occasional-need-help/', u'topic/144/page/1/nocturnal-diuresis-occasional-need-help/#7', u'topic/151/whatever-it-is-in-phentermine/', u'topic/151/page/1/whatever-it-is-in-phentermine/#2', u'topic/150/parkinsons-and-uti/', u'topic/150/page/1/parkinsons-and-uti/#2', u'topic/65/im-prone-to-rashes-and-need-help/', u'topic/65/page/1/im-prone-to-rashes-and-need-help/#15', u'topic/113/going-on-vacation/', u'topic/113/page/1/going-on-vacation/#10', u'topic/149/prognosis/', u'topic/149/page/1/prognosis/#6', u'topic/137/diapers-are-best/', u'topic/137/page/1/diapers-are-best/#5', u'topic/147/paranoid-about-odor/', u'topic/147/page/1/paranoid-about-odor/#7', u'topic/43/nervous-bladder/', u'topic/43/page/1/nervous-bladder/#16', u'topic/145/aneurin-bevan-continence-system/', u'topic/145/page/1/aneurin-bevan-continence-system/#3', u'topic/142/has-anyone-tried-this-reusable-underwear/', u'topic/142/page/1/has-anyone-tried-this-reusable-underwear/#7', u'topic/5/urinary-incontinence-in-men/', u'topic/5/page/1/urinary-incontinence-in-men/#5', u'topic/9/sharing-bladder-or-bowel-health-information/', u'topic/9/page/1/sharing-bladder-or-bowel-health-information/#2', u'topic/141/anyone-tried-the-afex-external-catheter/', u'topic/141/page/1/anyone-tried-the-afex-external-catheter/#5', u'topic/135/help/', u'topic/135/page/1/help/#8', u'topic/69/question-about-bedwetting-children/', u'topic/69/page/1/question-about-bedwetting-children/#14', u'topic/139/artificial-urinary-sphinchter/', u'topic/139/page/1/artificial-urinary-sphinchter/#5', u'topic/118/27-year-old-female/', u'topic/118/page/1/27-year-old-female/#8', u'topic/134/19-and-been-incontinent-all-my-life/', u'topic/134/page/1/19-and-been-incontinent-all-my-life/#5', u'topic/138/this-is-very-hard/', u'topic/138/page/1/this-is-very-hard/#4', u'topic/130/our-journey-and-how-we-get-there/', u'topic/130/page/1/our-journey-and-how-we-get-there/#15', u'topic/132/home-made-incontinence-pads/', u'topic/132/page/1/home-made-incontinence-pads/#2', u'topic/116/abdominal-surgery-and-diaper-wearing/', u'topic/116/page/1/abdominal-surgery-and-diaper-wearing/#4', u'topic/44/43-year-old-bed-wetter/', u'topic/44/page/1/43-year-old-bed-wetter/', u'topic/44/page/2/43-year-old-bed-wetter/', u'topic/44/page/2/43-year-old-bed-wetter/#35', u'topic/125/once-labeled-neurogenic-bladder-now-where/', u'topic/125/page/1/once-labeled-neurogenic-bladder-now-where/#4', u'topic/121/overactive-bladder/', u'topic/121/page/1/overactive-bladder/#10', u'topic/129/curious-and-shocked-seeking-advice/', u'topic/129/page/1/curious-and-shocked-seeking-advice/#4', u'topic/127/yoga/', u'topic/127/page/1/yoga/#3', u'topic/124/too-wet-for-words/', u'topic/124/page/1/too-wet-for-words/#7', u'topic/123/some-advice-please/', u'topic/123/page/1/some-advice-please/#4', u'topic/115/suggestions-please/', u'topic/115/page/1/suggestions-please/#10', u'topic/114/essential-oils/', u'topic/114/page/1/essential-oils/#2', u'topic/97/oops/', u'topic/97/page/1/oops/#4', u'topic/120/moving/', u'topic/120/page/1/moving/#3', u'topic/119/levator-ani-syndrone/', u'topic/119/page/1/levator-ani-syndrone/#2', u'topic/107/college-student-looking-for-supportstories/', u'topic/107/page/1/college-student-looking-for-supportstories/#6', u'topic/112/white-clumps-in-catheter-tube/', u'topic/112/page/1/white-clumps-in-catheter-tube/#7', u'topic/102/oab-driving-me-crazy/', u'topic/102/page/1/oab-driving-me-crazy/#8', u'topic/110/tibial-nerve-stimulation-therapy/', u'topic/110/page/1/tibial-nerve-stimulation-therapy/#5', u'topic/108/over-40/', u'topic/108/page/1/over-40/#3', u'topic/106/help/', u'topic/106/page/1/help/#6', u'topic/105/newbie/', u'topic/105/page/1/newbie/#5', u'topic/103/reccommendations-for-doctors/', u'topic/103/page/1/reccommendations-for-doctors/#9', u'topic/53/finally-an-answer/', u'topic/53/page/1/finally-an-answer/#17', u'topic/101/new-here---first-timer/', u'topic/101/page/1/new-here---first-timer/#5', u'topic/99//', u'topic/99/page/1//#6', u'topic/93/fecal-incontinence--multiple-sclerosis/', u'topic/93/page/1/fecal-incontinence--multiple-sclerosis/#27', u'topic/96/oab-light-incontinence/', u'topic/96/page/1/oab-light-incontinence/#2', u'topic/94/i-thought-this-would-be-gone-by-now/', u'topic/94/page/1/i-thought-this-would-be-gone-by-now/#7', u'topic/84/its-embarrassing/', u'topic/84/page/1/its-embarrassing/#6', u'topic/61/27-year-old-female/', u'topic/61/page/1/27-year-old-female/#13', u'topic/49/what-product-should-i-use/', u'topic/49/page/1/what-product-should-i-use/#10', u'topic/50/27-and-bedwetting/', u'topic/50/page/1/27-and-bedwetting/#14', u'topic/80/wetting/', u'topic/80/page/1/wetting/#30', u'topic/40/bedwetting-women/', u'topic/40/page/1/bedwetting-women/#7', u'topic/90/urinary-incontinence/', u'topic/90/page/1/urinary-incontinence/#2', u'topic/89/urodynamic--cystocopy/', u'topic/89/page/1/urodynamic--cystocopy/#5', u'topic/77/post-prostatectomy/', u'topic/77/page/1/post-prostatectomy/#5', u'topic/27/products/', u'topic/27/page/1/products/#7', u'topic/71/stress-incontinence-and-alternate-solution/', u'topic/71/page/1/stress-incontinence-and-alternate-solution/#4', u'topic/83/lifestyle-changes-and-bladder-retraining/', u'topic/83/page/1/lifestyle-changes-and-bladder-retraining/#10', u'topic/74/coping-with-feelings-of-being-defective/', u'topic/74/page/1/coping-with-feelings-of-being-defective/#4', u'topic/72/self-catherization/', u'topic/72/page/1/self-catherization/#3', u'topic/85/medical-anal-plugs/', u'topic/85/page/1/medical-anal-plugs/#1', u'topic/51/i-cured-myself-drug-free-when-doctors-gave-u/', u'topic/51/page/1/i-cured-myself-drug-free-when-doctors-gave-u/#14', u'topic/82/mesh-vs-flesh/', u'topic/82/page/1/mesh-vs-flesh/#3', u'topic/81/page-doesnt-load-topics/', u'topic/81/page/1/page-doesnt-load-topics/#3', u'topic/79/synapses/', u'topic/79/page/1/synapses/#8', u'topic/78/synapsis/', u'topic/78/page/1/synapsis/#1', u'topic/76/proteins-and-need-to-urinate/', u'topic/76/page/1/proteins-and-need-to-urinate/#1', u'topic/75/suffering-incontinence-due-to-ibs/', u'topic/75/page/1/suffering-incontinence-due-to-ibs/#3', u'topic/67/new/', u'topic/67/page/1/new/#5', u'topic/55/leaving-the-country-with-incontinence/', u'topic/55/page/1/leaving-the-country-with-incontinence/#10', u'topic/63/girlfriend-of-an-occasional-bed-wetter/', u'topic/63/page/1/girlfriend-of-an-occasional-bed-wetter/#11', u'topic/66/condom-catheter/', u'topic/66/page/1/condom-catheter/#6', u'topic/64/not-been-able-to-wee-awlfull/', u'topic/64/page/1/not-been-able-to-wee-awlfull/#2', u'topic/62/please-help/', u'topic/62/page/1/please-help/#3', u'topic/59/wetting-cured/', u'topic/59/page/1/wetting-cured/#7', u'topic/60/my-biggest-secret/', u'topic/60/page/1/my-biggest-secret/#6', u'topic/10/consulting-doctor-on-best-way-to-void/', u'topic/10/page/1/consulting-doctor-on-best-way-to-void/#2', u'topic/26/diet-and-exercise/', u'topic/26/page/1/diet-and-exercise/#2', u'topic/25/behavioral-modifications/', u'topic/25/page/1/behavioral-modifications/#2', u'topic/19/traveling-with-incontinence/', u'topic/19/page/1/traveling-with-incontinence/#4', u'topic/28/incontinence-is-just-a-symptom/', u'topic/28/page/1/incontinence-is-just-a-symptom/#5', u'topic/57/forums/', u'topic/57/page/1/forums/#3', u'topic/54/wet/', u'topic/54/page/1/wet/#6', u'topic/42/36-year-old-male---daily-nighttime-enuresis/', u'topic/42/page/1/36-year-old-male---daily-nighttime-enuresis/#3', u'topic/24/procedures/', u'topic/24/page/1/procedures/#3', u'topic/52/new--here/', u'topic/52/page/1/new--here/#13', u'topic/47/wife-of-a-nightly-bedwetter/', u'topic/47/page/1/wife-of-a-nightly-bedwetter/#8', u'topic/35/have-you-heard-of-this-app/', u'topic/35/page/1/have-you-heard-of-this-app/#4', u'topic/45/bedwetting-stopped-now-cant-sleep/', u'topic/45/page/1/bedwetting-stopped-now-cant-sleep/#6', u'topic/41/mother-of-a-sufferer/', u'topic/41/page/1/mother-of-a-sufferer/#8', u'topic/29/jury-duty-and-oab/', u'topic/29/page/1/jury-duty-and-oab/#9', u'topic/36/can-drinking-too-much-tea-really-contribute/', u'topic/36/page/1/can-drinking-too-much-tea-really-contribute/#3', u'topic/38/can-zanaflex-cause-sleep-wetting/', u'topic/38/page/1/can-zanaflex-cause-sleep-wetting/#3', u'topic/37/surgery-failed--now-what/', u'topic/37/page/1/surgery-failed--now-what/#1', u'topic/11/urinary-incontinence-in-women/', u'topic/11/page/1/urinary-incontinence-in-women/#3', u'topic/30/seeking-oab-patients-for-research-study/', u'topic/30/page/1/seeking-oab-patients-for-research-study/#2', u'topic/34/causes-of-incontinence/', u'topic/34/page/1/causes-of-incontinence/#1', u'topic/33/kegel/', u'topic/33/page/1/kegel/#3', u'topic/32/prostatectomy-kegels/', u'topic/32/page/1/prostatectomy-kegels/#2', u'topic/31/in-remission-from-pca-still-have-nocturia/', u'topic/31/page/1/in-remission-from-pca-still-have-nocturia/#1', u'topic/22/join-paid-study-on-incontinence/', u'topic/22/page/1/join-paid-study-on-incontinence/#1', u'topic/16/doing-kegel-exercises/', u'topic/16/page/1/doing-kegel-exercises/#1', u'topic/15/pelvic-organ-prolapse-management/', u'topic/15/page/1/pelvic-organ-prolapse-management/#2', u'topic/13/pregnancy-and-childbirth/', u'topic/13/page/1/pregnancy-and-childbirth/#2', u'topic/12/best-kegel-app/', u'topic/12/page/1/best-kegel-app/#1', u'topic/4/talking-with-your-loved-one-about-their-incontinence/', u'topic/4/page/1/talking-with-your-loved-one-about-their-incontinence/#1', u'topic/20/staying-active-with-incontinence/', u'topic/20/page/1/staying-active-with-incontinence/#1', u'topic/8/bph/', u'topic/8/page/1/bph/#3', u'topic/3/a-place-to-vent/', u'topic/3/page/1/a-place-to-vent/#1']
    def __init__(self, *args, **kwargs):
                super(ElementSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        return [FormRequest.from_response(response,
                    formdata={'registerUserName': 'helloworld123', 'registerPass': 'helloworld123'},
                    callback=self.after_main_login)]

    def after_main_login(self, response):
        for url in self.thread_urls:
            split_url = url.split('/')
            if split_url[2] != 'page':
                yield response.follow(url, callback=self.parse_post_pages)

    def parse_post_pages(self, response):
        posts_ids = response.xpath('//div[contains(@class, "post-container")]/@id').extract()
        subject = response.xpath('//h1[@class="thread-title-headline left"]/text()').extract()
        for post_id in posts_ids:
            post_container = '//div[contains(@class,"post-container")][@id = "' + post_id
            post_content_in_list = response.xpath( post_container +'"]//tr[2]/td//text()').extract()
            post_content = ''.join(post_content_in_list)
            post_number = response.xpath(post_container + '"]/table[@class="post-table"]//tr[3]/td[@class="post-share"]/text()').extract()
            yield{
                'PAGE_NUMBER_OF_THE_POST' : response.xpath('//div[@class="pages-thread-right"]//text()').extract()[-1],
                'SUBJECT' : subject[0].strip(),
                'POST_NUMBER' : post_number[0][0:8].replace("0x95",""),
                'USER' : response.xpath(post_container + '"]/table[@class="post-table"]//tr[1]/td[@class="post-name"]/a[contains(@href, "profile")]/text()').extract()[0],
                'POST' : post_content,
                'POST-UPVOTES' : response.xpath(post_container + '"]/table[@class="post-table"]//tr[1]/td[@class="post-moderate"]/div/span/span/text()').extract()[0],
                'USER-UPVOTES' : response.xpath(post_container + '"]/table[@class="post-table"]//tr[1]/td[@class="post-avatar"]/div/a[@class="postModpoints"]/text()').extract()[0],
                'TIME-STAMPS' : response.xpath(post_container + '"]/table[@class="post-table"]//tr[3]/td[@class="post-date"]/span/@title').extract()[0],
            }
        prev_page_link = response.xpath('//a[@class="link-thread-left"]/@href').extract()
        if len(prev_page_link) > 0:
            yield response.follow(prev_page_link[0],callback=self.parse_post_pages)

if __name__ == "__main__":
    spider = ElementSpider()
