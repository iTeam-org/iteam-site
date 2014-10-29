# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Log.useragent'
        db.add_column(u'stats_log', 'useragent',
                      self.gf('django.db.models.fields.CharField')(default='-', max_length=256),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Log.useragent'
        db.delete_column(u'stats_log', 'useragent')


    models = {
        u'stats.log': {
            'Meta': {'object_name': 'Log'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256'}),
            'method': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256'}),
            'referer': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'useragent': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256'})
        }
    }

    complete_apps = ['stats']