#!/usr/bin/env python
import sys
import time
from urllib import urlencode
from urllib2 import urlopen
from xml.dom import minidom

class PubmedNlp:
    """
    A Python library for accessing and retriving data from
    NCBI web services (http://nlp.ncibi.org/about.html).
    With this program a bio informatics person can get abstract by giving the id
    of a gene, or can acces gene information from a pubmed abstcat with
    pubmedid.
    
    Usage:
        >>> from pubmednlp import *
        >>> nlp = PubmedNlp()

        To get abstract by giving a gene id
        >>> nlp.getAbstractwGeneid("26854") # Will return maximum ten abstract
        # and gene info in each abstract.

        To get meta data related to a pubmedid

        >>> nlp.getMetaData("17523140")

        To get abstract with pmid

        >>> nlp.getAbstract(pmid='17523140')

        To get gene info in a pubmed abstract

        >>> nlp.geneData("17523140")

        
    """
    #BASEURL = "http://nlp.ncibi.org/fetch?"
    def __init__(self):
        """
        Class initialization.
        """
        self.BASEURL = "http://nlp.ncibi.org/fetch?"

    def getAbstractwGeneid(self, geneid, limit=10):
        """
        Function o fetch abstarct details with geneid .
        Returns a set of pubmed ID and abstract details
        """
        if limit > 1000:
            print "Limit is not permissible\
            maximum is 1000. Please correct accordingly"
            sys.exit()

        url = self.BASEURL + "tagger=nametagger&type=gene&id=" + \
        str(geneid) + "&limit=" + str(limit)
        time.sleep(4)
        #print url
        content = urlopen(url).read()
        xmldoc = minidom.parseString(content)
        results = xmldoc.getElementsByTagName("Result")
        #results = xmldoc.getElementsByTagName( "Result" )\
        #[0].getElementsByTagName( "Article" )[0].getAttribute( "pmid" )
        pmidsofgene = []

        for pmids in range(len(results)):
            nowpmid = results[pmids].getElementsByTagName("Article")\
            [0].getAttribute("pmid")
            pmidsofgene.append(nowpmid)

        abstract = {}

        for pmig in pmidsofgene:
            #abstract[pmig] = self.getAbstract( pmid = pmig )
            #print pmig
            abstract[pmig] = self.getMetaData(pmig)
            #print abstract
            time.sleep(4)

        retabs = abstract.values()


        return retabs



    def getAbstract(self, pmid=None, pmcid=None):
        """
        Function to extract PubMed abstract based on pubmedid.
        """
        if pmid != None and pmcid != None:
            pmiddict = {}
            pmciddict = {}
            pmidc = self.__getPmidAbstract(pmid)
            pmcidc = self.__getPmcidAbstract(pmcid)
            pmiddict[pmid] = pmidc
            pmciddict[pmcid] = pmcidc
            return pmiddict, pmciddict
        elif pmid != None and pmcid == None:
            pmidic = {}
            pmidcont = self.__getPmidAbstract(pmid)
            pmidic[pmid] = pmidcont
            return pmidic
        elif pmcid != None and pmid == None:
            pmciddict = {}
            pmcidcont = self.__getPmcidAbstract(pmcid)
            pmciddict[pmcid] = pmcidcont
            return pmciddict

    def __getPmidAbstract(self, pmid):
        """
        Function to fetch abstract based on pmid
        """
        urlpmid = self.BASEURL + "pmid=" + str(pmid)
        pmidcont = self.__getContent(urlpmid)
        pmidcont = " ".join(pmidcont)
        time.sleep(4)

        return pmidcont

    def __getPmcidAbstract(self, pmcid):
        """
        Fetch abstract based on PMCID
        """
        urlpmcid = self.BASEURL + "pmcid=" + str(pmcid)
        pmcidcont = self.__getContent(urlpmcid)
        pmcidcont = " ".join(pmcidcont)
        time.sleep(4)

        return pmcidcont



    def geneData(self, id):
        """
        Function to extract gene info from PubMed abstract
        """
        genedict = {}
        vlu = {'pmid':id, 'tagger':'nametagger', 'type':'gene'}
        urlv = urlencode(vlu)
        url = self.BASEURL + urlv
        #print url
        content = urlopen(url).read()
        xml_content = minidom.parseString(content)
        genetype = [gene.getAttribute("type") for\
        gene in xml_content.getElementsByTagName("Gene")]
        geneid = [gene.getAttribute("id") for\
        gene in xml_content.getElementsByTagName("Gene")]
        protine = [gene.firstChild.data for\
        gene in xml_content.getElementsByTagName("Gene")]
        for i in range(len(geneid)):
            genedict[geneid[i]] = genetype[i] + "##" + protine[i]

        return genedict


    def getMetaData(self, id):
        """
        Get literature with metadata.
        Title, Author/s, Journal, Date of Publishing, Content, 
        Gene info etc....
        """
        idn = str(id)
        url = self.BASEURL + 'pmid=' + idn + \
        "&tagger=nametagger&type=gene&metadata=all"
        content = urlopen(url).read()
        time.sleep(4)
        xml_cont = minidom.parseString(content)
        title = [tit.firstChild.data for tit in \
        xml_cont.getElementsByTagName('Title')]
        #print title
        art_title, journ_title = title[0], title[1]
        #For Journal Vol info

        jovol = xml_cont.getElementsByTagName('Journal')\
        [0].getElementsByTagName('Volume')[0].firstChild.data
        try:
            jissue = xml_cont.getElementsByTagName('Journal')\
            [0].getElementsByTagName('Issue')[0].firstChild.data
        except:
            jissue = " "
            pass
        jpages = xml_cont.getElementsByTagName('Journal')\
        [0].getElementsByTagName('Pages')[0].firstChild.data

        try:
            jmont = [fna.firstChild.data for fna in xml_cont.\
            getElementsByTagName('Month')]
            #print "%%%%%%%%%%%%%%%\n", jmont
        except:
            jmont = " "
            pass

        try:
            jyear = [fna.firstChild.data for fna in xml_cont.\
            getElementsByTagName('Year')]
        except:
            jyear = " "
            pass



     
        fname = []
        fname = [fna.firstChild.nodeValue for fna in \
        xml_cont.getElementsByTagName('ForeName')]
        lname = [lna.firstChild.nodeValue for lna in \
        xml_cont.getElementsByTagName('LastName')]

        auth_name = []

        for name in range(len(fname)):
            aname = lname[name] + " " + fname[name]
            auth_name.append(aname)
        #Added author name

        #sentences = [cont.firstChild.nodeValue for \
        sentences = [cont.firstChild.data for \
        cont in xml_cont.getElementsByTagName("Text")]
        #sentences = [cont.firstChild.data for \
        #cont in xml_cont.getElementsByTagName("Sentence")]
        #print sentences
        genedict = {}
        genetype = [gene.getAttribute("type") for\
        gene in xml_cont.getElementsByTagName("Gene")]
        geneid = [gene.getAttribute("id") for\
        gene in xml_cont.getElementsByTagName("Gene")]
        protine = [gene.firstChild.data for\
        gene in xml_cont.getElementsByTagName("Gene")]

        for i in range(len(geneid)):
            genedict[geneid[i]] = genetype[i] + " " + protine[i]

        genes = genedict.items()
        final_gene = []

        for ge in genes:
            final_gene.append("GeneId: " + ge[0] + "  GeneInfo: " + ge[1] )
        final_gene = "\n".join(final_gene)
        #print final_gene

        meta = "PUBMEDID: %s '\n'Title: %s  '\n'Authers: %s '\n'Journal: %s'\n'"\
        % (idn, art_title, ",".join(auth_name), journ_title)

        meta1 = "Vol: %s'\n'Issue: %s'\n'Month: %s Year: %s Pages: %s'\n'"\
        % (jovol, jissue, jmont[0], jyear[0], jpages)
        #print sentences

        abst = "Abstract: %s %s %s %s" \
        % (" ".join(sentences), '\n',final_gene,'\n')
        #% (" ".join(sentences), '\n'," ".join(final_gene),'\n')


        rmeta = meta + meta1 + abst

        return rmeta

    def __getContent(self, url):
        """
        Function for internal use.
        Fetch content from specified URL.
        """
        content = urlopen(url).read()
        time.sleep(4)
        xml_cont = minidom.parseString(content)
        sentences = [cont.firstChild.data for \
        cont in xml_cont.getElementsByTagName("Text")]
        #cont in xml_cont.getElementsByTagName("Sentence")]
        #print sentences
        return sentences


if __name__ == "__main__":
    ob = PubmedNlp()
    #gda = ob.geneData("17523140")
    gda = ob.geneData("17523140")
    #print gda
    #abstr = ob.getAbstract(pmid='17523140')
    #print abstr
    #print gda.items()
    #print "#################################"
    #print ob.getMetaData("17523140")
    #print "#################################"
    #ob.getAbstractwGeneid("26854")
    abs = ob.getAbstractwGeneid("26854")
    for a in abs:
        print a
    # print "#################################"
