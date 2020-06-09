from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from .models import tagpaircompare, tagpair as TP, relation
from stackapi import StackAPI
from django.utils.safestring import mark_safe
# import json
# from django.core import serializers
# import os

# Create your views here.
def robots(request):

    return render(request, 'robots.txt')

def google(request):

    return render(request, 'google5a111c130c6d4195.html')

def about(request):

    return render(request, 'about.html')

def google(request):

    return render(request, 'google5a111c130c6d4195.html')

def home(request):

    return render(request, 'home.html')

def sitemap(request):

    return render(request, 'sitemap.txt')

def sitemapmakeup(request):

    return render(request, 'sitemapmakeup.xml')

def tagpair(request,Tag):

    SITE = StackAPI('stackoverflow')
    ori_tag = [Tag]

    TagPairCompares = tagpaircompare.objects.filter(tag=Tag).values('simitag')
    if not TagPairCompares:
        raise Http404("Tag pair does not exist")

    tagsFetch = []
    for tag in TagPairCompares:
        tagname = tag['simitag']
        tagsFetch.append(tagname)
    tagswiki = SITE.fetch('tags/{tags}/wikis', tags=tagsFetch)
    tagsWikiDict = {}
    for item in tagswiki['items']:
        excerpt = item['excerpt']
        excerpt = excerpt.strip().split('. ')[0]
        if '.&' in excerpt:
            excerpt = excerpt.split('.&')[0]
        tagsWikiDict[item['tag_name']] = excerpt

    ori_tagwiki = {}
    ori_wiki = SITE.fetch('tags/{tags}/wikis',tags = ori_tag)['items'][0]['excerpt']
    ori_wiki = ori_wiki.strip().split('. ')[0]
    if '.&' in ori_wiki:
        ori_wiki = excerpt.split('.&')[0]
    ori_tagwiki[Tag] = ori_wiki

    return render(request, 'tagpair.html',{'tagsWikiDicts':tagsWikiDict,'ori_tagwikis':ori_tagwiki})


def makedescription(tag, simitag, features, others_qua):
    description = []
    preTitle = "{} vs {}: Comparison between {} and {} based on user comments from StackOverflow.".format(tag,simitag,tag, simitag)
    description.append(preTitle)
    for value in features.values():
        for examples in value.values():
            for row in examples:
                sentence = row[0]
                description.append(sentence[0].upper()+sentence[1:]+".")
                if len(description) == 3:
                    return " ".join(description)
    for value in others_qua.values():
        for examples in value.values():
            for row in examples:
                sentence = row[0]
                description.append(sentence[0].upper()+sentence[1:]+".")
                if len(description) == 3:
                    return " ".join(description)
    values = " ".join(description)

    return values


def tagcompare(request, twotags):
    # error = {}
    # error['msg'] = ['Technology pair is not found. Try another one.',1]
    # return render(request, 'home.html',{'Error':error})
    # def tagcompare(request, twotags):


    twotags = twotags.split("-vs-")
    tpair = sorted(twotags)
    # tpair = sorted([tag, simi])
    Tag = tpair[0]
    SimiTag = tpair[1]
    SITE = StackAPI('stackoverflow')

    Relation = relation.objects.filter(tag = Tag, simitag = SimiTag).values('quality','example_id','example')
    if Relation:

        #add in below for changes to squeeze rows in database
        #now relation only has one row, with format of ['better,faster','1234,2344','that is better, i think it is faster']
        RelationGroups = []
        qualityNew = []
        exampleIDNew = []
        exampleNew = []
        for eachonegroup in Relation:
            qualityNew += eachonegroup['quality'].strip().split(',')
            exampleIDNew += eachonegroup['example_id'].strip().split(',')
            exampleNew += eachonegroup['example'].strip().split(',')

        for theid, value in enumerate(qualityNew):
            if value != '':

                newdict = {}
                newdict['quality'] = value
                newdict['example_id'] = exampleIDNew[theid]
                newdict['example'] = exampleNew[theid]
                RelationGroups.append(newdict)

        #add in above for changes to squeeze rows in database

        #make a dictionary containing relation of quality, id, example
        features = {}
        IDS_noset = [] #1162378,1795117,1338597,259517,1338597
        totalcount = 0
        for eachone in RelationGroups: #relation acts like a dictionary #change Relation to RelationGroups
            totalcount+= 1

            postid = eachone['example_id']
            IDS_noset.append(int(postid))

            #info = SITE.fetch('posts/{ids}/revisions', ids = IDS)

            if ' overall' in eachone['quality']:
                quality = eachone['quality'].replace(' overall','')
                qualityCate = 'Others'
            elif ' in ' in eachone['quality']:
                quality = eachone['quality'].split(' in ')[0]
                qualityCate = eachone['quality'].split(' in ')[1]
            sentence = eachone['example']
            if quality != 'general':
                sentence = sentence.replace(quality,'<strong>'+quality+'</strong>')
                if quality not in sentence:
                    quals = quality.split()
                    if len(quals)>1:

                        sentence = sentence.replace(' '.join(quals[:-1]), '<strong>' + ' '.join(quals[:-1]) + '</strong>')

                        sentence = sentence.replace(' '.join(quals[1:]),
                                                    '<strong>' + ' '.join(quals[1:]) + '</strong>')

                sentence = mark_safe(sentence)
            if qualityCate not in features.keys():
                features[qualityCate] = {}
                features[qualityCate][quality] = [[sentence,eachone['example_id']]]
            else:
                if quality in features[qualityCate].keys():
                    features[qualityCate][quality].append([sentence,eachone['example_id']])
                else:
                    features[qualityCate][quality] = [[sentence,eachone['example_id']]]


        id_title = {} #id of post and title of that post, put into a dictionary

        # if not tested:
        #     raise Http404('lalal')
        IDS = sorted(IDS_noset)
        if len(IDS) > 99:
            loopTime = int(len(IDS)/100)
            for i in range(loopTime+1):
                if i == 0:
                    info = SITE.fetch('posts/{ids}', ids=IDS[:100], filter='!9Z(-wsMqT')
                    for item in info['items']:
                        id_title[item['post_id']] = item['title']
                elif i == loopTime:
                    info = SITE.fetch('posts/{ids}', ids=IDS[i*100:], filter='!9Z(-wsMqT')
                    for item in info['items']:
                        id_title[item['post_id']] = item['title']
                else:
                    info = SITE.fetch('posts/{ids}', ids=IDS[i * 100:(i+1) * 100], filter='!9Z(-wsMqT')
                    for item in info['items']:
                        id_title[item['post_id']] = item['title']
        else:
            info = SITE.fetch('posts/{ids}', ids=IDS, filter='!9Z(-wsMqT')
            for item in info['items']:
                id_title[item['post_id']] = item['title']



        for qualityCate, qualityDict in features.items():
            for quality, details in qualityDict.items():
                for item in details:
                    found = 0
                    for post_id, title in id_title.items():
                        if str(post_id) == item[1]:
                            item.append(title)
                            found = 1
                            break
                    if not found:
                        item.append('* (no title is found for this review)')

        #place others to the end of quality queue
        others_qua = {}
        for key in features.keys():
            if key.lower() == 'others':
                others_quality = features.pop(key, None)
                others_qua['others'] = others_quality
                break

        tagsFetch = [Tag,SimiTag]

        tagswiki = SITE.fetch('tags/{tags}/wikis',tags = tagsFetch)
        tagsWikiDict_tag = {}
        tagsWikiDict_simi = {}
        tagsWikiDict = {}

        for item in tagswiki['items']:
            excerpt = item['excerpt']
            excerpt = excerpt.strip().split('. ')[0]
            if '.&' in excerpt:
                excerpt = excerpt.split('.&')[0]

            tagsWikiDict[item['tag_name']] = excerpt

        tagsWikiDict_tag[Tag] = tagsWikiDict[Tag]
        tagsWikiDict_simi[SimiTag] = tagsWikiDict[SimiTag]

        description = makedescription(Tag, SimiTag, features, others_qua)

    else:
        raise Http404("Tag pair does not exist")

    return render(request, 'tagcompare.html',{'Description':description,'Features':features,'Others_qua':others_qua, 'TagsWikiDict_tag':tagsWikiDict_tag,'TagsWikiDict_simi':tagsWikiDict_simi, 'Tag':Tag, 'SimiTag':SimiTag})


def selecttag(request):

    if request.method == "POST":

        Tag = request.POST.get('tag').lower().strip()

        SITE = StackAPI('stackoverflow')
        ori_tag = [Tag]

        #get set of similar tags from tagpair database
        Tagpair = TP.objects.filter(tag__contains = '\t'+Tag+'\t') | TP.objects.filter(tag__startswith = Tag+'\t')
        """
        if not TagPairCompares:
            raise Http404("Tag pair does not exist")
        """

        #make sure tagpair exists
        if not Tagpair:
            error = {}
            error['msg'] = ['Similar technology is not found. Try another one.',0]
            return render(request, 'home.html',{'Error':error})

        #check the position of the searched tag: 0 or 1 or 2, and locate its similartags
        oritag = Tagpair[0].tag.strip().split('\t')
        pos = 0
        for index, value in enumerate(oritag):
            if value == Tag:
                pos = index
                break
        simitags = Tagpair[0].simitag.split(',')
        simitag = simitags[pos]
        tagsFetch = simitag.strip().split('\t')

        #assign simitags into tagsFetch

        tagswiki = SITE.fetch('tags/{tags}/wikis',tags = tagsFetch)
        tagsWikiDict = {}

        for item in tagswiki['items']:
            excerpt = item['excerpt']
            excerpt = excerpt.strip().split('. ')[0]
            if '.&' in excerpt:
                excerpt = excerpt.split('.&')[0]
            tagp = sorted([Tag, item['tag_name']])
            if relation.objects.filter(tag = tagp[0], simitag = tagp[1]):
                tagsWikiDict[item['tag_name']] = [excerpt,1]
            else:
                tagsWikiDict[item['tag_name']] = [excerpt,0]


        ori_tagwiki = {}
        ori_wiki = SITE.fetch('tags/{tags}/wikis',tags = ori_tag)['items'][0]['excerpt']
        ori_wiki = ori_wiki.strip().split('. ')[0]
        if '.&' in ori_wiki:
            ori_wiki = excerpt.split('.&')[0]
        ori_tagwiki[Tag] = ori_wiki

        return render(request, 'tagpair.html',{'tagsWikiDicts':tagsWikiDict,'ori_tagwikis':ori_tagwiki})


def tagcomparepost(request):


    if request.method == "POST":

        ttag = request.POST.get('tag').lower().strip()
        tsimi = request.POST.get('simi').lower().strip()
        tpair = sorted([ttag, tsimi])
        Tag = tpair[0]
        SimiTag = tpair[1]
        # SITE = StackAPI('stackoverflow')

        Relation = relation.objects.filter(tag = Tag, simitag = SimiTag).values('quality','example_id','example')
        if Relation:
            return HttpResponseRedirect("/"+Tag+"-vs-"+SimiTag+"/")
            # return HttpResponseRedirect("/"+Tag+"/"+SimiTag+"/")
        else:
            error = {}
            error['msg'] = ['Technology pair is not found. Try another one.',1]
            return render(request, 'home.html',{'Error':error})

def originaltagcomparepost(request):


    if request.method == "POST":

        ttag = request.POST.get('tag').lower().strip()
        tsimi = request.POST.get('simi').lower().strip()

        tpair = sorted([ttag,tsimi])
        Tag = tpair[0]
        SimiTag = tpair[1]
        SITE = StackAPI('stackoverflow')

        Relation = relation.objects.filter(tag = Tag, simitag = SimiTag).values('quality','example_id','example')
        if Relation:

            #make a dictionary containing relation of quality, id, example

            RelationGroups = []
            qualityNew = []
            exampleIDNew = []
            exampleNew = []
            for eachonegroup in Relation:
                qualityNew += eachonegroup['quality'].strip().split(',')
                exampleIDNew += eachonegroup['example_id'].strip().split(',')
                exampleNew += eachonegroup['example'].strip().split(',')

            for theid, value in enumerate(qualityNew):
                if value != '':

                    newdict = {}
                    newdict['quality'] = value
                    newdict['example_id'] = exampleIDNew[theid]
                    newdict['example'] = exampleNew[theid]
                    RelationGroups.append(newdict)


            features = {}
            IDS_noset = [] #1162378,1795117,1338597,259517,1338597
            totalcount = 0 #monitor the counts of ID to be passed in to stack API, shoule not exceed 100
            for eachone in RelationGroups:
                totalcount += 1
                if totalcount <= 100:
                    postid = eachone['example_id']
                    IDS_noset.append(int(postid))

                    #info = SITE.fetch('posts/{ids}/revisions', ids = IDS)
                    if ' overall' in eachone['quality']:
                        quality = eachone['quality'].replace(' overall','')
                        qualityCate = 'Others'
                    elif ' in ' in eachone['quality']:
                        quality = eachone['quality'].split(' in ')[0]
                        qualityCate = eachone['quality'].split(' in ')[1]
                    if qualityCate not in features.keys():
                        features[qualityCate] = {}
                        features[qualityCate][quality] = [[eachone['example'],eachone['example_id']]]
                    else:
                        if quality in features[qualityCate].keys():
                            features[qualityCate][quality].append([eachone['example'],eachone['example_id']])
                        else:
                            features[qualityCate][quality] = [[eachone['example'],eachone['example_id']]]
                else:
                    break

            id_title = {} #id of post and title of that post, put into a dictionary

            IDS = sorted(IDS_noset)
            info = SITE.fetch('posts/{ids}',ids = IDS, filter = '!9Z(-wsMqT')
            for item in info['items']:
                id_title[item['post_id']] = item['title']

            for qualityCate, qualityDict in features.items():
                for quality, details in qualityDict.items():
                    for item in details:
                        found = 0
                        for post_id, title in id_title.items():
                            if str(post_id) == item[1]:
                                item.append(title)
                                found = 1
                                break
                        if not found:
                            item.append('* (no title is found for this review)')


            others_qua = {}
            for key in features.keys():
                if key.lower() == 'others':
                    others_quality = features.pop(key, None)
                    others_qua['others'] = others_quality
                    break



            tagsFetch = [Tag,SimiTag]


            tagswiki = SITE.fetch('tags/{tags}/wikis',tags = tagsFetch)
            tagsWikiDict_tag = {}
            tagsWikiDict_simi = {}
            tagsWikiDict = {}


            for item in tagswiki['items']:
                excerpt = item['excerpt']
                excerpt = excerpt.strip().split('. ')[0]
                if '.&' in excerpt:
                    excerpt = excerpt.split('.&')[0]

                tagsWikiDict[item['tag_name']] = excerpt

            tagsWikiDict_tag[Tag] = tagsWikiDict[Tag]
            tagsWikiDict_simi[SimiTag] = tagsWikiDict[SimiTag]

        else:
            error = {}
            error['msg'] = ['Technology pair is not found. Try another one.',1]
            return render(request, 'home.html',{'Error':error})

        return render(request, 'tagcompare.html',{'Features':features,'Others_qua': others_qua, 'TagsWikiDict_tag':tagsWikiDict_tag,'TagsWikiDict_simi':tagsWikiDict_simi})
