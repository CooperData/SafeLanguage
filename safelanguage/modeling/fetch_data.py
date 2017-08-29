# this is a modification from sklearn fetch_data.py script
# simple python script to collect text paragraphs from various languages on the
# same topic namely the Wikipedia encyclopedia itself

import os
from urllib.request import Request, build_opener
import lxml.html
from lxml.etree import ElementTree
import numpy as np
import codecs
import shutil
from safelanguage.ResourceHandler import ResourceHandler
import wikipedia

html_folder = u'./data/html'
text_folder = u'./data/paragraphs'
short_text_folder = u'./data/short_paragraphs'


def download_data(data_size='small'):

    languages = ['es', 'fr', 'de', 'it', 'pt', 'en']
    create_folder(languages)

    if data_size == 'small':
        download_small_data()
    elif data_size == 'all':
        download_all_data()
    else:
        print('data_size should be small (default) or all')


def language_folder_path(paragraph_size, language):
    if paragraph_size == 'small':
        folder_path = os.path.join(short_text_folder, language)
    elif paragraph_size == 'normal':
        folder_path = os.path.join(text_folder, language)
    return folder_path


def create_folder(languages):
    if not os.path.exists(html_folder):
        os.makedirs(html_folder)

    for lang in languages:
        text_lang_folder = language_folder_path('normal', lang)
        if not os.path.exists(text_lang_folder):
            os.makedirs(text_lang_folder)

        short_text_lang_folder = language_folder_path('small', lang)
        if not os.path.exists(short_text_lang_folder):
            os.makedirs(short_text_lang_folder)


def download_all_data():
    resource_handler = ResourceHandler()
    feature_articles = resource_handler.get_feature_pages()
    for language in feature_articles.keys():
        articles = feature_articles.get(language)
        wikipedia.set_lang(language)
        for article in articles:
            i = 0
            content = wikipedia.page(article).content
            split_content = content.splitlines()
            paragraphs = [re.sub(r'\[[^]]*\]\u200b', '', p.strip()) for p in split_content if len(p.strip()) > 0]
            for paragraph in paragraphs:
                if len(paragraph) < 100:
                    write_small_paragraph(paragraph)
                else:
                    write_normal_paragraph(paragraph)
            break
            i += 1

    print(feature_articles)


def write_small_paragraph(paragraph):
    pass


def write_normal_paragraph(paragraph):
    pass


def download_small_data():
    print('small data')
    n_words_per_short_text = 5
    pages = {
        u'de': u'http://de.wikipedia.org/wiki/Wikipedia',
        u'en': u'https://en.wikipedia.org/wiki/Wikipedia',
        u'es': u'http://es.wikipedia.org/wiki/Wikipedia',
        u'fr': u'http://fr.wikipedia.org/wiki/Wikip%C3%A9dia',
        u'it': u'http://it.wikipedia.org/wiki/Wikipedia',
        u'pt': u'https://pt.wikipedia.org/wiki/Wikip%C3%A9dia'
    }

    for lang, page in pages.items():
        opener = build_opener()
        html_filename = os.path.join(html_folder, lang + '.html')
        if not os.path.exists(html_filename):
            print("Downloading %s" % page)
            request = Request(page)
            request.add_header('User-Agent', 'OpenAnything/1.0')
            html_content = opener.open(request).read()
            open(html_filename, 'wb').write(html_content)

        # decode the payload explicitly as UTF-8 since lxml is confused for some
        # reason
        with codecs.open(html_filename, 'r', 'utf-8') as html_file:
            html_content = html_file.read()
        tree = ElementTree(lxml.html.document_fromstring(html_content))
        i = 0
        j = 0
        for p in tree.findall('//p'):
            content = p.text_content()
            if len(content) < 100:
                # skip paragraphs that are too short - probably too noisy and not
                # representative of the actual language
                continue

            text_filename = os.path.join(language_folder_path('normal', lang),
                                         '%s_%04d.txt' % (lang, i))
            print("Writing %s" % text_filename)
            open(text_filename, 'wb').write(content.encode('utf-8', 'ignore'))
            i += 1

            # split the paragraph into fake smaller paragraphs to make the
            # problem harder e.g. more similar to tweets
            words = content.split()
            n_groups = len(words) / n_words_per_short_text
            if n_groups < 1:
                continue
            groups = np.array_split(words, n_groups)

            for group in groups:
                small_content = u" ".join(group)

                short_text_filename = os.path.join(language_folder_path('small', lang),
                                                   '%s_%04d.txt' % (lang, j))
                print("Writing %s" % short_text_filename)
                open(short_text_filename, 'wb').write(
                    small_content.encode('utf-8', 'ignore'))
                j += 1
                if j >= 1000:
                    break


def delete_data():
    if os.path.exists('./data'):
        shutil.rmtree('./data')

