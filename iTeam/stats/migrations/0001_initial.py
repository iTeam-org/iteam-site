# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Log'
        db.create_table(u'stats_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(default='-', max_length=256)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('method', self.gf('django.db.models.fields.CharField')(default='-', max_length=256)),
            ('referer', self.gf('django.db.models.fields.CharField')(default='-', max_length=256)),
        ))
        db.send_create_signal(u'stats', ['Log'])


    def backwards(self, orm):
        # Deleting model 'Log'
        db.delete_table(u'stats_log')


    models = {
        u'stats.log': {
            'Meta': {'object_name': 'Log'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256'}),
            'method': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256'}),
            'referer': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '256'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['stats']