#!/usr/bin/env python

from embedly import Embedly

KEY = '86840b64930448618775378298644a01'

PREVIEW_HTML = '''
<div class="url-preview">
   <div class="url-credit">
      <span class="url-provider">
         <a href="{provider_url}">{provider_name}</a>
      </span>
      <span class="url-author-name">{author_name}</span>
   </div>
   <div class="url-thumbnail">
      <a href="{url}"><img src="{thumbnail_url}"/></a>
   </div>
   <div class="url-title">{title}</div>
   <div class="url-description">{description}</div>
   <div class="url-read-more">
      <a href="{url}">Read the article on {provider_url} &gt;</a>
   </div>
</div>
'''

class UrlPreviewError(Exception): pass

class UrlPreview(object):

    FIELDS = [
        'author_name',
        'description',
        'provider_name',
        'provider_url',
        'thumbnail_url',
        'thumbnail_width',
        'thumbnail_height',
        'title',
        'url']

    def __init__(self):
        self.client = Embedly(KEY)

    def getPreview(self, url):
        obj = self.client.oembed(url)
        
        if obj.get('error'):
            return ''
        
        # fill in some blanks
        for field in self.FIELDS:
            if field not in obj.data:
                obj.data[field] = ''

        return PREVIEW_HTML.format(**obj.data)

    def getData(self, url):
        return self.client.oembed(url)

    def getDataAsText(self, url):
        obj = self.getData(url)
        keys = sorted(obj.data.keys())
        o = ''
        for k in keys:
            o += '%-17s: %s' % (k, obj.data[k]) + '\n'
        return o

    def run(self):
        '''Command line interface'''

        from vlib.cli import CLI

        commands = ['preview_html <url>',
                    'get_data <url>']
        options = {}
        self.cli = CLI(self.process, commands, options)
        self.cli.process()

    def process(self, *args):
        '''Process Command line requests'''

        from vlib.utils import validate_num_args

        args = list(args)
        cmd = args.pop(0)

        if cmd == 'preview_html':
            validate_num_args('preview_html', 1, args)
            url = args.pop(0)
            return self.getPreview(url)

        elif cmd == 'get_data':
            validate_num_args('get_data', 1, args)
            url = args.pop(0)
            return self.getDataAsText(url)

        else:
            raise UrlPreviewError('Unrecognized command: %s' % cmd)

if __name__ == '__main__':
    UrlPreview().run()
