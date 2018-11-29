from lxml import etree
for e in etree.iterparse('/home/cleverhandle1/src/sf_bipolar/data/output/isis/enmedia.hizb-ut-tahrir.info_80.xml'):
    if e[1].text != None and "audios" in e[1].text:
        print(('http://enmedia.hizb-ut-tahrir.info/' + e[1].text).encode('utf-8'))
